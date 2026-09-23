"""Input 3 (Variant B) - bio-single-cell-differential-abundance
scCODA exactly as SKILL.md:106-121, plus the reference-cell-type question the Skill devotes a
whole section to (SKILL.md:43-45): does the verdict flip with a different reference?
SYNTHETIC 8-sample PBMC set; ground truth is an NK expansion and nothing else.
Run with tools/sccoda-venv/Scripts/python.exe (the shared venv's arviz is too new for scCODA).
"""
import pandas as pd
import numpy as np
from sccoda.util import cell_composition_data as dat
from sccoda.util import comp_ana as mod

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
tc = pd.read_csv(D + '/truth_cells.csv')
tc = tc[~tc.true_doublet.astype(bool) & ~tc.true_low_quality.astype(bool)]
ss = pd.read_csv(D + '/sample_sheet.csv').set_index('sample')
tc['condition'] = tc['sample'].map(ss['condition'])
tc['batch'] = tc['sample'].map(ss['batch'])

# --- SKILL.md:111-113, verbatim shape ---
counts = pd.crosstab(tc['sample'], tc['true_cell_type']).reset_index()
meta = tc[['sample', 'condition', 'batch']].drop_duplicates()
counts = counts.merge(meta, on='sample')
print('per-sample count table (the input scCODA wants):')
print(counts.to_string(index=False))
cell_types = [c for c in counts.columns if c not in ('sample', 'condition', 'batch')]

data = dat.from_pandas(counts, covariate_columns=['sample', 'condition', 'batch'])
print('\nscCODA data object:', data)


def run(formula, reference, tag):
    m = mod.CompositionalAnalysis(data, formula=formula, reference_cell_type=reference)
    # TOOLS.md note 2: the real signature is sample_hmc(num_results=..., num_burnin=...)
    r = m.sample_hmc(num_results=20000, num_burnin=5000)
    r.set_fdr(est_fdr=0.1)
    ce = r.credible_effects()
    hits = [str(i) for i, v in ce.items() if bool(v)]
    eff = r.effect_df
    print(f'\n[{tag}] formula="{formula}" reference="{reference}"')
    print(f'  reference actually used: {m.reference_cell_type} '
          f'({cell_types[m.reference_cell_type] if isinstance(m.reference_cell_type, (int, np.integer)) else m.reference_cell_type})')
    print(f'  credible effects at est_fdr=0.1: {hits if hits else "NONE"}')
    cols = [c for c in ['Final Parameter', 'log2-fold change', 'Inclusion probability']
            if c in eff.columns]
    print(eff[cols].round(3).to_string())
    return set(hits)


base = run('condition', 'automatic', 'automatic reference')

print('\n--- SKILL.md:43-45: does the verdict flip with a different reference? ---')
flips = {}
for ct in cell_types:
    h = run('condition', ct, f'reference={ct}')
    flips[ct] = h
print('\nSUMMARY of credible effects by reference choice:')
for ct, h in flips.items():
    print(f'  reference {ct:20s} -> {sorted(x.split("[")[-1].rstrip("]").strip("'") for x in h) if h else "NONE"}')
print('\nGROUND TRUTH: NK cells 6% -> ~13%; nothing else changed.')

print('\n--- batch-adjusted formula (SKILL.md:63) ---')
run('batch + condition', 'automatic', 'batch + condition')
print('DONE')
