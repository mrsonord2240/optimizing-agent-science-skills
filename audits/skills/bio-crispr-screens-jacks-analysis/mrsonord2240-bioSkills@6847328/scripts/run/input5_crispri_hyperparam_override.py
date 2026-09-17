"""
Input 5 (Scope Boundary). CRISPRi chemistry-mismatch hyperparameter override recipe --
SKILL.md's own "Efficacy collapsed near zero for all guides" Failure Mode fix. Pre-fix,
this recipe named an undocumented interface with no runnable example (P1 finding,
executed: false). Post-fix, SKILL.md gives a concrete functools.partial-based override.
This input runs that exact code block verbatim against real data and confirms:
  (1) it actually executes and produces output with the overridden prior,
  (2) jacks.infer.inferJACKSGene is restored to the default afterward (asserted, not
      just claimed), so later runs in the same session are unaffected.
"""
import sys, os
sys.path.insert(0, r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks")
import functools
import jacks.infer
from jacks.jacks_io import runJACKS

EX = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks\example-small"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out5"
os.makedirs(OUT, exist_ok=True)

counts_path = f"{EX}/example_count_data.tab"
repmap_path = f"{EX}/example_repmap.tab"
guide_map_path = counts_path

_default_gene_fit = jacks.infer.inferJACKSGene
print(f"Default inferJACKSGene before override: {jacks.infer.inferJACKSGene}")

# Verbatim from SKILL.md's Failure Modes section (post-fix)
jacks.infer.inferJACKSGene = functools.partial(_default_gene_fit, mu0_x=1.0, var0_x=4.0)
print(f"Overridden inferJACKSGene: {jacks.infer.inferJACKSGene}")

try:
    runJACKS(
        countfile=counts_path,
        replicatefile=repmap_path,
        guidemappingfile=guide_map_path,
        rep_hdr='Replicate', sample_hdr='Sample', common_ctrl_sample='CTRL',
        sgrna_hdr='sgRNA', gene_hdr='Gene',
        outprefix=f'{OUT}/jacks_crispri_override',
        apply_w_hp=False,
    )
    print("PASS: run completed with overridden efficacy prior (var0_x=4.0).")
finally:
    jacks.infer.inferJACKSGene = _default_gene_fit
    print(f"\nRestored inferJACKSGene after override: {jacks.infer.inferJACKSGene}")
    assert jacks.infer.inferJACKSGene is _default_gene_fit, "FAIL: restoration did not work"
    print("PASS: inferJACKSGene correctly restored to the pre-override default function object.")

# Compare efficacy SD before/after override to confirm the override actually changed inference,
# not just accepted the kwarg silently.
import pandas as pd
default_grna = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out1\whp_false_canonical_grna_JACKS_results.txt"
override_grna = f"{OUT}/jacks_crispri_override_grna_JACKS_results.txt"
d = pd.read_csv(default_grna, sep='\t')
o = pd.read_csv(override_grna, sep='\t')
d_std = (d['X2'] - d['X1']**2).clip(lower=0).pow(0.5)
o_std = (o['X2'] - o['X1']**2).clip(lower=0).pow(0.5)
print(f"\nEfficacy posterior SD, default prior (var0_x=1.0): mean={d_std.mean():.3f}")
print(f"Efficacy posterior SD, overridden prior (var0_x=4.0): mean={o_std.mean():.3f}")
if o_std.mean() > d_std.mean():
    print("PASS: overriding var0_x visibly widened the efficacy posterior, confirming the override took effect (not silently ignored).")
else:
    print("NOTE: SD did not widen as expected -- re-check the override mechanism.")

print("\n=== Follow-up run using default inferJACKSGene to confirm restoration holds for later calls ===")
runJACKS(
    countfile=counts_path, replicatefile=repmap_path, guidemappingfile=guide_map_path,
    rep_hdr='Replicate', sample_hdr='Sample', common_ctrl_sample='CTRL',
    sgrna_hdr='sgRNA', gene_hdr='Gene',
    outprefix=f'{OUT}/jacks_after_restore', apply_w_hp=False,
)
after = pd.read_csv(f'{OUT}/jacks_after_restore_grna_JACKS_results.txt', sep='\t')
identical = (after['X1'].round(6) == d['X1'].round(6)).all()
print(f"Post-restore run identical to original default run: {identical}")
