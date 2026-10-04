"""Inspect output of SKILL.md Boruta block (3) on Golub 1000 probes: real vs permuted labels. Usage: python -W error::FutureWarning boruta_inspect.py <SKILL.md> <golub_top1000.csv>"""
import sys, re
sys.dont_write_bytecode = True
import pandas as pd, numpy as np
df = pd.read_csv(sys.argv[2]); y = (df.pop('label') == 'AML').astype(int); X = df.astype(float)
blk = re.findall(r"```python\n(.*?)```", open(sys.argv[1], encoding='utf-8').read(), re.S)[3]
for nm, yy in (('real', y), ('permuted', pd.Series(np.random.default_rng(1).permutation(y.values)))):
    ns = {'X': X, 'y': yy}; exec(compile(blk, 'SKILL.md#block3', 'exec'), ns)
    print(f'BORUTA {nm}: confirmed={len(ns["confirmed"])} tentative={len(ns["tentative"])}', flush=True)
