'''DIA Input 6 (NEW, public data, canonical route): the Skill's PREDICTED-LIBRARY route run with the real DIA-NN 2.6.1 Academia
binary on three Orbitrap Astral 5-min 250 pg DIA runs from PXD070049 (CC0, Van Puyvelde 2026). The two-step run is in
public-work/diann_libfree (library prediction from the Skill's b01 command) + public-work/diann_predlib_mzml (search).
This script: (a) runs the Skill's b03 filter block VERBATIM on the real report.parquet; (b) tests the Skill's claim that the
*_matrix.tsv files apply an EXTRA 5% run-specific protein FDR so the matrix count is LOWER than the report count; (c) checks the
Skill's documented output-file listing against what DIA-NN 2.6.1 actually wrote; (d) checks quantitative accuracy against the
known HYE mixing design. Run as a file: python in6_public_predlib.py'''
import os, re, time
import numpy as np, pandas as pd

OUT = 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/public-work/diann_predlib_mzml/diann_out'
FASTA = 'F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/public-data/PXD070049/fasta/uniprotkb_proteome_HYE_UniversalContaminants.fasta'
BLK = 'F:/OpenScience/audits/bio-proteomics-dia-analysis/rerun/blocks/b03_DIA_NN_Output_and_Correct_Filtering.py'
EXPECT = {'A/B': {'HUMAN': 0.0, 'YEAST': 1.0, 'ECOLI': -2.0}, 'C/A': {'HUMAN': 0.0, 'YEAST': -3.32, 'ECOLI': 2.68}}

rep_path = os.path.join(OUT, 'report.parquet')
raw = pd.read_parquet(rep_path)
print('real DIA-NN 2.6.1 report:', rep_path, '| rows', len(raw), '| runs', raw['Run'].nunique())
want = ['Q.Value', 'PG.Q.Value', 'Global.Q.Value', 'Global.PG.Q.Value', 'Lib.Q.Value', 'Lib.PG.Q.Value', 'PG.MaxLFQ', 'Protein.Group', 'Run']
print('columns the Skill filter needs -> present:', {c: (c in raw.columns) for c in want})

# (c) the Skill's documented output listing vs what DIA-NN actually wrote
listed = ['report.parquet', 'report.stats.tsv', 'report.pg_matrix.tsv', 'report.pr_matrix.tsv', 'report.gg_matrix.tsv']
on_disk = sorted(os.listdir(OUT))
print('Skill-listed output files present:', {f: (f in on_disk) for f in listed})
print('extra files DIA-NN 2.6.1 wrote that the Skill does not list:', [f for f in on_disk if f not in listed and not f.startswith('report-first-pass')])

# (a) the Skill's filter block, verbatim, with only the parquet path swapped
src = open(BLK, encoding='utf-8').read()
assert src.count("'diann_out/report.parquet'") == 1
ns = {}
t0 = time.time()
try:
    exec(src.replace("'diann_out/report.parquet'", repr(rep_path)), ns)
    pg = ns['pg']
    print(f'[b03 verbatim] OK in {time.time() - t0:.1f} s | matrix {pg.shape} | -inf {int(np.isinf(pg.values).sum())} | NaN {int(pg.isna().sum().sum())}')
except Exception as e:
    pg = None
    print('[b03 verbatim] ERROR:', type(e).__name__, e)

# (b) report count vs matrix count -- the Skill says the matrix is LOWER because of --matrix-spec-q 0.05
lvl = raw[(raw['Q.Value'] <= 0.01) & (raw['PG.Q.Value'] <= 0.01)]
mat = pd.read_csv(os.path.join(OUT, 'report.pg_matrix.tsv'), sep='\t')
mat_n = mat['Protein.Group'].nunique() if 'Protein.Group' in mat.columns else len(mat)
print('protein groups: report run-level filter', lvl['Protein.Group'].nunique(),
      '| report + global (Skill b03)', None if pg is None else len(pg),
      '| report.pg_matrix.tsv rows', mat_n)
print("Skill claim 'matrix count can be LOWER than the report count' holds here:", mat_n < lvl['Protein.Group'].nunique())

# (d) quantitative accuracy vs the known HYE design
species = {}
for line in open(FASTA, encoding='utf-8'):
    if line.startswith('>'):
        acc = line[1:].split()[0].split('|')
        acc = acc[1] if len(acc) > 1 else acc[0]
        m = re.search(r'OS=([^=]+?) OX=', line)
        s = m.group(1) if m else ''
        species[acc] = ('HUMAN' if s.startswith('Homo sapiens') else 'YEAST' if 'cerevisiae' in s
                        else 'ECOLI' if s.startswith('Escherichia coli') else 'OTHER')

def group_species(g):
    sp = {species.get(a.strip(), 'OTHER') for a in g.split(';')}
    return sp.pop() if len(sp) == 1 else 'MIXED'

if pg is not None:
    runs = {c: next((r for r in pg.columns if f'Condition_{c}_' in r), None) for c in 'ABC'}
    sp = pd.Series({g: group_species(g) for g in pg.index})
    print('species of protein groups in matrix:', sp.value_counts().to_dict())
    for pair, (num, den) in {'A/B': ('A', 'B'), 'C/A': ('C', 'A')}.items():
        r = (pg[runs[num]] - pg[runs[den]]).dropna()
        s = sp.loc[r.index]
        rows = []
        for k, exp in EXPECT[pair].items():
            v = r[s == k]
            if len(v):
                rows.append(f'{k}: n={len(v)} median {v.median():+.2f} (expected {exp:+.2f}) IQR {v.quantile(.25):+.2f}..{v.quantile(.75):+.2f}')
        print(f'{pair} log2 ratio |', ' | '.join(rows))
