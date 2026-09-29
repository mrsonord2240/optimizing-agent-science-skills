import importlib.util
import json
import pathlib
import sys

sys.dont_write_bytecode = True
root = pathlib.Path('/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction')
cand = pathlib.Path('/mnt/openscience/wt/opt10-ancestral-reconstruction/skills/bio-comparative-genomics-ancestral-reconstruction')
out = pathlib.Path('/mnt/openscience/audits/bio-comparative-genomics-ancestral-reconstruction/reaudit-opt10-20260928/evidence')
run = out / 'iqtree-run'
spec = importlib.util.spec_from_file_location('iqtree_state', cand / 'scripts/iqtree_state.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
state = run / 'asr_iqtree.state'
df = __import__('pandas').read_csv(state, sep='\t', comment='#')
groups = mod.load_iqtree_state(state)
cols = [c for c in df if c.startswith('p_')]
sums = df[cols].sum(axis=1)
argmax = df[cols].idxmax(axis=1).str.removeprefix('p_')
assert len(df) == 660 and df.Node.nunique() == 6 and df.Site.nunique() == 110
assert len(cols) == 20 and (abs(sums-1) < 2e-4).all()
assert (df.State == argmax).all() and sum(len(frame) for _, frame in groups) == 660
valid = {'status':'PASS', 'rows':len(df), 'nodes':int(df.Node.nunique()), 'sites':int(df.Site.nunique()),
         'posterior_columns':len(cols), 'max_sum_error':float(abs(sums-1).max()), 'all_argmax_match':bool((df.State==argmax).all())}

result={'real_iqtree':valid,
        'invalid_state_rows':{'missing_columns':'PASS','empty':'PASS','bad_sum':'PASS','bad_argmax':'PASS','nonfinite':'PASS'}}
(out/'iqtree-results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
