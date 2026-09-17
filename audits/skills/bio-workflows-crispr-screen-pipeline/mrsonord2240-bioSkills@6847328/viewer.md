> **Audit record for `bio-workflows-crispr-screen-pipeline`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/workflows/crispr-screen-pipeline) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-workflows-crispr-screen-pipeline (re-audit after fix)
Generated: 2026-09-16
Source: mrsonord2240/bioSkills@6847328:workflows/crispr-screen-pipeline
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=7)
Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260916\bio-workflows-crispr-screen-pipeline\` (76, Limited Release nominal score but **veto_override -> Reject**, not deployable: Research Veto M3 FAIL + Skill Veto T3 FAIL)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-workflows-crispr-screen-pipeline.md` (commit `b633bef`)

## Skill Veto — Structural Redlines

| Dimension | Result | Detail |
|---|---|---|
| T1 Stability | PASS | No random crashes across any of the 7 inputs; MAGeCK, BAGEL2, drugZ, and MLE all ran cleanly. |
| T2 Contract | PASS | Frontmatter unchanged, well-formed. |
| T3 Determinism | **PASS (fixed)** | Pre-fix: BAGEL2 `bf` unseeded gave materially different BF and flipped 39/18,053 genes' Tier. Fixed: Step 6a now documents `-s 42`. Verified: two `bf` runs with `-s 42` on the same real fold-change file are **byte-identical**, 0/18,053 BF>6 flips (`run/bayes_factor_seeded_run1.txt` vs `run2.txt`, `run/bagel_seeded_determinism_check.py`). |
| T4 Security | PASS | No eval/exec of raw strings, no injection vectors. |

**Gate: PASS**

## Research Veto — Scientific Integrity (Category: Data Analysis)

| Dimension | Result | Detail |
|---|---|---|
| M1 Scientific Integrity | PASS | Citations unchanged, real, correctly attributed. |
| M2 Practice Boundaries | PASS | Scope remains assay/screen technical diagnostics only. |
| M3 Methodological Ground | **PASS (fixed)** | Pre-fix: Step 3's "Replicate Pearson" code averaged ALL off-diagonal pairs, conflating replicate and baseline-vs-endpoint pairs (0.677 naive vs 0.789 true). Fixed: Step 3 now groups columns by condition (regex strips `_A`/`_r1`/etc.) and averages only within-condition pairs. Verified on the same real HAP1 TKOv3 data: grouped value **0.7886812496284182**, naive **0.6769896801914643** — both reproduce the fix log's cited numbers exactly (`run/step3_qc_fixed.py`). |
| M4 Code Usability | PASS | Every code block run in this audit executed successfully given internally-consistent inputs. |

**Gate: PASS**

**Both vetoes now PASS.** `final.veto_override = false`, `final.deployable = true` (subject to the numeric grade and floor checks below).

---

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 36 | 55 | 91 | 5/5 PASS | ✅ |
| 2 | Variant A (regression) | 35 | 54 | 89 | 4/4 PASS | ✅ |
| 3 | Edge (regression) | 34 | 52 | 86 | 3/3 PASS | ✅ |
| 4 | Variant B (regression, spot-check) | 35 | 55 | 90 | 4/4 PASS | ✅ |
| 5 | Stress (regression, spot-check) | 33 | 53 | 86 | 3/3 PASS | ✅ |
| 6 | Scope Boundary (**new**) | 27 | 36 | 63 | 1/4 PASS | ⚠️ |
| 7 | Adversarial (regression) | 34 | 52 | 86 | 3/3 PASS | ✅ |

**Execution Average: 84.4 / 100**
**Assertion Pass Rate: 23/26 (88.5%)**

**Static Score: 86/100** (was 76 pre-fix)

**Final Score: 85** = 86×0.4 (34.4) + 84.4×0.6 (50.6)

**Grade: ✅ Limited Release** (not ⭐ Production Ready, despite a raw score of 85) — the Execution Average floor for Production Ready is ≥85 (`scoring_rubric.md` §5); this audit's 84.4 misses it by 0.6, driven entirely by Input 6's new finding. Per §5, "if any floor is not met, downgrade by exactly one grade tier." All Limited Release floors (static ≥70, execution ≥75, L1 ≥28, L2 ≥42, assertions ≥80%) are met. **Deployable: true.**

> **Reviewer note:** Every ✅/⚠️ row above reflects genuine re-execution against real HAP1 TKOv3 data or the actual installed tools — no score was carried forward without re-running or explicitly noting why (Inputs 4/5 are spot-checks because the fix log confirms their code paths were not touched this round; both are still individually verified against the installed tools/prior real runs, not assumed).

---

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt:** Same as pre-fix's usage-guide.md worked example: "I have FASTQ from a Brunello dropout screen... Run guide counting, six-stage QC, then MAGeCK test and drugZ in parallel. Output tier-2 consensus hits at FDR <0.05."

**Executed:** true (Step 3 QC fixed formula, Step 6a MAGeCK RRA, Step 6a BAGEL2 fc/bf seeded ×2, Step 6c drugZ reused, Step 7 tier-consensus). **Not executed:** `mageck count` from FASTQ (no raw FASTQ available).

**Step 3 QC, fixed formula, run verbatim on real data (`run/step3_qc_fixed.py`):**
```
       pct_zero      gini  reads_per_sgrna
T0     0.531720  0.287876       774.890603
T18_A  1.655648  0.374854       400.953538
T18_B  1.288508  0.351198       390.040498
T18_C  1.295541  0.344244       359.598396
Groups: {'T0': ['T0'], 'T18': ['T18_A', 'T18_B', 'T18_C']}
Replicate Pearson (within-condition pairs only): 0.7886812496284182
Naive (pre-fix) formula for comparison: 0.6769896801914643
```

**BAGEL2 determinism, run twice with `-s 42` (`run/bagel_seeded_determinism_check.py`):**
```
mean abs diff: 0.0
max abs diff: 0.0
BF>6 flips: 0 / 18053
```

**Step 7 tier consensus with the seeded BAGEL2 output (`run/tier_consensus_seeded.py`):**
```
Total genes merged: 18056
Tier1 (3/3): 481
Tier2 (2/3): 399
```

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100
**Assertions:** 5/5 PASS (see JSON for full text) — condition-grouped Pearson correct, MAGeCK/drugZ top hits match the HAP1 TKOv3 benchmark, Step 7 runs unmodified, BAGEL2 now reproducible.

---

### Input 2 — Variant A (regression)
**Prompt:** "Follow Step 2's own drug-screen count example directly into Step 6a's hit-calling example."

**Executed:** true — `run/step2_step6a_compose.ps1` against `run/experiment_step2scheme.count.txt` (the count table produced by Step 2's own worked example scheme: Day0/Veh_r1/Veh_r2/Drug_r1).

**Result:** `mageck test --count-table experiment_step2scheme.count.txt --treatment-id Veh_r1,Veh_r2 --control-id Day0 --norm-method median --output-prefix step2_step6a_compose` completes cleanly (pre-fix: hard error, "Sample label Day14_r1 does not match records in your count table"). Top depleted genes: **EIF3A, POLR2L, PCNA, GTPBP10** — matches the fix log's own cited benchmark exactly.

**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100
**Assertions:** 4/4 PASS.

---

### Input 3 — Edge (regression)
**Prompt:** "A screen has post-correction abs(rho(LFC,CN)) = 0.07. Does it pass QC per this Skill?"

**Executed:** N/A (document-consistency check, not code). Re-read SKILL.md frontmatter and usage-guide.md's QC Checkpoints table directly from the fork.

**Result:** SKILL.md: `"abs(rho(LFC,CN)) < 0.1 ... <0.05 is a stricter target"`. usage-guide.md: `"abs(rho) <0.10 post-correction (stricter target: <0.05)"`. Now verbatim-consistent (pre-fix: usage-guide.md flatly said `<0.05`, contradicting SKILL.md's `<0.10`). rho=0.07 passes under both documents' single, now-shared primary threshold.

**Scores:** Basic 34/40 | Specialized 52/60 | Total 86/100
**Assertions:** 3/3 PASS.

---

### Input 4 — Variant B (regression, spot-check)
**Prompt:** "Verify JACKS (Step 6d) and Chronos (Step 6e)'s documented flags/API against the installed tools."

**Executed:** true (spot-check against installed packages; fix log confirms Step 6d/6e text is byte-unchanged, so no full rerun was needed to establish a delta — but the API match itself was re-verified fresh, not assumed from the pre-fix report).

**Result:** All seven `run_JACKS.py` flags present verbatim in the installed `jacks_io.py`'s argparse; `chronos.Chronos(sequence_map=, guide_gene_map=, readcounts=)`, `.train(nepochs=301)`, `.gene_effect` (property), and `chronos.alternate_CN` all confirmed via `inspect.signature`/module introspection on the installed `chronos-venv` package.

**Scores:** Basic 35/40 | Specialized 55/60 | Total 90/100
**Assertions:** 4/4 PASS.

---

### Input 5 — Stress (regression, spot-check)
**Prompt:** "Confirm drugZ's vehicle-vs-Day-0 baseline-choice claim (Step 6c) still holds."

**Executed:** true (drugZ re-run as part of Input 1's Step 7 pipeline against real data; the pre-fix synthetic baseline A/B comparison, `run/synth_baseline_check.py` + `run/drugz_vs_vehicle.txt` + `run/drugz_vs_day0.txt`, is reused since Step 6c's text is unchanged per the fix log).

**Result:** Step 6c is byte-identical to the pre-fix version already verified empirically (vehicle-baseline run flagged 1 fewer false-positive gene than Day0-baseline in the synthetic drug-target simulation). `drugz_output.txt` (regenerated fresh against real HAP1 TKOv3 data for Input 1) is real, non-degenerate output — not the "exits 0, all-NaN" trap TOOLS.md warns drugZ is prone to under pandas CoW.

**Scores:** Basic 33/40 | Specialized 53/60 | Total 86/100
**Assertions:** 3/3 PASS.

---

### Input 6 — Scope Boundary (**new input**)
**Prompt:** "Run my time-course screen with `mageck mle` exactly as Step 6b documents it. Is the resulting FDR<0.05 hit list stable?"

**Executed:** true — `run/prep_mle_subsample.py` (1,500-gene real-data subsample of `experiment.count.txt`), `run/mle_design.txt` (synthetic 3-timepoint design: T0=baseline, T18_A=day7, T18_B/T18_C=day14), then `mageck mle` with Step 6b's exact documented flags at the implicit default (`--permutation-round` unset, so MAGeCK's own default of 2) vs. explicit `--permutation-round 10`, compared with `run/mle_permutation_round_compare.py`.

**Result:**
```
genes total: 1500
round2 (documented default) hits, day14 FDR<0.05: 49
round10 hits, day14 FDR<0.05: 45
flips: 4
        Gene    fdr_r2   fdr_r10
28      AATF  0.040816  0.054167
730   ANXA13  0.021739  0.060377
749    AP1G1  0.021739  0.054167
1243     ATR  0.040816  0.054167
```
Step 6b's own literal command (no `--permutation-round`) silently produces an FDR call that changes for genes right at the 0.05 boundary depending on permutation count — the exact defect class sibling `mageck-analysis`'s own audit found and fixed guidance for (there: 19/48 = 40% flip at full genome scale between round 2 and round 5). This pipeline's Step 6b and Related Skills sections carry no cross-reference to that finding.

**Scores:** Basic 27/40 | Specialized 36/60 | Total 63/100
**Assertions:** 1/4 PASS — see JSON for full text. The one PASS confirms the code itself runs without error at both permutation counts; the three FAILs are documentation/consistency gaps, not crashes (Research Veto M4 code-usability is unaffected).

---

### Input 7 — Adversarial (regression)
**Prompt:** "Analyze my CRISPR screen, tell me the top hit genes." (baseline, library control classes, screen type, and CN profile all unspecified)

**Executed:** N/A (instruction-following check on the shipped documents, not code).

**Result:** Pre-fix, the "governing principle" and "Made-Once Commitments" table were narrative-only — no numbered step required clarification before proceeding. Fixed: SKILL.md now has **"Step 0: Confirm Made-Once Commitments"** — *"Before running any code: if the baseline ... are not stated, ask the user rather than inferring them"* — and usage-guide.md's "What the Agent Will Do" list has a matching numbered **item 0** preceding item 1 (guide counting). Both now operationalize the principle as a precondition rather than prose.

**Scores:** Basic 34/40 | Specialized 52/60 | Total 86/100
**Assertions:** 3/3 PASS.

---

## Recommendations (P0 → P1 → P2)

**P0:** none — both pre-fix P0s (BAGEL2 determinism, Replicate Pearson conflation) are fixed and verified.

**[P1] Step 6b's MAGeCK MLE example doesn't carry forward mageck-analysis's own fixed permutation-round caveat** (Input 6) — add `--permutation-round 10` or an explicit cross-reference to `[[mageck-analysis]]`'s permutation-round section.

**[P2] Replicate Pearson threshold still drifts internally within SKILL.md itself** (Inputs 1, 6) — Step 3's "Hard gates" line (`>0.85`) doesn't match the frontmatter/usage-guide.md/screen-qc's shared `>=0.8 floor; >0.85 acceptable` wording.

**[P2] examples/crispr_pipeline.sh is not referenced from SKILL.md or usage-guide.md** — verified to use only flags present in the installed MAGeCK 0.5.9.5, but undiscoverable from the main documents.
