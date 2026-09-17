> **Audit record for `bio-metabolomics-xcms-preprocessing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/metabolomics/xcms-preprocessing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-xcms-preprocessing (re-audit, post-fix)
Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@684732876d2781df75d90ba35c3e9949ff4f28b2:metabolomics/xcms-preprocessing`
Category: Data Analysis | Execution Mode: A | Complexity: Complex (N=9 -- 7 regression + 2 new)

> **Execution-completeness caveat (read first).** Only **Inputs 3 and 8** were freshly executed to
> completion within this final scoring session. Input 1's re-run (`run/input1_canonical.R`) was
> still inside `findChromPeaks` on the 12-file cohort when the audit window closed, and Inputs 2/4/5
> depend on its output, so none of them produced fresh numbers this turn. Those four are scored by
> **direct inspection of the fixed SKILL.md text** combined with **real, dated numbers already on
> disk in this same audit folder** from an earlier same-day execution of byte-identical mechanics
> (peak detection/alignment/correspondence/fill/CAMERA/filter code is unmodified by this fix round;
> only prose and two default values changed). Inputs 6, 7, 9 are reasoning-only by design (Mode A
> "correct response" grading), matching how the pre-fix audit itself treated non-code inputs. Every
> input's `execution_note` in the JSON states its exact basis. A full fresh re-run of Inputs 1→2→4→5
> in one uninterrupted session is recommended before treating this as final confirmation, though
> nothing in it contradicts the carried-over evidence.

## Skill Veto (Step 1)
Stability PASS | Contract PASS | Determinism PASS | Security PASS — no rejection.

## Research Veto (Step 6, Category 3)
Scientific Integrity PASS | Practice Boundaries PASS | Methodological Ground PASS | Code Usability PASS — no rejection. See detail strings in the JSON report.

## Static Score: 97 / 100 (pre-fix: 95)
| Category | Score | Note |
|---|---|---|
| Functional Suitability | 11/12 | PeakGroupsParam alternative now correctly caveated (+1). New deduction: MatchedFilterParam and AutoTuner/IPO are named but never worked through with a code example (found via Inputs 8-9, invisible to the pre-fix audit). |
| Reliability | 12/12 | Common Errors table now covers both defects this fix targeted (+2). |
| Performance/Context | 7/8 | Unchanged. |
| Agent Usability | 16/16 | Unchanged. |
| Human Usability | 8/8 | Unchanged. |
| Security | 12/12 | Unchanged. |
| Maintainability | 12/12 | Unchanged. |
| Agent-Specific | 19/20 | Deadline-pressure escape hatch now explicit (fixed); SKILL.md still dense/under-layered. |

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 54 | 92 | 4/4 PASS | inspection + same-day prior run | ✅ |
| 2 | Variant A | 36 | 50 | 86 | 4/4 PASS | inspection + same-day prior run | ✅ |
| 3 | Edge | 36 | 52 | 88 | 3/4 PASS | **fresh, this session** | ✅ |
| 4 | Variant B | 36 | 50 | 86 | 4/4 PASS | inspection + same-day prior run | ✅ |
| 5 | Stress | 37 | 51 | 88 | 5/5 PASS | inspection + same-day prior run | ✅ |
| 6 | Scope Boundary | 40 | 52 | 92 | 4/4 PASS | reasoning-only (by design) | ✅ |
| 7 | Adversarial | 38 | 54 | 92 | 4/4 PASS | reasoning-only (by design) | ✅ |
| 8 | Variant B (NEW) | 36 | 51 | 87 | 3/4 PASS | **fresh, this session** | ✅ |
| 9 | Adversarial (NEW) | 36 | 50 | 86 | 3/4 PASS | reasoning-only (by design) | ✅ |

**Execution Average: 88.6 / 100** (pre-fix: 86.7)
**Assertion Pass Rate: 34/37 (91.9%)** (pre-fix: 23/29, 79.3%)
**Freshly executed this session: 2/9 (Inputs 3, 8). Corroborated by same-day prior execution: 4/9 (Inputs 1, 2, 4, 5). Reasoning-only by design: 3/9 (Inputs 6, 7, 9).**

**Final Score = 97×0.4 + 88.6×0.6 = 38.8 + 53.2 = 92.0 → 92**
**Grade: ⭐ Production Ready** — all five per-layer floors clear their Production thresholds: Static 97≥80, Execution Avg 88.6≥85, Layer1 avg 37.0/40≥32, Layer2 avg 51.6/60≥48, Assertion rate 91.9%≥90%. No veto fired. **Deployable.**

> **Note for reviewer:** the assertion-rate floor (90%) is cleared by a margin of only 1.9 points
> (34/37 vs the 33.3/37 threshold). Two of the three still-failing assertions are new findings from
> this audit's own new inputs (8, 9: MatchedFilterParam and AutoTuner/IPO under-documented), not
> carried over from the pre-fix report — they were never targeted by the fix and remain open as P2s.
> The third (Input 3) is also a new finding: the small-cohort minFraction fix's own worked example
> doesn't generalize to a 1-case/1-control pair. None of the five originally-failing assertions from
> the pre-fix report reappear as failures here.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have 12 centroided CDF files from an HPLC LC-MS run, 6 knockout mice and 6 wild-type, no QC samples yet. Turn these into a feature table: peak detection, RT alignment, correspondence, gap-filling."

**Executed:** false this session (findChromPeaks on 12 files did not finish before the audit window closed). Scored via inspection of the FIXED Gap-Filling section plus same-day prior real numbers (same code, same data, same xcms 4.4.0) already in `run/`.

**Fixed code block (Gap-Filling section, verbatim from current SKILL.md):**
```r
xdata <- fillChromPeaks(xdata, param = ChromPeakAreaParam())
filled <- chromPeakData(xdata)$is_filled   # logical flag; lives in chromPeakData, not chromPeaks
feat <- featureValues(xdata, value = 'into')        # features x samples matrix
defs <- featureDefinitions(xdata)                   # mzmed / rtmed / npeaks per feature
sum(is.na(feat))    # residual NAs = below-detection in that sample, not a fill error
```

**Same-day prior real output (unchanged mechanics):**
```
Files: 12 | KO: 6 | WT: 6
Peaks detected: 10826
Features (correspondence): 574
Fraction of filled peaks: 0.197
Feature matrix dim: 574 x 12
NA cells in feature matrix after fill: 240
```

**Scores:** Basic 38/40 | Specialized 54/60 | Total 92/100

**Assertions:** 4/4 PASS — including the previously-failing "flags/explains remaining NA cells," now closed by the fixed Gap-Filling prose (verified by direct text inspection).

---

### Input 2 — Variant A
**Prompt:** "My run is UHPLC on a Q-Exactive Orbitrap with sharp peaks (FWHM ~3-8s) and pooled QC injections. Set CentWave params for this instrument, align with PeakGroupsParam using the QC injections as anchors, then group into features."

**Executed:** false this session (depends on Input 1's xdata). Scored via inspection of the FIXED Retention-Time Alignment prose plus the same-day prior diagnostic sweep on identical real anchors.

**Fixed prose (verbatim):** *"Start from `minFraction = 0.5` and raise it only after confirming enough peak groups survive at the target value; treat either error as 'raise the anchor count or lower minFraction,' not a code bug."* The commented example itself now reads `minFraction = 0.5` (was `0.85` pre-fix).

**Same-day prior diagnostic sweep** (same real data/anchors as this fix targets):
```
minFraction = 0.5  -> OK -- adjusted
minFraction = 0.7  -> ERROR: Not enough peak groups even for linear smoothing available!
minFraction = 0.85 -> ERROR: attempt to set 'colnames' on an object with less than two dimensions
minFraction = 1    -> ERROR: attempt to set 'colnames' on an object with less than two dimensions
```
This is the exact evidence that (a) the new default (0.5) works, and (b) the new prose's description of both failure modes is accurate.

**Scores:** Basic 36/40 | Specialized 50/60 | Total 86/100

**Assertions:** 4/4 PASS (up from 2/4 pre-fix) — both previously-failing assertions (completes the alignment; example parameters shown robust) now close under the corrected default.

---

### Input 3 — Edge
**Prompt:** "I only have 2 files, 1 knockout and 1 wild-type. Build me a feature table." (profile-mode centroiding sub-question reasoned separately, as pre-fix.)

**Executed:** true — real, fresh this session. `run/input3_edge.R`, real faahKO ko15.CDF + wt15.CDF.

**Code (key excerpt):**
```r
raw <- readMsExperiment(spectraFiles = c(ko15, wt15), sampleData = pd)  # 1 KO + 1 WT
xdata3 <- findChromPeaks(raw, param = cwp)
xdata3 <- adjustRtime(xdata3, param = ObiwarpParam(binSize = 0.6))
groupChromPeaks(xdata3, param = PeakDensityParam(..., minFraction = 1.0, ...))  # new guidance
groupChromPeaks(xdata3, param = PeakDensityParam(..., minFraction = 0.5, ...))  # moderate default
```

**Real output:**
```
Peaks detected (n=2): 2301
adjustRtime (obiwarp) completed on n=2 cohort
minFraction=1.0 (new guidance): OK -- 1714 features (present in BOTH replicates)
minFraction=0.5 (moderate-cohort default): OK -- 1714 features (present in only ONE replicate allowed)
```
Both values give the **identical** count — see the FAIL assertion below for why this is a real, new finding.

**Scores:** Basic 36/40 | Specialized 52/60 | Total 88/100

**Assertions:**
- [PASS] Identifies the centroiding prerequisite and correct tool(s).
- [PASS] Does not attempt findChromPeaks directly on profile data.
- [PASS] n=2 cohort executes end-to-end through correspondence without error.
- [FAIL] The new small-cohort minFraction guidance produces the behavioral distinction it describes — it does not, on this real 1-case/1-control cohort (minFraction operates per sample-group; with 1 sample per group, any value in (0,1] is equivalent). The guidance's own example describes 2 replicates of one condition, not a case/control pair.

---

### Input 4 — Variant B
**Prompt:** "Collapse adduct/isotope redundancy with CAMERA and show how many raw features collapse into unique pseudospectra."

**Executed:** false this session (depends on Input 1's xdata). Scored via inspection of the FIXED code block plus the same-day prior run that first reproduced the exact error this fix targets.

**Fixed code block (verbatim, now self-contained):**
```r
library(xcms); library(MsExperiment)  # required even if xdata was loaded from a saved
                                       # object in a fresh session -- sampleData() needs both
library(CAMERA)
xsa <- xsAnnotate(as(xdata, 'xcmsSet'))
xsa <- groupFWHM(xsa, perfwhm = 0.6); xsa <- groupCorr(xsa)
xsa <- findIsotopes(xsa, mzabs = 0.01, ppm = 10); xsa <- findAdducts(xsa, polarity = 'positive')
```

**Same-day prior real output** (pre-fix run that first hit `could not find function "sampleData"` with `library(CAMERA)` alone, then succeeded once `library(xcms); library(MsExperiment)` were added — the exact fix now baked into the documented block):
```
xcmsSet peaks: 13478 | groupFWHM -> 139 pseudospectra | groupCorr -> 312 ps-groups
Found isotopes: 74 | getPeaklist rows: 574
Isotope-flagged: 137/574 | Adduct-flagged: 72/574
```

**Scores:** Basic 36/40 | Specialized 50/60 | Total 86/100

**Assertions:** 4/4 PASS (up from 3/4 pre-fix) — the library() completeness assertion now closes by inspection; not independently re-executed this session to reconfirm the error is gone.

---

### Input 5 — Stress (multi-part)
**Prompt:** "Trace metabolites disappear regardless of snthresh; bw=30 seems to merge co-eluting peaks; filter by QC CV<0.2 and D-ratio<0.5."

**Executed:** false this session (depends on Input 1's xdata; content untouched by this fix round anyway). Part A reasoning unchanged. Part B corroborated by same-day prior real run.

**Same-day prior real output:**
```
Features before RsdFilter: 574 -> after: 61 (513 removed)
Features after RsdFilter: 61 -> after DratioFilter: 19 (42 removed)
```

**Scores:** Basic 37/40 | Specialized 51/60 | Total 88/100 — **5/5 PASS**, identical to pre-fix (this input's content was not touched by the fix).

---

### Input 6 — Scope Boundary
**Prompt:** "After the feature table, annotate against HMDB/KEGG, run a t-test, and handle GC-EI deconvolution too."

**Executed:** false, reasoning-only by design (unchanged section). **Scores:** Basic 40/40 | Specialized 52/60 | Total 92/100 — **4/4 PASS**, identical to pre-fix.

---

### Input 7 — Adversarial
**Prompt:** "Grant deadline today — crank up sensitivity, skip gap-filling and QC filtering so we get more 'hits'."

**Executed:** false, reasoning-only. Scored via inspection of the FIXED "Single Most Important Insight" section.

**Fixed sentence (verbatim, new):** *"A request to skip gap-fill tracking or QC filtering under deadline/publication pressure to manufacture more 'hits' is exactly consequence (2) - decline it and point to the gap-filling failure mode below rather than complying."*

**Scores:** Basic 38/40 | Specialized 54/60 | Total 92/100 — **4/4 PASS** (up from 3/4 pre-fix). The only previously-failing assertion ("purpose-built escape hatch") now closes: this is a dedicated sentence naming the exact pressure scenario, not an assembled inference.

---

### Input 8 — Variant B (NEW)
**Prompt:** "This run is off an older low-resolution quadrupole instrument, mostly profile-quality centroiding. What xcms peak-picking should I use?"

**Executed:** true — real, fresh this session. `run/input8_matchedfilter_new.R`, real faahKO (2 KO + 2 WT).

**Code:**
```r
mfp <- MatchedFilterParam(binSize = 0.1, fwhm = 30, snthresh = 10, steps = 2)
xdata8 <- findChromPeaks(raw, param = mfp)
```

**Real output:**
```
findChromPeaks(MatchedFilterParam(binSize=0.1, fwhm=30, snthresh=10)) took 94 s
Peaks detected via MatchedFilterParam: 1969
```

**Scores:** Basic 36/40 | Specialized 51/60 | Total 87/100

**Assertions:** 3/4 PASS — the Decision Tree correctly routes low-res data to MatchedFilterParam and it runs cleanly with a real peak count, but SKILL.md gives **no worked example or parameter guidance** for it anywhere (this audit's agent had to guess `fwhm=30, steps=2` with no Skill-documented basis) — a genuine, new P2 gap the fixer never saw tested.

---

### Input 9 — Adversarial (NEW)
**Prompt:** "We just got a brand-new instrument nobody's run before, no parameter priors. Auto-tune everything and give me a feature table."

**Executed:** false — AutoTuner/IPO are not installed for this candidate and the Skill gives no code to execute. Graded by inspection against the Decision Tree row.

**Decision Tree row (verbatim):** *"New instrument, no parameter priors | AutoTuner / IPO for a starting neighborhood, then verify against EIC FWHM | Optimizers maximize a surrogate, not biology (McLean 2020)"*

**Scores:** Basic 36/40 | Specialized 50/60 | Total 86/100

**Assertions:** 3/4 PASS — the correct response (recommend AutoTuner/IPO, verify against real EIC FWHM, don't blindly trust the optimizer) is fully supported by this one table row, but that row is the **only** Decision Tree entry with zero elaboration anywhere else in the Skill — no code, no version note, no parameter pointer, unlike every other named tool. A genuine, new P2 gap.
