import json,time,sys,hashlib,platform,os
from pathlib import Path
from collections import Counter
from limits import install
stats,job=install()
from generate import primary_orders,graph_key
from solve import solve
from verify import verify,secondary

root=Path(__file__).resolve().parent
out=root/'runs'/'pilot-001'; out.mkdir(parents=True,exist_ok=False)
def write(name,value): (out/name).write_text(json.dumps(value,indent=2),encoding='utf-8')
def hashes(): return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*.py'))}
before=hashes(); started=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
coverage=[]; distribution=Counter(); total_bases=0; graph_count=0; candidate=None
handles={name:(out/(name+'.jsonl')).open('w',encoding='utf-8') for name in ['graphs','bases','certificates']}
status='running'
try:
    for n,expected in ((3,(2,3)),(4,(2,4)),(5,(2,3))):
        e=tuple(sorted(tuple(sorted((i,(i+1)%n))) for i in range(n)))
        r=solve(n,e); verify(r); assert (r['beta'],r['beta2'])==expected
    for n,graphs,counts in primary_orders():
        t=time.process_time(); counts['n']=n; counts['solved']=0; counts['bases']=0; counts['penalties']=Counter()
        counts.update(secondary(n,list(graphs.values())))
        for key in sorted(graphs):
            if time.process_time()>6000: raise TimeoutError('Reserved closeout budget reached')
            r=solve(n,graphs[key]); verify(r)
            r['key']=key
            cert={'key':key,'table_columns':['cardinality','first_failing_pair_resolving','first_failing_pair_fault_tolerant'],'table':r['table']}
            g={k:v for k,v in r.items() if k not in ('table','bases')}; g['base_count']=len(r['bases'])
            for name,record in [('graphs',g),('certificates',cert)]: handles[name].write(json.dumps(record,separators=(',',':'))+'\n'); handles[name].flush()
            for b in r['bases']:
                handles['bases'].write(json.dumps(dict(key=key,n=n,**b),separators=(',',':'))+'\n')
                distribution[b['p']]+=1; counts['penalties'][b['p']]+=1
            handles['bases'].flush()
            graph_count+=1; total_bases+=len(r['bases']); counts['solved']+=1; counts['bases']+=len(r['bases'])
            if any(b['p']>=2 for b in r['bases']):
                candidate=r; write('counterexample.json',r); status='counterexample_verified'; break
        counts['cpu_seconds_solve_verify_and_coverage']=time.process_time()-t
        counts['complete']=counts['solved']==counts['classes']; coverage.append(counts); write('coverage.json',coverage)
        print(json.dumps(counts),flush=True)
        if candidate: break
    else: status='finite_assertion_verified'
except BaseException as error:
    status='failed'; write('error.json',{'type':type(error).__name__,'message':str(error)}); raise
finally:
    for f in handles.values(): f.close()
    outputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()}
    write('manifest.json',dict(status=status,start_utc=started,end_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),argv=sys.argv,python=sys.version,executable=sys.executable,platform=platform.platform(),cpu_count=os.cpu_count(),input_hashes_before=before,input_hashes_after=hashes(),outputs=outputs,resources=stats(),graphs_verified=graph_count,bases_verified=total_bases,penalty_counts=dict(distribution),min_p=min(distribution) if distribution else None,max_p=max(distribution) if distribution else None,randomness=False))
print(json.dumps({'status':status,'graphs':graph_count,'bases':total_bases,'penalties':dict(distribution),'resources':stats()}),flush=True)
