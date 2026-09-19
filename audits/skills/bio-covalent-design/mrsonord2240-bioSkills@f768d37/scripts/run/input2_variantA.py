# Input 2 (Variant A): "For 30 acrylamide compounds in series.csv, compute alpha-C substituent
# count and compare it with measured GSH rates and kinact/Ki without treating it as a LUMO
# calculation." (verbatim example prompt, usage-guide.md "Reactivity SAR")
# We use a smaller synthetic 8-compound acrylamide series with SYNTHETIC "measured" GSH half-life
# and kinact/Ki values (clearly labeled synthetic) to test whether the skill compares alpha
# substitution against measured data rather than substituting it as a reactivity prediction.
from warhead_classifier import classify_warheads
from alpha_sub import acrylamide_alpha_substitution_count

# (name, smiles, SYNTHETIC measured GSH t1/2 [min], SYNTHETIC measured kinact/Ki [M^-1 s^-1])
series = [
    ('AC-01', 'C=CC(=O)Nc1ccccc1', 42, 1850),                # unsubstituted acrylamide
    ('AC-02', 'C=C(C)C(=O)Nc1ccccc1', 210, 310),              # alpha-methyl (methacrylamide)
    ('AC-03', 'C=C(c1ccccc1)C(=O)Nc1ccccc1', 95, 640),        # alpha-phenyl
    ('AC-04', 'C=CC(=O)N1CCCCC1', 38, 2010),                  # unsubstituted, cyclic amine
    ('AC-05', 'C=C(Cl)C(=O)Nc1ccccc1', 5, 9800),               # alpha-chloro acrylamide (very reactive)
    ('AC-06', 'C=C(F)C(=O)Nc1ccccc1', 60, 1420),               # alpha-fluoro acrylamide
    ('AC-07', 'C=CC(=O)Nc1ccc(F)cc1', 40, 1900),               # unsubstituted, para-F aniline
    ('AC-08', 'C=C(C)C(=O)Nc1ccc(Cl)cc1', 195, 340),           # alpha-methyl, para-Cl aniline
]

print(f"{'id':8s} {'alpha_subs':10s} {'reactivity_tier':16s} {'GSH_t1/2(min, synthetic)':26s} {'kinact/Ki(synthetic)'}")
for name, smi, gsh_t12, kk in series:
    matches = classify_warheads(smi)
    alpha = acrylamide_alpha_substitution_count(smi)
    tier = matches.get('acrylamide', matches.get('alpha_substituted_acrylamide', matches.get('methacrylamide', {}))).get('reactivity_tier', 'NOT ACRYLAMIDE-CLASS') if matches else 'no match'
    print(f"{name:8s} {str(alpha):10s} {tier:16s} {gsh_t12:<26} {kk}")

print()
print("Correlation check (does alpha-substitution COUNT alone predict measured kinact/Ki?):")
import statistics
alphas = [acrylamide_alpha_substitution_count(smi) for _, smi, _, _ in series]
kks = [kk for _, _, _, kk in series]
# Pearson r without numpy/scipy dependency assumption issues
n = len(alphas)
mean_a, mean_k = statistics.mean(alphas), statistics.mean(kks)
cov = sum((a - mean_a) * (k - mean_k) for a, k in zip(alphas, kks))
sd_a = (sum((a - mean_a) ** 2 for a in alphas)) ** 0.5
sd_k = (sum((k - mean_k) ** 2 for k in kks)) ** 0.5
r = cov / (sd_a * sd_k)
print(f"Pearson r(alpha_substitution_count, measured kinact/Ki) = {r:.3f}")
print("(Reported to demonstrate whether alpha-count alone is a reliable single-feature reactivity")
print(" surrogate on this synthetic series -- SKILL.md explicitly says it is NOT a stand-alone")
print(" reactivity prediction and must be considered alongside electronics/measured data.)")
