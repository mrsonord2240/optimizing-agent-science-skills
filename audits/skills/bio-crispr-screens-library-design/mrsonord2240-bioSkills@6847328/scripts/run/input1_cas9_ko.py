# Input 1 (Canonical) regression test: Cas9 KO library, 8 synthetic DDR genes.
# Verbatim find_sgrna_candidates/annotate_exon_position/select_independent_guides/build_oligo
# from the fixed SKILL.md's "Score and Rank sgRNAs for a Target Gene" section.
import re
import numpy as np
import pandas as pd
from Bio.Seq import Seq

np.random.seed(1)

def find_sgrna_candidates(cds_sequence, pam='NGG', guide_length=20):
    pam_pattern = re.compile(f'(?=([ACGT]{{{guide_length}}}{pam.replace("N", "[ACGT]")}))')
    candidates = []
    for strand, seq in [('+', cds_sequence), ('-', str(Seq(cds_sequence).reverse_complement()))]:
        for m in pam_pattern.finditer(seq):
            spacer = m.group(1)[:guide_length]
            if 'TTTT' in spacer or spacer.count('G') + spacer.count('C') not in range(6, 15):
                continue
            candidates.append({'spacer': spacer, 'strand': strand,
                               'pos_in_cds': m.start() if strand == '+' else len(seq) - m.start() - 23,
                               'gc_frac': (spacer.count('G') + spacer.count('C')) / guide_length})
    return pd.DataFrame(candidates)

def annotate_exon_position(candidates_df, cds_length):
    lo, hi = 0.05 * cds_length, 0.65 * cds_length
    return candidates_df[(candidates_df['pos_in_cds'] >= lo) & (candidates_df['pos_in_cds'] <= hi)].copy()

def select_independent_guides(candidates_df, n_guides, min_spacing=5, score_col='score'):
    ranked = candidates_df.sort_values(score_col, ascending=False)
    selected = []
    for _, cand in ranked.iterrows():
        if any(abs(cand['pos_in_cds'] - s['pos_in_cds']) < min_spacing for s in selected):
            continue
        selected.append(cand)
        if len(selected) == n_guides:
            break
    return pd.DataFrame(selected)

def build_oligo(spacer, vector='lentiGuide-Puro', subpool_idx=None):
    subpool_fwd = {
        1: 'GGAAAGGACGAAACACCG',
        2: 'GAGGCACTGGGCAGGTACCG',
    }.get(subpool_idx, 'GGAAAGGACGAAACACCG')
    scaffold_short = 'GTTTAAGAGCTATGCTGGAAACAGCATAGCAAG'
    oligo = subpool_fwd + spacer + scaffold_short
    if len(oligo) > 200:
        raise ValueError(f'Oligo length {len(oligo)} exceeds the 200 nt design budget; check the vendor limit')
    return oligo

# 8 synthetic DDR-pathway-length genes (600nt CDS each), deterministic per-gene seed
genes = ['ATM', 'ATR', 'BRCA1', 'BRCA2', 'CHEK1', 'CHEK2', 'PARP1', 'RAD51']
bases = ['A', 'C', 'G', 'T']

print('=== INPUT 1: Cas9 KO library, 8 synthetic DDR genes (post-fix regression) ===')
all_rows = []
shortfall = []
for i, gene in enumerate(genes):
    rng = np.random.RandomState(100 + i)
    cds = ''.join(rng.choice(bases, 600))
    cand = find_sgrna_candidates(cds)
    cand = annotate_exon_position(cand, len(cds))
    if cand.empty:
        shortfall.append((gene, 0))
        continue
    cand = cand.copy()
    cand['score'] = 1 - (cand['gc_frac'] - 0.5).abs() * 2
    sel = select_independent_guides(cand, 4, min_spacing=5, score_col='score')
    if len(sel) < 4:
        shortfall.append((gene, len(sel)))
    for _, g in sel.iterrows():
        all_rows.append({'gene': gene, 'sequence': g['spacer'], 'pos_in_cds': g['pos_in_cds'],
                          'gc_frac': g['gc_frac'], 'score': g['score'], 'type': 'targeting'})

lib = pd.DataFrame(all_rows)
print(f'Genes requested: {len(genes)}; genes with <4 guides after independence filter: {shortfall}')
print(f'Total targeting guides: {len(lib)}')

# Controls (same proportions as SKILL.md worked example)
ctrl_rows = []
rng_ctrl = np.random.RandomState(999)
for i in range(50):
    seq = ''.join(rng_ctrl.choice(bases, 20))
    ctrl_rows.append({'gene': f'NTC_{i+1:03d}', 'sequence': seq, 'pos_in_cds': np.nan, 'gc_frac': np.nan, 'score': np.nan, 'type': 'non-targeting'})
for gene in ['RPS3', 'RPL11', 'EIF3A', 'POLR2A']:
    seq = ''.join(rng_ctrl.choice(bases, 20))
    ctrl_rows.append({'gene': gene, 'sequence': seq, 'pos_in_cds': np.nan, 'gc_frac': np.nan, 'score': np.nan, 'type': 'essential-control'})
for gene in ['SEPT2', 'CD81', 'ACTB', 'GAPDH']:
    seq = ''.join(rng_ctrl.choice(bases, 20))
    ctrl_rows.append({'gene': gene, 'sequence': seq, 'pos_in_cds': np.nan, 'gc_frac': np.nan, 'score': np.nan, 'type': 'nonessential-control'})
seq = ''.join(rng_ctrl.choice(bases, 20))
ctrl_rows.append({'gene': 'AAVS1', 'sequence': seq, 'pos_in_cds': np.nan, 'gc_frac': np.nan, 'score': np.nan, 'type': 'safe-harbor'})

full = pd.concat([lib, pd.DataFrame(ctrl_rows)], ignore_index=True)
full['forward_oligo'] = full['sequence'].apply(lambda s: build_oligo(s))
print(f'Total library rows (targeting + controls): {len(full)}')
print(full['type'].value_counts())

# --- Spacing check: verify no two selected guides for the same gene are <5nt apart ---
min_gaps = []
for gene, grp in lib.groupby('gene'):
    positions = sorted(grp['pos_in_cds'].tolist())
    if len(positions) > 1:
        gaps = [positions[i+1] - positions[i] for i in range(len(positions) - 1)]
        min_gaps.append((gene, min(gaps)))
print('Per-gene minimum pairwise spacing (pos_in_cds):', min_gaps)
assert all(g >= 5 for _, g in min_gaps), 'FAIL: a gene has guides closer than min_spacing=5'
print('ASSERT PASS: every gene\'s selected guides are >=5nt apart')

assert (full['forward_oligo'].str.len() > 0).all()
assert full['sequence'].apply(len).eq(20).all()
print('ASSERT PASS: all spacers 20nt, all oligos non-empty')

full.to_csv('input1_ko_library.csv', index=False)
print('Saved input1_ko_library.csv')
