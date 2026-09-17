# Input 5 (Edge/New, real data): independently reproduce the fix log's own primary claim
# -- that select_independent_guides(min_spacing=5) raises the minimum pairwise spacing
# on a REAL gene's CDS while still filling the quota -- using a live NCBI E-utilities
# fetch, not the fix author's own script. This input did not exist in the pre-fix audit
# (which used synthetic CDS only).
import re
import sys
import urllib.request
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

print('=== INPUT 5: Real TP53 CDS (NM_000546.6), live NCBI efetch (post-fix, new input) ===')

url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
       "?db=nuccore&id=NM_000546.6&rettype=fasta_cds_na&retmode=text")
try:
    with urllib.request.urlopen(url, timeout=30) as resp:
        fasta_text = resp.read().decode('utf-8')
except Exception as e:
    print(f'NCBI fetch failed: {e}')
    sys.exit(1)

lines = fasta_text.strip().splitlines()
header = lines[0]
cds = ''.join(lines[1:]).upper().replace('U', 'T')
print(f'Fetched header: {header}')
print(f'CDS length: {len(cds)} nt')
assert len(cds) > 0 and set(cds) <= set('ACGTN'), 'Fetched sequence is not a clean nucleotide CDS'

cand = find_sgrna_candidates(cds)
cand = annotate_exon_position(cand, len(cds))
print(f'Raw candidates after 5-65% CDS + composition filter: {len(cand)}')
cand = cand.copy()
cand['score'] = 1 - (cand['gc_frac'] - 0.5).abs() * 2

# Reproduce the pre-fix defect: naive top-12-by-score with NO spacing filter
naive_top12 = cand.sort_values('score', ascending=False).head(12)
naive_positions = sorted(naive_top12['pos_in_cds'].tolist())
naive_gaps = [naive_positions[i+1] - naive_positions[i] for i in range(len(naive_positions) - 1)]
print(f'\nNaive top-12-by-score (NO spacing filter) minimum pairwise gap: {min(naive_gaps)}nt '
      f'(pairs <5nt apart: {sum(1 for g in naive_gaps if g < 5)})')

# Apply the fix
sel12 = select_independent_guides(cand, 12, min_spacing=5, score_col='score')
sel_positions = sorted(sel12['pos_in_cds'].tolist())
sel_gaps = [sel_positions[i+1] - sel_positions[i] for i in range(len(sel_positions) - 1)] if len(sel_positions) > 1 else []
print(f'select_independent_guides(min_spacing=5) filled: {len(sel12)}/12 requested')
print(f'Minimum pairwise gap among SELECTED guides: {min(sel_gaps) if sel_gaps else "n/a"}nt')
print(f'Full pairwise-gap distribution (sorted): {sel_gaps}')

assert len(sel12) == 12, f'FAIL: quota not filled ({len(sel12)}/12) even though {len(cand)} raw candidates exist'
assert min(sel_gaps) >= 5, 'FAIL: two selected guides are <5nt apart'
print('ASSERT PASS: quota filled (12/12) AND every pairwise gap >=5nt -- matches fix log claim exactly')

# Second part of the fix log's claim: behavior when the quota CANNOT be met --
# request more guides than min_spacing=5 can possibly pack into this CDS's 5-65% window.
window_len = 0.60 * len(cds)
theoretical_max_at_spacing5 = int(window_len // 5)
over_quota = theoretical_max_at_spacing5 + 20
sel_over = select_independent_guides(cand, over_quota, min_spacing=5, score_col='score')
print(f'\nRequesting {over_quota} guides (deliberately > what {len(cand)} candidates at min_spacing=5 can supply): '
      f'select_independent_guides returned {len(sel_over)} (no crash, no padding, quota under-filled as expected)')
assert len(sel_over) <= len(cand)
assert len(sel_over) < over_quota, 'FAIL: function claimed to fill an unmeetable quota'
if len(sel_over) > 1:
    over_positions = sorted(sel_over['pos_in_cds'].tolist())
    over_gaps = [over_positions[i+1] - over_positions[i] for i in range(len(over_positions) - 1)]
    assert min(over_gaps) >= 5
    print(f'ASSERT PASS: even when over-requested, all {len(sel_over)} returned guides remain >=5nt apart '
          f'(no near-duplicate smuggled in to hit the quota)')

sel12.to_csv('input5_tp53_selected_guides.csv', index=False)
print('\nSaved input5_tp53_selected_guides.csv')
