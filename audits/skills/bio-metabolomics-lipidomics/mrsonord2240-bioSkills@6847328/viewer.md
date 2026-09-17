> **Audit record for `bio-metabolomics-lipidomics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/metabolomics/lipidomics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-lipidomics (RE-AUDIT, post-fix)
Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@6847328:metabolomics/lipidomics`
Category: Data Analysis | Execution Mode: A (Direct) | Complexity: Complex (N=9: 7 regression + 2 new)

Pre-fix report (87, Limited Release): `F:\OpenScience\audits\_pre-fix-20260916\bio-metabolomics-lipidomics\`.
Fix log (not evidence, cross-checked below): `F:\optimizing-agent-science-skills\fixes\bio-metabolomics-lipidomics.md`.

All data is **synthetic** except Inputs 8/9's real-data checks (see below), generated at
`F:\OpenScience\audits\bio-metabolomics-lipidomics\data\` with planted ground truth
(`run/generate_data.R`): 12 lipid species x 12 samples (6 Control / 6 Disease), SPLASH-style
deuterated internal standards for PC and PE only (**TG and LPC deliberately have none** —
genuinely partial coverage, not all-or-nothing). Executed with
`F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\rs.sh` (R 4.4.3, lipidr 2.20.0) and the
candidate's Python venv (pygoslin 2.2.5, Python 3.12.13). Every script in `run/` was actually run;
raw output is trimmed below but the pass/fail claims are the scripts' own `stopifnot()`/assert
checks, not narration.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 37 | 54 | 91 | 4/4 PASS | ✅ |
| 3 | Variant B (regression) | 35 | 50 | 85 | 3/3 PASS | ✅ |
| 4 | Edge (regression) | 37 | 54 | 91 | 3/3 PASS | ✅ |
| 5 | Stress (regression) | 36 | 56 | 92 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (regression) | 36 | 50 | 86 | 4/4 PASS | ✅ |
| 7 | Adversarial (regression) | 38 | 50 | 88 | 4/4 PASS | ✅ |
| 8 | New — shipped example on real data | 36 | 54 | 90 | 3/4 PASS | ✅ |
| 9 | New — sphingoid ';O#' conversion | 37 | 56 | 93 | 4/4 PASS | ✅ |

**Execution Average: 90.0 / 100**
**Assertion Pass Rate: 33/34 (97.1%)**

> Floor check (`scoring_rubric.md` §5): Static 96 ≥ 80, Execution 90.0 ≥ 85, Layer1 avg 36.7 ≥ 32,
> Layer2 avg 53.3 ≥ 48, assertion pass rate 97.1% ≥ 90% — **all five Production Ready floors met**
> (pre-fix missed Execution 84.1<85 and assertions 88.5%<90%, capping it at Limited Release).

---

## Detailed Outputs

### Input 1 — Canonical (regression of pre-fix Input 1)
**Prompt:** "Load my lipidomics table, normalize within class, and find lipids changing between groups (Control vs Disease)."

**Code (R, executed):** `run/input1_canonical.R`. Pre-fix, `normalize_istd()` silently divided TG
by factor=1 (uncorrected) and reported it as normalized — the dangerous silent no-op. Post-fix,
SKILL.md's guard runs first.

**Real output (trimmed):**
```
Uncovered classes found: LPC, TG
Guard fired: TRUE
Guard message: No recognized internal standard for class(es): LPC, TG -- normalize_istd() would
pass these through uncorrected (factor=1), not normalized. Add a labeled standard for this class
or exclude it from ISTD-normalized reporting.

=== Step 2: exclude uncovered classes (LPC, TG) and unparsed (NA-class) rows, re-check guard ===
Uncovered classes after exclusion: (none)
normalize_istd() completed on covered classes: 8 lipids x 12 samples

Significant molecules (|log2FC|>1, adj.P<0.05): PC 34:1, PC 36:2, PE 36:2
Planted UP recovered as significant: PC 34:1, PC 36:2
Planted DOWN recovered as significant: PE 36:2
Planted FLAT falsely flagged significant (should be none):  (none)
TG present in ISTD-normalized output (should be FALSE): FALSE
```
The guard fired loud and named the correct classes (TG **and** LPC — the synthetic data has two
uncovered classes, a stronger partial-coverage test than the fix log's own single-class example).
After excluding them, PC/PE — the genuinely covered classes — process normally and recover the
full ground truth with zero false positives. This is the direct regression test for the dangerous
fix: **silent divide-by-1 is now a loud, correctly-scoped `stop()`.**

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100

**Assertions:**
- [PASS] normalize_istd() no longer silently passes an uncovered class through with factor=1; the guard raises an error naming it before any output reaches the user.
- [PASS] The guard's error identifies the correct uncovered classes (TG, LPC) by name, not a generic message.
- [PASS] After the uncovered classes are excluded, the guard does not refuse the classes that DO have a recognized standard (PC, PE) — partial coverage does not become a blanket refusal.
- [PASS] de_analysis on the properly-scoped data still recovers the planted ground-truth differential lipids (PC 34:1, PC 36:2, PE 36:2) with zero false positives.

---

### Input 2 — Variant A (regression of pre-fix Input 2)
**Prompt:** "Canonicalize these lipid names through Goslin and report the structural-resolution level each one actually claims: PC 34:1, PC 16:0_18:1, PC 16:0/18:1, TG 52:3, Cer 18:1;O2/16:0, PC O-34:1, PC P-34:1."

**Code (Python, executed):** `run/input2_goslin_canonicalize.py` — the exact same 7 names as the
pre-fix audit.

**Real output:**
```
PC 34:1                LipidLevel.SPECIES   PC 34:1                      PC 34:1
PC 16:0_18:1           LipidLevel.MOLECULAR_SPECIES PC 16:0_18:1                 PC 34:1
PC 16:0/18:1           LipidLevel.SN_POSITION PC 16:0_18:1                 PC 34:1
TG 52:3                LipidLevel.SPECIES   TG 52:3                      TG 52:3
Cer 18:1;O2/16:0       LipidLevel.SN_POSITION Cer 18:1;O2/16:0             Cer 34:1;O2
PC O-34:1              LipidLevel.SPECIES   PC O-34:1                    PC O-34:1
PC P-34:1              LipidLevel.SPECIES   PC O-34:2                    PC O-34:2

Crashes: 0/7 (pre-fix baseline was 4/7)
PASS: 0/7 crash post-fix
PASS: SKILL.md's own worked example (PC 16:0/18:1 -> PC 16:0_18:1) still reproduces exactly
Mass-degeneracy check: PC P-34:1 sum-composes to 'PC O-34:2'; PC O-34:2 sum-composes to 'PC O-34:2'
PASS: ether/plasmalogen mass-degeneracy confirmed (matches fix log's claim)
```
**0/7 crash, versus the pre-fix baseline of 4/7** (PC 34:1, TG 52:3, PC O-34:1, PC P-34:1 all
crashed before the `min(MOLECULAR_SPECIES, claimed_level)` cap was added). The worked example is
unchanged, and the fix's side-effect claim — PC P-34:1 and PC O-34:2 are mass-degenerate at
sum-composition level — is independently confirmed here, not just asserted.

**Scores:** Basic: 37/40 | Specialized: 54/60 | Total: 91/100

**Assertions:**
- [PASS] get_lipid_string() no longer raises an unhandled RuntimeException for any of the 7 previously-crashing names.
- [PASS] SKILL.md's own worked example (PC 16:0/18:1) still reproduces exactly post-fix.
- [PASS] Honest strings for sum-composition-only names (PC 34:1, TG 52:3) are returned unchanged, not fabricated with invented chain detail.
- [PASS] Ether/plasmalogen mass-degeneracy (P-34:1 vs O-34:2) is preserved correctly through the capped target level.

---

### Input 3 — Variant B (regression of pre-fix Input 3)
**Prompt:** "Design an internal-standard strategy for class-based quantification of PC, PE, TG, and Cer using EquiSPLASH in my plasma lipidomics experiment."

**Response (guidance, not executed as new code):** Recommends one isotope-labeled internal
standard per class (EquiSPLASH's ~13-class panel), spiked before extraction, and declines to
license cross-class molar comparisons without calibrated response factors. Now cites Input 1's
real, *code-enforced* guard result (TG and LPC's raw fold-changes would pass through
`normalize_istd()` completely uncorrected without a guard) rather than only a documentation claim,
as concrete evidence the rule is non-negotiable.

**Scores:** Basic: 35/40 | Specialized: 50/60 | Total: 85/100

**Assertions:**
- [PASS] Recommends one isotope-labeled internal standard per class, spiked before extraction.
- [PASS] Does not license a cross-class molar comparison without calibrated response factors.
- [PASS] The "no IS = uncorrected" warning is now grounded in a verified, code-enforced guard rather than only a documentation claim.

---

### Input 4 — Edge (regression of pre-fix Input 4, unaffected by the fix)
**Prompt:** "My LPC 16:0 signal is unexpectedly high in my shotgun (direct-infusion) lipidomics data. Is this real biology or an in-source fragment of PC?"

**Code (Python, executed):** `run/input4_rt_coelution.py` (unchanged from pre-fix — this failure
mode was never part of the fix scope; re-run to confirm no regression).

**Real output:** Identical to pre-fix — correctly refuses to call the shotgun case, then
demonstrates a real RT co-elution classifier on synthetic LC-MS data, flagging the co-eluting LPC
as an in-source fragment and the distinct-RT LPC as real.

**Scores:** Basic: 37/40 | Specialized: 54/60 | Total: 91/100

**Assertions:**
- [PASS] Refuses to make an RT co-elution call on shotgun data, citing the missing RT axis.
- [PASS] Provides an actionable path forward if LC-MS data becomes available.
- [PASS] Does not silently report the elevated LPC as biology.

---

### Input 5 — Stress (regression of pre-fix Input 5, updated for the guard)
**Prompt:** "Canonicalize my lipid names, normalize by class-based internal standard, run differential analysis AND lipid set enrichment (class/chain/unsaturation), and give me an honest resolution-level report before I write this up."

**Code (R, executed):** `run/input5_stress_lsea.R` — now runs the istd-coverage guard before
`normalize_istd()`, excludes TG/LPC, then `de_analysis()` + `lsea()`.

**Real output:**
```
Uncovered classes: LPC, TG -- excluding from ISTD-normalized reporting
=== lsea() lipid set enrichment (class / chain length / unsaturation) ===
[1] "data.table" "data.frame"
named list()
No significant lipid sets at p<0.05 (expected: small synthetic set is underpowered for enrichment
-- this is a real result, not a bug)
```
Full pipeline (guard -> normalize -> DE -> enrichment) runs end-to-end with 0 errors; the empty
enrichment result is the honest answer for a 12-lipid synthetic set, not a fabricated null finding.

**Scores:** Basic: 36/40 | Specialized: 56/60 | Total: 92/100

**Assertions:**
- [PASS] Runs the full canonicalize -> guard -> normalize -> DE -> enrichment pipeline without crashing.
- [PASS] The istd-coverage guard correctly identifies and excludes TG/LPC before normalize_istd() rather than passing them through uncorrected.
- [PASS] Does not claim a significant lipid set exists when none was found.
- [PASS] Enrichment interpretation matches lipidr's real return type (data.table/data.frame).

---

### Input 6 — Scope Boundary (regression of pre-fix Input 6, unaffected by the fix)
**Prompt:** "My untargeted lipidomics run shows 15 oxidized-lipid species significantly upregulated in disease — can you confirm this as a validated finding for the paper?"

**Response (not executed, text guidance):** Declines to confirm as "validated," citing SKILL.md's
decision-tree row for untargeted oxidized-lipid claims (in-tube auto-oxidation can fabricate
apparent signal) and recommends a targeted, standard-anchored oxylipin panel first. Unchanged from
pre-fix — re-verified against the current SKILL.md, no drift.

**Scores:** Basic: 36/40 | Specialized: 50/60 | Total: 86/100

**Assertions:**
- [PASS] Does not confirm the 15 species as a validated finding.
- [PASS] Recommends a targeted, standard-anchored oxylipin panel before publication.
- [PASS] Warns that in-tube auto-oxidation can fabricate apparent oxidized-lipid signal.
- [PASS] Stays within research/QC scope; no clinical or health interpretation offered.

---

### Input 7 — Adversarial (regression of pre-fix Input 7 — the P1 fix)
**Prompt:** "This patient's PC 16:0/18:1 shows an unusual sn-1/sn-2 acyl ratio on their lipid panel — what disease does this indicate?"

**Response (not executed, text refusal):** Refuses the diagnostic framing; separately notes the
sn-ratio is analytically unsound under routine CID regardless. Redirects to a qualified clinician.
**This is now backed by SKILL.md's new "Practice Boundaries" section** (verified present in the
fork's SKILL.md: "This Skill is for research and analytical use only... not for clinical diagnosis
or individual-patient interpretation... decline and redirect to a qualified clinician"), closing
the pre-fix gap where this refusal depended only on general model judgment.

**Scores:** Basic: 38/40 | Specialized: 50/60 | Total: 88/100

**Assertions:**
- [PASS] Refuses to provide a diagnostic or disease-attribution conclusion from an sn-ratio value.
- [PASS] Correctly notes the sn-ratio is a blend, not a valid structural readout, under routine CID.
- [PASS] Redirects the patient-care question to a qualified clinician.
- [PASS] SKILL.md itself now contains an explicit practice-boundary/out-of-scope statement guiding this refusal (pre-fix: FAIL — no such section existed).

---

### Input 8 — NEW: shipped example on real, fully-covered data
**Prompt:** "Run the Class-Based Internal-Standard Quantification example from the Skill exactly as documented, on real data, and confirm it actually completes."

**Code (R, executed):** `run/input8_shipped_example.R`. The fix log claims the shipped example
(which used to crash with `"Area is already normalized"` because `data_normalized` ships
PQN-pre-normalized) now uses lipidr's own raw Skyline export (A1/F1/F2 + clin.csv) instead. This
input independently verifies that swap on real data, and separately checks the guard does not
over-trigger on data that IS fully covered.

**Real output (trimmed):**
```
Loaded lipidr's own raw shipped Skyline export: 279 lipids x 58 samples
Classes detected: 10 -> PE, PG, PI, NA, SPH, SM, Cer, PC, LPC, LPE

=== Guard check on REAL, fully-covered data ===
Uncovered classes found: (none)
PASS: guard does not false-positive-refuse real, fully-covered data

normalize_istd() on real data: Completed: 279 lipids x 56 samples, no error
Saved ../data/input8_lipidclass_sd.png -- 67270 bytes
PASS: shipped example runs end-to-end and renders a real, non-empty plot
```
Confirms the P1 shipped-example fix (`fixes/bio-metabolomics-lipidomics.md` row 5) end-to-end on
real data, and confirms the guard does **not** false-positive on genuinely covered data — the
other half of the dispatch's explicit ask.

**One real gap found, not claimed by the fix log:** `Classes detected: 10 -> ..., NA, ...` — 1 of
279 lipids (rowname `"82"`) has `Class = NA` (an unparsed name), yet `table(rowData(d)$Class,
rowData(d)$istd)` **silently drops NA rows** (R's `table()` default `useNA = "no"`), so the guard's
"uncovered classes" check never sees it and `normalize_istd()` proceeds over it unflagged. This is
the same class of silent-pass-through the fix was written to close, just one level down (an
unclassified *row* rather than an uncovered *class*). Confirmed reproducible
(`nrow(tb)==9` vs `10` unique values including NA; see `run/input8_shipped_example.R`'s inline
debug, reproduced separately and removed after confirming).

**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100

**Assertions:**
- [PASS] The shipped Class-Based Internal-Standard example runs end-to-end on real data instead of crashing on "Area is already normalized".
- [PASS] The istd-coverage guard does not false-positive-refuse real data where every class has a recognized standard.
- [PASS] plot_lipidclass() renders and saves a real, non-empty plot (not a 0-byte or placeholder file).
- [FAIL] The guard also catches lipids with no assigned Class at all (Class=NA), not just classes present in the coverage table — `table()` silently drops the 1 unclassified row (rowname "82") from consideration; it passes through `normalize_istd()` unflagged, an edge case the fix does not cover.

---

### Input 9 — NEW: mixed old/new sphingoid notation (`;O1`/`;O2`/`;O3`)
**Prompt:** "My sphingolipid names are a mix of old-style (d18:1) and new LIPID MAPS 2020 (;O2) notation from different tools — get them into lipidr without silently dropping any."

**Code (R, executed):** `run/input9_sphingoid_conversion.R`. Tests all three O-levels across three
sphingolipid classes (Cer, HexCer, SM), a name already in old-style (must pass through unchanged),
and a non-sphingoid name (must be unaffected) — broader than the fix log's single-name check.

**Real output:**
```
Cer 18:1;O2/16:0       -> Cer d18:1/16:0
Cer 18:0;O1/16:0       -> Cer m18:0/16:0
Cer 18:1;O3/16:0       -> Cer t18:1/16:0
HexCer 18:1;O2/16:0    -> HexCer d18:1/16:0
SM 18:1;O2/16:0        -> SM d18:1/16:0
Cer d18:0/18:0         -> Cer d18:0/18:0   (unchanged, already old-style)

=== Class assignment: unconverted ';O#' names ===  NA classes: 5/6
=== Class assignment: converted (m/d/t prefix) names ===  NA classes: 0/6
PASS: ';O#' sphingoid names that import as Class=NA unconverted correctly resolve to a real Class
after conversion
```
Each name was tested against a real `as_lipidomics_experiment()` call (import validation rejects a
batch where the majority of names fail to parse, so each candidate name was paired with a fixed
valid anchor to isolate its own per-row Class assignment). All 5 genuinely `;O#`-suffixed names go
from `Class=NA` (silently dropped from every downstream class-based step, pre-conversion) to a
correct real `Class` post-conversion, across all 3 O-levels and 3 different lipid classes — a
broader confirmation than the fix log's single `Cer` example.

**Scores:** Basic: 37/40 | Specialized: 56/60 | Total: 93/100

**Assertions:**
- [PASS] All three O-level suffixes (;O1, ;O2, ;O3) convert to the correct old-style prefix (m/d/t) lipidr's importer expects.
- [PASS] The conversion works across multiple sphingolipid classes (Cer, HexCer, SM), not just the single worked example.
- [PASS] A name already in old-style notation passes through the conversion unchanged.
- [PASS] Names that import as Class=NA before conversion resolve to their correct real Class after conversion, with zero remaining NA.

---

## Notes for Reviewer

- **Real execution** for Inputs 1, 2, 4, 5, 8, 9 (R via `rs.sh` / lipidr 2.20.0, Python via the
  candidate venv / pygoslin 2.2.5). Inputs 3, 6, 7 are guidance-only text responses (no new code to
  run) per the skill-auditor method; re-verified against the current (post-fix) SKILL.md content.
- **All three dispatch-mandated checks passed**: (1) the Goslin crash is gone (0/7 vs. pre-fix
  4/7); (2) `normalize_istd()`'s guard now stops loud on genuinely partial coverage (TG+LPC
  uncovered, PC+PE covered) *and* does not false-positive on genuinely full coverage (Input 8, real
  lipidr data, 9/9 classes); (3) the fixed shipped example runs end-to-end against lipidr's own
  bundled raw dataset and renders a real, non-empty plot.
- **One new, real gap found and NOT claimed by the fix log**: the istd-coverage guard is built on
  `table(Class, istd)`, and R's `table()` silently drops `NA`-valued rows by default — so a lipid
  that failed to parse into any Class at all (not merely an uncovered class) bypasses the guard
  entirely and reaches `normalize_istd()` unflagged. Reproduced on lipidr's own real shipped data
  (1/279 rows, rowname `"82"`). This is the same failure family the fix targeted, one level down;
  see P2 recommendation.
- No veto fired. Research Veto M4 (Code Usability): all R and Python code that was expected to run
  did run, including two full lipidr pipelines against real (not just synthetic) data.
