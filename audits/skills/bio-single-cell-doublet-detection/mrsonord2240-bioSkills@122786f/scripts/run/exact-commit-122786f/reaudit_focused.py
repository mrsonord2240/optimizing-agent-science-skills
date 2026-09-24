"""Focused exact-commit re-audit for bio-single-cell-doublet-detection."""
from __future__ import annotations

import ast
import re
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc

COMMIT = '122786f78fef5de2a71fb2e8ec10388ad0f66d7c'
ROOT = Path(r'F:/OpenScience/worktrees/bio-single-cell-doublet-detection-fixpass')
SKILL = ROOT / 'single-cell/doublet-detection/SKILL.md'
EXAMPLE = ROOT / 'single-cell/doublet-detection/examples/doubletfinder.R'
DATA = Path(r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples/all_samples_filtered.h5ad')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f'PASS: {message}')


head = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
require(head == COMMIT, f'exact source commit is {COMMIT}')
text = SKILL.read_text(encoding='utf-8')
fences = re.findall(r'```(?:python|r)\n(.*?)```', text, flags=re.S)
require(len(fences) == 4, 'all four executable code fences are present')
py_fences = [f for f in fences if 'sc.pp.scrublet' in f]
require(len(py_fences) == 2, 'both Scrublet code fences are present')
for fence in py_fences:
    ast.parse(fence)
require('SerialParam(RNGseed = 20260924)' in text, 'scDblFinder uses an explicit worker RNG seed')
require('does not control BiocParallel workers' in text,
        'scDblFinder base-seed limitation is documented')
require('sub = adata[mask].copy()' in text and "adata.obs.loc[mask, 'doublet_score']" in text,
        'per-sample Scrublet writes copied-subset results back to the parent')
require("raise RuntimeError('Scrublet did not return scores for every sample" in text,
        'unscored cells stop the workflow')
require('compare co-expression with the dataset-wide rate' in text,
        'ambient-aware co-expression limitation is adjacent to the heuristic')
require('## What to report' in text and 'homotypic limitation' in text,
        'required doublet-detection report fields are present')
example = EXAMPLE.read_text(encoding='utf-8')
require('reuse.pANN = FALSE' not in example, 'DoubletFinder example omits invalid logical reuse.pANN')
require('cannot xtfrm data frames' in text, 'DoubletFinder failure mode has an actionable Common Errors entry')

# Execute the exact pooled-sample fence with two capture lanes.  The audit
# fixture has raw counts and a sample column; map it to the code-fence keys.
adata = sc.read_h5ad(DATA)
adata = adata[adata.obs['sample'].isin(['S1', 'S2'])].copy()
adata = adata[adata.obs.groupby('sample', observed=True).head(256).index].copy()
adata.obs['sample_id'] = adata.obs['sample'].astype(str).values
adata.obs['lane_id'] = adata.obs['sample'].astype(str).values
expected_groups = adata.obs.groupby('sample_id', observed=True).size()
pooled_fence = next(f for f in py_fences if "sample_key = 'sample_id'" in f)
scope = {'adata': adata, 'sc': sc, 'pd': pd, 'np': np}
exec(pooled_fence, scope)
out = scope['adata']
require({'doublet_score', 'predicted_doublet'} <= set(out.obs.columns),
        'parent AnnData receives both Scrublet columns')
require(not out.obs['doublet_score'].isna().any(), 'every parent cell has a doublet score')
require(out.obs.groupby('sample_id', observed=True)['doublet_score'].size().equals(expected_groups)
        and len(expected_groups) == 2,
        'both capture lanes were scored independently')

# The source fence should also fail closed if capture metadata are absent.
missing_meta = adata[:10].copy()
missing_meta.obs.drop(columns=['lane_id'], inplace=True)
try:
    exec(pooled_fence, {'adata': missing_meta, 'sc': sc, 'pd': pd, 'np': np})
except ValueError as exc:
    require('Add capture metadata' in str(exc), 'missing capture metadata produces a useful failure')
else:
    raise AssertionError('missing capture metadata must not be silently accepted')

print('ALL FOCUSED RE-AUDIT ASSERTIONS PASSED: 15/15')
