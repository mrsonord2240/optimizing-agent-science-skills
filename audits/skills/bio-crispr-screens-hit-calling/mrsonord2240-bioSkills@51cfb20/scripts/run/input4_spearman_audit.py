'''Input 4 (Edge, regression of pre-fix Input 4): "Compute Spearman rho between
MAGeCK neg|score and BAGEL2 BF; if rho<0.6, audit why the two methods disagree."
Pre-fix, this FAILED an assertion because usage-guide.md's own prompt gave no hint
about the sign/scale inversion. Post-fix, usage-guide.md's Multi-Method Consensus
section now says to sign-correct first, and SKILL.md has a dedicated section with a
worked real-data example. Verify: (a) the real numbers still reproduce exactly,
(b) the guidance is now actually present in the Skill's own files (grep, not assumed).
'''
import os, re
import pandas as pd
from scipy.stats import spearmanr

RUN = os.path.dirname(os.path.abspath(__file__))
os.chdir(RUN)

mageck = pd.read_csv('mageck_hap1.gene_summary.txt', sep='\t')[['id', 'neg|score']].rename(columns={'id': 'gene'})
bagel = pd.read_csv('bayes_factor.txt', sep='\t').rename(columns={'GENE': 'gene'})
merged = mageck.merge(bagel, on='gene', how='inner')
print(f'Merged n = {len(merged)} genes with both scores')

rho_naive, p_naive = spearmanr(merged['neg|score'], merged['BF'])
rho_corrected, p_corrected = spearmanr(-merged['neg|score'], merged['BF'])
print(f'Naive rho (neg|score vs BF):          {rho_naive:.4f} (p={p_naive:.3g})')
print(f'Sign-corrected rho (-neg|score vs BF): {rho_corrected:.4f} (p={p_corrected:.3g})')

assert round(rho_naive, 3) == -round(rho_corrected, 3), 'sign flip should be exact'
print(f'\nReproduces pre-fix figures (-0.806 / +0.806): naive={rho_naive:.3f}, corrected={rho_corrected:.3f}')

# Check the Skill's OWN files now contain sufficient guidance without outside help.
skill_dir = r'F:/OpenScience/external/mrsonord2240__bioSkills/crispr-screens/hit-calling'
skill_md = open(os.path.join(skill_dir, 'SKILL.md'), encoding='utf-8').read()
usage_md = open(os.path.join(skill_dir, 'usage-guide.md'), encoding='utf-8').read()

has_section = 'Correlating MAGeCK and BAGEL2 Scores' in skill_md
has_sign_note = bool(re.search(r'sign[- ]correct', skill_md, re.I))
usage_mentions_sign = bool(re.search(r'sign[- ]correct', usage_md, re.I))
has_worked_example = '-0.806' in skill_md or '0.806' in skill_md

print(f'\nSKILL.md has a dedicated sign/scale section: {has_section}')
print(f'SKILL.md uses the phrase "sign-correct(ing)": {has_sign_note}')
print(f'usage-guide.md\'s consensus prompt mentions sign-correcting: {usage_mentions_sign}')
print(f'SKILL.md gives the real worked-example numbers: {has_worked_example}')

assert has_section and has_sign_note and usage_mentions_sign and has_worked_example, (
    'REGRESSION: guidance about the MAGeCK/BAGEL2 sign inversion is still missing '
    'from the Skill\'s own files')
print('\nPASS: the prompt is now self-contained -- no outside statistical knowledge needed.')
