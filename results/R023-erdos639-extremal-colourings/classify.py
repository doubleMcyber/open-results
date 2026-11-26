import sys, itertools
n=int(sys.argv[1]); fn=sys.argv[2]
ids={}; k=0
for i in range(n):
    for j in range(i+1,n): ids[(i,j)]=k; k+=1
E=k
cols=[int(x) for x in open(fn)]
def adj(c):
    return [[0]*n for _ in range(n)], 
def canon(c):
    # canonical form: min over perms and complement; use refinement by degree to prune
    best=None
    M=[[0]*n for _ in range(n)]
    for (i,j),e in ids.items():
        v=(c>>e)&1; M[i][j]=M[j][i]=v
    full=(1<<E)-1
    for flip in (0,1):
        A=[[ (M[i][j]^flip) if i!=j else 0 for j in range(n)] for i in range(n)]
        deg=[sum(r) for r in A]
        # sort vertices by degree, permute only within degree classes
        order=sorted(range(n),key=lambda v:deg[v])
        groups=[]
        for v in order:
            if groups and deg[groups[-1][0]]==deg[v]: groups[-1].append(v)
            else: groups.append([v])
        for combo in itertools.product(*[itertools.permutations(g) for g in groups]):
            p=[v for g in combo for v in g]
            code=tuple(A[p[i]][p[j]] for i in range(n) for j in range(i+1,n))
            if best is None or code<best: best=code
    return best
classes={}
for c in cols:
    # include complement colouring implicitly via flip
    classes.setdefault(canon(c),0)
    classes[canon(c)]+=1
print(n,len(cols),"classes up to perm+colour swap:",len(classes))
for k_,v in sorted(classes.items(), key=lambda x:x[1]):
    pass
