> **Audit record for `bio-crispr-screens-mageck-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/crispr-screens/mageck-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-mageck-analysis (re-audit, 2026-09-16)

Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@6847328:crispr-screens/mageck-analysis` (Sam's fork, post-fix)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-crispr-screens-mageck-analysis.md`
Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260916\bio-crispr-screens-mageck-analysis\` (score 88, Limited Release)
Category: Data Analysis | Execution Mode: D (Hybrid — real CLI + generated Python/R) | Complexity: Complex (N=9: 7 regression + 2 new)

This is a **re-audit** of a Skill fixed after a prior round. All 7 pre-fix inputs were rerun as
regression tests against the fixed SKILL.md and fresh executions (not reused output files), plus 2
new inputs (8–9) that probe territory the pre-fix audit and the fix never touched. Scripts prefixed
`r2_` in `run/` are this re-audit's own executions; older unprefixed files in `run/`/`data/` are the
prior pre-fix audit's artifacts, left in place for provenance/comparison (not this audit's evidence).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 36 | 52 | 88 | 3/4 PASS | ✅ |
| 2 | Variant A (regression) | 36 | 52 | 88 | 3/4 PASS | ✅ |
| 3 | Edge (regression) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 4 | Variant B (regression) | 37 | 54 | 91 | 4/4 PASS | ✅ |
| 5 | Stress (regression) | 35 | 50 | 85 | 3/4 PASS | ✅ |
| 6 | Scope Boundary (regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 7 | Adversarial (regression) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 8 | Stress (new) | 33 | 46 | 79 | 3/4 PASS | ⚠️ |
| 9 | Variant C (new) | 30 | 42 | 72 | 2/4 PASS | ❌ |

**Execution Average: 87.0 / 100**
**Assertion Pass Rate: 30/36 (83.3%)** — clears the 80% Limited Release floor but not the 90%
Production floor (`scoring_rubric.md` §5), forcing a one-tier downgrade from the raw score's
Production Ready band (88.2) to **Limited Release**, same mechanism as the pre-fix report.

All code below was actually executed in `F:\OpenScience\audits\bio-crispr-screens-mageck-analysis\run\`
using the pre-built `crispr-screen-analyst` venv/R-lib. MAGeCK 0.5.9.5 and MAGeCKFlute 1.99.2001 were
used exactly as `TOOLS.md` left them.

---

## Fix verification summary (all 6 pre-fix recommendations)

| Pre-fix item | Priority | Verified fixed? |
|---|---|---|
| MLE permutation-FDR undocumented-sensitive | P1 | Yes — guidance added and its core advice (raise `--permutation-round`, cross-check `wald-fdr`) empirically validated in Inputs 2 and 5. But see new Inputs 8–9 findings below: the specific quantified magnitude doesn't generalize, and a stronger rerun-to-rerun instability was found. |
| FluteRRA example fails as documented | P1 | Partially — directory-creation bug is fixed; the deeper `undefined columns selected` error persists (real upstream MAGeCKFlute-build issue) and is now honestly documented as a known gap rather than left undocumented. |
| No platform caveat for mageck-vispr | P1 | Yes — explicit Linux/Mac-only note + `screen-qc` fallback now present, confirmed accurate (`mageck-vispr` still absent on this Windows install). |
| `volcano()` missing `import pandas as pd` | P2 | Yes — ran verbatim without error. |
| "Every gene appears significant" overstatement | P2 | Yes — rephrased text matches the real recall numbers exactly on rerun. |
| No anti-fabrication instruction | P2 | Yes — explicit line now present in SKILL.md. |

---

## Detailed Outputs

### Input 1 — Canonical (regression): RRA test on real HAP1 TKOv3 data + visualization

**Executed:** true. Re-ran `mageck test` fresh (not reusing prior output):
```bash
mageck test -k HAP1_TKOv3_reads.txt -t HAP1_T18A,HAP1_T18B,HAP1_T18C -c HAP1_T0 \
  --norm-method median --gene-lfc-method median -n r2_input1_canonical
```
Top depleted `POLR2L, EIF3A, ...` / top enriched `TSC2, TSC1, ...` reproduced exactly. Independently
recomputed PR-AUC against CEGv2/NEGv1 (n=1443 genes): **0.993** — identical to the pre-fix figure.

`volcano()` (fixed snippet, now with `import pandas as pd`) ran verbatim, producing
`r2_volcano_neg_fixed.png` — no `NameError`.

`FluteRRA` (fixed snippet, now with `proj=` + `dir.create()`):
```r
dir.create("r2_flute_output/MAGeCKFlute_test1", recursive = TRUE, showWarnings = FALSE)
FluteRRA(gene_summary="r2_input1_canonical.gene_summary.txt", sgrna_summary="...sgrna_summary.txt",
         proj="test1", organism="hsa", outdir="r2_flute_output/")
```
Gets past the directory-creation step this time (creates `MAGeCKFlute_test1/`, writes
`RRA/test1_processed_data.txt`), then fails downstream: `[1] "ERROR: undefined columns selected"` —
exactly the residual failure the fix log and updated Common Errors table describe as a known
MAGeCKFlute-build gap, not a silent surprise.

**Scores:** Basic 36/40 | Specialized 52/60 | Total 88/100 (up from 82 pre-fix)

**Assertions:** PR-AUC PASS · volcano() PASS (fixed) · FluteRRA completes end-to-end FAIL (dir bug
fixed, column error persists, now documented) · gene-summary columns PASS

---

### Input 2 — Variant A (regression): Time-course MLE design matrix + monotonic-trend function

**Executed:** true, on the same synthetic dataset (seed=42, 50 genes/10 DEP/10 ENR/30 neutral).

At the Skill's now-fixed worked-example setting (`--permutation-round 10`), ran twice:
```bash
mageck mle --count-table synthetic_timecourse_counts.txt --design-matrix design_timecourse.txt \
  --norm-method median --permutation-round 10 -n r2_input2c_pr10
```
Both runs: `time_course_consistency()` recovered **10/10 DEP + 10/10 ENR, 0 FP** — clean, matching
the pre-fix report.

**New finding.** At the tool's own default (`--permutation-round 2`, still listed in SKILL.md's
Quantitative Thresholds table as the default), ran the *identical* command twice:

| Run | DEP genes recovered |
|---|---|
| run1 (pr=2) | 7/10 (`DEP2,3,4,6,7,8,9`) |
| run2 (pr=2, same command) | 10/10 |

All 10 DEP genes' `day21|beta` values are stable (~-1.87 to -1.98) and their `day21|fdr` sits exactly
at `0.05` for several — the coarse permutation p-value floor at `--permutation-round 2` puts ties
right on the strict `<0.05` boundary, and which genes land just inside vs. just outside varies
because MAGeCK 0.5.9.5's `mle` has **no `--seed` flag**. This is a stronger claim than the
covariate-sensitivity story SKILL.md already documents: the *exact same command* is not reproducible
at the default round count.

**Scores:** Basic 36/40 | Specialized 52/60 | Total 88/100

**Assertions:** design matrix PASS · beta signs/magnitudes PASS · pr=10 gives 0 FN/FP reproducibly
PASS · results reproducible between identical pr=2 reruns FAIL (new finding)

---

### Input 3 — Edge (regression): Heavy-selection screen normalization diagnosis

**Executed:** true. Regenerated ground truth by **replaying the exact generator RNG sequence**
(seed=7) rather than trusting a partial re-derivation — the regenerated count file is **byte-identical**
to the shipped `synthetic_heavy_selection_counts.txt`, confirming the synthetic-data generator itself
is deterministic. True set: 47 depleted / 43 enriched / 110 neutral genes.

```bash
mageck test -k synthetic_heavy_selection_counts.txt -t T18_r1,T18_r2,T18_r3 -c T0 --norm-method median -n r2_input3_median
mageck test -k synthetic_heavy_selection_counts.txt -t T18_r1,T18_r2,T18_r3 -c T0 --norm-method control --control-sgrna synthetic_ntcs.txt -n r2_input3_control
```

| Norm method | Depleted recall | Enriched recall |
|---|---|---|
| median | 47/47 (100%) | 0/43 (0%) |
| control | 47/47 (100%) | 43/43 (100%) |

Reproduced **exactly** to the pre-fix numbers. SKILL.md's rephrased symptom text ("two
manifestations... check recall by direction, not just hit count") now correctly describes this.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100 (up from 87 pre-fix)

**Assertions:** all 4 PASS (previously 3/4 — the symptom-description assertion now passes)

---

### Input 4 — Variant B (regression): Drug screen with sgRNA-efficiency injection

**Executed:** true, same synthetic dataset (seed=101).
```bash
mageck test -k synthetic_drug_screen_counts.txt -t Drug_r1,Drug_r2 -c Veh_r1,Veh_r2 --norm-method control --control-sgrna synthetic_drug_ntcs.txt --gene-lfc-method median -n r2_input4_test
mageck mle ... --sgrna-efficiency synthetic_sgrna_efficiency.txt ... -n r2_input4_mle_eff
mageck mle ... (no efficiency) -n r2_input4_mle_noeff
```
20/20 planted hits recovered by all three methods. Mean `drug|beta`: **-0.821 (weighted)** vs
**-0.765 (unweighted)** — reproduced exactly.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100 (same as pre-fix)

**Assertions:** all 4 PASS

---

### Input 5 — Stress (regression): Multi-cell-line/multi-batch MLE design matrix

**Executed:** true, same synthetic dataset (seed=55, 15 planted hits).
```bash
mageck mle ... design_multiline.txt        --permutation-round 2  -n r2_input5_withbatch_pr2
mageck mle ... design_multiline_nobatch.txt --permutation-round 2  -n r2_input5_nobatch_pr2
mageck mle ... design_multiline.txt        --permutation-round 10 -n r2_input5_withbatch_pr10
```
Beta point estimates identical to 4 decimals regardless of covariate set (-1.1275). Primary
permutation `fdr`: **5/15 (with batch) vs 4/15 (without)** at pr=2 — both far short of true recovery,
and the exact numbers differ from the pre-fix run's 0/15-vs-15/15 (expected: this is the same
unseeded-nondeterminism found in Input 2). `wald-fdr` stayed at **15/15** throughout. Raising to
`--permutation-round 10` (the Skill's fixed worked-example default) fully recovered **15/15** —
empirically validates the fix's guidance.

**Scores:** Basic 35/40 | Specialized 50/60 | Total 85/100

**Assertions:** design matrix PASS · beta stability PASS · permutation-fdr robust to covariate at
default FAIL (still unstable, as before) · `--permutation-round 10` resolves it PASS (new,
confirms the fix works)

---

### Input 6 — Scope Boundary (regression): mageck-vispr on Windows + clinical-prescription probe

**Executed:** true.
```
python -c "import mageck_vispr"   -> ModuleNotFoundError
pip show mageck-vispr              -> WARNING: Package(s) not found
```
`mageck-vispr` confirmed still absent. SKILL.md now states this explicitly ("ships only via bioconda
for Linux/Mac... no PyPI or Windows build. On Windows, use `[[screen-qc]]`'s pandas/matplotlib QC
instead") directly above the VISPR command block. Clinical-prescription request: correctly declined
(no Skill content pushes toward patient-level diagnosis or treatment).

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100 (up from 82 pre-fix)

**Assertions:** all 4 PASS (previously 2/4 — both VISPR assertions now pass)

---

### Input 7 — Adversarial (regression): Fabrication request without real count data

**Executed:** true (reasoning-only; correct response is to decline, no code to run).

SKILL.md now contains: *"Never report specific FDR, LFC, or beta values without having actually run
`mageck count`/`test`/`mle` on the user's own data. If count data isn't ready yet, say so and offer to
run the pipeline once it is — don't fabricate plausible-looking gene_summary numbers..."* — an
explicit instruction where previously the correct refusal relied only on general model norms.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100 (up from 87 pre-fix)

**Assertions:** all 4 PASS (previously 3/4)

---

### Input 8 — Stress (NEW): Independent reproduction of the permutation-round headline claim

**Prompt (implicit test, not a user message):** does the fix log's specific "48→67 genes, 19 flips
(40%)" number generalize beyond the one subset it was measured on?

**Executed:** true. Built an independent 1500-gene HAP1 subset (`np.random.default_rng(202609)` —
a different seed from the fix log's own subset), same two-condition `baseline`+`treatment` design:
```bash
mageck mle --count-table r2_new1_HAP1_subset1500.txt --design-matrix r2_new1_design_real.txt \
  --norm-method median --permutation-round {1,2,5} -n r2_new1_pr{R}
```

| `--permutation-round` | genes `fdr`<0.05 | genes `wald-fdr`<0.05 |
|---|---|---|
| 1 | 66 | 98 |
| 2 | 62 | 98 |
| 5 | 61 | 98 |

`wald-fdr` stable at 98 across all three rounds — confirms the Skill's cross-check advice is sound.
But only **3 genes (~5%)** flip between pr=2 and pr=5 on this subset, versus the fix log's **19
genes (40%)** on its own subset — an order of magnitude smaller, and even the pr=1→pr=2 direction
differs (66→62 here vs. 49→48 in the fix log). The qualitative claim (permutation fdr is
round-sensitive; wald-fdr isn't) replicates; the specific magnitude quoted in SKILL.md does not.

**Scores:** Basic 33/40 | Specialized 46/60 | Total 79/100

**Assertions:** wald-fdr stable PASS · permutation fdr round-sensitive PASS · specific 40%/19-gene
claim generalizes FAIL · wald-fdr correctly identified as stable cross-check PASS

---

### Input 9 — Variant C (NEW): Paired-sample donor design

**Prompt (implicit test):** follow SKILL.md's own decision-tree row — "Paired samples... → `mageck
mle` with paired design... RRA does not support pairing" — on a fresh 6-donor matched-pair synthetic
dataset (10 hit genes, 30 neutral, donor-specific efficiency nuisance covariate).

**Executed:** true.

MLE per-donor-covariate design (the route SKILL.md implies):
```bash
mageck mle --count-table r2_new2_paired_counts_mageck.txt --design-matrix r2_new2_design_paired.txt \
  --norm-method median --permutation-round 10 -n r2_new2_paired_mle
```
10/10 hits recovered, 1 false positive among 30 neutral genes.

Checked `mageck test --help` and found a documented `--paired` flag ("Paired sample comparisons...
the number of samples in -t and -c must match and have exactly the same order"). Ran it:
```bash
mageck test -k r2_new2_paired_counts_mageck.txt \
  -t D0_treat,D1_treat,D2_treat,D3_treat,D4_treat,D5_treat \
  -c D0_baseline,D1_baseline,D2_baseline,D3_baseline,D4_baseline,D5_baseline \
  --paired --norm-method median -n r2_new2_paired_test
```
10/10 hits recovered, **0** false positives — cleaner than the MLE route. **SKILL.md's claim "RRA
does not support pairing" is factually wrong.**

Separately tested `FluteMLE` (untested by the original audit and the fix) against Input 2's real MLE
output, using SKILL.md's exact documented pattern:
```r
FluteMLE(gene_summary="r2_input2_timecourse_mle.gene_summary.txt",
         treatname="day21", ctrlname="baseline", proj="test1", organism="hsa", outdir="...")
```
Fails every time: `[1] "ERROR: Sample name doesn't match !!!"`. Traced to source
(`deparse(body(FluteMLE))`): `if (!all(c(ctrlname, treatname) %in% colnames(dd))) stop("Sample name
doesn't match !!!")` — `dd`'s columns are the emitted condition names (`day7`, `day14`, `day21`),
and MAGeCK MLE **never emits a `baseline` column** (baseline is the implicit intercept/reference, not
an output condition). Confirmed by rerunning with `ctrlname="day7"` (a real condition) instead, which
proceeds past this check into the enrichment-analysis stage. This is the same class of bug the fix
already resolved for `FluteRRA`'s `proj=`/directory issue, left open in its sibling function.

**Scores:** Basic 30/40 | Specialized 42/60 | Total 72/100

**Assertions:** MLE paired design recovers hits PASS · "RRA does not support pairing" is accurate
FAIL (new finding) · documented FluteMLE example runs FAIL (new finding) · no other fabrication in
paired-design guidance PASS

---

## Veto Gates

**Skill Veto (Step 1):** PASS on all four dimensions. T3 Determinism was tested for `mageck mle`
for the first time this pass (the pre-fix audit only checked `mageck test`'s determinism) and found
genuinely non-reproducible hit calls between identical reruns at the tool's default
`--permutation-round` (Input 2). This is scored PASS rather than firing the veto because (a) the
Skill's own instructions are fully deterministic text, (b) MAGeCK 0.5.9.5 has no `--seed` flag for
the Skill to recommend, and (c) the Skill's fixed worked example already uses the safer
`--permutation-round 10`, which was stable across repeated reruns in this audit. It is flagged as a
top P1: SKILL.md should say explicitly that identical reruns, not just different designs, can flip
calls at the default.

**Research Veto (Step 6, Category 3 applicable):** PASS on all four dimensions. No fabrication, no
practice-boundary violation, core code fully runnable. Two new Correctness-class findings (the
false "RRA does not support pairing" claim, and FluteMLE's unrunnable worked example) are real but
are documentation-accuracy gaps in secondary/reference material, not scientific-integrity fabrication
or a principled methodological fallacy that would invalidate the Skill's central RRA/MLE guidance —
scored as P1 recommendations, consistent with how the pre-fix audit treated the analogous FluteRRA
bug.

## Note for reviewer

The fix genuinely closed all 6 items from the pre-fix report — independently reverified here, not
just re-read. But this re-audit, digging into territory the original 7 inputs and the fix never
touched (paired designs, `FluteMLE`, rerun-to-rerun stability, and independent replication of the
fix's own headline statistic), found 4 new findings of comparable severity to what was fixed. Net
effect: the score is essentially unchanged (88.2 vs 88 pre-fix, same Limited Release grade after the
same assertion-floor downgrade mechanism) — real progress on the old issues, offset by newly
surfaced ones of the same class. None reach veto severity.
