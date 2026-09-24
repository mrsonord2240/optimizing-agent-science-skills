'''Data-import Input 5 (regression, stress): same 8 samples by DDA (MaxQuant) and DIA (DIA-NN). Load both, quantify missingness,
MNAR vs MCAR, imputation advice, overlap. Blocks b02, b03, b04 executed verbatim. SYNTHETIC data with truth.'''
import os, numpy as np, pandas as pd
os.chdir('F:/OpenScience/audits/bio-proteomics-data-import/rerun/work')
B = '../blocks/'
def run(f, ns):
    with open(B + f, encoding='utf-8') as fh:
        exec(fh.read(), ns)
    return ns
dda = run('b02_Loading_and_Cleaning_MaxQuant_proteinGro.py', {})
dia = run('b03_Loading_DIA_NN_report_parquet.py', {})
diag = run('b04_Diagnosing_the_Missingness_Contract.py', {})['assess_missingness']
M1 = dda['matrix'].set_index('leading_protein'); c1 = dda['lfq_cols']
M2 = dia['matrix']; c2 = list(M2.columns)
r1, r2 = diag(M1, c1), diag(M2, c2)
print(f"DDA MaxQuant LFQ : missing {r1['total_pct']:.1f}% | corr(abundance, #missing) {r1['abundance_missing_corr']:.3f}")
print(f"DIA DIA-NN      : missing {r2['total_pct']:.1f}% | corr(abundance, #missing) {r2['abundance_missing_corr']:.3f}")
print('overlap: DDA', len(M1), '| DIA', len(M2), '| both', len(set(M1.index) & set(M2.index)))
truth = pd.read_csv('../../data/truth_proteins.csv').set_index('protein')
t2 = truth.reindex(M2.index)
q = pd.qcut(t2['base_log2'], 4, labels=['Q1 low', 'Q2', 'Q3', 'Q4 high'])
print('DIA missing % by TRUE abundance quartile:', (100 * M2.isna().mean(axis=1).groupby(q, observed=True).mean()).round(1).to_dict())
skill = open('F:/OpenScience/external/mrsonord2240__bioSkills/proteomics/data-import/SKILL.md', encoding='utf-8').read()
print('Skill still says DIA is MCAR / tolerates standard imputers:', ('closer to MCAR' in skill) or ('tolerates standard imputers' in skill))
print('Skill DIA decision-tree row routes by diagnostic:', 'Run the same diagnostic' in skill)
