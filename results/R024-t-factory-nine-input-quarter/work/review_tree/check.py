import json, itertools, numpy as np, sympy as sp
from fractions import Fraction
tree=json.load(open('../../results/tree_best.json'))
n=9
P1={'I':np.eye(2),'X':np.array([[0,1],[1,0]]),'Y':np.array([[0,-1j],[1j,0]]),'Z':np.diag([1,-1])}
def op(s):
    sg=-1 if s[0]=='-' else 1
    body=s[1:] if s[0] in '+-' else s
    assert len(body)==n
    M=np.array([[1]],dtype=complex)
    for c in body: M=np.kron(M,P1[c])
    return sg*M
def sympl(s):
    body=s[1:] if s[0] in '+-' else s
    x=[c in 'XY' for c in body]; z=[c in 'ZY' for c in body]
    return np.array(x+z,dtype=int)
def comm(a,b): return (sympl(a)[:n]@sympl(b)[n:]+sympl(a)[n:]@sympl(b)[:n])%2==0
# leaves with paths
leaves=[]
def walk(t,path):
    if 'leaf' in t: leaves.append((t['leaf'],path)); return
    walk(t['plus'],path+[('+',t['measure'])]); walk(t['minus'],path+[('-',t['measure'])])
walk(tree,[])
print('leaves',len(leaves))
I=np.eye(2**n)
def proj(s,sign): return (I+sign*op(s))/2
# state set
T=np.array([1,np.exp(1j*np.pi/4)])/np.sqrt(2)
T9=T
for _ in range(8): T9=np.kron(T9,T)
Zd=np.diag([1,-1])
def Zop(e):
    d=np.ones(2**n)
    for q in range(n):
        if e[q]:
            idx=np.arange(2**n); d=d*(1-2*((idx>>(n-1-q))&1))
    return d
es=list(itertools.product([0,1],repeat=n))
V=np.stack([Zop(e)*T9 for e in es],axis=1)  # 512 x 512 columns
wts=np.array([sum(e) for e in es])
res=[]
ok1=True; rank_ok=True
Pis=[]
allbasis=[]
for li,(gens,path) in enumerate(leaves):
    # structure
    ng=len(gens); assert ng==8
    cm=all(comm(a,b) for a in gens for b in gens)
    S=np.array([sympl(g) for g in gens])
    # GF2 rank
    M=S.copy()%2; r=0
    for c in range(2*n):
        piv=[i for i in range(r,8) if M[i,c]]
        if not piv: continue
        M[[r,piv[0]]]=M[[piv[0],r]]
        for i in range(8):
            if i!=r and M[i,c]: M[i]^=M[r]
        r+=1
    # group membership: build stabilizer group as signed matrices (256 elements) via symplectic+sign check using matrices
    Pi=I.astype(complex)
    for g in gens: Pi=Pi@proj(g,1)
    rk=round(np.trace(Pi).real)
    herm=np.allclose(Pi,Pi.conj().T); idem=np.allclose(Pi@Pi,Pi)
    # path ops in group: Pi * (sign*P) == Pi  (i.e. sign*P stabilises code space)
    mem=all(np.allclose(op(m)*(1 if sg=='+' else -1)@Pi,Pi) for sg,m in path)
    # path projectors applied directly
    Pp=Pi.copy()
    chain=I.astype(complex)
    for sg,m in path: chain=proj(m,1 if sg=='+' else -1)@chain
    Pfull=Pi@chain
    implied=np.allclose(Pfull,Pi)
    Pis.append(Pi)
    # ideal state
    psi=Pfull@T9; a0=np.vdot(psi,psi).real; psi0=psi/np.sqrt(a0)
    # logical Bloch: normalizer enumeration
    # use rank-2 space: find normalizer reps by brute force over Paulis commuting with all gens
    res.append(dict(li=li,depth=len(path),comm=cm,rank=r,trace=rk,herm=herm,idem=idem,member=mem,implied=implied,a0=a0,psi0=psi0,Pfull=Pfull,Pi=Pi,gens=gens))
    print(li,'depth',len(path),'comm',cm,'gf2rank',r,'tr',rk,'herm/idem',herm,idem,'path in stab',mem,'implied',implied,'A0',a0)
print('A0 total',sum(r['a0'] for r in res))
# orthogonality
mx=0
for i in range(32):
    for j in range(i+1,32):
        mx=max(mx,np.abs(res[i]['Pfull']@res[j]['Pfull']).max() if False else np.abs(Pis[i]@Pis[j]).max())
print('max |Pi_i Pi_j| entry',mx)
# T-like check
letters='IXYZ'
allP=list(itertools.product(range(4),repeat=n))
bits=np.array([[ (c in (1,2)) for c in p]+[(c in (2,3)) for c in p] for p in allP],dtype=int)
def tlike(r):
    Sg=np.array([sympl(g) for g in r['gens']])
    # commutes with all gens
    cm=((bits[:,:n]@Sg[:,n:].T + bits[:,n:]@Sg[:,:n].T)%2==0).all(axis=1)
    idxs=np.nonzero(cm)[0]
    psi=r['psi0']; vals={}
    for k in idxs:
        s='+'+''.join(letters[c] for c in allP[k])
        v=np.vdot(psi,op(s)@psi).real
        vals[round(abs(v),6)]=vals.get(round(abs(v),6),0)+1
    return len(idxs),vals
tl=[]
for r in res:
    t=tlike(r); tl.append(t)
    print(r['li'],'normalizer size',t[0],'|<P>| histogram',t[1])
# polynomial coefficients
A=np.zeros(10);H=np.zeros(10);Aw=np.zeros(10)
for r in res:
    Pf=r['Pfull']; W=Pf@V   # accepted vectors
    w=(np.abs(W)**2).sum(axis=0)
    f=np.abs(r['psi0'].conj()@W)**2
    for k in range(10):
        m=wts==k
        A[k]+=w[m].sum(); H[k]+=(w-f)[m].sum()
# prob weight p^k(1-p)^(9-k): sums over patterns of weight k already
p=sp.symbols('p')
Ap=sum(sp.nsimplify(0)*p for _ in [0]); 
def rat(x):
    fr=Fraction(float(x)).limit_denominator(2**20)
    assert abs(float(fr)-x)<1e-9,(x,fr)
    return sp.Rational(fr.numerator,fr.denominator)
Ar=[rat(x) for x in A]; Hr=[rat(x) for x in H]
print('A per-weight',Ar); print('H per-weight',Hr)
Apoly=sp.expand(sum(Ar[k]*p**k*(1-p)**(9-k) for k in range(10)))
Hpoly=sp.expand(sum(Hr[k]*p**k*(1-p)**(9-k) for k in range(10)))
D=2-15*p+87*p**2-256*p**3+408*p**4-336*p**5+112*p**6
N=27*p**2-141*p**3+324*p**4-384*p**5+224*p**6-48*p**7
print('A(p)=',Apoly); print('H(p)=',Hpoly)
print('A==D/8',sp.expand(Apoly-D/8)==0,' H==N/8',sp.expand(Hpoly-N/8)==0)
E=sp.expand(20*p**2*Apoly-Hpoly); print('E(p)=',E)
Q=sp.cancel(E/p**2); print('E/p^2=',Q)
print('Q(0)=',Q.subs(p,0),' Q(0.01)=',float(Q.subs(p,sp.Rational(1,100))))
print('real roots of Q in [0,0.01]:',sp.Poly(Q,p).count_roots(0,sp.Rational(1,100)))
print('min Q on [0,.01] (grid)',min(float(Q.subs(p,sp.Rational(i,10000))) for i in range(101)))
print('Q derivative sign at ends',float(sp.diff(Q,p).subs(p,0)),float(sp.diff(Q,p).subs(p,sp.Rational(1,100))))
print('A(0.01)',float(Apoly.subs(p,sp.Rational(1,100))),'eps(0.01)',float((Hpoly/Apoly).subs(p,sp.Rational(1,100))))
