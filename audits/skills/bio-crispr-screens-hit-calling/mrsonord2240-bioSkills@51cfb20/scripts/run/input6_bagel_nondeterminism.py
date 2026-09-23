'''Input 6 (Scope Boundary, regression of pre-fix Input 6): "BAGEL2 gave me different
Bayes Factors on two reruns of the same data -- is this a real biology change?"
Pre-fix, this Skill's own files had zero mention of seed/determinism despite the
frontmatter promising help "interpreting unstable hit lists across reruns", and the
fix had to be derived entirely from the sibling bagel-essentiality audit. Post-fix,
verify (a) the real numbers still reproduce, (b) SKILL.md/usage-guide.md now contain
the guidance directly (not just by cross-link), (c) the cross-link to
bagel-essentiality is accurate (its Reproducibility section really does say what
this Skill claims it says).
'''
import os, re
import pandas as pd

RUN = os.path.dirname(os.path.abspath(__file__))
os.chdir(RUN)

rep1 = pd.read_csv('bayes_factor.txt', sep='\t').rename(columns={'BF': 'BF_rep1'})
rep2 = pd.read_csv('bayes_factor_rep2.txt', sep='\t').rename(columns={'BF': 'BF_rep2'})
merged = rep1.merge(rep2, on='GENE', how='inner')
merged['diff'] = (merged['BF_rep1'] - merged['BF_rep2']).abs()
max_diff = merged['diff'].max()
merged['hit1'] = merged['BF_rep1'] > 6
merged['hit2'] = merged['BF_rep2'] > 6
n_flip = int((merged['hit1'] != merged['hit2']).sum())
print(f'Genes compared: {len(merged)}')
print(f'Max |BF_rep1 - BF_rep2|: {max_diff:.2f}')
print(f'Genes flipping across BF>6 between reruns: {n_flip}')

assert round(max_diff, 1) == 26.7 or abs(max_diff - 26.72) < 0.1, f'expected ~26.7, got {max_diff}'
assert n_flip == 33, f'expected 33 flips, got {n_flip}'
print('\nReproduces the audited figures exactly (max diff 26.7, 33 flips).')

skill_dir = r'F:/OpenScience/external/mrsonord2240__bioSkills/crispr-screens/hit-calling'
skill_md = open(os.path.join(skill_dir, 'SKILL.md'), encoding='utf-8').read()
usage_md = open(os.path.join(skill_dir, 'usage-guide.md'), encoding='utf-8').read()

has_seed_guidance_skill = bool(re.search(r'-s\s*<int>|--seed|fixed seed', skill_md, re.I))
has_seed_guidance_usage = bool(re.search(r'-s\s*<int>|--seed|fixed seed|unseeded', usage_md, re.I))
has_own_numbers = '26.7' in skill_md or '26.72' in skill_md
has_crosslink = '[[bagel-essentiality]]' in skill_md

print(f'\nSKILL.md contains seed/determinism guidance of its own: {has_seed_guidance_skill}')
print(f'usage-guide.md contains seed/determinism guidance of its own: {has_seed_guidance_usage}')
print(f'SKILL.md states the real 26.7/33-flip figures directly (not just via link): {has_own_numbers}')
print(f'SKILL.md cross-links bagel-essentiality: {has_crosslink}')

assert has_seed_guidance_skill and has_seed_guidance_usage and has_own_numbers, (
    'REGRESSION: this Skill still relies entirely on the sibling audit for the fix')
print('PASS: guidance is now self-contained in this Skill\'s own files, not only via cross-link.')

# Verify the cross-link to bagel-essentiality is ACCURATE, not just present.
bagel_skill_path = r'F:/OpenScience/external/mrsonord2240__bioSkills/crispr-screens/bagel-essentiality/SKILL.md'
bagel_skill = open(bagel_skill_path, encoding='utf-8').read()
has_repro_section = 'Reproducibility: Fixing the Random Seed' in bagel_skill
has_matching_numbers = ('26.7' in bagel_skill) and ('33' in bagel_skill)
print(f'\nbagel-essentiality SKILL.md has the named "Reproducibility: Fixing the Random Seed" section: {has_repro_section}')
print(f'bagel-essentiality SKILL.md states matching 26.7/33 figures: {has_matching_numbers}')
assert has_repro_section and has_matching_numbers, 'cross-link target does not actually contain what is claimed'
print('PASS: citation to bagel-essentiality is accurate.')
