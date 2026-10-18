from itertools import combinations

def adjacency(n,edges):
    a=[set() for _ in range(n)]
    for u,v in edges: a[u].add(v); a[v].add(u)
    return a

def tree_key(n,edges):
    a=adjacency(n,edges)
    def rooted(v,p): return '('+''.join(sorted(rooted(u,v) for u in a[v] if u!=p))+')'
    # Minimum over all roots is also a complete, exact tree invariant.
    return min(rooted(v,-1) for v in range(n))

def graph_key(n,edges):
    a=adjacency(n,edges); live=set(range(n)); leaves=[v for v in live if len(a[v])==1]
    deg=list(map(len,a))
    while leaves:
        v=leaves.pop(); live.remove(v)
        for u in a[v]:
            if u in live:
                deg[u]-=1
                if deg[u]==1: leaves.append(u)
    assert len(live)>=3
    cycle=[min(live)]; previous=-1
    while True:
        choices=sorted(a[cycle[-1]] & live - {previous})
        nxt=choices[0]; previous=cycle[-1]
        if nxt==cycle[0]: break
        cycle.append(nxt)
    assert set(cycle)==live
    def branch(v,p): return '('+''.join(sorted(branch(u,v) for u in a[v] if u!=p and u not in live))+')'
    seq=[branch(v,-1) for v in cycle]
    variants=[]
    for order in (seq,seq[::-1]):
        variants.extend('|'.join(order[i:]+order[:i]) for i in range(len(order)))
    return str(len(cycle))+':'+min(variants)

def primary_orders(max_n=10):
    trees={'()':()}
    for n in range(2,max_n+1):
        new={}
        for edges in trees.values():
            a=adjacency(n-1,edges)
            for v in range(n-1):
                if len(a[v])<3:
                    e=tuple(sorted(edges+((v,n-1),)))
                    new.setdefault(tree_key(n,e),e)
        trees=new
        if n<3: continue
        graphs={}; candidates=0
        for t in (trees[k] for k in sorted(trees)):
            a=adjacency(n,t)
            for u,v in combinations(range(n),2):
                if v not in a[u] and len(a[u])<3 and len(a[v])<3:
                    e=tuple(sorted(t+((u,v),))); candidates+=1
                    graphs.setdefault(graph_key(n,e),e)
        yield n,graphs,dict(trees=len(trees),edge_additions=candidates,classes=len(graphs))
