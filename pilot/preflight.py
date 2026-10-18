import argparse,json,time,subprocess,sys
from limits import install
p=argparse.ArgumentParser(); p.add_argument('mode',choices=['normal','cpu','memory','child','wall']); args=p.parse_args()
stats,job=install(cpu=1 if args.mode=='cpu' else 10,wall=1 if args.mode=='wall' else 15,memory=60_000_000 if args.mode=='memory' else 2_500_000_000)
if args.mode=='normal': print(json.dumps(stats()))
elif args.mode=='cpu':
    while True: pass
elif args.mode=='wall': time.sleep(20)
elif args.mode=='memory':
    try: x=bytearray(100_000_000)
    except MemoryError: print('memory limit enforced'); sys.exit(0)
    raise RuntimeError('Memory limit failed')
elif args.mode=='child':
    try: subprocess.run([sys.executable,'-c','pass'],check=True)
    except (OSError,subprocess.CalledProcessError): print('child limit enforced'); sys.exit(0)
    raise RuntimeError('Child limit failed')
