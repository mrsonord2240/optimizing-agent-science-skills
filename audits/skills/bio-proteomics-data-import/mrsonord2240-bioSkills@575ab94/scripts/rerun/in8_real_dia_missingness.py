'''Data-import Input 8 (NEW, public data): does the Skill's missingness contract hold on REAL DIA data?
The pass-1 fix rewrote the DIA missingness claim to "fewer missing values but still mostly intensity-dependent, choose the
imputer from the diagnostic". That was verified on synthetic tables only. Here the Skill's DIA import block (b03) and its
assess_missingness function (b04) are executed VERBATIM on a real DIA-NN 2.6.1 report from PXD070049 (CC0, Orbitrap Astral
5-min 250 pg, 3 runs). Also reproduces the degenerate-mask defect in the MaxQuant block when no flag column is present.
Run as a file: python in8_real_dia_missingness.py'''
import numpy as np, pandas as pd

REP = 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/public-work/diann_predlib_mzml/diann_out/report.parquet'
B03 = 'F:/OpenScience/audits/bio-proteomics-data-import/rerun/blocks/b03_Loading_DIA_NN_report_parquet.py'
B02 = 'F:/OpenScience/audits/bio-proteomics-data-import/rerun/blocks/b02_Loading_and_Cleaning_MaxQuant_proteinGro.py'
B04 = 'F:/OpenScience/audits/bio-proteomics-data-import/rerun/blocks/b04_Diagnosing_the_Missingness_Contract.py'

# --- the Skill's DIA import block, verbatim (only the parquet path substituted) -------------------
src = open(B03, encoding='utf-8').read()
assert src.count("'report.parquet'") == 1
ns = {}
exec(src.replace("'report.parquet'", repr(REP)), ns)
m = ns['matrix']
print(f'[b03 verbatim on REAL DIA-NN 2.6.1 output] matrix {m.shape} | -inf {int(np.isinf(m.values).sum())} | '
      f'NaN {int(m.isna().sum().sum())} ({100 * m.isna().mean().mean():.1f}%)')

# --- the Skill's assess_missingness, verbatim ----------------------------------------------------
ns4 = {}
exec(open(B04, encoding='utf-8').read(), ns4)
cols = list(m.columns)
d = ns4['assess_missingness'](m, cols)
print(f'[b04 verbatim] total missing {d["total_pct"]:.1f}% | abundance-missingness corr {d["abundance_missing_corr"]:.3f} '
      f'(negative => MNAR / left-censored) | missing per run {dict(zip([c.split("Condition_")[-1][:1] for c in cols], d["per_sample"].tolist()))}')

# independent check of the same claim: is missingness concentrated in low-abundance proteins?
ab = m.mean(axis=1)
q = pd.qcut(ab.rank(method='first'), 4, labels=['Q1 low', 'Q2', 'Q3', 'Q4 high'])
print('missing % by mean-abundance quartile:', {str(k): round(float(100 * m[q == k].isna().mean().mean()), 1) for k in q.cat.categories})

# --- degenerate mask in the MaxQuant block when NO flag column is present -------------------------
# The Skill's Common Errors table promises pg.get('Only identified by site', '') guards a missing column.
# With ALL THREE absent, each .get() returns the scalar '' and the mask collapses to the Python bool True.
tiny = pd.DataFrame({'Protein IDs': ['P1;P2', 'P3'], 'Gene names': ['A;B', 'C'],
                     'LFQ intensity S1': [10.0, 0.0], 'LFQ intensity S2': [20.0, 30.0]})
mask = (tiny.get('Reverse', '') != '+') & (tiny.get('Potential contaminant', '') != '+') & (tiny.get('Only identified by site', '') != '+')
print('mask when all three flag columns are absent ->', repr(mask), type(mask).__name__)
tiny.to_csv('proteinGroups.txt', sep='\t', index=False)
try:
    exec(open(B02, encoding='utf-8').read(), {})
    print('b02 on a flagless table: ran')
except Exception as e:
    print('b02 on a flagless table ->', type(e).__name__ + ':', e)
