import json, itertools, sys
for n in (6,7,8):
    cl=json.load(open(f"classes{n}.json")); E=n*(n-1)//2
    iu=[(i,j) for i in range(n) for j in range(i+1,n)]
    print("n=",n)
    for k,v in sorted(cl.items(), key=lambda x:int(x[0])):
        code=int(k); bits=[(code>>(E-1-e))&1 for e in range(E)]
        A=[[0]*n for _ in range(n)]
        for e,(i,j) in enumerate(iu): A[i][j]=A[j][i]=bits[e]
        cov=set()
        for a,b,c in itertools.combinations(range(n),3):
            s=A[a][b]+A[a][c]+A[b][c]
            if s in(0,3): cov|={(a,b),(a,c),(b,c)}
        unc=[e for e in iu if e not in cov]
        U=[[0]*n for _ in range(n)]
        for i,j in unc: U[i][j]=U[j][i]=1
        # bipartite check of uncovered graph: components, degrees
        degs=sorted(sum(r) for r in U)
        # find 2-colouring
        side={}; ok=True
        for s in range(n):
            if s in side or sum(U[s])==0: continue
            side[s]=0; st=[s]
            while st:
                x=st.pop()
                for y in range(n):
                    if U[x][y]:
                        if y not in side: side[y]=1-side[x]; st.append(y)
                        elif side[y]==side[x]: ok=False
        iso=[v_ for v_ in range(n) if sum(U[v_])==0]
        print(" class size(edge0-fixed colourings)=",v,"red edges",sum(bits),"unc",len(unc),"unc degs",degs,"bipartite",ok,"mono triangles",sum(1 for a,b,c in itertools.combinations(range(n),3) if A[a][b]+A[a][c]+A[b][c] in (0,3)),"isolated-in-U",len(iso))
