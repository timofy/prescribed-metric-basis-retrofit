import hashlib,json,random,shutil
from pathlib import Path
r=Path(__file__).resolve().parent
source=r.parent/'pilot/runs/pilot-001/graphs.jsonl'
shutil.copyfile(source,r/'input-graphs.jsonl')
graphs=[json.loads(s) for s in source.read_text().splitlines() if json.loads(s)['n']<=8]
cases=[]
def add(f,g,e):
 cases.append(dict(id=f+'-'+str(sum(c['family']==f for c in cases)).zfill(3),family=f,n=max(max(x[:2]) for x in e)+1,edges=e,source_key=g['key'],baseline_beta=g['beta'],baseline_beta2=g['beta2']))
for g in graphs:add('baseline',g,[[u,v,1] for u,v in sorted(g['edges'])])
rng=random.Random(20261018)
for g in graphs:
 for j in range(3):
  e=[[u,v,rng.randint(1,4)] for u,v in sorted(g['edges'])]
  if len({x[2] for x in e})==1:e[0][2]=1+e[0][2]%4
  add('weighted',g,e)
for g in graphs:
 deg=[sum(v in x for x in g['edges']) for v in range(g['n'])]
 if g['n']<=7 and 3 in deg:add('degree4',g,[[u,v,1] for u,v in sorted(g['edges'])]+[[deg.index(3),g['n'],1]])
for g in graphs:
 deg=[sum(v in x for x in g['edges']) for v in range(g['n'])]
 options=[(u,v) for u in range(g['n']) for v in range(u+1,g['n']) if [u,v] not in g['edges'] and deg[u]<=2 and deg[v]<=2]
 if options:add('bicyclic',g,[[u,v,1] for u,v in sorted(g['edges'])]+[[*options[0],1]])
(r/'planned-cases.json').write_text(json.dumps(cases,separators=(',',':')))
print({f:sum(c['family']==f for c in cases) for f in ['baseline','weighted','degree4','bicyclic']})
