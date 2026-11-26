# (1) exact counts from bias.c output: min k and number of nonsingular matrices at min k, n=3..7, versus (2*floor(n/2)+1)!!
# (2) the nonsingular family for larger n: every matching / matching+diagonal config, exact rational determinant, n<=10
from math import comb
from fractions import Fraction
import itertools
def dfact(m):
    r=1
    while m>1: r*=m; m-=2
    return r
for n in range(3,8):
    L=[tuple(map(int,l.split())) for l in open(f"out{n}.txt").read().splitlines()[1:]]
    f=n*(n+1)//2
    k,s=next((k,comb(f,k)-s) for k,s in L if comb(f,k)-s)
    print(n,"min k",k,"count",s,"formula",dfact(2*(n//2)+1),"ok",k==n//2 and s==dfact(2*(n//2)+1))
def det(M):
    n=len(M);M=[[Fraction(x) for x in r] for r in M];d=Fraction(1)
    for k in range(n):
        p=next((i for i in range(k,n) if M[i][k]!=0),None)
        if p is None:return 0
        if p!=k:M[k],M[p]=M[p],M[k];d=-d
        d*=M[k][k]
        for i in range(k+1,n):
            f=M[i][k]/M[k][k]
            for j in range(k,n):M[i][j]-=f*M[k][j]
    return d
def matchings(vs,size):
    if size==0: yield (); return
    if len(vs)<2*size: return
    v=vs[0];rest=vs[1:]
    yield from matchings(rest,size)   # v unmatched
    for i,w in enumerate(rest):
        for m in matchings(rest[:i]+rest[i+1:],size-1): yield ((v,w),)+m
for n in range(3,11):
    k=n//2; cnt=0; bad=0
    # all B with k upper-triangle entries of form: matching of size k (off-diag only) or (k-1)-matching + one diagonal (even n)
    cfgs=[(m,()) for m in matchings(list(range(n)),k)]
    if n%2==0:
        for m in matchings(list(range(n)),k-1):
            used={x for e in m for x in e}
            for u in range(n):
                if u not in used: cfgs.append((m,(u,)))
    for m,dg in cfgs:
        M=[[1]*n for _ in range(n)]
        for a,b in m: M[a][b]=M[b][a]=-1
        for u in dg: M[u][u]=-1
        cnt+=1; bad+= det(M)==0
    print(n,"configs",cnt,"singular among them",bad,"formula",dfact(2*(n//2)+1))
