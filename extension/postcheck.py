import json,hashlib,itertools
from pathlib import Path
from limits import install
stats,job=install(cpu=30,wall=40,memory=200000000,working_set=200000000)
r=Path(__file__).resolve().parent
for n,h in json.loads((r/'freeze.json').read_text()).items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
cases=json.loads((r/'planned-cases.json').read_text());rows=[json.loads(s) for s in (r/'results.jsonl').read_text().splitlines()]
assert [x['id'] for x in cases]==[x['id'] for x in rows]
certs=[];topologies={}
for c,x in zip(cases,rows):
 assert c['edges']==x['edges'] and c['n']==x['n']
 n=x['n'];e=x['edges'];deg=[sum(v in edge[:2] for edge in e) for v in range(n)]
 assert len({tuple(sorted(edge[:2])) for edge in e})==len(e)
 assert all(u!=v and w>0 for u,v,w in e)
 assert (len(e)-n+1,max(deg))==((2,max(deg)) if x['family']=='bicyclic' else (1,max(deg)))
 assert max(deg)==4 if x['family']=='degree4' else max(deg)<=3
 topologies.setdefault(x['family'],set()).add((n,tuple(sorted(tuple(edge) for edge in e))))
 for s in x['noise_layouts']:
  sensors=[k for k in range(n) if s['mask']>>k&1];d=x['distances'];candidates=[]
  for u,v in itertools.combinations(range(n),2):
   for lost in sensors:
    survivors=[k for k in sensors if k!=lost]
    gap=max([abs(d[u][k]-d[v][k]) for k in survivors],default=0)
    candidates.append((gap,u,v,lost,survivors))
  gap,u,v,lost,survivors=min(candidates)
  assert gap==s['m2']
  # At epsilon=m2/2, midpoint readings lie in both closed error boxes.
  twice_readings=[d[u][k]+d[v][k] for k in survivors]
  assert all(abs(y-2*d[u][k])<=gap and abs(y-2*d[v][k])<=gap for k,y in zip(survivors,twice_readings))
  certs.append({'case':x['id'],'mask':s['mask'],'m2':gap,'ambiguous_pair':[u,v],'erased_sensor':lost,'remaining_sensors':survivors,'twice_midpoint_readings':twice_readings,'ambiguity_at_epsilon':str(gap)+'/2'})
(r/'noise-boundary-certificates.jsonl').write_text(''.join(json.dumps(x,separators=(',',':'))+'\n' for x in certs))
report={'status':'PASS','all_case_ids_accounted_for':len(rows),'skipped':0,'noise_certificates':len(certs),'labelled_distinct_cases':{f:len(s) for f,s in topologies.items()},'freeze_hashes_unchanged':True,'resources':stats(),'method':'Explicit all-erasure maximum separation, and exact midpoint ambiguity at boundary; not independent human review'}
(r/'postcheck.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
