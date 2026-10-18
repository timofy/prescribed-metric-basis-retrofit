"""Post-run serialization/hash and label audit; never generates new graph classes."""
import json,hashlib,time,itertools
from pathlib import Path
from collections import defaultdict,Counter
from limits import install
stats,job=install(cpu=50,wall=60,memory=500_000_000,working_set=600_000_000)
from verify import verify
from generate import graph_key
root=Path(__file__).resolve().parent; out=root/'runs'/'pilot-001'
def read(name): return json.loads((out/name).read_text())
manifest=read('manifest.json')
for name,digest in manifest['input_hashes_after'].items(): assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest
for name,digest in manifest['outputs'].items(): assert hashlib.sha256((out/name).read_bytes()).hexdigest()==digest
for item in json.loads((root/'freeze.sha256.json').read_text(encoding='utf-8-sig')): assert hashlib.sha256((root/item['path']).read_bytes()).hexdigest()==item['sha256']
graphs=[json.loads(line) for line in (out/'graphs.jsonl').read_text().splitlines()]
bases=defaultdict(list)
for line in (out/'bases.jsonl').read_text().splitlines():
    b=json.loads(line); bases[b['key']].append({k:v for k,v in b.items() if k not in ('n','key')})
certs={r['key']:r for r in map(json.loads,(out/'certificates.jsonl').read_text().splitlines())}
assert len(graphs)==len(certs)==len(bases)==331
candidate=None; relabelings=0; subset_count=0; pgraphs=Counter()
for g in graphs:
    r=dict(g,bases=bases[g['key']],table=certs[g['key']]['table']); subset_count+=verify(r)['subsets']
    n=g['n']; perms=list(itertools.permutations(range(n))) if n<=5 else [tuple(reversed(range(n))),tuple((i+1)%n for i in range(n))]
    for perm in perms:
        edges=sorted(tuple(sorted((perm[u],perm[v]))) for u,v in g['edges'])
        assert graph_key(n,edges)==g['key']
        # A relabeling's pair obstruction and witness masks are transported exactly.
        for b in r['bases']:
            mb=sum(1<<perm[i] for i in range(n) if b['base']>>i&1)
            ms=sum(1<<perm[i] for i in range(n) if b['superset']>>i&1)
            assert mb&ms==mb and mb.bit_count()==g['beta'] and ms.bit_count()==b['rho']
        relabelings+=1
    if any(b['p']==1 for b in r['bases']): pgraphs[n]+=1
    if candidate is None and any(b['p']==1 for b in r['bases']):
        selected=next(b for b in r['bases'] if b['p']==1)
        candidate=dict(r,selected_base=selected,interpretation='Penalty-one example for external verification; not a counterexample')
(out/'external-verification-candidate.json').write_text(json.dumps(candidate,indent=2),encoding='utf-8')
result=dict(status='passed',graphs_roundtrip_verified=len(graphs),bases_roundtrip_verified=sum(map(len,bases.values())),subsets_roundtrip_verified=subset_count,relabelings_checked=relabelings,graphs_with_penalty_one_by_n=dict(pgraphs),resources=stats())
(out/'saved-artifact-audit.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result)); print(json.dumps({k:v for k,v in candidate.items() if k not in ('table','distances','bases')}))
