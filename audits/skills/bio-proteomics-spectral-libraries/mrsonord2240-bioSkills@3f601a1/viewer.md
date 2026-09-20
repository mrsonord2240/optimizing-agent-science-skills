> **Audit record for `bio-proteomics-spectral-libraries`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@3f601a1](https://github.com/mrsonord2240/bioSkills/tree/3f601a1a50af8c52724edd5393938e2bda44cd79/proteomics/spectral-libraries) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-spectral-libraries (RE-AUDIT)
Generated: 2026-09-19
Audit kind: re-audit, after fix `fix/pt-speclib` @ `3f601a1` (fork `mrsonord2240/bioSkills`)
Prior audit: 87, Production Ready (archived at `F:/OpenScience/audits/_pre-fix-20260919/bio-proteomics-spectral-libraries/`)
Fix log: `F:/optimizing-agent-science-skills/fixes/bio-proteomics-spectral-libraries.md`
Auditor: independent re-auditor (not the original auditor, not the fixer)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 2 | Variant A (re-audited, fresh peptides) | 36 | 54 | 90 | 4/4 PASS | ✅ |
| 3 | Edge (regression) | 36 | 53 | 89 | 4/4 PASS | ✅ |
| 4 | Variant B (re-audited, fresh peptide pair) | 35 | 52 | 87 | 4/5 PASS | ✅ |
| 5 | Stress (regression) | 38 | 57 | 95 | 4/4 PASS | ✅ |

**Execution Average: 91.0 / 100** (was 83.6)
**Assertion Pass Rate: 21/22** (was 19/22)

**Static score: 96/100** (was 92/100) · **Final score: 93** (was 87) · **Grade: Production Ready ⭐** (unchanged tier, improved score)

## Method

Per `AUDIT_BRIEF.md`'s re-audit rules: re-ran the 3 unaffected inputs (1, 3, 5) as regression
tests against the live public Koina server to confirm the fix touched nothing else; independently
re-verified all 4 fixed findings using **fresh data the fixer did not use** (different peptides,
a genuinely empty ms2pip model_dir, a fresh DeepLC calibration/prediction set); and added new
inputs of my own — repeated-run determinism testing (5x each for shuffle/reverse/pseudo-reverse)
and a from-scratch OpenSWATH TSV build — that surfaced two findings the fix did not fully close.

All code was executed, not just inspected. Full scripts are in `run/`, data in `data/`.

## Detailed Outputs

### Input 1 — Canonical (regression re-run)
**Prompt:** "Predict fragment intensities for LGGNEQVTR via Koina Prosit and calibrate its iRT."
**Output:** Re-ran the fixer's/original auditor's exact SKILL.md-documented pattern against the
live Koina server. `Koina('Prosit_2019_intensity', ...).predict(inputs)` returned 5 annotated
fragments (y1+1 … b3+1) with real m/z. iRT calibration via `scipy.stats.linregress` on synthetic
anchors gave R^2=1.000.
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:** 5/5 PASS — unchanged from the pre-fix audit; this code path was not touched by
the fix.

### Input 2 — Variant A (re-audited, fresh peptides/model dirs)
**Prompt:** "Predict fragment intensities and RT locally with MS2PIP and DeepLC, no Koina/network
dependency."
**Output (DeepLC):**
```
from psm_utils import PSM, PSMList
import deeplc
cal_psms = PSMList(...)   # 11 CiRT peptides (TASEFDSAIAQDK, SNAQLIVK, ... VLDSVTLQLK),
                          # a DIFFERENT calibration set from the fix's own IRT_PEPTIDES verification
pred_psms = PSMList(...)  # LGGNEQVTR, GTFIIDPGGVIR, DGLDAASYYAPVR — held out, not in calibration set
result = deeplc.predict_and_calibrate(pred_psms, psm_list_reference=cal_psms)
# -> array([15.29, 93.98, 22.91])
```
Confirmed `dir(deeplc)` has no `DeepLC` attribute in this venv (deeplc 4.5.0) — the module-level
API is the only one available, matching the fix.

**Output (MS2PIP):** `~/.ms2pip` already held cached HCD2021 model files: 66,684,707 +
850,608,128 bytes = 917.3 MB total, matching the fix's "~915MB" claim closely. With those files
cached, `ms2pip.predict_batch(psms, model='HCD')` completed in 2.0s. With a genuinely empty
`model_dir`, `ms2pip.predict_batch(psms, model='HCD2019', model_dir=...)` downloaded 8,540,238 +
8,916,224 bytes = 17.4 MB (matching the fix's "~17MB" claim) and completed in 13-17s, returning
real per-fragment `ProcessingResult` objects.
**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100 (was 66/100, PARTIAL)
**Assertions:** 4/4 PASS — both the previously-hanging ms2pip call and the previously-broken
deeplc snippet now complete correctly via the documented paths, independently confirmed on data
the fixer did not use.

### Input 3 — Edge (regression re-run)
**Prompt:** "Scan candidate NCE values against a reference spectrum, and predict fragments for a
peptide with an invalid residue and an absurdly long peptide."
**Output:** NCE scan 20-40 against Koina; best NCE=40 (corr=0.740), matching the pre-fix audit's
result exactly. Edge case (`LGGNEQVTRX`, `K*60`) raised `InferenceServerException`, caught
cleanly, not silently returned as zeros.
**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:** 4/4 PASS — unchanged; not touched by the fix.

### Input 4 — Variant B (re-audited, fresh peptide pair: YILAGVENSK / TPVISGGPYEYR)
**Prompt:** "Convert this OpenSWATH transition list to TraML and generate decoys."
**Output:**
```
# placeholder ProductMz (400-410 range) + blank Annotation:
Number of target peptides: 2
Number of decoy peptides: 0
Error: ... below the threshold of 80.0%

# real y-ion m/z (pyteomics.mass.fast_mass) + literal Annotation (y1^1..y6^1):
Number of target peptides: 2
Number of decoy peptides: 2   <- success, matches the fix's documented requirement exactly
```
Determinism (5 repeated runs each, `-threads 1`, md5-compared):
- `pseudo-reverse`: 5/5 identical md5 — fully deterministic, confirmed independently.
- `reverse`: 4/5 identical md5; run 4 differed by a last-ULP float value
  (`669.838062918220999` vs `...221112`) in an "isolation window target m/z" metadata field only
  — not the decoy peptide sequence or fragment m/z used for scoring. **This is new information
  the fix did not have**: its own verification diffed only 2 runs each and found reverse
  byte-identical; a 1-in-5 intermittent difference was not caught at that sample size.
- `shuffle`: differs every run (peptide sequences themselves change), matching the fix's finding.
- `shift`: still rejects every peptide as a duplicate, matching the fix's documented limitation.

**New finding (not in the fix log):** the fixer's `input4_library.tsv` includes a
`transition_group_id` column; my from-scratch TSV omitted it. Without it, `TargetedFileConverter`
silently merged both distinct peptides (which shared `PrecursorCharge=2`) into a single
`<Peptide id="_2">` group — `Number of target peptides: 1` instead of 2 — with no error at any
stage. This is not documented anywhere in the Skill and is a more severe failure mode than the
now-fixed 0-decoy case, because it produces no error and no signal that anything is wrong.
**Scores:** Basic: 35/40 | Specialized: 52/60 | Total: 87/100 (was 74/100)
**Assertions:** 4/5 PASS — the core fix holds; the "fields are fully documented" assertion still
fails because of the `transition_group_id` gap above.

### Input 5 — Stress (regression re-run)
**Prompt:** "Calibrate RT using CiRT peptides (no iRT spike-in) with LOWESS for a nonlinear
gradient, then give me a QC report."
**Output:** Linear fit R^2=0.986, residual SS 10.9098; LOWESS residual SS 0.2054 — LOWESS reduces
residual SS by >50x, exactly matching the pre-fix audit. QC report: precursors 4, proteins 3,
rows 4.
**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:** 4/4 PASS — unchanged; not touched by the fix.

## Veto Gates

- **Skill Veto (T1-T4): PASS.** T3 (determinism) given special attention per this re-audit's
  brief: the shuffle-decoy non-determinism is now correctly documented as expected tool behavior
  rather than an undisclosed defect, and the recommended replacement (`pseudo-reverse`) is
  confirmed genuinely deterministic across 5 independent runs. The reverse-method float-noise
  finding above is real but affects only a non-scored metadata field at ~1e-10 relative
  magnitude — far below any mass-spec decision threshold (ppm-level, ~1e-6) — so it does not rise
  to "critical numerical results fluctuate randomly."
- **Research Veto (M1-M4): PASS.** No fabricated citations/statistics; no clinical scope;
  methodological claims (LOWESS vs linear, decoy requirements) independently re-verified; all
  generated code executed successfully on fresh test data.

> **Note for reviewer:** The one ⚠️-worthy item is Input 4's still-open `transition_group_id` gap
> (filed as a new P1) — a documentation gap, not a runtime failure of anything the fix touched.
