"""Exact finite extension; independent signature/deletion verifier; no dependencies."""
import json,hashlib,heapq,itertools,time,sys,platform,datetime,traceback
from pathlib import Path
from limits import install
ROOT=Path(__file__).resolve().parent
if (ROOT/'run-manifest.json').exists():raise RuntimeError('Existing launch: no automatic budget reset')
for n,h in json.loads((ROOT/'freeze.json').read_text()).items():
 assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
stats,job=install(cpu=1000,wall=1100,memory=3300000000,working_set=3000000000)
manifest={'status':'running','started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),'argv':sys.argv,'assertion_tested':'finite prescribed-basis premium and deterministic bounded-error separation, per frozen protocol','cases_completed':0,'independent_check':'Dijkstra and tuple-signature deletion for every subset'}
def save():
 manifest['resources']=stats();(ROOT/'run-manifest.json').write_text(json.dumps(manifest,indent=2))
def guard():
 if time.process_time()>1100:raise TimeoutError('CPU budget guard')
def distances(n,edges):
 d=[[0 if i==j else 10**9 for j in range(n)] for i in range(n)]
 for u,v,w in edges:d[u][v]=d[v][u]=w
 for k in range(n):
  for i in range(n):
   for j in range(n):d[i][j]=min(d[i][j],d[i][k]+d[k][j])
 # Independent shortest-path implementation.
 a=[[] for _ in range(n)]
 for u,v,w in edges:a[u].append((v,w));a[v].append((u,w))
 for s in range(n):
  dd=[10**9]*n;dd[s]=0;q=[(0,s)]
  while q:
   dist,v=heapq.heappop(q)
   if dist!=dd[v]:continue
   for u,w in a[v]:
    if dist+w<dd[u]:dd[u]=dist+w;heapq.heappush(q,(dd[u],u))
  assert dd==d[s]
 return d
def solve(n,e):
 guard();d=distances(n,e);pairs=list(itertools.combinations(range(n),2))
 masks=[sum(1<<s for s in range(n) if d[u][s]!=d[v][s]) for u,v in pairs]
 table=[];independent=[]
 def unique(sensors):return len({tuple(d[v][s] for s in sensors) for v in range(n)})==n
 for m in range(1<<n):
  count=[(m&x).bit_count() for x in masks]
  row=[min(count)>=1,min(count)>=2];table.append(row)
  sensors=[s for s in range(n) if m>>s&1]
  check=[unique(sensors),len(sensors)>=2 and all(unique([s for s in sensors if s!=lost]) for lost in sensors)]
  assert row==check,(m,row,check)
  independent.append(check)
 res=[m for m,r in enumerate(table) if r[0]];fts=sorted([m for m,r in enumerate(table) if r[1]],key=lambda m:(m.bit_count(),m))
 beta=min(m.bit_count() for m in res);beta2=fts[0].bit_count();bases=[]
 for b in res:
  if b.bit_count()!=beta:continue
  sup=next(m for m in fts if m&b==b)
  rho=min(m.bit_count() for m,r in enumerate(independent) if r[1] and m&b==b)
  assert rho==sup.bit_count()
  bases.append({'mask':b,'rho':rho,'p':rho-beta2,'superset':sup})
 assert beta==min(m.bit_count() for m,r in enumerate(independent) if r[0])
 assert beta2==min(m.bit_count() for m,r in enumerate(independent) if r[1])
 def noise(m):
  sensors=[s for s in range(n) if m>>s&1]
  gaps=[sorted([abs(d[u][s]-d[v][s]) for s in sensors],reverse=True)+[0,0] for u,v in pairs]
  m1=min(g[0] for g in gaps);m2=min(g[1] for g in gaps)
  return {'mask':m,'m1':m1,'m2':m2,'epsilon':['0','1/4','1/2','1'],'robust_without_loss':[m1*den>2*num for num,den in [(0,1),(1,4),(1,2),(1,1)]],'robust_one_erasure':[m2*den>2*num for num,den in [(0,1),(1,4),(1,2),(1,1)]]}
 layouts=sorted({fts[0]}|{b['mask'] for b in bases}|{b['superset'] for b in bases})
 return {'distances':d,'beta':beta,'beta2':beta2,'beta2_witness':fts[0],'bases':bases,'subset_flags':table,'noise_layouts':[noise(m) for m in layouts],'verification':'PASS'}
save()
try:
 fixture=solve(3,[[0,1,1],[0,2,1],[1,2,1]])
 assert (fixture['beta'],fixture['beta2'])==(2,3)
 fixture=solve(3,[[0,1,1],[0,2,2],[1,2,2]])
 assert fixture['distances']==[[0,1,2],[1,0,2],[2,2,0]] and fixture['beta']==1 and fixture['beta2']==2
 manifest['fixtures']='PASS'
 cases=json.loads((ROOT/'planned-cases.json').read_text());stopped=set();counterexamples=[]
 with (ROOT/'results.jsonl').open('w',encoding='utf-8') as out:
  for c in cases:
   guard()
   if c['family'] in stopped:
    out.write(json.dumps({'id':c['id'],'family':c['family'],'status':'skipped-after-counterexample'})+'\n');continue
   result=solve(c['n'],c['edges'])
   if c['family']=='baseline':assert (result['beta'],result['beta2'])==(c['baseline_beta'],c['baseline_beta2'])
   row={**c,**result,'status':'completed'};out.write(json.dumps(row,separators=(',',':'))+'\n');out.flush()
   manifest['cases_completed']+=1
   bad=[b for b in result['bases'] if b['p']>1]
   if bad:
    assert c['family']!='baseline'
    stopped.add(c['family']);counterexamples.append({'case':c['id'],'basis':bad[0]})
   manifest['counterexamples']=counterexamples;save()
 manifest['status']='completed'
except Exception:
 manifest['status']='resource-limit' if sys.exc_info()[0] is TimeoutError else 'failed';manifest['error']=traceback.format_exc();raise
finally:
 manifest['finished']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
print(json.dumps(manifest,indent=2))
