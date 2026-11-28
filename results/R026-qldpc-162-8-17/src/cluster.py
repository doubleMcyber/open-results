"""Exact connected-closure search for low-weight nontrivial logicals (own implementation).
Min-weight nontrivial logical L has no proper nonempty closed subset (else a lighter nontrivial one exists),
so growing from a seed by always resolving an odd-parity check is complete for weight<=W."""
import numpy as np, numba as nb

def prep(checks, logicals):
    """checks: nc x n 0/1 matrix defining the closure condition; logicals: k x n test vectors."""
    nc,n=checks.shape
    mw=int(checks.sum(1).max()); mc=int(checks.sum(0).max())
    cq=-np.ones((nc,mw),np.int32); ql=-np.ones((n,mc),np.int32)
    for c in range(nc):
        idx=np.nonzero(checks[c])[0]; cq[c,:len(idx)]=idx
    for q in range(n):
        idx=np.nonzero(checks[:,q])[0]; ql[q,:len(idx)]=idx
    return cq,ql,np.ascontiguousarray(logicals,dtype=np.uint8),mc

@nb.njit(cache=True)
def search(cq,ql,lg,maxcol,W,seed,excl,stop_first):
    nc,mw=cq.shape; n=ql.shape[0]; k=lg.shape[0]
    state=np.zeros(n,np.int8); par=np.zeros(nc,np.int8); nfree=np.zeros(nc,np.int32)
    for c in range(nc):
        for j in range(mw):
            if cq[c,j]>=0: nfree[c]+=1
    def_unsat=0
    # exclusions
    for t in range(len(excl)):
        q=excl[t]; state[q]=2
        for j in range(ql.shape[1]):
            c=ql[q,j]
            if c>=0: nfree[c]-=1
    cand=np.zeros((W+2,8),np.int32); ncand=np.zeros(W+2,np.int32); idx=np.zeros(W+2,np.int32)
    S=np.zeros(W+2,np.int32); w=0; unsat=0; nf=0
    found=np.full(W+2,-1,np.int32); nfound=0; minfound=10**9
    nodes=0; closed_trivial=0; closed_nontriv=0
    # add seed
    q=seed; state[q]=1; S[w]=q; w+=1
    for j in range(ql.shape[1]):
        c=ql[q,j]
        if c>=0:
            par[c]^=1; nfree[c]-=1
            if par[c]==1: unsat+=1
            else: unsat-=1
    mode=0
    while True:
        if mode==0:
            nodes+=1
            back=False
            if unsat==0:
                nt=False
                for i in range(k):
                    p=0
                    for t in range(w): p^=lg[i,S[t]]
                    if p: nt=True;break
                if nt:
                    closed_nontriv+=1
                    if w<minfound:
                        minfound=w; nfound=w
                        for t in range(w): found[t]=S[t]
                    if stop_first: return nodes,minfound,found,nfound,closed_trivial,closed_nontriv
                else:
                    closed_trivial+=1
                back=True
            elif w+(unsat+maxcol-1)//maxcol>W:
                back=True
            else:
                best=-1; bf=100
                for c in range(nc):
                    if par[c]==1 and nfree[c]<bf:
                        bf=nfree[c]; best=c
                if bf==0: back=True
                else:
                    f=nf; nf+=1; m=0
                    for j in range(mw):
                        q=cq[best,j]
                        if q>=0 and state[q]==0:
                            cand[f,m]=q; m+=1
                    ncand[f]=m; idx[f]=0
                    for j in range(m):    # tentatively exclude later as we go; mark none now
                        pass
                    # exclusions applied progressively: qubits before idx are excluded
                    for j in range(m):
                        pass
            if back: mode=2
            else: mode=1
        if mode==2:
            if nf==0: break
            f=nf-1; q=cand[f,idx[f]]
            # remove q from S
            state[q]=0; w-=1
            for j in range(ql.shape[1]):
                c=ql[q,j]
                if c>=0:
                    par[c]^=1; nfree[c]+=1
                    if par[c]==1: unsat+=1
                    else: unsat-=1
            # exclude q
            state[q]=2
            for j in range(ql.shape[1]):
                c=ql[q,j]
                if c>=0: nfree[c]-=1
            idx[f]+=1
            mode=1
        if mode==1:
            f=nf-1
            if idx[f]==ncand[f]:
                for j in range(ncand[f]):
                    q=cand[f,j]; state[q]=0
                    for jj in range(ql.shape[1]):
                        c=ql[q,jj]
                        if c>=0: nfree[c]+=1
                nf-=1; mode=2
            else:
                q=cand[f,idx[f]]; state[q]=1; S[w]=q; w+=1
                for j in range(ql.shape[1]):
                    c=ql[q,j]
                    if c>=0:
                        par[c]^=1; nfree[c]-=1
                        if par[c]==1: unsat+=1
                        else: unsat-=1
                mode=0
    return nodes,minfound,found,nfound,closed_trivial,closed_nontriv

def sector_search(HX,HZ,sector,W,stop_first=False,N=None):
    """sector 'X': x in ker HZ, nontrivial vs Z-logicals; sector 'Z': z in ker HX, nontrivial vs X-logicals.
    Seeds: qubit 0 (no exclusions) and qubit N (left block excluded)  [uses translation symmetry; verified separately]."""
    from rlib import logical_basis
    n=HX.shape[1]; N=n//2 if N is None else N
    LX,LZ=logical_basis(HX,HZ)
    checks,lg=(HZ,LZ) if sector=='X' else (HX,LX)
    cq,ql,lgp,mc=prep(checks,lg)
    out=[]
    for seed,excl in [(0,np.zeros(0,np.int32)),(N,np.arange(N,dtype=np.int32))]:
        r=search(cq,ql,lgp,mc,W,seed,excl,stop_first)
        out.append(r)
    return out
