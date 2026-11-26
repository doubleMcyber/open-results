from itertools import combinations
from fractions import Fraction
def det(M):
    M=[[Fraction(x) for x in r] for r in M]; n=len(M); d=Fraction(1)
    for c in range(n):
        p=next((r for r in range(c,n) if M[r][c]!=0),None)
        if p is None: return 0
        if p!=c: M[c],M[p]=M[p],M[c]; d=-d
        d*=M[c][c]
        for r in range(c+1,n):
            f=M[r][c]/M[c][c]
            if f:
                for j in range(c,n): M[r][j]-=f*M[c][j]
    return d
def dfact(m):
    r=1
    while m>1: r*=m; m-=2
    return r
for n in range(3,10):
    pos=[(i,j) for i in range(n) for j in range(i,n)]
    for k in range(0,n):
        cnt=0
        for S in combinations(pos,k):
            A=[[1]*n for _ in range(n)]
            for i,j in S: A[i][j]=A[j][i]=-1
            if det(A)!=0: cnt+=1
        if cnt: print(n,'min k',k,'count',cnt,'claim',n//2,dfact(2*(n//2)+1)); break
