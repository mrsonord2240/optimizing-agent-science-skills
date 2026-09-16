# Re-audit 2026-09-15, PTM Inputs 2 and 6 (and the motif part of 4): the fork's SKILL.md "Expand the MaxQuant Site
# Table" block and motif block, extracted programmatically and exec'd VERBATIM with cwd set to the data folder.
import os, re, sys
import numpy as np, pandas as pd
SKILL = r'F:/OpenScience/external/mrsonord2240__bioSkills/proteomics/ptm-analysis/SKILL.md'
blocks = re.findall(r'```python\n(.*?)```', open(SKILL, encoding='utf-8').read(), flags=re.S)
EXPAND = next(b for b in blocks if 'mult_cols' in b)
MOTIF = next(b for b in blocks if 'matched_background' in b)
HERE = os.path.dirname(os.path.abspath(__file__))

def run_expand(folder):
    cwd = os.getcwd(); os.chdir(folder)
    try:
        ns = {}
        exec(compile(EXPAND, 'SKILL.md expand block', 'exec'), ns)
        return ns
    finally:
        os.chdir(cwd)

which = sys.argv[1]
if which == 'in2':
    ns = run_expand(os.path.join(HERE, '..', 'data', 'phospho'))
    ph, long = ns['phospho'], ns['long']
    print('sites after REV/CON + class I:', len(ph), '| per-run multiplicity columns:', len(ns['mult_cols']))
    print('run labels:', sorted(long.run.unique()))
    m = long.pivot_table(index=['site_id', 'multiplicity'], columns='run', values='log2_intensity')
    print('site x multiplicity x run matrix:', m.shape, '| column medians:', m.median().round(2).to_dict())
    print('residues (class I):', ph['Amino acid'].value_counts().to_dict())
    print('blank Gene names ->', ph.loc[ph['Gene names'].isna(), 'site_id'].tolist())
    truth = pd.read_csv(os.path.join(HERE, '..', 'data', 'phospho', 'truth_sites.csv'))
    sw = truth.loc[truth.multiplicity_switch, 'site'].tolist()
    C = ['C1', 'C2', 'C3', 'C4']; T = ['T1', 'T2', 'T3', 'T4']
    for s in sw:
        acc = s.split('_')[0]; row = ph[ph['Protein'] == acc]
        if row.empty:
            print('switch site', s, 'not class I'); continue
        r = row.iloc[0]
        coll = np.log2(r[[f'Intensity {x}' for x in T]].astype(float).replace(0, np.nan).mean() / r[[f'Intensity {x}' for x in C]].astype(float).replace(0, np.nan).mean())
        g = lambda n: np.log2(r[[f'Intensity {x}___{n}' for x in T]].astype(float).replace(0, np.nan).mean() / r[[f'Intensity {x}___{n}' for x in C]].astype(float).replace(0, np.nan).mean())
        print(f'switch {s}: collapsed {coll:+.2f} | ___1 {g(1):+.2f} | ___2 {g(2):+.2f}')
    # motif block verbatim right after, as SKILL.md orders them; then the Skill's own functions with a matched background
    mns = {'phospho': ph}
    exec(compile(MOTIF, 'SKILL.md motif block', 'exec'), mns)
    fasta = {}
    for rec in open(os.path.join(HERE, '..', 'data', 'phospho', 'synthetic.fasta'), encoding='utf-8').read().split('>')[1:]:
        head, *seq = rec.split('\n'); fasta[head.split('|')[1]] = ''.join(seq)
    fg = mns['foreground']
    bg = mns['matched_background'](fasta, ph['Protein'].unique(), residues='STY')
    tab = mns['motif_enrichment'](fg, bg)
    print('motif block ran: foreground', len(fg), '| matched background', len(bg))
    print(tab.head(4).to_string(index=False))
    ph.to_csv(os.path.join(HERE, 'in2_classI_sites.csv'), index=False)

elif which == 'in6':
    # NEW: older MaxQuant export: no-space filename, 'Contaminant' column, a site at exactly 0.75, a blank gene
    import shutil, tempfile
    src = pd.read_csv(os.path.join(HERE, '..', 'data', 'phospho', 'Phospho (STY)Sites.txt'), sep='\t', low_memory=False)
    old = src.rename(columns={'Potential contaminant': 'Contaminant'})
    i075 = old.index[old['Localization prob'] < 0.75][0]
    old.loc[i075, 'Localization prob'] = 0.75
    old.loc[old.index[0], 'Gene names'] = np.nan
    tmp = os.path.join(HERE, 'in6_oldmq'); os.makedirs(tmp, exist_ok=True)
    old.to_csv(os.path.join(tmp, 'Phospho(STY)Sites.txt'), sep='\t', index=False)
    print('REV rows:', int((old.Reverse == '+').sum()), '| Contaminant rows:', int((old.Contaminant == '+').sum()))
    ns = run_expand(tmp)
    ph = ns['phospho']
    print('file used:', ns['sites_file'], '| contaminant column:', ns['contaminant_col'])
    print('sites kept:', len(ph), '| 0.75 site kept:', bool((ph['Localization prob'] == 0.75).any()),
          '| REV/CON left:', int(((ph.Reverse == '+') | (ph.Contaminant == '+')).sum()))
    print('site_id for blank gene row:', ph.loc[ph['Gene names'].isna(), 'site_id'].tolist())
    print('run labels:', sorted(ns['long'].run.unique()))
    # example's class bins on the 0.75 boundary
    cls = pd.cut(pd.Series([0.2499, 0.25, 0.5, 0.7499, 0.75, 1.0]), bins=[0, 0.25, 0.5, 0.75, 1.0 + 1e-9], labels=['IV', 'III', 'II', 'I'], right=False)
    print('example binning [0.2499,0.25,0.5,0.7499,0.75,1.0] ->', list(cls))
