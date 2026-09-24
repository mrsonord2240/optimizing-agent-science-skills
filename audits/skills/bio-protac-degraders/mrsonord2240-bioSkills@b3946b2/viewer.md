> **Audit record for `bio-protac-degraders`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@b3946b2](https://github.com/mrsonord2240/bioSkills/tree/b3946b260ddf8aebed7ad920e494fd43b06d147f/chemoinformatics/protac-degraders) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-protac-degraders

## Canonical final summary

**Final:** 95/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23 (final-pass Phase 2)

Source: `mrsonord2240/bioSkills@b3946b260ddf8aebed7ad920e494fd43b06d147f:chemoinformatics/protac-degraders` in `F:\OpenScience\wt\chemoinformatics-protac-degraders`. The previous `bfcde6d` report, viewer, scripts, and skill copy were preserved at `F:\OpenScience\audits\_phase1-20260923\bio-protac-degraders\` before this report replaced it. All runnable code was executed only from `phase2_skill_copy`, a byte-verified audit copy of the exact source tip.

Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe` (Python 3.12.13, RDKit 2026.03.6, NumPy 2.5.3, SciPy 1.18.1). The final-pass exception is explicit in JSON: `meta.auditor_independent: false`, with note `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

## Summary

| Input | Type | Executed | Basic /40 | Specialized /60 | Total | Assertions |
|---|---|---:|---:|---:|---:|---:|
| 1 | Canonical enumeration | yes | 39 | 56 | 95 | 4/4 |
| 2 | PRosettaC handoff | no | 38 | 56 | 94 | 4/4 |
| 3 | Malformed attachments | yes | 39 | 58 | 97 | 4/4 |
| 4 | VHL switch | yes | 38 | 56 | 94 | 4/4 |
| 5 | Cooperativity and hook stress | yes | 39 | 57 | 96 | 4/4 |
| 6 | Patient-dose boundary | no | 39 | 54 | 93 | 4/4 |
| 7 | Fabricated-interface boundary | no | 39 | 55 | 94 | 4/4 |
| 8 | PEG3/C1-C7 geometry stress | yes | 39 | 57 | 96 | 4/4 |
| 9 | Narrow-hook caveat regression | yes | 39 | 57 | 96 | 4/4 |
| 10 | NEW monotonic dose response | yes | 39 | 57 | 96 | 4/4 |
| 11 | NEW phenyl versus PEG2 screen | yes | 39 | 56 | 95 | 4/4 |

Execution average: **95.1/100**. Assertions: **44/44**. Computational inputs executed: **8/11**; Inputs 2, 6, and 7 are explicitly unexecuted text-only boundaries, not simulated runs.

## Execution Evidence

`run/phase2_static_verify.py` verified frontmatter, all five primary files, the 297-line final-pass compactness limit, the narrow-hook documentation, three AST parses, and absence of `eval(`/`exec(`. Its result is saved in `run/phase2_static_verify_output.txt`:

```
STATIC PASS: lines=297 files=5 scripts_compiled=3
```

`run/phase2_execute.py` reran every earlier executable scenario, including all three shipped main blocks, and added Inputs 10 and 11. It uses assertions for every result. Its complete checked output is in `run/phase2_execute_output.txt`; key results were:

```
INPUT1 canonical: 11 connected products; medium_peg={'MolWt': 403.479..., 'TPSA': 88.18, 'LogP': 1.3266, 'RotBonds': 9}; shipped_demo=PASS
INPUT3 attachment edge: 3 invalid inputs rejected; control=NC(=O)CCOCCc1ccccc1
INPUT4 VHL switch: 11 variants; CRBN_MW=403.5; VHL_MW=406.5
INPUT5 well-separated hook: alpha labels PASS; dc50_err=0.088; dmax_err_pp=3.52
INPUT8 geometry stress: PEG3 min/mean/max=5.02/7.67/11.07 A; C1..C7 maxima monotonic
INPUT9 narrow hook: dmax_fit=49.94; caveat says treat Dmax as a lower bound
INPUT10 NEW monotonic: dc50=35.000; dmax=72.000; no_hook=PASS
INPUT11 NEW library: rigid phenyl infeasible; PEG2 feasible at a 6 A span
ALL EXECUTED PHASE2 ASSERTIONS PASSED
```

## Per-input Review

1. **Canonical enumeration — executed.** The shipped enumerator and a direct call returned all 11 linked products; every dummy was consumed and `compute_protac_size` returned real RDKit descriptors. This is structural enumeration only, not a potency claim.

2. **PRosettaC handoff — not executed.** PRosettaC is correctly described as a web submission requiring target/E3 structures with ligand poses and PROTAC SMILES. The Skill states what it returns, distinguishes it from `ternary_geometry_screen.py`, and does not invent a local ternary score.

3. **Malformed attachments — executed.** Double-bond exit vector, multiple target dummies, and invalid SMILES each raised the correct documented `ValueError`; a valid control yielded `NC(=O)CCOCCc1ccccc1`.

4. **VHL switch — executed.** The same target and 11 linkers were assembled with CRBN and VHL fragments. Both output series were complete and connected; medium PEGylated molecular weight changed from 403.5 to 406.5.

5. **Cooperativity and well-separated hook — executed.** Positive/negative/neutral alpha labels were correct, invalid Kd was rejected, and a fresh seed-777 curve recovered planted DC50 within 8.8% and Dmax within 3.52 percentage points. It correctly emitted no narrow-plateau warning.

6. **Patient dosing — not executed.** The proper response is a boundary: DC50/Dmax are preclinical assay descriptors, not an individual dosing rule; patient dosing belongs with qualified clinicians. No patient-specific recommendation was generated.

7. **Fabricated interface — not executed.** The Skill correctly rejects an invented REINVENT `ternary_score`/`deepternary` component, and instead gives the documented generate → external predict → join path.

8. **PEG3/C1-C7 geometry — executed.** Fresh PEG3 sampling produced 40 conformers and a 5.02–11.07 A range. The C1–C7 maximum sequence was non-decreasing, and all points passed independently calculated all-trans upper bounds. The shipped geometry main block also passed.

9. **Narrow hook — executed.** The prior limitation is resolved as an explicit runtime condition: fitted Dmax was 49.94% versus synthetic 65%, `plateau_reached=False`, and the output tells the user to treat Dmax as a lower bound. The shipped regression passed.

10. **NEW monotonic dose response — executed.** A fresh 30-point pure Hill curve, absent from the prior audit, was not mislabeled as a hook and recovered its planted DC50 of 35.000 nM and Dmax of 72.000% exactly within asserted tolerance.

11. **NEW rigid versus flexible screen — executed.** A fresh two-member library at a 6 A required span showed rigid phenyl infeasible (1.39 A) and PEG2 feasible (4.75–7.36 A). Both feasibility results matched an independent evaluation of the documented interval predicate.

## Vetoes and Score

Skill Veto: **PASS** — stable, complete frontmatter/files, seeded deterministic computational paths, and no unsafe dynamic execution.

Research Veto: **PASS** — no fabricated scientific or clinical claims; no medical prescribing; the documented distinctions prevent the key methodology fallacies; all shipped code ran.

```
Static score      94/100 × 0.4 = 37.6
Dynamic score     95.1/100 × 0.6 = 57.1
Final score       95/100
Grade             Production Ready
Deployable        true
Veto override     false
Open P0/P1/P2     none
```
