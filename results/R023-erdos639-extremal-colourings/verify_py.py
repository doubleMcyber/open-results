# independent numpy check for n<=7: max uncovered edges and number of extremal colourings (edge 0 fixed to colour 0)
import numpy as np, itertools, sys
for n in (4,5,6,7):
    E=n*(n-1)//2
    ids={}
    k=0
    for i in range(n):
        for j in range(i+1,n): ids[(i,j)]=k;k+=1
    c=np.arange(1<<(E-1),dtype=np.int64)
    cov=np.zeros_like(c)
    for a,b,d in itertools.combinations(range(n),3):
        m=(1<<ids[(a,b)])|(1<<ids[(a,d)])|(1<<ids[(b,d)])
        x=c&m
        mono=(x==0)|(x==m)
        cov|=np.where(mono,m,0)
    unc=E-np.array([bin(v).count("1") for v in cov]) if E<=15 else None
    if unc is None:
        pc=np.zeros_like(cov)
        t=cov.copy()
        while t.any():
            pc+= (t&1); t>>=1
        unc=E-pc
    mx=unc.max()
    print(n,"max uncovered",mx,"count",int((unc==mx).sum()))
