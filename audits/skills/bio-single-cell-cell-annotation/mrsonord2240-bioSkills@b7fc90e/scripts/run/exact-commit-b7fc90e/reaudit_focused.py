"""Focused re-audit for bio-single-cell-cell-annotation at b7fc90e.

Uses the existing CellTypist fixture to exercise the corrected input contract
and the current SKILL.md code fence, then executes the QC-first triage fence
against a small labelled in-memory fixture.
"""
from __future__ import annotations

import ast
import os
import re
import subprocess
from pathlib import Path

import anndata as ad
import celltypist
import numpy as np
import pandas as pd
import scanpy as sc

COMMIT = 'b7fc90e69bdf4839b958a13b37581945ba694413'
ROOT = Path(r'F:/OpenScience/worktrees/bio-single-cell-cell-annotation-fixpass')
SKILL = ROOT / 'single-cell/cell-annotation/SKILL.md'
DATA = Path(r'F:/OpenScience/audits/bio-single-cell-cell-annotation/run/input1_celltypist.h5ad')

os.environ.setdefault(
    'CELLTYPIST_FOLDER',
    r'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/cache/celltypist',
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f'PASS: {message}')


head = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
require(head == COMMIT, f'exact source commit is {COMMIT}')
text = SKILL.read_text(encoding='utf-8')
fences = re.findall(r'```(?:python|r)\n(.*?)```', text, flags=re.S)
require(len(fences) == 5, 'all five executable code fences are present')
py_fences = [f for f in fences if 'celltypist.annotate' in f or "required = {'leiden'" in f]
for fence in py_fences:
    ast.parse(fence)
require("over_clustering='leiden'" in text, 'CellTypist majority voting receives explicit clustering')
require('seeded upstream result' in text, 'CellTypist clustering reproducibility precondition is documented')
require('Raw counts raise `ValueError`' in text, 'raw-count failure mode is current')
require('No features overlap with the model' in text, 'gene-ID failure mode is current')
require('Pruning does **not** detect confidently wrong nearest-label calls' in text,
        'SingleR pruning limitation is explicit')
require('Screen **every** cluster first' in text and 'not an artifact screen' in text,
        'triage is QC-first rather than confidence-first')
require('NormalizeData(seurat_obj)' in text, 'marker validation initializes a normalized data layer')

# Exercise the current CellTypist call shape and both documented hard failures.
a = sc.read_h5ad(DATA)
probe = a[:128].copy()
probe.X = probe.layers['counts'].copy()
sc.pp.normalize_total(probe, target_sum=1e4)
sc.pp.log1p(probe)
require('leiden' in probe.obs, 'fixture supplies seeded over-clustering')
first = celltypist.annotate(probe, model='Immune_All_Low.pkl', majority_voting=True,
                             over_clustering='leiden').predicted_labels['majority_voting']
second = celltypist.annotate(probe, model='Immune_All_Low.pkl', majority_voting=True,
                              over_clustering='leiden').predicted_labels['majority_voting']
require(first.equals(second), 'explicit over-clustering gives repeatable majority labels')

raw = a[:32].copy()
raw.X = raw.layers['counts'].copy()
try:
    celltypist.annotate(raw, model='Immune_All_Low.pkl', majority_voting=False)
except ValueError as exc:
    require('Invalid expression matrix' in str(exc), 'raw counts raise documented invalid-matrix error')
else:
    raise AssertionError('raw counts must not annotate silently')

ensembl = probe[:32].copy()
ensembl.var_names = ensembl.var['gene_ids'].astype(str).values
ensembl.var_names_make_unique()
try:
    celltypist.annotate(ensembl, model='Immune_All_Low.pkl', majority_voting=False)
except ValueError as exc:
    require('No features overlap with the model' in str(exc), 'Ensembl IDs raise documented no-overlap error')
else:
    raise AssertionError('Ensembl IDs must not return labels')

# Execute the current QC-first fence against a fixture where a high-confidence
# cluster is an obvious QC artifact and a low-confidence cluster is clean.
obs = pd.DataFrame({
    'leiden': ['clean'] * 3 + ['artifact'] * 3,
    'pct_counts_mt': [2.0, 2.1, 1.9, 24.0, 23.0, 25.0],
    'n_genes_by_counts': [1500, 1450, 1550, 120, 110, 130],
    'predicted_doublet': [False, False, False, True, True, True],
    'sample': ['s1', 's2', 's1', 's1', 's1', 's1'],
    'conf_score': [0.20, 0.22, 0.18, 0.96, 0.95, 0.97],
})
adata = ad.AnnData(X=np.zeros((len(obs), 1)), obs=obs)
triage = next(f for f in fences if "required = {'leiden'" in f)
scope = {'adata': adata}
exec(triage, scope)
qc = scope['qc']
require(set(qc.index) == {'clean', 'artifact'}, 'QC table retains every cluster')
require(qc.loc['artifact', 'doublet_rate'] > qc.loc['clean', 'doublet_rate'],
        'high-confidence artifact is surfaced by QC evidence')
require(qc.loc['artifact', 'median_conf_score'] > qc.loc['clean', 'median_conf_score'],
        'confidence is retained as secondary evidence, not a prefilter')
print('ALL FOCUSED RE-AUDIT ASSERTIONS PASSED: 15/15')
