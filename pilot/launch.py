"""One bounded launch containing controls, fixtures, exact search and verification."""
import json,subprocess,sys,time
from pathlib import Path
from limits import install
stats,job=install(cpu=7000,wall=6900,memory=3_300_000_000,active=2,working_set=256_000_000)
root=Path(__file__).resolve().parent
log=root/'launch-record.json'
if log.exists(): raise RuntimeError('No fresh budget on restart; review existing launch record')
record={'status':'preflight','checks':[]}
def save():
    record['resources']=stats(); log.write_text(json.dumps(record,indent=2),encoding='utf-8')
save()
try:
    for mode in ['normal','memory','child','cpu','wall']:
        t=time.monotonic()
        r=subprocess.run([sys.executable,str(root/'preflight.py'),mode],cwd=root,capture_output=True,text=True,timeout=20)
        item={'mode':mode,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'wall_seconds':time.monotonic()-t}
        record['checks'].append(item); save()
        if mode in ['normal','memory','child']: assert r.returncode==0,item
        elif mode=='wall': assert r.returncode==124,item
        else: assert r.returncode!=0 and item['wall_seconds']<10,item
    record['status']='running'; save()
    r=subprocess.run([sys.executable,str(root/'run.py')],cwd=root,timeout=6650)
    record['worker_exit']=r.returncode; record['status']='finished' if r.returncode==0 else 'failed'
finally: save()
