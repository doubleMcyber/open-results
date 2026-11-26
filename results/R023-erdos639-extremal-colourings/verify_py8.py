import numpy as np, itertools
n=8; E=28
ids={}; k=0
for i in range(n):
    for j in range(i+1,n): ids[(i,j)]=k;k+=1
tris=[(1<<ids[(a,b)])|(1<<ids[(a,c)])|(1<<ids[(b,c)]) for a,b,c in itertools.combinations(range(n),3)]
best=-1; cnt=0
CH=1<<22
for start in range(0,1<<(E-1),CH):
    c=np.arange(start,start+CH,dtype=np.int64)
    cov=np.zeros_like(c)
    for m in tris:
        x=c&m
        cov|=np.where((x==0)|(x==m),m,0)
    # popcount
    v=cov.copy(); pc=np.zeros_like(v)
    for _ in range(E):
        pc+=v&1; v>>=1
    unc=E-pc
    mx=int(unc.max())
    if mx>best: best=mx; cnt=int((unc==mx).sum())
    elif mx==best: cnt+=int((unc==mx).sum())
print("n=8 max uncovered",best,"count",cnt)
