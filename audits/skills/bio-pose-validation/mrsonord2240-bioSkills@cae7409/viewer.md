> **Audit record for `bio-pose-validation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@cae7409](https://github.com/mrsonord2240/bioSkills/tree/cae740920eb752a820afd1efb953e28916bf41e5/chemoinformatics/pose-validation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pose-validation (RE-AUDIT after fix)

Generated: 2026-09-19
Re-auditor: independent agent (not the original auditor, not the fixer)
Source: `mrsonord2240/bioSkills@cae7409:chemoinformatics/pose-validation` (worktree `F:\OpenScience\wt\cg-pose`, branch `fix/cg-pose-validation`)
Pre-fix report archived to: `F:\OpenScience\audits\_pre-fix-20260919\bio-pose-validation\`
Fix log (claim, not evidence): `F:\optimizing-agent-science-skills\fixes\bio-pose-validation.md`
Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\` — PoseBusters 0.6.5, RDKit 2026.03.6, pandas 3.0.5

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 39 | 57 | 96 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 37 | 55 | 92 | 3/3 PASS | ✅ |
| 3 | Edge (regression) | 38 | 57 | 95 | 5/5 PASS | ✅ |
| 4 | Variant B (regression) | 38 | 57 | 95 | 3/3 PASS | ✅ |
| 5 | Stress (regression) | 36 | 56 | 92 | 4/4 PASS | ✅ |
| 6 | New — chirality-config gap | 36 | 54 | 90 | 3/4 PASS | ⚠️ |
| 7 | New — independent planarity bisection | 38 | 56 | 94 | 3/3 PASS | ✅ |

**Execution Average: 93.4 / 100**
**Assertion Pass Rate: 25/26 (96.2%)**

> Note for reviewer: Input 6's one FAIL is a genuinely new finding (P2), not a regression — see below.

---

## Regression: original 5 inputs re-run

All 5 of the original audit's inputs were re-run with the original auditor's own scripts, unmodified, against the fixed Skill and the same real docking data (RCSB 3PTB trypsin + AutoDock-Vina-redocked benzamidine).

### Input 1 — Canonical: dock config on the real Vina pose

Ran `input1_canonical.py` unchanged. Output unchanged from the pre-fix run: 22/22 boolean columns pass, `pb_valid=True`.

The one assertion that FAILED pre-fix — "SKILL.md's dock-config claim accurately describes the returned columns vs redock" — now PASSES. I did **not** reuse the fixer's verification script; I wrote my own (`reaudit_dock_vs_redock.py`) and got:

```
dock n_cols: 22
redock n_cols: 28
redock-only columns: ['double_bond_stereochemistry', 'mol_true_loaded', 'molecular_bonds',
                       'molecular_formula', 'rmsd_≤_2å', 'tetrahedral_chirality']
dock-only columns (should be empty): []
```

Excluding `mol_true_loaded` (a loading-status column, not a check — same reasoning the original audit and the fix log used), that is exactly the 5 checks the corrected SKILL.md now names: molecular_formula, molecular_bonds, double_bond_stereochemistry, tetrahedral_chirality, RMSD. **Independently confirmed.**

### Input 2 — Variant A: MMFF94 strain

Ran `input2_variant_a_strain.py` unchanged. Result: `strain_kcal = 4.162648`, `note = ok` — identical to the pre-fix run and to the fixer's claim, and to my own separate run of `examples/validate_poses.py` below.

### Input 3 — Edge: clash / stretched-bond / puckered-ring poses

Ran `input3_edge_bad_poses.py` unchanged:

```
=== clash_pose.sdf (dock config, vs receptor) ===
pb_valid: False | failed checks: ['minimum_distance_to_protein', 'volume_overlap_with_protein']

=== stretched_bond.sdf (mol config, ligand-only) ===
pb_valid: False | failed checks: ['bond_lengths', 'bond_angles']

=== puckered_ring.sdf (mol config, ligand-only) ===
pb_valid: True | failed checks: []

=== control: good pose (mode1_fixed.sdf) under mol config, should pass everything ===
pb_valid: True
```

Identical to the pre-fix run. The assertion that FAILED pre-fix ("SKILL.md's 0.25 Å cutoff matches the real threshold") is retired — the fix removed that hard-cutoff claim. The replacement assertion ("the corrected, hedged guidance matches real behavior") PASSES: `puckered_ring.sdf` (0.6 Å raw ring-atom displacement, ~0.289 Å by the Skill's own formula) still passes `aromatic_ring_flatness`, consistent with the corrected bracket and squarely inconsistent with the old 0.25 Å claim.

### Input 4 — Variant B: redock RMSD/PB-valid reconciliation

Ran `input4_variant_b_redock_rmsd.py` unchanged:

```
pb_valid: True
rmsd_≤_2å: True
stereo checks -- double_bond_stereochemistry: True, tetrahedral_chirality: True
Reconciliation table verdict: RMSD<=2A + PB-valid: physically plausible and close to reference
```

Identical to the pre-fix run. The assertion that FAILED pre-fix ("redock only adds the RMSD column") now PASSES per the corrected table, cross-checked with the same independent `reaudit_dock_vs_redock.py` script used for Input 1.

### Input 5 — Stress: batch pose_qc_pipeline

Ran `input5_stress_batch_pipeline.py` unchanged:

```
Included in PB-valid ranked shortlist: [mode1..mode8]_fixed.sdf (all 8)
Best-scoring PB-valid pose: ../data/mode1_fixed.sdf (Vina -6.106 kcal/mol)
Clash pose excluded from shortlist: True
```

Identical to the pre-fix run.

---

## Independent verification of the fixer's two P1 fixes

**These use different code, and for the planarity claim, different data, than either the original auditor or the fixer.**

### dock vs redock column gap (see Input 1/4 above)

Independently re-derived via `reaudit_dock_vs_redock.py`, not the fixer's or original auditor's script. Result matches the corrected SKILL.md claim exactly (5-column gap: molecular_formula, molecular_bonds, double_bond_stereochemistry, tetrahedral_chirality, RMSD).

### Aromatic planarity cutoff — two independent displacement series

The fixer bisected a 4-point series (steps 0.6/1.0/1.5/2.0 Å) displacing **ring atom index 0** of `mode1_fixed.sdf`'s aromatic ring, finding 0.2888 Å passes and 0.4524 Å fails. I built two of my own series, displacing a **different ring atom (index 2 of the ring tuple, RDKit atom idx 7)**, with different step values:

```
=== reaudit_planarity_series.py (fine series, 0.15-0.46A) ===
  step_A  skill_formula_A  bust_aromatic_ring_flatness
    0.15           0.0741                         True
    0.22           0.1088                         True
    0.30           0.1482                         True
    0.38           0.1870                         True
    0.46           0.2252                         True   <- never fails in this range

=== reaudit_planarity_series2.py (extended series, 0.6-2.2A) ===
  step_A  skill_formula_A  bust_aromatic_ring_flatness
    0.60           0.2901                         True   <- last pass
    0.90           0.4175                        False   <- first fail
    1.20           0.5224                        False
    1.50           0.5971                        False
    1.80           0.6362                        False
    2.20           0.7136                        False
```

**Independently confirmed**: the real pass/fail transition falls between 0.2901 Å (passes) and 0.4175 Å (fails), closely matching the fixer's claimed ~0.29–0.45 Å bracket, using a different perturbed atom and different step sizes. A pose scoring 0.29 Å — right where the old, now-removed 0.25 Å "implausible" cutoff would have flagged it — still genuinely passes the real check. The old claim is confirmed wrong; the new bracket is confirmed right.

### Bundled fixture smoke test

Ran `examples/validate_poses.py` directly (not the fixer's transcript) 3 times in a row:

```
   pose_idx  pb_valid  strain_kcal
0         0      True     4.162648
OK: fixture pose is PB-valid, strain computed successfully.
```

Identical all 3 runs. Deterministic, matches the fixer's claimed exact value (4.162648 kcal/mol) and the original audit's independent run of the same underlying code. Confirmed `examples/fixtures/receptor.pdb` is byte-identical to the original audit's real 3PTB receptor fixture (`diff` clean). This is a real, reproducible smoke test — not a fabricated number.

---

## New Input 6 — chirality-config gap (novel molecule, not used elsewhere in this audit)

**Prompt:** "I docked a chiral fragment blind (no reference structure) and QC'd it with the Skill's 'dock' config — does PoseBusters actually catch a chirality-inverted pose that way, or only under redock?"

Built (R)-1-phenylethanol (`C[C@H](O)c1ccccc1`) as the "reference" and its (S) enantiomer (`C[C@@H](O)c1ccccc1`) as the "docked pose with an inverted stereocenter" — a molecule/chemotype used nowhere else in this audit, the original audit, or the fix log.

```
=== redock config, mol_true = correct (R), mol_pred = inverted (S) ===
tetrahedral_chirality: False                     <- correctly caught

=== dock config, mol_pred = inverted (S) alone, no reference ===
has tetrahedral_chirality column: False          <- structurally cannot be checked

=== mol config, mol_pred = inverted (S) alone ===
has tetrahedral_chirality column: False          <- ALSO cannot be checked
```

3 of 4 assertions PASS: the new caveat's prediction holds on an independent chemotype. The 4th assertion FAILS and is a **new finding**:

> **SKILL.md's `mol` config table row still lists "stereo" among what `mol` includes** — `Intra-ligand only (sanity, bonds, angles, rings, stereo, energy)`. Verified: `PoseBusters(config='mol').bust()` returns 12 columns (`mol_pred_loaded, sanitization, inchi_convertible, all_atoms_connected, no_radicals, bond_lengths, bond_angles, internal_steric_clash, aromatic_ring_flatness, non-aromatic_ring_non-flatness, double_bond_flatness, internal_energy`) — **no `tetrahedral_chirality`, no `double_bond_stereochemistry`**. This directly contradicts the fix's own new caveat sentence three lines above the config table ("Double-bond stereo, chirality... are reference checks: they only run when mol_true is supplied"). `git diff` on the staging commit confirms the `mol` row was untouched by the fix — only the `dock` row and the caveat sentence were corrected.

This is a real, previously-unflagged defect (P2 — a documentation inconsistency, not a code or veto issue).

## New Input 7 — independent aromatic-planarity bisection

Covered above under "Independent verification of the fixer's two P1 fixes." Counted as a distinct dynamic-score input here because it used entirely independent perturbation code/data from both the original audit and the fix.

---

## Redundancy pass check

Diffed `usage-guide.md` pre-fix vs. post-fix (`git diff 0776dc9 cae7409 -- chemoinformatics/pose-validation/usage-guide.md`) against the fix log's claims:

- Prerequisites (`pip install ...`) removed from usage-guide.md — confirmed present instead in SKILL.md's Version Compatibility section.
- Quick Start bullets folded into Example Prompts — confirmed; "Identify chirality-inverted poses in my DiffDock output" now appears as its own Example Prompt ("Chirality/stereo check").
- "What the Agent Will Do" and 4 of 5 Tips deleted — confirmed, and each deleted line is a genuine restatement of SKILL.md content (When-to-Apply table, Strain Energy section, Reconciliation table, Common Errors table).
- The 5th tip ("use PoseBusters as filter, not absolute reject") — confirmed moved, not dropped: it now appears verbatim (reworded) as a new row in SKILL.md's Common Errors table ("Otherwise-reasonable pose rejected on one borderline check").

**Verdict: the redundancy-pass claim is accurate. No content was lost.**

---

## Veto Gates

- **Skill Veto (T1–T4):** PASS, unchanged from the original audit — no stability, contract, determinism, or security issues found.
- **Research Veto (M1–M4):** PASS. No fabricated results; every numeric claim in the fixed SKILL.md was independently re-verified against the real running library; no diagnostic/prescriptive content; strain energy still correctly framed as a diagnostic, not a rigorous free energy; all 7 inputs' code ran to completion.

## Score

```
Static Score   : 90/100  x 40% = 36.0
Dynamic Score   : 93.4/100  x 60% = 56.0
FINAL SCORE    : 92.0 / 100
GRADE          : ⭐ Production Ready
Deployable     : true
Veto override  : false

Floors: Static >=80 (90 ✓) | Execution >=85 (93.4 ✓) | L1 >=32 (37.4 ✓) | L2 >=48 (56.0 ✓) | Assertions >=90% (96.2% ✓)
All Production Ready floors met -- no downgrade.
```

## Recommendation

One open P2 (new finding, see Input 6): the `mol` config table row's "stereo" wording contradicts the fix's own caveat. This does not block landing — no P0, no open P1, no veto, deployable, core well above 85.
