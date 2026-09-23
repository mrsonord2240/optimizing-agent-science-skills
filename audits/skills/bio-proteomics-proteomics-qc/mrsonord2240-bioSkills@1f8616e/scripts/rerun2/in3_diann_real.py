# Re-audit batch C, Input 3 (NEW). REAL data: PXD070049 DIA (CC0), 3 Astral 5-min 250 pg runs,
# one per HYE condition, searched with DIA-NN 2.6.1 (public-work/diann_libbased_mzml/diann_out/report.parquet).
# Prompt: "Three DIA runs, one per condition, no replicates. QC them before I look at fold changes."
# Everything is the SKILL.md code, exec'd verbatim from the fork via skill.py.
import numpy as np, pandas as pd
from skill import S

P = 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/public-work/diann_libbased_mzml/diann_out/report.parquet'
d = pd.read_parquet(P)
d['run'] = d['Run'].str.extract(r'Condition_([ABC])_REP1')[0]
print('REAL DIA-NN report:', d.shape, '| runs:', sorted(d.run.unique()))

# --- Skill decision-tree row: "DIA matrix, how many proteins are real -> filter Global.Q.Value and Global.PG.Q.Value" ---
print('\n[Skill row] Precursor q != protein q; both needed')
for col in ('Q.Value', 'Global.Q.Value', 'PG.Q.Value', 'Global.PG.Q.Value'):
    print(f'  {col:20s} <=0.01: {(d[col] <= 0.01).mean():.4f} of {len(d)} precursor rows')
run_only = d[(d['Q.Value'] <= 0.01) & (d['PG.Q.Value'] <= 0.01)]
both = run_only[(run_only['Global.Q.Value'] <= 0.01) & (run_only['Global.PG.Q.Value'] <= 0.01)]
print(f'  protein groups passing run-level q only : {run_only["Protein.Group"].nunique()}')
print(f'  protein groups also passing GLOBAL q    : {both["Protein.Group"].nunique()}'
      f'  (global filter removes {run_only["Protein.Group"].nunique() - both["Protein.Group"].nunique()})')

# --- Skill line 81: the un-normalised DIA-NN column is Precursor.Quantity, NOT Precursor.Normalised / PG.MaxLFQ ---
q = both.pivot_table(index='Precursor.Id', columns='run', values='Precursor.Quantity', aggfunc='sum')
grp = pd.Series({r: r for r in q.columns})          # one run per condition -> each is its own group
print('\n[Skill raw_sample_qc] on Precursor.Quantity (the un-normalised column the Skill names):')
print(S['raw_sample_qc'](q, grp).round(3).to_string())
print('NOTE: with n=1 per condition, fold_total_vs_group and ids_vs_group are each a sample against itself.')
grp_all = pd.Series({r: 'all' for r in q.columns})  # the only usable baseline here: the run set itself
print('\nsame, with all three runs treated as one baseline group:')
qc = S['raw_sample_qc'](q, grp_all)
print(qc.round(3).to_string())
print('Skill loading rule: exclude if total signal >=2x below group median, or ID count >15-20% below.')

# --- normalised columns hide/alter this, per the Skill's failure mode ---
for col in ('Precursor.Normalised', 'PG.MaxLFQ'):
    m = both.pivot_table(index='Precursor.Id', columns='run', values=col, aggfunc='sum')
    tot = m.sum(); print(f'  {col:22s} total per run, rel to median: {(tot/tot.median()).round(3).to_dict()}')
tot = q.sum(); print(f'  {"Precursor.Quantity":22s} total per run, rel to median: {(tot/tot.median()).round(3).to_dict()}')

# --- zeros as missing (Skill line 81) ---
pg = both.pivot_table(index='Protein.Group', columns='run', values='PG.MaxLFQ', aggfunc='max')
print(f'\nPG.MaxLFQ zeros present: {(pg == 0).sum().sum()}; after replace(0, nan) the Skill counts them as missing.')
pg = pg.replace(0, np.nan)
log2 = np.log2(pg)
print('protein groups x runs:', log2.shape, '| complete in all 3:', int(log2.notna().all(axis=1).sum()))
print('missingness_profile (present fraction by abundance decile):', S['missingness_profile'](log2).round(2).tolist())

# --- what the Skill REFUSES to compute here ---
print('\n[Skill stop conditions with one replicate per condition]')
try:
    rc = S['replicate_correlation'](log2, grp)
    print('  replicate_correlation returned', len(rc), 'pairs')
except Exception as e:
    print('  replicate_correlation ->', type(e).__name__, e)
try:
    cv = S['median_cv_linear'](pg, grp)
    print('  median_cv_linear ->', cv.round(3).to_dict('records'))
except Exception as e:
    print('  median_cv_linear ->', type(e).__name__, e)
info = pd.DataFrame({'batch': ['b1', 'b1', 'b1'], 'condition': list(q.columns)}, index=q.columns)
try:
    S['pca_batch_check'](log2, info)
except Exception as e:
    print('  pca_batch_check ->', type(e).__name__, e)

# --- Level-1 metrics the Skill names in its description, computed from what DIA-NN reports ---
print('\n[Level-1 metrics the Skill names: RT/iRT fit, FWHM] -- available in the DIA-NN report:')
for r, sub in d[d['Q.Value'] <= 0.01].groupby('run'):
    rt_r = np.corrcoef(sub['RT'], sub['Predicted.RT'])[0, 1]
    print(f'  {r}: precursors {len(sub):5d} | RT vs Predicted.RT r={rt_r:.4f} | '
          f'median FWHM {sub["FWHM"].median():.4f} min | median Quantity.Quality {sub["Quantity.Quality"].median():.3f}')
print('The Skill lists RT/iRT fit and FWHM as Level-1 metrics but gives NO code or threshold for either;')
print('the numbers above were computed by the auditor, not by anything the Skill provides.')
