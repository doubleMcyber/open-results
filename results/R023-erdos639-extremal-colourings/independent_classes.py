import itertools,sys
def run(n):
    E=[(i,j) for i in range(n) for j in range(i+1,n)]; idx={e:k for k,e in enumerate(E)}; m=len(E)
    T=[(1<<idx[(a,b)])|(1<<idx[(a,c)])|(1<<idx[(b,c)]) for a,b,c in itertools.combinations(range(n),3)]
    full=(1<<m)-1; best=-1; ext=[]
    for r in range(1<<m):
        cov=0
        for t in T:
            x=r&t
            if x==t or x==0: cov|=t
        u=m-bin(cov).count('1')
        if u>best: best,ext=u,[]
        if u==best: ext.append(r)
    S=set(ext)
    def perm(r,p):
        o=0
        for k,(i,j) in enumerate(E):
            if r>>k&1:
                a,b=sorted((p[i],p[j])); o|=1<<idx[(a,b)]
        return o
    gens=[]
    for i in range(1,n):
        p=list(range(n)); p[0],p[i]=p[i],p[0]; gens.append(p)
    seen=set(); orbits=0
    for r in ext:
        if r in seen: continue
        orbits+=1; st=[r]; seen.add(r)
        while st:
            x=st.pop()
            for y in [perm(x,p) for p in gens]+[x^full]:
                assert y in S
                if y not in seen: seen.add(y); st.append(y)
    print(n,best,len(ext),'classes',orbits)
for n in (6,7): run(n)
