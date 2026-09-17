# Supplementary check (not one of the 8 scored inputs): does find_sgrna_candidates
# crash or silently misbehave on malformed sequence input? The fix log explicitly left
# this unverified ("no crash observed, out of ticketed scope"). Checked independently here.
import re
import pandas as pd
from Bio.Seq import Seq

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

tests = {
    'lowercase acgt': 'atgaaacgtgggcccattaggctgatccggtactttgggtga',
    'has N ambiguity code': 'ATGAAACGTGGGNCCCATTAGGCTGATCCGGTACTTTGGGTGA',
    'garbage char (space/digit)': 'ATGAAACGTGGG CCCATTAGGCTGATCCGGTACTTTGGGT2GA',
    'empty string': '',
}
for name, seq in tests.items():
    try:
        df = find_sgrna_candidates(seq)
        print(f'{name}: OK (no exception), {len(df)} candidates')
    except Exception as e:
        print(f'{name}: RAISED {type(e).__name__}: {e}')

print('\nFinding: no crash on any malformed input (confirms fix log). But lowercase input '
      'silently returns 0 candidates with no warning that the regex is case-sensitive -- a '
      'user who pastes a lowercase FASTA CDS gets an empty, unexplained result rather than '
      'an error or an uppercase() normalization step. This is a genuinely new finding (not '
      'in the fix log or pre-fix report), degrades safely (no crash) but silently.')
