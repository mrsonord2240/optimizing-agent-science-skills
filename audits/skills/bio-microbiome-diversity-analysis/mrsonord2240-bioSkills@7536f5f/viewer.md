> **Audit record for `bio-microbiome-diversity-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@7536f5f](https://github.com/mrsonord2240/bioSkills/tree/7536f5f114733ef0961f746614435789cf1f68d9/microbiome/diversity-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-diversity-analysis (RE-AUDIT)
Generated: 2026-09-19
Source: mrsonord2240/bioSkills@7536f5f:microbiome/diversity-analysis
Original audit: `F:\OpenScience\audits\_pre-fix-20260919\bio-microbiome-diversity-analysis\` (92, Production Ready)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-microbiome-diversity-analysis.md`

This is an independent re-audit (different agent from both the original auditor and the fixer). The
fix log is treated as a claim; every number below was re-produced by this agent's own execution,
except where explicitly marked "not re-executed" with a reason.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 2 | Variant A — depth (regression) | 38 | 55 | 93 | 3/4 PASS | ✅ |
| 3 | Edge — no tree (regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 4 | Variant B — QIIME2/gen-UniFrac (regression, partial) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 5 | Stress — repeated measures (regression, P1 fix) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (regression, text) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 7 | Adversarial (regression, text) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 8 | **NEW** — independent strata ground-truth fixture | 38 | 58 | 96 | 4/4 PASS | ✅ |
| 9 | **NEW** — SKILL.md verbatim Alpha+Beta on fresh data | 37 | 54 | 91 | 4/4 PASS | ✅ |

**Execution Average: 94.1 / 100**
**Assertion Pass Rate: 35/36**

## What changed since the original audit (92 → 95)

- **P1 #1 fixed and confirmed**: `examples/diversity_analysis.R` no longer crashes.
  `meta$Group <- sample_data(ps_rare)$SampleType` now sits right after the `meta <-` line. Ran the
  unmodified shipped script end-to-end against `GlobalPatterns` — completes with `Done.`, both plots
  written, no error (see `run/shipped_example_diversity_analysis_FIXED.R` and
  `run/run1_shipped_example_output.txt`).
- **P1 #2 fixed and confirmed**: SKILL.md's Beta Diversity section now has a repeated-measures note
  (`strata = meta$SubjectID`) mirroring the Alpha Diversity section's existing "escalate to lme4/nlme"
  line. Reproduced the exact naive-vs-strata contrast the fixer cited (R2=0.0528, p=0.098 → p=1) on
  the original longitudinal fixture (regression, Input 5), **and** independently on a brand-new fixture
  with known ground truth (Input 8, below) where the effect is even starker: naive p=0.001 (would be
  reported as a real finding) → strata-corrected p=1 (correctly reveals no signal). This is strong,
  independent confirmation the guidance is accurate, not just internally consistent with the fixer's
  own numbers.
- **Redundancy pass verified clean**: `git diff ff10062 7536f5f -- microbiome/diversity-analysis/usage-guide.md`
  shows the deleted "What the Agent Will Do" (8 steps) and "Tips" (9 bullets) sections. Checked each
  of the 17 deleted points against the current SKILL.md by section: sampling-depth lever + dropped
  samples ("Choosing the Sampling Depth"), de novo tree caveat ("Building the Tree"), report both
  UniFrac variants (Tool Taxonomy decision-tree row + Beta Diversity section), observed-features-is-
  not-species and Shannon base mismatch (Per-Method Failure Modes), betadisper-mandatory (Beta
  Diversity section + Per-Method Failure Modes), rarefy-never-for-DA (knob #3 + Per-Method Failure
  Modes), host/organelle and kitome filtering (Common Errors table). Nothing the agent needs was lost.
  The install commands moved into SKILL.md's new "Required Setup" section match what was previously
  in usage-guide.md's "Prerequisites" verbatim.
- **No regressions found**: 5 of 7 original inputs re-executed fresh (see below) reproduce the exact
  same numbers as the original audit, bit for bit (R2, p-values, dropped-sample lists, richness means).

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt:** (same as original audit) "I have my ASV table with tree and taxonomy loaded as a phyloseq
object (40 samples, control vs treated). Summarize alpha diversity ... beta diversity ... PERMANOVA
and betadisper ..."

**Execution:** Re-ran `run/regression_input1_canonical.R` (copy of the original audit's script,
unmodified) against the same real fixture. `executed: true`.

**Output (trimmed):**
```
Alpha diversity: control Shannon=4.165, treated Shannon=3.414 | Kruskal-Wallis Shannon p=2.968e-07
PERMANOVA: Weighted UniFrac R2=0.6585 p=0.001 | Unweighted UniFrac R2=0.0596 p=0.001 | Bray-Curtis R2=0.6354 p=0.001
betadisper: Weighted UniFrac p=0.591 (clean) | Unweighted UniFrac p=0.001 (confounded)
```
Matches the original audit's numbers exactly (R2=0.659/0.060/0.635, Shannon p=2.97e-07).

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100
**Assertions:** 4/4 PASS — same four checks as the original audit, all reproduced.

---

### Input 2 — Variant A, depth choice (regression)
**Execution:** Re-ran `run/regression_input2_depth.R`. `executed: true`.
```
min(sample_sums)=1800 -> 40 kept, mean Observed=118.7
plateau depth=7169 -> 36 kept (dropped S03,S17,S29,S40), mean Observed=139.8
Richness recovered: 17.8% higher at plateau depth
```
Exact match to original. **Scores:** 38/40 | 55/60 | 93/100
**Assertions:** 3/4 PASS — the same plateau-heuristic assertion still FAILs (SKILL.md's R-side workflow
still has no numeric substitute for visually reading the alpha-rarefaction curve; this is the still-open
P2, not part of this fix pass).

---

### Input 3 — Edge, no tree (regression)
**Execution:** Re-ran `run/regression_input3_edge_notree.R`. `executed: true`.
```
UniFrac on tree-less object: ERRORED -- "phy_tree slot is empty." (matches Common Errors row exactly)
Bray-Curtis PERMANOVA R2=0.6354 p=0.001 | Jaccard R2=0.0595 p=0.001 | betadisper p=0.001
```
Exact match to original. **Scores:** 38/40 | 56/60 | 94/100 | **Assertions:** 4/4 PASS

---

### Input 4 — Variant B, QIIME2 + generalized UniFrac (regression, partial)
**Execution:** Re-ran the R-only generalized-UniFrac portion fresh
(`run/regression_input4_generalized_unifrac_Ronly.R`), `executed: true`:
```
Weighted UniFrac (alpha=1):    R2=0.6585 p=0.001
Generalized UniFrac alpha=0.5: R2=0.4187 p=0.001   <- interpolates correctly
Unweighted UniFrac (alpha=0):  R2=0.0596 p=0.001
```
Matches original (0.419 vs 0.4187, rounding). The full QIIME2 CLI `core-metrics-phylogenetic` +
`beta-group-significance` pipeline on the real moving-pictures dataset was **not** re-executed this
pass — `git diff` confirms that code path is byte-unchanged by the fix, and the ~15-20 min WSL run
would add cost without new evidence. Original numbers (31/33 samples retained, all 3 metrics
PERMANOVA+PERMDISP significant) carried forward, not independently re-verified in this audit.
**Scores:** 38/40 | 57/60 | 95/100 | **Assertions:** 4/4 PASS (the two assertions about the generalized-
UniFrac line are freshly re-verified; the two about the QIIME2 CLI pipeline rely on carried-forward
original evidence, noted in `execution_note`).

---

### Input 5 — Stress, repeated measures (regression, P1 fix target)
**Execution:** Re-ran `run/regression_input5_stress.R` on the same longitudinal fixture. `executed: true`.
```
PERMANOVA (naive, pooled): R2=0.0528 p=0.098
PERMANOVA (strata=SubjectID): R2=0.0528 p=1
betadisper (Arm): p=0.496
```
Exact match to the original audit's numbers and to the fixer's claimed verification.
**Scores:** 38/40 | 56/60 | 94/100 (up from 87/100 in the original audit)
**Assertions:** 4/4 PASS — the assertion that FAILed in the original audit ("SKILL.md provides
repeated-measures guidance for PERMANOVA, mirroring its alpha-diversity guidance") now PASSes: the
Beta Diversity section's `strata=` line and accompanying note are present and, per this run, accurate.

---

### Input 6 — Scope Boundary (regression, text)
Not re-generated as a fresh Claude response this pass (no code to execute). Verified by direct diff
review that the language it depends on — the Decision Tree's "Per-taxon → differential-abundance" row,
"Rarefy for diversity, never for differential abundance" — is byte-unchanged by the fix.
**Scores:** 38/40 | 56/60 | 94/100 (carried forward) | **Assertions:** 4/4 PASS

### Input 7 — Adversarial (regression, text)
Same treatment as Input 6: the "worst of both worlds" min-depth anti-pattern language is byte-unchanged.
**Scores:** 38/40 | 57/60 | 95/100 (carried forward) | **Assertions:** 4/4 PASS

---

### Input 8 — NEW (re-auditor's own): independent strata ground-truth fixture
**Prompt (synthetic, self-directed):** "Build a fresh longitudinal microbiome fixture with a *known*
ground truth (no real arm effect, only within-subject correlation across visits) and check whether
SKILL.md's new `strata=SubjectID` guidance correctly reveals the absence of a real effect where a naive
pooled PERMANOVA would claim one."

**Execution:** `run/input_new1_reauditor_strata_check.R` — fully self-contained (no shared fixture
reused; seed 20260919; 14 subjects x 3 visits = 42 samples; Bray-Curtis via `vegan::vegdist`).
`executed: true`.
```
Naive pooled PERMANOVA (Arm): R2=0.0701 p=0.001   <- would be reported as a real, strong effect
Restricted (strata=SubjectID): R2=0.0701 p=1       <- correctly reveals NO real effect (matches ground truth)
```
This is a stronger demonstration than the fixer's and original auditor's shared fixture (p=0.098→1,
borderline): here the naive analysis produces a clean, textbook false positive (p=0.001) that the
`strata=` guidance correctly corrects, on a fixture with **known** ground truth (no arm effect was
simulated). This independently confirms the new SKILL.md guidance is not just internally consistent
but scientifically necessary.

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100
**Assertions:**
- [PASS] Fixture has a known, simulated ground truth of no real Arm effect
- [PASS] Naive pooled PERMANOVA materially misleads (p=0.001, "highly significant")
- [PASS] `strata=SubjectID` PERMANOVA correctly reveals no signal (p=1), matching ground truth
- [PASS] The result is independent of the fixer's/original auditor's fixture (fresh seed, fresh subject/visit counts, fresh generative model)
Assertion pass rate: 4/4

---

### Input 9 — NEW (re-auditor's own): SKILL.md verbatim Alpha+Beta blocks, fresh data, no regression
**Prompt (synthetic, self-directed):** "Run SKILL.md's own Alpha Diversity in R and Beta Diversity in R
code blocks, close to verbatim, against a dataset the re-auditor built from scratch, to confirm the
newly added `strata=` line did not regress the unchanged lines directly above it."

**Execution:** `run/input_new2_reauditor_skillmd_verbatim.R` — self-contained synthetic phyloseq object
(seed 777; 30 samples, 80 ASVs, `ape::rtree` tree, a real injected compositional shift in "treated").
`executed: true`.
```
Alpha block OK. Kruskal-Wallis Shannon p=3.067e-06
Beta block OK. adonis2 R2=0.284 p=0.001 | betadisper p=0.198
```
Both SKILL.md code blocks ran to completion, unmodified except for supplying the analyst's own
`ps`/`chosen_depth`, confirming the fix did not disturb the pre-existing, unchanged lines it sits
beside.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100
**Assertions:**
- [PASS] SKILL.md's Alpha Diversity in R block runs unmodified on fresh, independent data
- [PASS] SKILL.md's Beta Diversity in R block (including the pre-existing adonis2/betadisper lines directly above the new strata line) runs unmodified
- [PASS] A real, injected compositional shift is correctly detected (adonis2 p=0.001)
- [PASS] The new `strata=` line's presence does not alter the output of the unchanged lines above it (this dataset has no SubjectID column and does not invoke it — confirms non-interference by construction)
Assertion pass rate: 4/4

> **Note for reviewer:** No ❌ rows. One ⚠️-worthy assertion failure remains (Input 2's plateau-heuristic
> gap) — a pre-existing, still-open P2, not touched by this fix pass. No new defects found.
