'''PUBLIC DATA check (PXD070049, CC0; Van Puyvelde et al. 2026): DIA-NN 2.6.1 output from the Skill's predicted-library command
on three Orbitrap Astral 5-min 250 pg DIA runs (Conditions A, B, C; one replicate each). Runs the dia-analysis filter block (b03)
and the data-import DIA block (b03) VERBATIM on the real report.parquet, maps protein groups to species from the shipped FASTA,
and checks log2 ratios against the known HYE mixing design (A/B: human 0, yeast +1, E. coli -2; C/A: human 0, yeast -3.32,
E. coli +2.68). Usage: python public_hye_check.py <diann_out_dir>'''
import os, sys, re, time, collections
import numpy as np, pandas as pd

OUT = sys.argv[1] if len(sys.argv) > 1 else 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/public-work/diann_libfree/diann_out'
FASTA = 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/public-data/PXD070049/fasta/uniprotkb_proteome_HYE_UniversalContaminants.fasta'
DIA_BLK = 'F:/OpenScience/audits/bio-proteomics-dia-analysis/rerun/blocks/b03_DIA_NN_Output_and_Correct_Filtering.py'
IMP_BLK = 'F:/OpenScience/audits/bio-proteomics-data-import/rerun/blocks/b03_Loading_DIA_NN_report_parquet.py'
EXPECT = {'A/B': {'HUMAN': 0.0, 'YEAST': 1.0, 'ECOLI': -2.0}, 'C/A': {'HUMAN': 0.0, 'YEAST': -3.32, 'ECOLI': 2.68}}

species = {}
for line in open(FASTA, encoding='utf-8'):
    if line.startswith('>'):
        acc = line[1:].split()[0].split('|')
        acc = acc[1] if len(acc) > 1 else acc[0]
        os_ = re.search(r'OS=([^=]+?) OX=', line)
        s = os_.group(1) if os_ else ''
        species[acc] = 'HUMAN' if s.startswith('Homo sapiens') else 'YEAST' if 'cerevisiae' in s else 'ECOLI' if s.startswith('Escherichia coli') else 'OTHER'

def group_species(pg):
    sp = {species.get(a.strip(), 'OTHER') for a in pg.split(';')}
    return sp.pop() if len(sp) == 1 else 'MIXED'

rep_path = os.path.join(OUT, 'report.parquet')
raw = pd.read_parquet(rep_path)
print('DIA-NN report:', rep_path, '| rows', len(raw), '| runs', raw['Run'].nunique(), '| columns include:',
      [c for c in ['Q.Value', 'PG.Q.Value', 'Global.Q.Value', 'Global.PG.Q.Value', 'Lib.Q.Value', 'Lib.PG.Q.Value', 'PG.MaxLFQ'] if c in raw.columns])

def run_block(path, label, prefix):
    src = open(path, encoding='utf-8').read()
    src = src.replace(f"'{prefix}'", repr(rep_path))
    ns = {}
    t0 = time.time()
    try:
        exec(src, ns)
        m = ns.get('pg', ns.get('matrix'))
        print(f'[{label}] verbatim block OK in {time.time() - t0:.1f} s | matrix {m.shape} | -inf {int(np.isinf(m.values).sum())} | NaN {int(m.isna().sum().sum())}')
        return m
    except Exception as e:
        print(f'[{label}] verbatim block ERROR: {type(e).__name__}: {e}')
        return None

m_dia = run_block(DIA_BLK, 'dia-analysis b03', 'diann_out/report.parquet')
m_imp = run_block(IMP_BLK, 'data-import b03', 'report.parquet')
lvl = raw[(raw['Q.Value'] <= 0.01) & (raw['PG.Q.Value'] <= 0.01)]
print('protein groups: run-level filters only', lvl['Protein.Group'].nunique(), '| + global filters (dia-analysis block)',
      None if m_dia is None else len(m_dia), '| data-import block', None if m_imp is None else len(m_imp))
per_run = raw[(raw['Q.Value'] <= 0.01)].groupby('Run')['Precursor.Id'].nunique()
print('precursors at Q.Value<=0.01 per run:', per_run.to_dict())

m = m_dia if m_dia is not None else m_imp
if m is not None:
    runs = {c: next((r for r in m.columns if f'Condition_{c}_' in r), None) for c in 'ABC'}
    sp = pd.Series({pg: group_species(pg) for pg in m.index})
    print('species of protein groups in matrix:', sp.value_counts().to_dict())
    for pair, (num, den) in {'A/B': ('A', 'B'), 'C/A': ('C', 'A')}.items():
        r = (m[runs[num]] - m[runs[den]]).dropna()
        s = sp.loc[r.index]
        rows = []
        for k, exp in EXPECT[pair].items():
            v = r[s == k]
            if len(v):
                rows.append(f'{k}: n={len(v)} median {v.median():+.2f} (expected {exp:+.2f}) IQR {v.quantile(.25):+.2f}..{v.quantile(.75):+.2f}')
        print(f'{pair} log2 ratio |', ' | '.join(rows))
