from collections import deque
from itertools import combinations
from generate import adjacency

def solve(n,edges):
    a=adjacency(n,edges); d=[]
    assert len(edges)==n and max(map(len,a))<=3 and len(set(edges))==n
    for s in range(n):
        row=[-1]*n; row[s]=0; q=deque([s])
        while q:
            v=q.popleft()
            for u in a[v]:
                if row[u]<0: row[u]=row[v]+1; q.append(u)
        assert min(row)>=0
        d.append(row)
    pairs=list(combinations(range(n),2))
    distinguishes=[sum(1<<s for s in range(n) if d[u][s]!=d[v][s]) for u,v in pairs]
    table=[]; resolving=[]; ft=[]
    for mask in range(1<<n):
        counts=[(mask&ds).bit_count() for ds in distinguishes]
        bad1=next((pairs[i] for i,x in enumerate(counts) if x<1),None)
        bad2=next((pairs[i] for i,x in enumerate(counts) if x<2),None)
        table.append([mask.bit_count(),bad1,bad2])
        if bad1 is None: resolving.append(mask)
        if bad2 is None: ft.append(mask)
    beta=min(m.bit_count() for m in resolving); beta2=min(m.bit_count() for m in ft)
    bases=[b for b in resolving if b.bit_count()==beta]
    ft.sort(key=lambda m:(m.bit_count(),m)); results=[]
    for b in bases:
        s=next(s for s in ft if s&b==b)
        results.append(dict(base=b,rho=s.bit_count(),p=s.bit_count()-beta2,superset=s))
    return dict(n=n,edges=edges,distances=d,beta=beta,beta2=beta2,beta2_witness=ft[0],bases=results,table=table)
