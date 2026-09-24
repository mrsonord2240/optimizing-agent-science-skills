> **Audit record for `bio-crispr-screens-mageck-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@d2134ad](https://github.com/mrsonord2240/bioSkills/tree/d2134ad0c94f2e442d6c21f81f51b00db4ca15e1/crispr-screens/mageck-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-mageck-analysis

Generated: 2026-09-24 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@d2134ad0c94f2e442d6c21f81f51b00db4ca15e1:crispr-screens/mageck-analysis`
Audit type: final pass
Category: Data Analysis · Execution mode: D · Complexity: Complex · N = 9 · Executed: 9

## What the Skill claims to do

MAGeCK pooled-CRISPR screen analysis with RRA/MLE selection, normalization, paired testing, and downstream visualization.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical regression | 38 | 57 | **95** | 4/4 | yes | ✅ |
| 2 | Time-course regression | 38 | 57 | **95** | 5/5 | yes | ✅ |
| 3 | Heavy-selection regression | 38 | 57 | **95** | 3/3 | yes | ✅ |
| 4 | Drug-screen regression | 38 | 56 | **94** | 5/5 | yes | ✅ |
| 5 | Multi-line/batch regression | 38 | 56 | **94** | 5/5 | yes | ✅ |
| 6 | Scope-boundary regression | 38 | 56 | **94** | 1/1 | yes | ✅ |
| 7 | Adversarial regression | 38 | 58 | **96** | 1/1 | yes | ✅ |
| 8 | Fresh permutation edge | 38 | 56 | **94** | 4/4 | yes | ✅ |
| 9 | Fresh paired-design edge | 38 | 58 | **96** | 4/4 | yes | ✅ |

**Execution Average: 94.8 / 100** · **Assertion Pass Rate: 32/32**

**Static: 94/100** · Static weighted 37.6 + dynamic weighted 56.9 = **94/100** → ⭐ Production Ready, deployable.

---

## Veto gates

### Skill veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| stability | PASS |  |
| contract | PASS |  |
| determinism | PASS |  |
| security | PASS |  |

### Research veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| scientific integrity | PASS | No invented results; all reported run outcomes come from final-pass outputs. |
| practice boundaries | PASS | Guidance remains limited to pooled-screen analysis, not patient treatment. |
| methodological ground | PASS | Paired RRA, multifactor MLE, and permutation uncertainty are now accurately delimited. |
| code usability | PASS | All runnable core CLI routes exercised in the final-pass harness completed. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 12/12 | Decision table and worked examples align with the audited CLI. |
| reliability | 11/12 | Documents default-round uncertainty, baseline/intercept distinction, and external package recovery. |
| performance context | 7/8 | Keeps progressive disclosure through usage guide and examples. |
| agent usability | 16/16 | Explicit decision routes and error recoveries prevent the audited mistakes. |
| human usability | 8/8 | Commands and interpretation thresholds are readable and scoped. |
| security | 12/12 | No credentials or unsafe input interpolation. |
| maintainability | 12/12 | Version and package-compatibility boundaries are explicit. |
| agent specific | 16/20 | Precise trigger, real-data anti-fabrication rule, and sibling handoffs. |

## Input 1 — Canonical regression: Real HAP1 TKOv3 RRA, output-column and volcano checks

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Finding: Fresh final-pass execution; see _final_pass/bio-crispr-screens-mageck-analysis/run/verification.json.

| Assertion | Result | Evidence |
|---|---|---|
| i1_rra exits cleanly | PASS | reused completed current-pass output i1_rra.gene_summary.txt |
| input 1 RRA has high essential/nonessential separation | PASS | PR-style rank AUC=0.993 |
| input 1 volcano example includes pandas import | PASS | SKILL.md visualization block |
| input 1 gene-summary columns exist | PASS | RRA gene_summary columns |

## Input 2 — Time-course regression: Two independent round-10 MLE executions

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Finding: Fresh final-pass execution; see _final_pass/bio-crispr-screens-mageck-analysis/run/verification.json.

| Assertion | Result | Evidence |
|---|---|---|
| i2_pr10a exits cleanly | PASS | reused completed current-pass output i2_pr10a.gene_summary.txt |
| i2_pr10b exits cleanly | PASS | reused completed current-pass output i2_pr10b.gene_summary.txt |
| input 2 documented round 10 recovers planted time-course hits | PASS | found=20/20 |
| input 2 documented round 10 recovers planted time-course hits | PASS | found=20/20 |
| input 2 beta signs reproducible at round 10 | PASS | two fresh permutation-round-10 runs |

## Input 3 — Heavy-selection regression: Median versus control-sgRNA normalization

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 57/60 · **Total 95/100**
- Finding: Fresh final-pass execution; see _final_pass/bio-crispr-screens-mageck-analysis/run/verification.json.

| Assertion | Result | Evidence |
|---|---|---|
| i3_median exits cleanly | PASS | reused completed current-pass output i3_median.gene_summary.txt |
| i3_control exits cleanly | PASS | reused completed current-pass output i3_control.gene_summary.txt |
| input 3 control normalization restores masked enriched hits | PASS | median=0, control=43, total=43 |

## Input 4 — Drug-screen regression: Vehicle control and sgRNA-efficiency MLE

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Finding: Fresh final-pass execution; see _final_pass/bio-crispr-screens-mageck-analysis/run/verification.json.

| Assertion | Result | Evidence |
|---|---|---|
| i4_rra exits cleanly | PASS | reused completed current-pass output i4_rra.gene_summary.txt |
| i4_eff exits cleanly | PASS | reused completed current-pass output i4_eff.gene_summary.txt |
| i4_noeff exits cleanly | PASS | reused completed current-pass output i4_noeff.gene_summary.txt |
| input 4 MLE efficiency flags produce a valid weighted analysis | PASS | planted hits=20 |
| input 4 efficiency changes a nontrivial beta estimate | PASS | weighted=-0.788 |

## Input 5 — Multi-line/batch regression: Explicit batch-aware and no-batch MLE designs

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Finding: Fresh final-pass execution; see _final_pass/bio-crispr-screens-mageck-analysis/run/verification.json.

| Assertion | Result | Evidence |
|---|---|---|
| i5_batch exits cleanly | PASS | reused completed current-pass output i5_batch.gene_summary.txt |
| i5_nobatch exits cleanly | PASS | reused completed current-pass output i5_nobatch.gene_summary.txt |
| input 5 batch-aware design runs with explicit covariates | PASS | 15 planted hits present |
| input 5 MLE outputs beta and wald-fdr columns | PASS | batch-aware MLE result |
| input 5 alternate covariate design also runs | PASS | rows=60 |

## Input 6 — Scope-boundary regression: Windows VISPR fallback

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Finding: Fresh final-pass execution; see _final_pass/bio-crispr-screens-mageck-analysis/run/verification.json.

| Assertion | Result | Evidence |
|---|---|---|
| input 6 platform fallback is documented | PASS | mageck_vispr import exit=1 |

## Input 7 — Adversarial regression: No fabrication without observed count data

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 58/60 · **Total 96/100**
- Finding: Fresh final-pass execution; see _final_pass/bio-crispr-screens-mageck-analysis/run/verification.json.

| Assertion | Result | Evidence |
|---|---|---|
| input 7 anti-fabrication instruction is explicit | PASS | SKILL.md direct instruction |

## Input 8 — Fresh permutation edge: New deterministic HAP1 subset, rounds 2 and 5

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 56/60 · **Total 94/100**
- Finding: Fresh final-pass execution; see _final_pass/bio-crispr-screens-mageck-analysis/run/verification.json.

| Assertion | Result | Evidence |
|---|---|---|
| i8_pr2 exits cleanly | PASS | exit=0; log=i8_pr2.stdout.txt |
| i8_pr5 exits cleanly | PASS | exit=0; log=i8_pr5.stdout.txt |
| input 8 fresh subset preserves wald-fdr column | PASS | fresh 350-gene subset at rounds 2 and 5 |
| input 8 guidance labels run-specific flip count as illustrative | PASS | no generalized effect-size claim |

## Input 9 — Fresh paired-design edge: New matched-pair fixture using mageck test --paired

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 58/60 · **Total 96/100**
- Finding: Fresh final-pass execution; see _final_pass/bio-crispr-screens-mageck-analysis/run/verification.json.

| Assertion | Result | Evidence |
|---|---|---|
| i9_paired_rra exits cleanly | PASS | exit=0; log=i9_paired_rra.stdout.txt |
| input 9 paired RRA recovers the planted paired hits | PASS | 6/6 planted paired hits |
| input 9 no longer claims RRA lacks pairing | PASS | decision table and paired command guidance |
| input 9 FluteMLE uses emitted condition names | PASS | baseline intercept is not passed to FluteMLE |

## Key strengths

- All seven archived scenario classes were freshly rerun, including real HAP1 RRA and batch-aware MLE.
- Two new edge fixtures validate the repaired boundaries: paired two-condition RRA and screen-dependent permutation sensitivity.
- The final documentation removes the false RRA-pairing claim, uses emitted MLE condition names in FluteMLE, and warns that default permutation calls can vary on identical reruns.
