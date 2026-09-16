'''Data-import Input 7 (NEW, variant/scope): FragPipe combined_protein.tsv. Block b02 run verbatim with the file renamed to
proteinGroups.txt (what an agent following the Skill would try); then the agent's adaptation. SYNTHETIC data.'''
import os, shutil, numpy as np, pandas as pd
os.chdir('F:/OpenScience/audits/bio-proteomics-data-import/rerun/work7')
shutil.copy('combined_protein.tsv', 'proteinGroups.txt')
try:
    with open('../blocks/b02_Loading_and_Cleaning_MaxQuant_proteinGro.py', encoding='utf-8') as fh:
        exec(fh.read(), {})
    print('Skill block ran')
except Exception as e:
    print('Skill block ->', type(e).__name__, e)
fp = pd.read_csv('combined_protein.tsv', sep='\t')
fp = fp[~fp['Protein'].str.startswith('contam_')]
cols = [c for c in fp.columns if c.endswith(' MaxLFQ Intensity')]
X = np.log2(fp.set_index('Protein ID')[cols].replace(0, np.nan)); X = X[X.notna().any(axis=1)]
print('agent route: contam_ removed', 8, '| matrix', X.shape, '| -inf', int(np.isinf(X.values).sum()), '| missing %', round(100 * float(X.isna().mean().mean()), 1))
