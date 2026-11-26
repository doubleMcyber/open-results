# Usage: cc -O2 -o dump8 independent_dump8.c && ./dump8 | grep '^M' | cut -d' ' -f2 | python3 independent_classes8.py
import sys
n=8;E=[(i,j) for i in range(n) for j in range(i+1,n)];idx={e:k for k,e in enumerate(E)};full=(1<<28)-1
S=set(int(x) for x in sys.stdin if x.strip())
def perm(r,p):
    o=0
    for k,(i,j) in enumerate(E):
        if r>>k&1:
            a,b=sorted((p[i],p[j]));o|=1<<idx[(a,b)]
    return o
gens=[]
for i in range(1,n):
    p=list(range(n));p[0],p[i]=p[i],p[0];gens.append(p)
seen=set();orb=0
for r in S:
    if r in seen:continue
    orb+=1;st=[r];seen.add(r)
    while st:
        x=st.pop()
        for y in [perm(x,p) for p in gens]+[x^full]:
            assert y in S
            if y not in seen:seen.add(y);st.append(y)
print('n=8 extremal colourings',len(S),'classes',orb)
