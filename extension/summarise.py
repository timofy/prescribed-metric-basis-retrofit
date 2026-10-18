import json,collections
from pathlib import Path
r=Path(__file__).resolve().parent;rows=[json.loads(s) for s in (r/'results.jsonl').read_text().splitlines()];out={}
for family in ['baseline','weighted','degree4','bicyclic']:
 rr=[x for x in rows if x['family']==family];hist=collections.Counter(b['p'] for x in rr for b in x['bases']);sub=sum(len(x['subset_flags']) for x in rr)
 roles={}
 for role in ['minimum_basis','minimum_augmentation','unconstrained_ft']:
  selected=[]
  for x in rr:
   lookup={s['mask']:s for s in x['noise_layouts']}
   masks=[b['mask'] for b in x['bases']] if role=='minimum_basis' else [b['superset'] for b in x['bases']] if role=='minimum_augmentation' else [x['beta2_witness']]
   selected.extend(lookup[m] for m in masks)
  roles[role]={'rows':len(selected),'m2_histogram':dict(sorted(collections.Counter(s['m2'] for s in selected).items())),'robust_one_erasure_counts':[sum(s['robust_one_erasure'][j] for s in selected) for j in range(4)],'robust_without_loss_counts':[sum(s['robust_without_loss'][j] for s in selected) for j in range(4)]}
 out[family]={'cases':len(rr),'bases':sum(hist.values()),'premium_histogram':dict(hist),'subset_entries':sub,'noise_roles':roles}
(r/'summary.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

