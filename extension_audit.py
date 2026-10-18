import pathlib,json,hashlib,time,random,itertools,collections,ctypes,datetime
R=pathlib.Path(__file__).resolve().parent/'extension'
O=pathlib.Path(__file__).parent/'extension-audit';O.mkdir(exist_ok=True)
t=time.process_time();wall=time.perf_counter()
def read(n):return json.loads((R/n).read_text())
def lines(n):return [json.loads(x) for x in (R/n).read_text().splitlines()]
def hashes():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in R.iterdir() if p.is_file()}
before=hashes()
for n,h in read('freeze.json').items():assert before[n]==h
seeds=[x for x in lines('input-graphs.jsonl') if 3<=x['n']<=8]
assert len(seeds)==71
old=pathlib.Path(__file__).resolve().parent/'source-before.sha256.json'
assert before['input-graphs.jsonl']==json.loads(old.read_text())['runs\\pilot-001\\graphs.jsonl']
# Reconstruct ordered case inputs from protocol, without importing producer code.
families={f:[] for f in ['baseline','weighted','degree4','bicyclic']};rng=random.Random(20261018)
for g in seeds:
 n=g['n'];e=sorted(tuple(x) for x in g['edges']);a=[set() for _ in range(n)]
 for u,v in e:a[u].add(v);a[v].add(u)
 unit=[[*x,1] for x in e];families['baseline'].append((g,unit))
 for _ in range(3):
  weights=[rng.randrange(1,5) for edge in e]
  if min(weights)==max(weights):weights[0]=weights[0]%4+1
  families['weighted'].append((g,[[*edge,w] for edge,w in zip(e,weights)]))
 possible=[v for v in range(n) if len(a[v])==3]
 if n<=7 and possible:families['degree4'].append((g,unit+[[min(possible),n,1]]))
 nonedges=[(u,v) for u,v in itertools.combinations(range(n),2) if v not in a[u] and max(len(a[u]),len(a[v]))<=2]
 if nonedges:families['bicyclic'].append((g,unit+[[*min(nonedges),1]]))
plan=[]
for f,cases in families.items():
 for i,(g,e) in enumerate(cases):plan.append(dict(id=f+'-'+str(i).zfill(3),family=f,n=max(max(x[:2]) for x in e)+1,edges=e,source_key=g['key'],baseline_beta=g['beta'],baseline_beta2=g['beta2']))
assert plan==read('planned-cases.json')
rows=lines('results.jsonl');assert len(rows)==len(plan)==382
certs=lines('noise-boundary-certificates.jsonl');cm={(x['case'],x['mask']):x for x in certs};assert len(cm)==len(certs)
summary={f:dict(cases=0,bases=0,p=collections.Counter(),aug_pass=[0]*4,ft_pass=[0]*4,m2=collections.Counter(),distinct=set()) for f in families}
details=[];subset_count=0
for case,row in zip(plan,rows):
 assert time.process_time()-t<120,'bounded audit stop'
 assert all(row[k]==v for k,v in case.items()) and row['status']=='completed'
 n=case['n'];e=case['edges'];assert n<=8
 assert len({tuple(x[:2]) for x in e})==len(e) and all(0<=u<v<n and w>0 for u,v,w in e)
 deg=[sum(v in edge[:2] for edge in e) for v in range(n)]
 assert len(e)-n+1==(2 if case['family']=='bicyclic' else 1)
 assert max(deg)==4 if case['family']=='degree4' else max(deg)<=3
 # Bellman-Ford edge relaxation from scratch; neither original shortest-path routine.
 d=[]
 for source in range(n):
  ds=[10**6]*n;ds[source]=0
  for _ in range(n-1):
   prior=ds[:]
   for u,v,w in e:ds[u]=min(ds[u],prior[v]+w);ds[v]=min(ds[v],prior[u]+w)
  assert max(ds)<10**6;d.append(ds)
 assert d==row['distances']
 sensors=[[v for v in range(n) if m>>v&1] for m in range(1<<n)]
 resolving=[len({tuple(d[v][s] for s in ss) for v in range(n)})==n for ss in sensors]
 ft=[bool(ss) and all(resolving[m^(1<<s)] for s in ss) for m,ss in enumerate(sensors)]
 assert row['subset_flags']==[list(x) for x in zip(resolving,ft)]
 subset_count+=1<<n
 beta=min(len(sensors[m]) for m in range(1<<n) if resolving[m]);bases=[m for m in range(1<<n) if resolving[m] and len(sensors[m])==beta]
 ftsets=sorted((m for m in range(1<<n) if ft[m]),key=lambda m:(len(sensors[m]),m))
 beta2=len(sensors[ftsets[0]])
 assert (beta,beta2,ftsets[0])==(row['beta'],row['beta2'],row['beta2_witness'])
 assert [b['mask'] for b in row['bases']]==bases
 s=summary[case['family']];s['cases']+=1;s['bases']+=len(bases);s['distinct'].add((n,tuple(sorted(tuple(x) for x in e))))
 for b in row['bases']:
  best=next(m for m in ftsets if m&b['mask']==b['mask']);rho=len(sensors[best])
  assert (b['superset'],b['rho'],b['p'])==(best,rho,rho-beta2);s['p'][rho-beta2]+=1
 expected=set(bases)|{b['superset'] for b in row['bases']}|{ftsets[0]}
 assert [x['mask'] for x in row['noise_layouts']]==sorted(expected)
 noise={}
 for layout in row['noise_layouts']:
  m=layout['mask'];ss=sensors[m]
  # Enumerate every erased sensor and every target pair; do not use second-largest shortcut.
  full=[];lost=[]
  for u,v in itertools.combinations(range(n),2):
   full.append(max(abs(d[u][q]-d[v][q]) for q in ss))
   for erased in ss:lost.append((max((abs(d[u][q]-d[v][q]) for q in ss if q!=erased),default=0),u,v,erased))
  m1=min(full);m2=min(lost)[0]
  flags=[[gap*den>2*num for num,den in [(0,1),(1,4),(1,2),(1,1)]] for gap in [m1,m2]]
  assert (layout['m1'],layout['m2'])==(m1,m2)
  assert layout['epsilon']==['0','1/4','1/2','1']
  assert [layout['robust_without_loss'],layout['robust_one_erasure']]==flags
  c=cm.pop((case['id'],m));u,v=c['ambiguous_pair'];erased=c['erased_sensor'];survivors=[q for q in ss if q!=erased]
  assert u<v and erased in ss and c['remaining_sensors']==survivors and c['m2']==m2 and c['ambiguity_at_epsilon']==str(m2)+'/2'
  assert max((abs(d[u][q]-d[v][q]) for q in survivors),default=0)==m2
  assert c['twice_midpoint_readings']==[d[u][q]+d[v][q] for q in survivors]
  assert all(abs(y-2*d[u][q])<=m2 and abs(y-2*d[v][q])<=m2 for q,y in zip(survivors,c['twice_midpoint_readings']))
  noise[m]=(m2,flags[1])
 for b in row['bases']:
  gap,flags=noise[b['superset']];s['m2'][gap]+=1;s['aug_pass']=[a+int(b) for a,b in zip(s['aug_pass'],flags)]
  assert noise[b['mask']][0]==0
 s['ft_pass']=[a+int(b) for a,b in zip(s['ft_pass'],noise[ftsets[0]][1])]
 details.append(dict(id=case['id'],beta=beta,beta2=beta2,bases=len(bases),layouts=len(expected)))
assert not cm and subset_count==68576 and len(certs)==4675
for s in summary.values():s['distinct']=len(s['distinct'])
assert before==hashes()
times={n:dict(created=datetime.datetime.fromtimestamp((R/n).stat().st_ctime,datetime.timezone.utc).isoformat(),modified=datetime.datetime.fromtimestamp((R/n).stat().st_mtime,datetime.timezone.utc).isoformat()) for n in ['PROTOCOL.md','freeze.json','planned-cases.json','results.jsonl','run-manifest.json']}
class PMC(ctypes.Structure):
 _fields_=[('cb',ctypes.c_ulong),('PageFaultCount',ctypes.c_ulong)]+[(x,ctypes.c_size_t) for x in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
pm=PMC();pm.cb=ctypes.sizeof(pm);ctypes.windll.kernel32.GetCurrentProcess.restype=ctypes.c_void_p;ctypes.windll.psapi.GetProcessMemoryInfo.argtypes=[ctypes.c_void_p,ctypes.POINTER(PMC),ctypes.c_ulong]
assert ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.windll.kernel32.GetCurrentProcess(),ctypes.byref(pm),pm.cb)
out=dict(verdict='computational PASS; editorial corrections required',summary=summary,subset_entries=subset_count,noise_certificates=len(certs),cpu_seconds=time.process_time()-t,wall_seconds=time.perf_counter()-wall,peak_working_set_bytes=pm.PeakWorkingSetSize,timestamps=times,source_hashes=before,unchanged=True)
(O/'audit-result.json').write_text(json.dumps(out,indent=2));(O/'case-checks.json').write_text(json.dumps(details,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='source_hashes'},indent=2))
