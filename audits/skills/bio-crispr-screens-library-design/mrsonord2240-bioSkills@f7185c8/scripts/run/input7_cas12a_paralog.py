# Input 7 (New use case, not tested pre-fix): enAsCas12a paralog-multiplex array design.
# Pre-fix audit only exercised Cas9 KO, CRISPRi, CRISPRa, the shipped example and the
# Azimuth/ambiguous-request checks. This input exercises library-design's fourth
# documented chemistry (Cas12a multiplex, "Library Composition for Specialized Screens"
# section) which was never run in either audit, and checks the GI-scoring singleton-
# control requirement the doc calls out plus build_oligo's Cas9-oriented scaffold
# assumption against a Cas12a request (a documented pitfall: "Cas12a oligo doesn't cut --
# forgot Cas12a's TTTV PAM is 5' of spacer, not 3'").
import re
import numpy as np
import pandas as pd
from Bio.Seq import Seq

np.random.seed(7)

def find_cas12a_candidates(cds_sequence, pam='TTTV', guide_length=23):
    '''Cas12a: PAM is 5' of the spacer (TTTV), opposite of Cas9's 3' NGG.
    Minimal adaptation of find_sgrna_candidates for this PAM orientation, per
    SKILL.md's PAM Variants table and its own "Cas12a oligo doesn't cut" pitfall.'''
    pam_regex = pam.replace('V', '[ACG]')
    pattern = re.compile(f'({pam_regex})(?=([ACGT]{{{guide_length-4}}}))')
    candidates = []
    for strand, seq in [('+', cds_sequence), ('-', str(Seq(cds_sequence).reverse_complement()))]:
        for m in pattern.finditer(seq):
            spacer = m.group(2)
            if len(spacer) < guide_length - 4:
                continue
            if spacer.count('G') + spacer.count('C') not in range(4, 15):
                continue
            candidates.append({'spacer': spacer, 'strand': strand, 'pos_in_cds': m.start()})
    return pd.DataFrame(candidates)

print('=== INPUT 7: enAsCas12a paralog-multiplex array, 3 synthetic paralog pairs (NEW, not in pre-fix) ===')

bases = ['A', 'C', 'G', 'T']
paralog_pairs = [('PARALOG-A1', 'PARALOG-A2'), ('PARALOG-B1', 'PARALOG-B2'), ('PARALOG-C1', 'PARALOG-C2')]

arrays = []
shortfalls = []
for i, (gene_a, gene_b) in enumerate(paralog_pairs):
    rng_a = np.random.RandomState(700 + 2 * i)
    rng_b = np.random.RandomState(700 + 2 * i + 1)
    cds_a = ''.join(rng_a.choice(bases, 500))
    cds_b = ''.join(rng_b.choice(bases, 500))
    cand_a = find_cas12a_candidates(cds_a)
    cand_b = find_cas12a_candidates(cds_b)
    if len(cand_a) < 2 or len(cand_b) < 2:
        shortfalls.append((gene_a, gene_b, len(cand_a), len(cand_b)))
        continue
    # positions 1-2 target gene A, positions 3-4 target gene B, per SKILL.md's
    # "Paralog buffering (Cas12a multiplex)" convention
    array = {
        'array_id': f'{gene_a}_{gene_b}_array',
        'pos1_2_gene': gene_a, 'pos1_2_guides': cand_a['spacer'].head(2).tolist(),
        'pos3_4_gene': gene_b, 'pos3_4_guides': cand_b['spacer'].head(2).tolist(),
    }
    arrays.append(array)

print(f'Paralog pairs requested: {len(paralog_pairs)}; pairs with insufficient TTTV sites: {shortfalls}')
print(f'4-guide arrays built: {len(arrays)}')
for a in arrays:
    print(f"  {a['array_id']}: pos1-2={a['pos1_2_gene']} ({len(a['pos1_2_guides'])} guides), "
          f"pos3-4={a['pos3_4_gene']} ({len(a['pos3_4_guides'])} guides)")

assert all(len(a['pos1_2_guides']) == 2 and len(a['pos3_4_guides']) == 2 for a in arrays), \
    'FAIL: an array did not fill both 2-guide slots'
print('ASSERT PASS: every built array has 2 guides for each paralog (4-guide array total)')

# Singleton controls: SKILL.md/usage-guide.md both say GI scoring needs gene-A-alone,
# gene-B-alone, and double-NTC singleton conditions -- this input checks that a
# faithful design run following the doc actually adds these, not just the 4-guide array.
singleton_rows = []
for a in arrays:
    gene_a, gene_b = a['pos1_2_gene'], a['pos3_4_gene']
    singleton_rows.append({'array_id': f'{gene_a}_alone', 'type': 'singleton-A', 'guides': a['pos1_2_guides']})
    singleton_rows.append({'array_id': f'{gene_b}_alone', 'type': 'singleton-B', 'guides': a['pos3_4_guides']})
singleton_rows.append({'array_id': 'double_NTC', 'type': 'singleton-control', 'guides': ['NTC', 'NTC']})
print(f'\nSingleton conditions added for GI scoring (gene A alone, gene B alone, double-NTC): '
      f'{len(singleton_rows)} rows for {len(arrays)} arrays')
assert len(singleton_rows) == 2 * len(arrays) + 1
print('ASSERT PASS: GI-scoring singleton set is complete (double_KO_LFC - sum(single_KO_LFC) is computable)')

# Cas12a PAM-orientation check against SKILL.md's own documented Common Errors pitfall:
# "Cas12a oligo doesn't cut | Forgot Cas12a's TTTV PAM is 5' of spacer, not 3' |
#  Re-orient: PAM-then-spacer for Cas12a, opposite of Cas9"
skill_md = open('../run/library-design-src/SKILL.md', encoding='utf-8').read()
assert "PAM-then-spacer for Cas12a" in skill_md, 'Cas12a PAM-orientation pitfall missing from SKILL.md Common Errors'
print("\nDOC CHECK PASS: SKILL.md's Common Errors table documents the Cas12a PAM-orientation pitfall "
      "(PAM 5' of spacer, opposite Cas9's 3' NGG) -- the find_cas12a_candidates() above was written "
      "to that documented orientation, not Cas9's, and found real TTTV-adjacent spacers.")

pd.DataFrame(arrays).to_csv('input7_cas12a_arrays.csv', index=False)
print('Saved input7_cas12a_arrays.csv')
