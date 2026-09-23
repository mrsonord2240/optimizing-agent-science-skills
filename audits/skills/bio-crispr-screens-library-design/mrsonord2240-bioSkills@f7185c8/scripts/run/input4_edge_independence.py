# Input 4 (Edge) regression test: short/PAM-less synthetic CDS, guide-independence gap.
# Pre-fix finding: find_sgrna_candidates alone returned near-duplicate guides (19/20nt
# overlap) for a 42nt CDS. Post-fix: select_independent_guides should reject the
# near-duplicate and either fill the quota from other candidates or report a shortfall.
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

print('=== INPUT 4: Edge -- short/PAM-less CDS, guide-independence gap (post-fix regression) ===')

# Sub-case A: genuinely PAM-less 44nt CDS -- must still return 0 candidates, no crash
no_pam_cds = "ATATATATATATATATATATATATATATATATATATATATAT"
print(f'\n-- Sub-case A: genuinely PAM-less {len(no_pam_cds)}nt CDS --')
cand_a = find_sgrna_candidates(no_pam_cds)
print(f'genuinely PAM-less CDS -> candidates: {len(cand_a)}')
assert len(cand_a) == 0
print('ASSERT PASS: no crash, 0 candidates as expected')

# Sub-case B: the exact 42nt CDS from the pre-fix audit that produced the 19/20nt
# overlapping pair at pos_in_cds 15 and 16
short_cds = "ATGAAACGTGGGCCCATTAGGCTGATCCGGTACTTTGGGTGA"   # 42nt, has PAMs
print(f'\n-- Sub-case B: {len(short_cds)}nt CDS (pre-fix\'s near-duplicate case) --')
cand_b = find_sgrna_candidates(short_cds)
cand_b = annotate_exon_position(cand_b, len(short_cds))
print(f'CDS length: {len(short_cds)} nt')
print(f'Raw candidates surviving 5-65% CDS filter (composition-only, pre-fix behavior): {len(cand_b)}')
print(cand_b[['spacer', 'strand', 'pos_in_cds', 'gc_frac']].to_string(index=False))

# Reproduce the pre-fix defect explicitly: candidates 15 and 16 overlap by 19/20nt
positions = sorted(cand_b['pos_in_cds'].tolist())
pre_fix_min_gap = min(positions[i+1] - positions[i] for i in range(len(positions) - 1)) if len(positions) > 1 else None
print(f'Pre-fix (composition-only) minimum pairwise spacing among raw candidates: {pre_fix_min_gap}nt')

# Now apply the fix: select_independent_guides requesting the full 4-guide quota
cand_b = cand_b.copy()
cand_b['score'] = 1 - (cand_b['gc_frac'] - 0.5).abs() * 2
sel = select_independent_guides(cand_b, 4, min_spacing=5, score_col='score')
print(f'\nselect_independent_guides(min_spacing=5) selected: {len(sel)}/4 requested')
print(sel[['spacer', 'pos_in_cds', 'score']].to_string(index=False) if not sel.empty else '(none)')
if len(sel) > 1:
    sel_positions = sorted(sel['pos_in_cds'].tolist())
    post_fix_min_gap = min(sel_positions[i+1] - sel_positions[i] for i in range(len(sel_positions) - 1))
    print(f'Post-fix minimum pairwise spacing among SELECTED guides: {post_fix_min_gap}nt')
    assert post_fix_min_gap >= 5, 'FAIL: select_independent_guides let a near-duplicate pair through'
    print('ASSERT PASS: all selected guides are >=5nt apart (near-duplicate pair correctly excluded)')
else:
    print(f'Only {len(sel)} independent guide(s) available from this 42nt CDS after spacing filter -- '
          f'correctly reports a shortfall rather than padding with a near-duplicate.')

print(f'\nQuota vs actual, explicitly reported: requested=4, raw_candidates={len(cand_b)}, independent_selected={len(sel)}')
if len(sel) < 4:
    print(f'SHORTFALL: only {len(sel)}/4 independent guides available for this 42nt CDS -- '
          f'correct behavior is to report the shortfall (as here), not silently pad with overlapping guides.')
