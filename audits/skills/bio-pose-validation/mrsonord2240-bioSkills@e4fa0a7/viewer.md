> **Audit record for `bio-pose-validation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@e4fa0a7](https://github.com/mrsonord2240/bioSkills/tree/e4fa0a78b55a107b91337a3307faebf34a70644d/chemoinformatics/pose-validation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pose-validation

## Canonical final summary

**Final:** 95/100 — ⭐ Production Ready; deployable: true.

Source: `mrsonord2240/bioSkills@e4fa0a78b55a107b91337a3307faebf34a70644d:chemoinformatics/pose-validation`
Auditor independent: `false`
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

Generated: 2026-09-23

Source audited: `mrsonord2240/bioSkills@e4fa0a78b55a107b91337a3307faebf34a70644d:chemoinformatics/pose-validation`

Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst` — PoseBusters 0.6.5, RDKit 2026.03.6, pandas 3.0.5.

Final-pass exception: `meta.auditor_independent` is `false`; note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

The prior report and its data/run artifacts were preserved before this audit at `F:\OpenScience\audits\_pre-fix-20260922\bio-pose-validation\`. The source worktree was read-only and remained at the assigned tip.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Executed | Status |
|---|---|---:|---:|---:|---:|---|---|
| 1 | Canonical | 39 | 58 | 97 | 3/3 | Yes | ✅ |
| 2 | Variant A | 38 | 57 | 95 | 3/3 | Yes | ✅ |
| 3 | Edge | 39 | 57 | 96 | 4/4 | Yes | ✅ |
| 4 | Variant B | 39 | 57 | 96 | 3/3 | Yes | ✅ |
| 5 | Stress | 38 | 57 | 95 | 3/3 | Yes | ✅ |
| 6 | Edge | 38 | 57 | 95 | 4/4 | Yes | ✅ |
| 7 | Variant B | 39 | 57 | 96 | 4/4 | Yes | ✅ |
| 8 | Stress (fresh) | 39 | 57 | 96 | 3/3 | Yes | ✅ |
| 9 | Adversarial (fresh) | 37 | 54 | 91 | 3/3 | Yes | ✅ |

**Execution average:** 95.2 / 100
**Assertions:** 30 / 30 PASS

## Execution evidence

The audit-owned script [phase2_replay.py](run/phase2_replay.py) executed all inputs and asserted the outputs. It uses an exact byte-identical audit snapshot of each shipped Python file so Python import caching cannot write to the source worktree. Full console evidence is in [phase2_replay_output.txt](run/phase2_replay_output.txt).

```text
INPUT 1 PASS: dock bool_checks=22 pb_valid=True
INPUT 2 PASS: fixture __main__ and strain_kcal=4.162648 note=ok
INPUT 3 PASS: clash=[minimum_distance_to_protein, volume_overlap_with_protein];
              stretched=[bond_lengths, bond_angles]; puckered=True; control=True
INPUT 4 PASS: RMSD<=2 A=True pb_valid=True
INPUT 5 PASS: 8 valid Vina modes retained; clash excluded
INPUT 6 PASS: redock catches R/S inversion; dock/mol omit reference stereo checks
INPUT 7 PASS: 0.2888 A passes; 0.4524/0.5926/0.6575 A fail flatness
INPUT 8 PASS: fresh three-pose SDF retains the first PB-valid record
INPUT 9 PASS: fresh malformed SDF returns note=parse_fail, not a crash
ALL ASSERTIONS PASS: 9/9 inputs completed
```

The deliberate malformed-SDF input emitted RDKit's parse diagnostic. This was expected and was checked: the public function returned one row with `note=parse_fail` and null strain rather than claiming a numeric result or throwing.

## Detailed inputs

### Input 1 — canonical dock QC (executed)

Prompt: Run `dock` QC for a real Vina benzamidine pose against 3PTB and filter to PB-valid.

Output: 22 boolean checks, all true; PB-valid is true.

- PASS — documented boolean aggregation ran on the supplied SDF/PDB pair.
- PASS — the installed `dock` configuration returned 22 boolean checks.
- PASS — the positive-control pose was PB-valid.

### Input 2 — strain and example fixture (executed)

Prompt: Quantify relative MMFF94 strain for the docked pose and verify the shipped example can run.

Output: the actual `examples/validate_poses.py` main path printed its asserted fixture-success line. `ligand_strain_mmff(mode1_fixed.sdf)` returned `strain_kcal=4.162648`, `note=ok`.

- PASS — fixture smoke test completed.
- PASS — strain returned a structured score row.
- PASS — strain matches the regression value within 0.001 kcal/mol.

### Input 3 — physical-failure edge cases (executed)

Prompt: Differentiate a receptor clash, a stretched bond, a puckered ring, and a good control.

Output: clash failed `minimum_distance_to_protein` and `volume_overlap_with_protein`; stretched bond failed `bond_lengths` and `bond_angles`; puckered and control poses were PB-valid.

- PASS — protein clash rejected.
- PASS — bond geometry failure rejected.
- PASS — puckered regression pose has the documented authoritative-check result.
- PASS — unperturbed control passes.

### Input 4 — redock reconciliation (executed)

Prompt: Compare a redocked pose with real `mol_true`, reporting RMSD and PB-valid.

Output: RMSD <= 2 A is true, PB-valid is true, and both reference stereochemistry checks are true.

- PASS — redock completed with a reference ligand.
- PASS — it occupies the Yes/Yes reconciliation quadrant.
- PASS — reference-dependent stereo checks passed for the control.

### Input 5 — nine-file batch regression (executed)

Prompt: Execute the documented batch CLI over eight real Vina modes plus a deliberately clashing file.

Output: the shipped CLI printed `8 / 9 files have a PB-valid pose`; callable output retained the eight modes and excluded the clash.

- PASS — CLI syntax in SKILL.md executed.
- PASS — all valid Vina sources retained.
- PASS — clash source excluded.

### Input 6 — stereochemistry config boundary (executed)

Prompt: Test whether a blind `dock`/`mol` check can detect an R/S inversion.

Output: `redock` returned `tetrahedral_chirality=False`; `dock` and `mol` both lacked reference stereo columns. The current `mol` table correctly says stereo/chirality need `mol_true`.

- PASS — redock detected the inversion.
- PASS — dock omitted the unavailable reference check.
- PASS — mol omitted both reference stereo checks.
- PASS — current table wording matches live columns.

### Input 7 — planarity regression series (executed)

Prompt: Run the shipped supplementary planarity script and compare its diagnostic values to PoseBusters.

Output: 0.6 displacement -> 0.2888 A and passes; 1.0 -> 0.4524 A and fails; 1.5 -> 0.5926 A and fails; 2.0 -> 0.6575 A and fails.

- PASS — all four documented script invocations completed.
- PASS — pass-side diagnostic value reproduced.
- PASS — fail-side diagnostic value reproduced.
- PASS — later stronger perturbations failed the authoritative check.

### Input 8 — fresh multi-pose selection (executed)

Prompt: Validate a new file whose first record is invalid and next two records are valid.

Output: raw PB flags were `[False, True, True]`; the shipped batch function returned exactly one result, the first valid record (index 1).

- PASS — audit-owned multi-pose input has the intended boundary composition.
- PASS — batch processing returns one source-level selection.
- PASS — selection is first PB-valid, not last valid.

### Input 9 — fresh malformed SDF (executed)

Prompt: Request strain calculation for a malformed SDF and verify no false numeric result is produced.

Output: RDKit reported a parse error; `ligand_strain_mmff` returned `pose_idx=0`, `note=parse_fail`, and null `strain_kcal`.

- PASS — malformed input is preserved as an output row.
- PASS — failure is labelled `parse_fail`.
- PASS — no numeric strain is invented.

## Gates and final score

- Skill Veto T1–T4: PASS.
- Research Veto M1–M4: PASS.
- Static score: 94 / 100.
- Dynamic score: 95.2 / 100.

```text
94 x 0.4 = 37.6
95.2 x 0.6 = 57.1
Final = 94.7 -> 95 / 100
Grade = Production Ready
Deployable = true
Veto override = false
```

Production floors pass: static >= 80, execution >= 85, Layer 1 average 38.4 >= 32, Layer 2 average 56.8 >= 48, assertions 100% >= 90.

## Recommendation

P2 — `pose_qc_batch.py` exposes `rank` as a cumulative count of PB-valid records within a file, rather than a docking score or original pose ordinal. Rename it `valid_ordinal` or omit it from the CLI display; this does not affect the verified first-PB-valid selection behavior.

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@e4fa0a78b55a107b91337a3307faebf34a70644d:chemoinformatics/pose-validation`
- `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`
