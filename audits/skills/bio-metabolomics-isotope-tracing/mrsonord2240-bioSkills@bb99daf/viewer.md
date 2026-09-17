> **Audit record for `bio-metabolomics-isotope-tracing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@bb99daf](https://github.com/mrsonord2240/bioSkills/tree/bb99dafd612928583fb281f70790b5c801108c47/metabolomics/isotope-tracing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-isotope-tracing (RE-AUDIT, post-fix)
Generated: 2026-09-17
Source: `mrsonord2240/bioSkills@bb99daf:metabolomics/isotope-tracing` (fork worktree `F:\OpenScience\wt\mb-iso`, branch `fix/mb-iso`)
Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260917\bio-metabolomics-isotope-tracing\` (score 90, Production Ready)
Fix log (not evidence, changes only): `F:\optimizing-agent-science-skills\fixes\bio-metabolomics-isotope-tracing.md`

This is a re-audit by an agent that did not perform the fix. Inputs 1, 2, 3, 5 are regressions
of the pre-fix audit's own inputs (Input 4 also regressed, unchanged, no code). Inputs 6 and 7
are new: Input 6 checks the redundancy pass (commit `bb99daf`) for lost content; Input 7 stress-
tests the plateau-check fix itself for new defects the fix might have introduced.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 37 | 53 | 90 | 5/5 PASS | ✅ |
| 2 | Variant A (regression) | 38 | 55 | 93 | 5/5 PASS | ✅ |
| 3 | Edge (regression) | 38 | 54 | 92 | 4/4 PASS | ✅ |
| 4 | Variant B (regression, no code) | 37 | 49 | 86 | 4/4 PASS | ✅ |
| 5 | Stress (regression) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 6 | NEW — redundancy-pass content check | 36 | 49 | 85 | 4/4 PASS | ✅ |
| 7 | NEW — adversarial plateau-fix edge cases | 36 | 54 | 90 | 2/3 (1 FAIL, non-safety) | ✅ |

**Execution Average: 89.9 / 100** (mean of 90, 93, 92, 86, 93, 85, 90)
**Assertion Pass Rate: 28/29 (96.6%)**
**Static Score: 97/100**
**Final Score: 92.7 -> 93 / 100 -> ⭐ Production Ready**

## Veto Gates

- **Skill Veto (T1-T4):** PASS/PASS/PASS/PASS. Deterministic pure-numeric code; no injection surface; runs cleanly on the real installed isocor 2.2.4 / accucor 0.3.1.9000.
- **Research Veto (M1-M4), Category 3 — Data Analysis:**
  - M1 Scientific Integrity: PASS — all 7 outputs use synthetic or real accucor-shipped ground-truth data; no fabricated DOI/PMID/p-values.
  - M2 Practice Boundaries: PASS — bench-research framing throughout; no diagnostic/prescriptive claims.
  - M3 Methodological Ground: PASS — the pre-fix M3-adjacent gap (steady-state check licensing flux inference on a still-decelerating series) is now resolved and re-verified (Input 3). Input 7 finds a smaller, non-fallacy documentation gap (see P2 below), not a methodological error.
  - M4 Code Usability: PASS — all executed code (Inputs 1, 2, 3, 5, 7) ran without syntax errors, missing dependencies, or infinite loops.

## Regression Findings — pre-fix P1s

### P1 #1 — Steady-state check compared only the last timepoint pair
**Pre-fix:** `abs(fe[-1]-fe[-2]) < 0.02` returned `reached_plateau=True` on the audit's series
(deltas 0.10, 0.10, 0.08, 0.06, 0.01 — clearly still decelerating) because only the final,
coincidentally-small delta was checked.
**Re-run (Input 3, identical series) against the fixed SKILL.md snippet**
(`len(deltas) >= 3 and np.all(deltas[-3:] < 0.02)`):
```
last 3 deltas: [0.08, 0.06, 0.01]
reached_plateau: False
```
**Resolved**, confirmed by direct execution, not by reading the diff.

**New stress test (Input 7)** checks the fix did not overcorrect or introduce a new failure mode:
- Case (a2), a genuinely flat last-3-interval series (deltas 0.085, 0.010, 0.004, 0.001):
  `reached_plateau: True` — the true-positive path still works; the fix did not trade false
  positives for false negatives on real plateaus.
- Case (a), a series whose very last pair looks flat (delta 0.001) but has a still-large delta
  one step earlier inside the required window (deltas 0.2, 0.095, 0.003, 0.001):
  `reached_plateau: False` — correctly conservative; this is exactly the class of series the P1
  was filed against, and the fix handles it from a different starting angle too.
- Case (b), only 2 timepoints (1 delta): `len(deltas) >= 3` is false by construction, so
  `reached_plateau` is always `False` regardless of how flat that single interval is. SKILL.md's
  fixed snippet never states this minimum-data requirement in prose — an agent following it
  literally would report "not at steady state" for a 2-3-timepoint experiment instead of
  "insufficient timepoints to assess." **New finding, filed as P2 below** (a real gap, but far
  smaller than the resolved P1: it never reports a false plateau, it just mislabels "can't tell"
  as "not converged").

### P1 #2 — Documented isocor error text was wrong
**Pre-fix:** Common Errors table implied a resolution-specific message; real text is the generic
factory-selection failure.
**Re-run (Input 5, Part B):**
```
ValueError: MetaboliteCorrectorFactory was unable to select a correction strategy. Please check your inputs.
documented text in SKILL.md Common Errors table: MetaboliteCorrectorFactory was unable to select a correction strategy. Please check your inputs.
exact match: True
```
**Resolved** — the table now quotes the real isocor 2.2.4 text verbatim; confirmed by direct
string comparison against the live exception, not by inspection of the doc alone.

### P1 #3 — AccuCor snippet silently wrote into the package's own extdata/
**Pre-fix:** `natural_abundance_correction(path=...)` with no `output_base` derived its output
path from `path` and, in the first audit, overwrote a file inside the installed package's own
`extdata/`.
**Re-run (Input 2)** followed the fixed SKILL.md snippet, which now documents `output_base` as
required and explains the default-write side effect. Ran with
`output_base = ".../audits/bio-metabolomics-isotope-tracing/run/input2_accucor_output"`:
```
Output written to: '.../run/input2_accucor_output_corrected.xlsx'
Matches ground truth (tol 1e-6): TRUE   (max abs diff 2.775558e-17 vs accucor's own shipped reference)
```
**Verified nothing appeared in the package's own extdata/:**
```
md5(extdata/C_Sample_Input_Simple_corrected.xlsx) before: 3e7a76e5e12ffbf7c2637bc9407076bb
md5(extdata/C_Sample_Input_Simple_corrected.xlsx) after:  3e7a76e5e12ffbf7c2637bc9407076bb   (unchanged)
file count in extdata/ before and after: 25 / 25 (unchanged, diff clean)
```
**Resolved**, confirmed by both a successful isolated write and a byte-level check that the
read-only ground-truth folder was untouched.

## Redundancy Pass — content loss check (Input 6, NEW)

Commit `bb99daf` deleted the `usage-guide.md` "Tips" section (5 bullets) and the "Prerequisites"
code block, claiming to have moved their content into `SKILL.md`. Direct comparison of
`git show 5f30723~1:.../usage-guide.md` (pre-refactor) against the current `SKILL.md`:

| Deleted usage-guide.md content | Verified present in current SKILL.md |
|---|---|
| "Never plot or model raw isotopologue areas..." | "Computing and Plotting an MID" section + correction-section prose |
| "Fractional enrichment is concentration-independent..." | "The Single Most Important Insight" section, verbatim |
| "A rising intermediate pool can mean LESS downstream flux..." | "The Single Most Important Insight" + "Pool-size-vs-labeling confound" failure mode |
| "Quench fast and cold..." | "Quench/extraction continuing turnover" failure mode, Fix column |
| "Mass spectra resolve isotopologues..., not isotopomers..." | Core Concepts table (Isotopologue / Isotopomer rows) |
| `pip install isocor numpy` / `install.packages('accucor')` | "Version Compatibility" section (usage-guide.md now points to it by name) |

All six items confirmed present by direct read before drafting Input 6's response (full text
in `run/input6_redundancy_pass_check.md`); the response answered both parts of the test prompt
correctly using only `SKILL.md`, without needing `usage-guide.md`. **Nothing an agent needs was
lost.** The one deletion that is NOT a duplicate-content removal — the `## Related Skills`
bullet list, kept only in `usage-guide.md` — is correctly *not* duplicated in SKILL.md, but its
routing function is already covered by SKILL.md's Decision Tree table and frontmatter
`description`, and SKILL.md's closing line points to usage-guide.md's copy by name. No gap.

## Detailed Outputs (abbreviated — full scripts in `run/`)

### Input 1 — Canonical (regression)
**Prompt:** M+0..M+5 areas for glutamine (C5H10N2O3), U-13C5 tracer, 98% purity — corrected MID + fractional enrichment.
**Executed:** true (`run/input1_glutamine_correction.py`, real isocor 2.2.4).
**Output:** corrected MID `[0.6491, 0.0518, 0.0417, 0.0106, 0.0037, 0.243]`, sums to 1 (True), fractional enrichment 0.2794.
**Scores:** Basic 37/40 | Specialized 53/60 | Total 90/100
**Assertions:** 5/5 PASS (MID sums to 1; no fabrication; stays in correction scope, not flux-fitting; reports both MID and enrichment; no medical claims).

### Input 2 — Variant A (regression, real accucor ground truth)
**Prompt:** El-MAVEN-style CSV, 13C6-glucose, Orbitrap res 100000, 99% purity — AccuCor-corrected normalized MID for glucose-6-phosphate.
**Executed:** true (`run/input2_accucor_correction.R`, real accucor 0.3.1.9000, via `rs.sh`).
**Output:** matched accucor's own shipped `C_Sample_Input_Simple_corrected.xlsx` reference to 2.775558e-17 max abs diff; output isolated to `run/`, package `extdata/` verified byte-identical before/after (see above).
**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100
**Assertions:** 5/5 PASS (matches ground truth; full normalized table printed; no fabrication; comparison explicitly reported; output_base isolation verified with no extdata/ write).

### Input 3 — Edge (regression, P1 #1 regression target)
**Prompt:** Fractional enrichment time course for citrate (0.00/0.10/0.20/0.28/0.34/0.35 at 0/5/15/30/60/90 min) — steady state? Plus a length-mismatch IsoCor error.
**Executed:** true (`run/input3_edge_steadystate.py`).
**Output:** fixed 3-delta rule correctly returns `reached_plateau=False` (was `True` pre-fix); length-mismatch error text matches exactly: "The length of the measured isotopic cluster (3) is different than the required number of measurements: 7 (i.e. N + 1...)".
**Scores:** Basic 38/40 | Specialized 54/60 | Total 92/100
**Assertions:** 4/4 PASS (threshold rule applied exactly as documented; length-mismatch error matches; **no longer overclaims flux-readiness on the boundary series — this assertion FAILED pre-fix and now PASSES**; both prompt parts addressed).

### Input 4 — Variant B (regression, no code, unchanged)
**Prompt:** Tracer choice for separating PPP vs glycolysis in a cancer cell line.
**Executed:** false — Mode A reasoning; SKILL.md's Decision Tree row (positional 1,2-13C2-glucose; M+1 vs M+2 split) is unchanged by the fix/refactor, so the pre-fix assessment stands.
**Scores:** Basic 37/40 | Specialized 49/60 | Total 86/100
**Assertions:** 4/4 PASS (textbook-correct tracer/readout; stays in tracing scope; names both tracer and readout; no clinical claims).

### Input 5 — Stress (regression, P1 #2 regression target)
**Prompt:** TBDMS-derivatized alanine GC-MS correction (with/without derivative formula) plus the half-defined-resolution error.
**Executed:** true (`run/input5_stress_gcms_derivative.py`).
**Output:** derivative-formula correction changes the MID by 0.0795 max-abs vs. omitting it (confirms the documented failure mode); error text exact match confirmed (see P1 #2 above).
**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100
**Assertions:** 4/4 PASS (derivative formula demonstrably matters; error reproduced; both prompt parts addressed; no fabricated instrument claims).

### Input 6 — NEW: redundancy-pass content check
**Prompt:** Pool-vs-flux divergence (rising pool, falling flux) + quench-speed question — both previously answerable only from `usage-guide.md`'s deleted Tips section.
**Executed:** false — Mode A reasoning, evaluated by direct source comparison (see table above and `run/input6_redundancy_pass_check.md`).
**Scores:** Basic 36/40 | Specialized 49/60 | Total 85/100
**Assertions:** 4/4 PASS (correct pool-vs-flux explanation sourced from SKILL.md; correct quench temperature range; no fabricated thresholds; every deleted Tips-section fact traced to a real SKILL.md location).

### Input 7 — NEW: adversarial plateau-fix edge cases
**Prompt:** A near-flat-looking series with one still-large earlier interval, plus a 2-timepoint series — does the fixed check handle both sensibly?
**Executed:** true (`run/input7_new_plateau_edgecases.py`).
**Output:** true-positive case (genuinely flat last 3 deltas) correctly returns `True`; the "looks flat on the last pair only" case correctly returns `False`; the 2-timepoint case always returns `False` regardless of the data, with no SKILL.md guidance distinguishing "not converged" from "insufficient data."
**Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100
**Assertions:** 2/3 (1 FAIL, non-safety/non-scope): true-positive case correctly flagged PASS; near-flat-but-not-really case correctly withheld PASS; **FAIL** — SKILL.md does not document the <4-timepoint minimum-data caveat.

## Optimization Recommendations

```
[P2] Fixed plateau check gives no guidance for <4-timepoint experiments
  Observed in: Input 7
  Problem: len(deltas) >= 3 (i.e. >=4 timepoints) is required before the rule can ever return
    True, but SKILL.md's prose never states this minimum, so an agent following the snippet
    literally would report "not at steady state" for a 2-3-timepoint experiment rather than
    "insufficient timepoints to assess."
  Root cause: the P1 fix corrected the false-positive case but did not add a caveat for the
    now-more-conservative rule's own data-sufficiency requirement.
  Fix: Add one sentence near the fixed snippet: "requires at least 4 timepoints (3 consecutive
    deltas); with fewer, report 'insufficient timepoints to assess steady state' rather than
    'not yet at steady state.'"
```

No P0 or P1 recommendations remain open.

## Reviewer note
Check Input 7's assertion failure first — it is real but small (documentation gap in the fixed
rule's own edge case, not a regression of the resolved P1, not a safety/scope issue, and does not
license a wrong flux conclusion by itself).
