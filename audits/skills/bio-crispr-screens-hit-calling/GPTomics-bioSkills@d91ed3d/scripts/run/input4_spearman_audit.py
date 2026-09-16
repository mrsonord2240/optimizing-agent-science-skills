'''
Input 4 (Edge) -- "Compute Spearman rho between MAGeCK neg|score and BAGEL2 BF for my
HAP1 TKOv3 screen. If rho <0.6, audit why the two methods disagree." (usage-guide.md,
Multi-Method Consensus examples, verbatim prompt pattern.)

Edge case: BAGEL2 BF is a "higher = more essential" score while MAGeCK neg|score is a
"lower = more essential" p-value-like score (see Input 1 output: POLR2L has the SMALLEST
neg|score and a large positive BF). A correlation computed naively (without sign-flipping
one of the two) will come out strongly NEGATIVE, not positive -- testing whether the
Skill's own usage-guide.md prompt ("compute Spearman rho... if rho<0.6, audit why")
anticipates this sign mismatch or would send an agent chasing a false "disagreement".
'''
import pandas as pd
from scipy import stats

merged = pd.read_csv('input1_consensus_output.csv').dropna(subset=['mageck_neg_score', 'bagel_bf'])

rho_naive, p_naive = stats.spearmanr(merged['mageck_neg_score'], merged['bagel_bf'])
rho_signed, p_signed = stats.spearmanr(-merged['mageck_neg_score'], merged['bagel_bf'])

print(f'N genes with both scores: {len(merged)}')
print(f'Naive Spearman rho(MAGeCK neg|score, BAGEL2 BF)      = {rho_naive:.4f}  (p={p_naive:.2e})')
print(f'Sign-corrected Spearman rho(-neg|score, BAGEL2 BF)   = {rho_signed:.4f}  (p={p_signed:.2e})')
print()
if rho_naive < 0.6:
    print('Naive reading: rho < 0.6 -- usage-guide.md instructs "audit why the two methods disagree".')
    print('Correct reading: the scales are inverted, not disagreeing; rho is strongly negative')
    print('because MAGeCK neg|score is a p-value-like statistic (smaller = more essential) while')
    print('BAGEL2 BF is a log-likelihood ratio (larger = more essential). Sign-correcting recovers')
    print(f'a strong positive correlation (rho={rho_signed:.3f}), i.e. the methods AGREE well.')
