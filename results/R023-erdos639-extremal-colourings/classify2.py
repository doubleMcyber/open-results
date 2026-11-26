import sys, itertools, numpy as np
n=int(sys.argv[1]); fn=sys.argv[2]
iu=[(i,j) for i in range(n) for j in range(i+1,n)]
E=len(iu)
P=np.array(list(itertools.permutations(range(n))),dtype=np.int8)
I=np.array([a for a,b in iu]); J=np.array([b for a,b in iu])
w=(1<<np.arange(E,dtype=np.int64))[::-1] if E<63 else None
PI=P[:,I]; PJ=P[:,J]
def canon(c):
    A=np.zeros((n,n),dtype=np.int64)
    for e,(i,j) in enumerate(iu):
        A[i,j]=A[j,i]=(c>>e)&1
    best=None
    for flip in (0,1):
        B=A^flip
        codes=(B[PI,PJ]*w).sum(axis=1)
        m=int(codes.min())
        if best is None or m<best: best=m
    return best
cl={}
for line in open(fn):
    c=int(line); k=canon(c); cl[k]=cl.get(k,0)+1
print(n,"extremal colourings (edge0 fixed):",sum(cl.values()),"classes up to perm+colour swap:",len(cl))
import json; json.dump({str(k):v for k,v in cl.items()},open(f"classes{n}.json","w"))
