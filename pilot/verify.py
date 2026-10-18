"""Independent verifier: no imports from generator or solver."""
from itertools import combinations, product
from functools import lru_cache

def matrix(n,edges):
    a=[[False]*n for _ in range(n)]
    for u,v in edges:
        assert 0<=u<v<n and not a[u][v]
        a[u][v]=a[v][u]=True
    return a

def verify(record):
    n=record['n']; a=matrix(n,record['edges'])
    assert sum(sum(r) for r in a)==2*n and max(map(sum,a))<=3
    d=[[0 if i==j else 1 if a[i][j] else n+1 for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n): d[i][j]=min(d[i][j],d[i][k]+d[k][j])
    assert max(map(max,d))<n and d==record['distances']
    def resolves(s): return len({tuple(d[v][w] for w in s) for v in range(n)})==n
    rs=[]; fts=[]; table={}
    for k in range(n+1):
        for s in combinations(range(n),k):
            r=resolves(s)
            f=bool(s) and all(resolves(s[:i]+s[i+1:]) for i in range(len(s)))
            m=sum(2**v for v in s); table[m]=(r,f)
            if r: rs.append(s)
            if f: fts.append(s)
    beta=len(rs[0]); beta2=len(fts[0]); bases=[s for s in rs if len(s)==beta]
    assert (beta,beta2)==(record['beta'],record['beta2'])
    expected={sum(2**v for v in b):b for b in bases}
    assert set(expected)=={b['base'] for b in record['bases']}
    assert len(expected)==len(record['bases'])
    for result in record['bases']:
        b=expected[result['base']]
        candidates=[s for s in fts if set(b)<=set(s)]
        rho=len(candidates[0]); witness=min(sum(2**v for v in s) for s in candidates if len(s)==rho)
        assert (rho,rho-beta2,witness)==(result['rho'],result['p'],result['superset'])
    assert record['beta2_witness']==min(sum(2**v for v in s) for s in fts if len(s)==beta2)
    assert len(record['table'])==2**n
    for m,(size,bad1,bad2) in enumerate(record['table']):
        s=tuple(v for v in range(n) if m//2**v%2)
        assert size==len(s)
        r,f=table[m]; assert (bad1 is None)==r and (bad2 is None)==f
        for bad,threshold in ((bad1,1),(bad2,2)):
            if bad is not None:
                u,v=bad; assert u<v and sum(d[u][w]!=d[v][w] for w in s)<threshold
    return dict(bases=len(bases),subsets=2**n)

def invariant(n,edges):
    a=matrix(n,edges); degrees=list(map(sum,a))
    return tuple(sorted((degrees[v],tuple(sorted(degrees[u] for u in range(n) if a[v][u]))) for v in range(n)))

def isomorphic(n,e1,e2):
    a=matrix(n,e1); b=matrix(n,e2)
    da=list(map(sum,a)); db=list(map(sum,b))
    if sorted(da)!=sorted(db): return False
    ca=[(da[v],tuple(sorted(da[u] for u in range(n) if a[v][u]))) for v in range(n)]
    cb=[(db[v],tuple(sorted(db[u] for u in range(n) if b[v][u]))) for v in range(n)]
    candidates=[[w for w in range(n) if ca[v]==cb[w]] for v in range(n)]
    mapping={}; used=set()
    def walk():
        if len(mapping)==n: return True
        v=min((v for v in range(n) if v not in mapping),key=lambda v:(-sum(a[v][u] for u in mapping),len(candidates[v]),-da[v],v))
        for w in candidates[v]:
            if w not in used and all(a[v][u]==b[w][x] for u,x in mapping.items()):
                mapping[v]=w; used.add(w)
                if walk(): return True
                del mapping[v]; used.remove(w)
        return False
    return walk()

@lru_cache(None)
def rooted(size):
    if size==1: return ((),)
    out=set((t,) for t in rooted(size-1))
    for left in range(1,size-1):
        right=size-1-left
        for a in rooted(left):
            for b in rooted(right): out.add(tuple(sorted((a,b))))
    return tuple(sorted(out))

def compositions(total,length):
    if length==1:
        yield (total,); return
    for x in range(total+1):
        for tail in compositions(total-x,length-1): yield (x,)+tail

def secondary(n,primary_edges):
    # Raw cycle/attachment construction; exact adjacency isomorphism is equality.
    buckets={}; accepted=[]; raw=0
    for k in range(3,n+1):
        for sizes in compositions(n-k,k):
            for trees in product(*(rooted(s) if s else (None,) for s in sizes)):
                edges=[(i,(i+1)%k) for i in range(k)]; next_vertex=k
                def add(parent,tree):
                    nonlocal next_vertex
                    v=next_vertex; next_vertex+=1; edges.append((parent,v))
                    for child in tree: add(v,child)
                for v,t in enumerate(trees):
                    if t is not None: add(v,t)
                assert next_vertex==n
                e=tuple(sorted(tuple(sorted(x)) for x in edges)); raw+=1
                inv=invariant(n,e); bucket=buckets.setdefault(inv,[])
                if not any(isomorphic(n,e,old) for old in bucket): bucket.append(e); accepted.append(e)
    matched=set()
    for e in primary_edges:
        inv=invariant(n,e); matches=[i for i,other in enumerate(buckets.get(inv,[])) if isomorphic(n,e,other)]
        assert len(matches)==1
        ident=(inv,matches[0]); assert ident not in matched; matched.add(ident)
    assert len(matched)==len(accepted)==len(primary_edges)
    return dict(raw_cycle_constructions=raw,secondary_classes=len(accepted),matched_classes=len(matched))
