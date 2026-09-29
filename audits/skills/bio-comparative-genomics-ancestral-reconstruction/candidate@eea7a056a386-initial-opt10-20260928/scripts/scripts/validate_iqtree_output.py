#!/usr/bin/env python3
import importlib.util
import pathlib
import pandas as pd
import sys
sys.dont_write_bytecode = True

root=pathlib.Path('/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction')
cand=pathlib.Path('/mnt/openscience/wt/opt10-ancestral-reconstruction/skills/bio-comparative-genomics-ancestral-reconstruction')
p=root/'runs/iqtree-candidate/asr_iqtree.state'
assert p.exists() and p.stat().st_size > 0
df=pd.read_csv(p,sep='\t',comment='#')
pc=[x for x in df.columns if x.startswith('p_')]
assert {'Node','Site','State'} <= set(df.columns)
assert len(pc)==20
assert df[pc].notna().all().all()
assert ((df[pc].sum(axis=1)-1).abs()<2e-4).all()
assert (df['Site']>=1).all() and df['Node'].nunique() >= 1
spec=importlib.util.spec_from_file_location('candidate_iqstate',cand/'scripts/iqtree_state.py')
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
groups=mod.load_iqtree_state(p)
recombined=pd.concat([g for _,g in groups])
assert len(recombined)==len(df)
assert (recombined.max_post >= 0).all() and (recombined.max_post <= 1).all()
assert (recombined.State == recombined[pc].idxmax(axis=1).str.removeprefix('p_')).all()
print('rows',len(df),'nodes',df.Node.nunique(),'sites',df.Site.nunique(),'probability_columns',len(pc))
print('max_probability_sum_error',float((df[pc].sum(axis=1)-1).abs().max()))
print('state_columns','\t'.join(df.columns))

