"""Group and GF(2) library written for the fresh re-derivation."""
import json, numpy as np

def load_group(gid, path="groups.jsonl"):
    for line in open(path):
        r=json.loads(line)
        if r.get('gap_id')==list(gid): return r
    raise KeyError(gid)

def build_mult(gens):
    """gens[i][j] = index(e_j * s_i).  Returns M with M[i,j]=index(e_i*e_j).  Element 0 = identity."""
    gens=[np.array(g) for g in gens]; N=len(gens[0])
    M=-np.ones((N,N),dtype=np.int64)
    M[:,0]=np.arange(N)            # e_i * e = e_i
    seen=[0]; q=[0]
    while q:
        j=q.pop(0)
        for P in gens:
            j2=P[j]                # e_j2 = e_j * s
            col=P[M[:,j]]          # e_i*e_j2 = (e_i*e_j)*s
            if M[0,j2]==-1:
                M[:,j2]=col; q.append(j2)
            else:
                assert (M[:,j2]==col).all(), 'inconsistent word'
    assert (M>=0).all()
    return M

def check_group(M):
    N=len(M)
    assert (M[0]==np.arange(N)).all() and (M[:,0]==np.arange(N)).all()
    for i in range(N): assert sorted(M[i])==list(range(N)) and sorted(M[:,i])==list(range(N))
    # associativity: (i*j)*k == i*(j*k)
    for i in range(N):
        assert (M[M[i][:,None],np.arange(N)[None,:]]==M[i][M]).all(), 'not associative'
    return bool((M==M.T).all())

def cyclic(n):
    return np.array([[(i+j)%n for j in range(n)] for i in range(n)])

def Lmat(M,a):
    N=len(M); L=np.zeros((N,N),dtype=np.uint8)
    for s in a:
        for g in range(N): L[M[s,g],g]^=1     # L[s*g, g]
    return L
def Rmat(M,b):
    N=len(M); R=np.zeros((N,N),dtype=np.uint8)
    for s in b:
        for g in range(N): R[M[g,s],g]^=1     # R[g*s, g]
    return R
def code(M,a,b):
    L=Lmat(M,a); R=Rmat(M,b)
    HX=np.concatenate([L,R],1); HZ=np.concatenate([R.T,L.T],1)
    return HX,HZ

# ---- GF(2) linear algebra on python ints (rows as bitmasks) ----
def rows_to_ints(H):
    return [int(''.join(map(str,r[::-1])),2) if len(r) else 0 for r in np.asarray(H,dtype=np.uint8)]
def ints_to_mat(rows,n):
    return np.array([[ (r>>j)&1 for j in range(n)] for r in rows],dtype=np.uint8)
def rref_ints(rows):
    """returns reduced basis dict pivot->row (fully reduced)"""
    piv={}
    for r in rows:
        for p,v in piv.items():
            if (r>>p)&1: r^=v
        if r:
            p=r.bit_length()-1
            for q in list(piv):
                if (piv[q]>>p)&1: piv[q]^=r
            piv[p]=r
    return piv
def rank(H): return len(rref_ints(rows_to_ints(H)))
def nullspace(H):
    """basis of {x: H x = 0}, as list of ints"""
    H=np.asarray(H,dtype=np.uint8); m,n=H.shape
    A=H.copy(); pivcols=[]; r=0
    for c in range(n):
        p=None
        for i in range(r,m):
            if A[i,c]: p=i;break
        if p is None: continue
        A[[r,p]]=A[[p,r]]
        for i in range(m):
            if i!=r and A[i,c]: A[i]^=A[r]
        pivcols.append(c); r+=1
        if r==m: break
    free=[c for c in range(n) if c not in pivcols]
    out=[]
    for f in free:
        x=np.zeros(n,dtype=np.uint8); x[f]=1
        for i,c in enumerate(pivcols):
            if A[i,f]: x[c]=1
        out.append(x)
    return np.array(out,dtype=np.uint8).reshape(len(out),n)
def same_rowspace(A,B):
    ra=rref_ints(rows_to_ints(A)); rb=rref_ints(rows_to_ints(B))
    return ra==rb
def logical_basis(Hx,Hz):
    """X-type logical reps (ker Hz mod rowspace Hx) and Z-type (ker Hx mod rowspace Hz), each k x n"""
    def comp(Hker_of, Hstab):
        K=nullspace(Hker_of); S=rref_ints(rows_to_ints(Hstab)); out=[]
        cur=dict(S)
        for v in rows_to_ints(K):
            r=v
            for p,u in cur.items():
                if (r>>p)&1: r^=u
            if r:
                p=r.bit_length()-1
                for q in list(cur):
                    if (cur[q]>>p)&1: cur[q]^=r
                cur[p]=r; out.append(v)
        return ints_to_mat(out,Hx.shape[1])
    return comp(Hz,Hx), comp(Hx,Hz)   # (X logicals, Z logicals)
