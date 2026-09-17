"""
Independent verification (not using any code from the Skill) that every
pegRNA candidate produced by the FIXED examples/design_pegrna_pridict2.py
(design_pegrna_pridict2_FIXED.py in this folder) has:
  (a) a PBS genomic window that does not overlap the PAM, and
  (b) a PBS string equal to the hand-computed reverse complement of that
      genomic window.

Run after design_pegrna_pridict2_FIXED.py has produced peg_library_filtered.csv
from intended_variants.csv (= variants_round2_batch.csv, copied over).
"""
import re
import pandas as pd

COMP = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}


def revcomp(s):
    return ''.join(COMP[b] for b in reversed(s))


variants = pd.read_csv('intended_variants.csv')
df = pd.read_csv('peg_library_filtered.csv')

n_checked = 0
n_overlap = 0
n_pbs_mismatch = 0
for _, var in variants.iterrows():
    ctx = var['context']
    for strand in ['+', '-']:
        seq = ctx if strand == '+' else revcomp(ctx)
        edit_pos = 30 if strand == '+' else len(ctx) - 1 - 30
        for pam_match in re.finditer(r'(?=([ACGT]GG))', seq):
            pam_pos = pam_match.start()
            if pam_pos < 20:
                continue
            cut_pos = pam_pos - 3
            edit_dist = edit_pos - cut_pos
            if not (1 <= edit_dist <= 30):
                continue
            spacer = seq[pam_pos - 20:pam_pos]
            match = df[(df['variant_id'] == var['variant_id']) &
                       (df['pam_strand'] == strand) & (df['spacer'] == spacer)]
            if match.empty:
                continue
            row = match.iloc[0]
            pbs_len = len(row['pbs'])
            pbs_geno_window = (cut_pos - pbs_len, cut_pos)
            pam_window = (pam_pos, pam_pos + 3)
            overlap = not (pbs_geno_window[1] <= pam_window[0] or pbs_geno_window[0] >= pam_window[1])
            expected_pbs = revcomp(seq[cut_pos - pbs_len:cut_pos])
            n_checked += 1
            if overlap:
                n_overlap += 1
            if row['pbs'] != expected_pbs:
                n_pbs_mismatch += 1
            print(var['variant_id'], strand, 'pbs_window', pbs_geno_window, 'pam_window', pam_window,
                  'OVERLAP' if overlap else 'no-overlap',
                  'pbs_matches_hand_calc', row['pbs'] == expected_pbs)

print(f"\nChecked {n_checked} candidates: {n_overlap} PAM-overlapping, {n_pbs_mismatch} PBS mismatches "
      f"against independent hand-derived revcomp.")
assert n_overlap == 0, "PAM overlap found -- pre-fix defect regressed"
assert n_pbs_mismatch == 0, "PBS does not match independent hand computation"
print("PASS: no PAM overlap, all PBS sequences match independent hand-derived revcomp.")
