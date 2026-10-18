import collections, hashlib, itertools, json, pathlib, time, sys, ctypes
from independent_core import exact, canonical, distances

ROOT = pathlib.Path(__file__).resolve().parents[1] / 'pilot'
OUT = pathlib.Path(__file__).parent
START = time.process_time()
WALL = time.perf_counter()

def guard():
    if time.process_time() - START > 570:
        raise RuntimeError('CPU guard reached; stop before ten CPU minutes')

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(name):
    return [json.loads(line) for line in (ROOT/'runs/pilot-001'/name).read_text().splitlines()]

def cycle_keys(limit):
    # Rooted trees with <=2 children: root has one parent towards the cycle.
    trees = {0: [''], 1: ['()']}
    for n in range(2, limit-2):
        values = {'(' + t + ')' for t in trees[n-1]}
        for a in range(1, n-1):
            b = n-1-a
            for x in trees[a]:
                for y in trees[b]:
                    values.add('(' + ''.join(sorted([x,y])) + ')')
        trees[n] = sorted(values)
    def compositions(total, count):
        if count == 1:
            yield (total,)
        else:
            for a in range(total+1):
                for tail in compositions(total-a, count-1):
                    yield (a,) + tail
    levels = {}
    for n in range(3, limit+1):
        keys = set()
        for k in range(3, n+1):
            for sizes in compositions(n-k, k):
                for attachments in itertools.product(*(trees[s] for s in sizes)):
                    seq = ['(' + t + ')' for t in attachments]
                    keys.add(min(tuple(q[i:] + q[:i]) for q in (seq, seq[::-1]) for i in range(k)))
            guard()
        levels[n] = keys
    return levels

def main():
    before = {str(p.relative_to(ROOT)):digest(p) for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    (OUT/'source-before.sha256.json').write_text(json.dumps(before, indent=2))
    graphs, bases, certs = load('graphs.jsonl'), load('bases.jsonl'), load('certificates.jsonl')
    grouped = collections.defaultdict(list)
    for b in bases: grouped[b['key']].append(b)
    certmap = {c['key']:c for c in certs}
    assert len(certmap)==len(certs)==len(graphs)==331
    independent = cycle_keys(10)
    seen = collections.defaultdict(set)
    distribution = collections.Counter()
    details, contradictions = [], []
    for g in graphs:
        guard()
        n, edges, key = g['n'], g['edges'], g['key']
        d, adj = distances(n, edges)
        assert len(edges)==n and max(map(len,adj))<=3 and 3<=n<=10
        iso = canonical(n,edges)
        assert iso not in seen[n], ('duplicate class', key)
        seen[n].add(iso)
        a = exact(n,edges)
        assert d==g['distances'] and a['beta']==g['beta'] and a['beta2']==g['beta2'], key
        assert g['beta2_witness'] in a['ft_masks'] and g['beta2_witness'].bit_count()==a['beta2'], key
        rows=grouped.pop(key)
        assert len(rows)==g['base_count']==len(a['bases']) and {r['base'] for r in rows}==set(a['bases']), key
        for r in rows:
            b=r['base']; s=r['superset']; rho=a['rho'][b]
            assert r['n']==n and r['rho']==rho and r['p']==rho-a['beta2'], (key,b)
            assert s in a['ft_masks'] and s & b == b and s.bit_count()==rho, (key,b)
            distribution[r['p']]+=1
        # Audit every saved certificate failure-pair, not just optimal values.
        table=certmap[key]['table']; assert len(table)==1<<n
        for m,row in enumerate(table):
            assert row[0]==m.bit_count()
            for col,threshold,valid in [(1,1,m in a['resolving_masks']),(2,2,m in a['ft_masks'])]:
                pair=row[col]
                assert (pair is None)==valid, (key,m,col)
                if pair is not None:
                    u,v=pair
                    assert 0<=u<v<n
                    assert sum(d[u][s]!=d[v][s] for s in range(n) if m>>s&1)<threshold
        # Terminal fork: off-cycle degree-three vertex with two branches
        # consisting only of degree-two vertices ending at leaves.
        live=set(range(n)); deg=list(map(len,adj)); queue=collections.deque(v for v in live if deg[v]==1)
        while queue:
            v=queue.popleft(); live.remove(v)
            for w in adj[v]&live:
                deg[w]-=1
                if deg[w]==1: queue.append(w)
        L=0
        for v in set(range(n))-live:
            if len(adj[v])!=3: continue
            terminal=0
            for w in adj[v]:
                prev=v
                while len(adj[w])==2:
                    nxt=next(x for x in adj[w] if x!=prev); prev,w=w,nxt
                terminal += len(adj[w])==1
            L += terminal==2
        if any(r['p']>a['beta']-L for r in rows): contradictions.append(key)
        details.append(dict(key=key,n=n,beta=a['beta'],beta2=a['beta2'],bases=len(rows),L=L,
                            subsets=a['subset_count'],rho_histogram=dict(collections.Counter(a['rho'].values()))))
    assert not grouped
    for n in range(3,11): assert seen[n]==independent[n], ('coverage mismatch',n)
    assert dict(distribution)=={0:3761,1:139}
    witness_edges=[(0,1),(0,2),(0,3),(1,4),(2,5),(4,5),(5,6)]
    witness=exact(7,witness_edges); B=(1<<0)|(1<<5)
    assert witness['beta']==2 and witness['beta2']==3 and witness['rho'][B]==4
    assert sum(1<<s for s in [1,2,3]) in witness['ft_masks']
    assert sum(1<<s for s in [0,1,2,5]) in witness['ft_masks']
    calibrations=[]
    for n in range(3,11):
        for kind,edges in [('path',[(i,i+1) for i in range(n-1)]),('cycle',[(i,(i+1)%n) for i in range(n)])]:
            a=exact(n,edges)
            expected=(1,2) if kind=='path' else (2,4 if n==4 else 3)
            assert (a['beta'],a['beta2'])==expected, (kind,n)
            calibrations.append(dict(kind=kind,n=n,beta=a['beta'],beta2=a['beta2']))
    star=exact(4,[(0,1),(0,2),(0,3)]); assert (star['beta'],star['beta2'])==(2,3)
    after={str(p.relative_to(ROOT)):digest(p) for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    assert before==after, 'original files changed during audit'
    class PMC(ctypes.Structure):
        _fields_=[('cb',ctypes.c_ulong),('PageFaultCount',ctypes.c_ulong)]+[(x,ctypes.c_size_t) for x in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
    pm=PMC();pm.cb=ctypes.sizeof(pm)
    ctypes.windll.kernel32.GetCurrentProcess.restype=ctypes.c_void_p
    ctypes.windll.psapi.GetProcessMemoryInfo.argtypes=[ctypes.c_void_p,ctypes.POINTER(PMC),ctypes.c_ulong]
    assert ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(),ctypes.byref(pm),pm.cb)
    result=dict(verdict='PASS',graphs=len(graphs),bases=len(bases),coverage={n:len(v) for n,v in independent.items()},
                p_histogram=dict(distribution),subset_checks=sum(x['subsets'] for x in details),
                witness=witness,calibrations=calibrations,star_beta=[star['beta'],star['beta2']],
                optional_exchange_contradictions=contradictions,original_files_unchanged=True,
                cpu_seconds=time.process_time()-START,wall_seconds=time.perf_counter()-WALL,
                peak_working_set_bytes=pm.PeakWorkingSetSize,python=sys.version)
    (OUT/'audit-result.json').write_text(json.dumps(result,indent=2))
    (OUT/'graph-audit.json').write_text(json.dumps(details,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ['witness','calibrations']},indent=2))

if __name__=='__main__':
    try: main()
    except Exception as e:
        (OUT/'CRITICAL-STOP.txt').write_text(repr(e))
        raise
