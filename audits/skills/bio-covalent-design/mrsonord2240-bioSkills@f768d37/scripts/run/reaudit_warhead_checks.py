# Re-audit independent verification for bio-covalent-design (2026-09-19)
# Re-auditor: fresh agent, does not reuse the fixer's own test invocations beyond
# regression-running the shipped __main__ block once. All molecules below were chosen
# independently of fixes/bio-covalent-design.md's stated verification compounds
# (fixer used phenacyl chloride + chalcone; this script adds different ones and
# explicit negative controls).

import sys
sys.path.insert(0, 'skill_copy/examples')
from warhead_classifier import classify_warheads, WARHEAD_SMARTS

def show(label, smi):
    r = classify_warheads(smi)
    print(f'{label:45s} {smi:35s} -> {sorted(r.keys()) if r else r}')
    return r

print('=== 1. Regression: run shipped __main__ block (fixer + prior assertions) ===')
import subprocess
res = subprocess.run([sys.executable, 'skill_copy/examples/warhead_classifier.py'],
                      capture_output=True, text=True, cwd='.')
print('exit code:', res.returncode)
print(res.stdout)
if res.stderr:
    print('STDERR:', res.stderr)
assert res.returncode == 0, 'shipped script must exit 0'

print()
print('=== 2. New positive controls (not used by the fixer) ===')

# alpha_haloketone: different real Cys-reactive haloketone, not phenacyl chloride
r = show('4-bromophenacyl bromide (alpha-haloketone)', 'BrCC(=O)c1ccc(Br)cc1')
assert 'alpha_haloketone' in r

r = show('1-chloro-2-propanone (aliphatic alpha-haloketone)', 'CC(=O)CCl')
assert 'alpha_haloketone' in r

# alpha,beta-unsaturated ketone: different Michael-acceptor ketone, not chalcone
r = show('4-phenyl-3-buten-2-one (benzalacetone)', 'CC(=O)/C=C/c1ccccc1')
assert 'alpha_beta_unsaturated_ketone' in r

r = show('cyclohex-2-enone', 'O=C1CCCC=C1')
assert 'alpha_beta_unsaturated_ketone' in r

print()
print('=== 3. Negative controls: plain ketone must NOT trigger either new class ===')
r = show('acetophenone (plain aryl ketone, no halide/unsaturation)', 'CC(=O)c1ccccc1')
assert 'alpha_haloketone' not in r
assert 'alpha_beta_unsaturated_ketone' not in r

r = show('cyclohexanone (saturated, no halide)', 'O=C1CCCCC1')
assert 'alpha_haloketone' not in r
assert 'alpha_beta_unsaturated_ketone' not in r

print()
print('=== 4. Cross-contamination check: amide-based warheads must NOT co-match the new ketone keys ===')
amide_warheads = {
    'chloroacetamide': 'O=C(CCl)NCc1ccccc1',
    'bromoacetamide': 'O=C(CBr)NCc1ccccc1',
    'acrylamide (N-cyclohexyl)': 'C=CC(=O)N1CCCCC1',
    'methacrylamide': 'C=C(C)C(=O)N1CCCCC1',
}
for label, smi in amide_warheads.items():
    r = show(label, smi)
    assert 'alpha_haloketone' not in r, f'{label} spuriously matched alpha_haloketone'
    assert 'alpha_beta_unsaturated_ketone' not in r, f'{label} spuriously matched alpha_beta_unsaturated_ketone'

print()
print('=== 5. A halogenated AMIDE (not ketone) must not match alpha_haloketone either ===')
# 2-chloro-N-phenylacetamide is chloroacetamide already covered above; add a beta-halo
# amide variant to probe whether the ketone SMARTS over-generalizes to any C(=O)-C-X.
r = show('3-chloropropanamide (beta-haloamide, not alpha-haloketone)', 'O=C(N)CCCl')
assert 'alpha_haloketone' not in r  # CH2 is beta not alpha to a halide adjacent carbonyl carbon anyway

print()
print('=== 6. Independent overlap re-check (methacrylamide co-matches all 3 acrylamide-family keys) ===')
r = show('methacrylamide (overlap check)', 'C=C(C)C(=O)N1CCCCC1')
assert {'acrylamide', 'alpha_substituted_acrylamide', 'methacrylamide'} <= set(r)

print()
print('=== 7. SKILL.md table coverage: every documented warhead row (except the explicit')
print('    "various" heterocycle row) has a catalog key ===')
skill_md_rows = {
    'acrylamide', 'chloroacetamide', 'alpha_haloketone', 'vinyl_sulfone',
    'sulfonyl_fluoride', 'fluorosulfate_sufex', 'aldehyde', 'boronate', 'nitrile',
    'epoxide', 'alpha_beta_unsaturated_ketone', 'isothiocyanate', 'maleimide',
}
missing = skill_md_rows - set(WARHEAD_SMARTS)
print('missing from catalog:', missing)
assert not missing

print()
print('ALL RE-AUDIT ASSERTIONS PASSED')
