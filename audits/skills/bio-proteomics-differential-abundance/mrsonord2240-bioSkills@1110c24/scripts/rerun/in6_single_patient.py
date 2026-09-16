'''Input 6 (regression, scope boundary): one patient vs 12 controls. SYNTHETIC data. Skill Python block executed verbatim.'''
import pandas as pd
RR = 'F:/OpenScience/audits/bio-proteomics-differential-abundance'
ns = {}
exec(open(f'{RR}/rerun/blocks/b05_Python_Workflow.py', encoding='utf-8').read(), ns)
raw = pd.read_csv(f'{RR}/data/plasma_12v12.csv', index_col=0)
ctrl_cols = [c for c in raw.columns if c.startswith('ctrl')]
patient = ['case_01']
norm = ns['preprocess'](raw[ctrl_cols + patient])
try:
    ns['differential_abundance'](norm, patient, ctrl_cols)
except Exception as e:
    print(f'{type(e).__name__}: {e}')
skill = open('F:/OpenScience/external/mrsonord2240__bioSkills/proteomics/differential-abundance/SKILL.md', encoding='utf-8').read()
print('Scope sentence present:', 'diagnosis or treatment decisions for an individual patient' in skill)
