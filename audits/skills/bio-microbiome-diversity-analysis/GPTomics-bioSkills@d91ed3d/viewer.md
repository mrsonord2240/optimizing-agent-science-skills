> **Audit record for `bio-microbiome-diversity-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/microbiome/diversity-analysis) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-diversity-analysis
Generated: 2026-09-19
Source: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:microbiome/diversity-analysis

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 2 | Variant A | 38 | 55 | 93 | 3/4 PASS | ✅ |
| 3 | Edge | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 4 | Variant B | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 5 | Stress | 35 | 52 | 87 | 3/4 PASS | ✅ |
| 6 | Scope Boundary | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 7 | Adversarial | 38 | 57 | 95 | 4/4 PASS | ✅ |

**Execution Average: 93.3 / 100**
**Assertion Pass Rate: 26/28**

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have my ASV table with tree and taxonomy loaded as a phyloseq object (40 samples,
control vs treated). Summarize alpha diversity (Observed, Shannon, InvSimpson, Faith PD) and beta
diversity (weighted+unweighted UniFrac, Bray-Curtis), test the group difference with PERMANOVA and
betadisper, and tell me if diversity differs between groups."

**Execution:** Mode A. Real R run (`run/input1_canonical.R`) against the real fixture phyloseq object
(`datagen/asvtable/phyloseq_object.rds`, 200 taxa x 40 samples, real tree + taxonomy, control/treated
groups) following SKILL.md's exact pattern (`rarefy_even_depth`, `estimate_richness`, `picante::pd`,
`UniFrac`, `adonis2`, `betadisper`). `executed: true`.

**Output (trimmed):**
```
Chosen depth (10th pctile): 7169 | Samples dropped: 4 -> S03, S17, S29, S40
Alpha diversity: control Shannon=4.17 (exp=64.5), treated Shannon=3.41 (exp=30.5)
Kruskal-Wallis Shannon: chi-sq=26.27 p=2.97e-07 | Observed: p=3.89e-07 | Faith PD: p=1.52e-06
PERMANOVA: Weighted UniFrac R2=0.659 p=0.001 | Unweighted UniFrac R2=0.060 p=0.001 | Bray-Curtis R2=0.635 p=0.001
betadisper: Weighted UniFrac p=0.591 (clean location effect) | Unweighted UniFrac p=0.001 (dispersion-confounded)
```

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100

**Assertions:**
- [PASS] Output declares the sampling depth AND the exact dropped-sample list, per SKILL.md's mandatory reporting requirement.
- [PASS] Output reports both weighted AND unweighted UniFrac PERMANOVA rather than cherry-picking the significant one.
- [PASS] Output pairs every PERMANOVA with betadisper and correctly distinguishes a clean location effect (weighted UniFrac, betadisper p=0.591) from a dispersion-confounded result (unweighted UniFrac, betadisper p=0.001) — a genuine, non-trivial distinction on real data, exactly the failure mode SKILL.md's "PERMANOVA dispersion" section warns about.
- [PASS] Faith PD and Shannon are real, non-placeholder numeric values that differ meaningfully and significantly between groups.
Assertion pass rate: 4/4

---

### Input 2 — Variant A (sampling-depth choice)
**Prompt:** "Pick a rarefaction sampling depth from my feature table and tell me which samples it
drops."

**Execution:** Mode A. Real R run (`run/input2_variantA_depth_min_vs_plateau.R`) quantifying
SKILL.md's claim that `min(sample_sums)` is "the worst of both worlds" against the same real fixture.
`executed: true`.

**Output (trimmed):**
```
Depth range: 1800 - 59288 (median 19470.5)
min(sample_sums) = 1800 -> all 40 samples kept, mean Observed richness = 118.7
plateau depth (7169, 10th pctile) -> 36 samples kept (4 dropped: S03,S17,S29,S40), mean Observed richness = 139.8
Richness recovered at plateau depth: 17.8% higher than the min-depth choice
```

**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100

**Assertions:**
- [PASS] Output reports the exact dropped-sample list at the chosen depth, not just a count.
- [PASS] Output explicitly avoids recommending `min(sample_sums)`, matching SKILL.md's "worst of both worlds" guidance.
- [PASS] Output quantifies the real richness cost of the min-depth choice (118.7 vs 139.8 mean Observed, 17.8% difference) rather than a generic warning.
- [FAIL] Output substitutes a fixed 10th-percentile heuristic for the SKILL's gold-standard method ("find where the alpha-rarefaction curve plateaus") without confirming the chosen depth actually sits on a richness plateau — SKILL.md's R-side workflow gives no numeric heuristic as a substitute for visually reading the alpha-rarefaction curve, so an agent has to improvise one.
Assertion pass rate: 3/4

---

### Input 3 — Edge (no phylogenetic tree)
**Prompt:** "I don't have a tree for my ASVs — can you still give me alpha and beta diversity and
test my two groups?"

**Execution:** Mode A. Real R run (`run/input3_edge_notree.R`) on a tree-stripped copy of the same
fixture, testing SKILL.md's documented Common-Errors fallback path. `executed: true`.

**Output (trimmed):**
```
Has tree after stripping: FALSE
Alpha diversity (non-phylogenetic) computed OK: Observed/Shannon by group
UniFrac on tree-less object: ERRORED as documented -- "phy_tree slot is empty."
Bray-Curtis PERMANOVA: R2=0.635 p=0.001 | Jaccard PERMANOVA: R2=0.060 p=0.001
Bray-Curtis betadisper: p=0.001 (dispersion-confounded, same caveat applies to the non-phylogenetic fallback)
```

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100

**Assertions:**
- [PASS] `UniFrac()` on a tree-less phyloseq object errors with a specific, diagnosable message matching SKILL.md's Common Errors row exactly ("no `phy_tree` slot ... attach a tree").
- [PASS] Non-phylogenetic alpha (Observed/Shannon) and beta (Bray-Curtis/Jaccard) diversity are still computed successfully as a documented fallback.
- [PASS] The fallback Bray-Curtis PERMANOVA is still correctly paired with betadisper, and correctly flags a significant dispersion confound.
- [PASS] The Skill fails loudly with a clear message rather than silently returning a wrong/garbage UniFrac value.
Assertion pass rate: 4/4

---

### Input 4 — Variant B (QIIME2 CLI core-metrics-phylogenetic + generalized UniFrac)
**Prompt:** "My reads are real V4 16S single-end amplicon data (QIIME2's moving-pictures tutorial
dataset, 4 body sites). Run the QIIME2 core-metrics-phylogenetic workflow end to end — pick a
sampling depth, build a tree, compute all four alpha and four beta metrics — and test whether
community composition differs by body site with PERMANOVA and permdisp. Also compute generalized
UniFrac (alpha=0.5) in R and tell me where it sits relative to weighted and unweighted."

**Execution:** Mode A/CLI. Real, full QIIME2 2024.10.1 pipeline in the WSL `qiime2-amplicon-2024.10`
env against the real moving-pictures dataset (Caporaso et al., 33 samples, 4 body sites: gut, left
palm, right palm, tongue): `tools import` (EMPSingleEndSequences) -> `demux emp-single` ->
`dada2 denoise-single` (trunc-len 120) -> `phylogeny align-to-tree-mafft-fasttree` ->
`diversity core-metrics-phylogenetic` (sampling depth 1103, the dataset's standard tutorial depth) ->
`diversity beta-group-significance` (permanova + permdisp, pairwise) on weighted/unweighted
UniFrac and Bray-Curtis by `body-site`. Plus a real R run of SKILL.md's verbatim generalized-UniFrac
line (`GUniFrac::GUniFrac(..., alpha=0.5)`) on the R fixture. `executed: true`.

**Output (trimmed):** Full numbers in `run/qiime2_beta_significance_results.txt`.

```
Rarefied sample size: 31 of 33 (2 samples dropped at depth 1103 -- confirms the silent-drop
behavior on a second, independent real dataset, not just the R fixture)

PERMANOVA by body-site (4 groups):
  Weighted UniFrac:   pseudo-F=19.76  p=0.001
  Unweighted UniFrac: pseudo-F=9.32   p=0.001
  Bray-Curtis:        pseudo-F=7.95   p=0.001

PERMDISP by body-site (mandatory companion check):
  Weighted UniFrac:   F=2.87   p=0.026  (significant)
  Unweighted UniFrac: F=13.78  p=0.002  (strongly significant)
  Bray-Curtis:        F=4.99   p=0.003  (significant)

SKILL.md verbatim generalized-UniFrac (GUniFrac::GUniFrac alpha=0.5) line ran without modification:
  Weighted UniFrac (alpha=1):    R2=0.659 p=0.001
  Generalized UniFrac alpha=0.5: R2=0.419 p=0.001   <- correctly interpolates between the two
  Unweighted UniFrac (alpha=0):  R2=0.060 p=0.001
```

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100

**Assertions:**
- [PASS] The full `core-metrics-phylogenetic` CLI pipeline (SKILL.md's central documented tool) runs to completion on real 16S data, producing all four alpha vectors and four beta distance matrices as documented.
- [PASS] The sampling-depth-drops-samples behavior is confirmed on a second, independent real dataset (33 -> 31 samples at the tutorial's standard depth), not just the R fixture.
- [PASS] Every beta metric shows BOTH a significant PERMANOVA and a significant PERMDISP on this real, dramatic body-site effect -- correctly following SKILL.md's own rule ("if betadisper is significant the adonis2 result is ambiguous — state it"), an agent must report even this obvious, textbook-strong biological difference as location-and/or-dispersion rather than a clean location-only effect.
- [PASS] The generalized-UniFrac verbatim SKILL.md code line runs unmodified and produces a result that correctly interpolates between weighted and unweighted UniFrac, exactly as the Decision Tree table claims ("alpha=0.5 compromise").
Assertion pass rate: 4/4

---

### Input 5 — Stress (repeated-measures / longitudinal design)
**Prompt:** "I have a longitudinal microbiome study — 3 timepoints per subject (baseline/week4/week8),
placebo vs treatment arms. Give me alpha diversity across visits, and test whether beta diversity
(weighted UniFrac) differs by treatment arm with PERMANOVA."

**Execution:** Mode A. Real R run (`run/input5_stress_repeated_measures.R`) on the real longitudinal
fixture (`datagen/asvtable/long_phyloseq.rds`, 36 samples, 12 subjects x 3 visits, placebo/treatment).
`executed: true`.

**Output (trimmed):**
```
Naive Kruskal-Wallis Shannon ~ Arm (pools all 3 visits, ignores repeated measures): p=0.309
Mixed model (lme4, Subject random effect): Arm effect p=0.32 (not significant)
PERMANOVA (naive, pseudo-replicated, all 3 visits pooled): R2=0.053 p=0.098
PERMANOVA (restricted permutations, strata=SubjectID): R2=0.053 p=1
betadisper (Arm): p=0.496
```

**Scores:** Basic: 35/40 | Specialized: 52/60 | Total: 87/100

**Assertions:**
- [PASS] Alpha and beta diversity are computed correctly on the repeated-measures fixture.
- [FAIL] SKILL.md provides repeated-measures guidance ("escalate to lme4/nlme for covariates or repeated measures") only in the Alpha Diversity section; the Beta Diversity / PERMANOVA section and its code block have no mention of non-independence, pseudo-replication, or vegan's `strata=` argument anywhere in the Skill.
- [PASS] When restricted permutations (`strata=SubjectID`) are correctly applied, the PERMANOVA conclusion changes materially (naive p=0.098 -> corrected p=1), demonstrating the pseudo-replication risk is real and quantifiable on this exact design, not theoretical.
- [PASS] The qualitative conclusion (no significant Arm effect) does not flip to a false positive in this instance, but the naive p-value materially overstates the evidence (0.098, "borderline/trending") relative to the corrected analysis (p=1, no signal).
Assertion pass rate: 3/4

---

### Input 6 — Scope Boundary (per-taxon redirect)
**Prompt:** "Beta diversity looks different between my control and treated groups (PERMANOVA
p=0.001 on weighted UniFrac). Which specific ASVs/species are driving that difference? Give me a
ranked list of taxa that are significantly enriched in the treated group with p-values."

**Execution:** Mode A (text/routing response; see `run/input6_scope_boundary_response.md` for the
full simulated response). `executed: true` (no code required or generated — correctly so).

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100

**Assertions:**
- [PASS] Output does not perform per-taxon significance testing itself.
- [PASS] Output explicitly redirects to differential-abundance, matching SKILL.md's frontmatter and Decision Tree row ("Per-taxon 'which bug changed' -> differential-abundance").
- [PASS] Output correctly warns against reusing the rarefied table for DA ("Rarefy for diversity, never for differential abundance").
- [PASS] Output offers an in-scope compositional alternative (RPCA loadings) rather than a flat refusal.
Assertion pass rate: 4/4

---

### Input 7 — Adversarial (min-depth anti-pattern request)
**Prompt:** "My samples have wildly different sequencing depths (1800 to 59288 reads). To avoid
losing any samples in rarefaction, just rarefy everyone to the minimum depth (1800) and give me
Shannon diversity by group."

**Execution:** Mode A (text response grounded in Input 2's real numbers; see
`run/input7_adversarial_response.md`). `executed: true`.

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100

**Assertions:**
- [PASS] Output does not blindly comply with the min(sample_sums) request — pushes back with the SKILL.md-documented rationale before proceeding.
- [PASS] Output quantifies the actual cost/benefit on the user's own numbers (18% richness difference, 4 dropped samples) rather than a generic warning.
- [PASS] Output reports the specific dropped-sample list, matching SKILL.md's mandatory reporting instruction.
- [PASS] Output remains forgiving — still offers the user's originally requested min-depth version rather than a flat refusal.
Assertion pass rate: 4/4

> **Note for reviewer:** No ❌ rows. The two ⚠️-worthy assertion failures (Input 2, Input 5) are both
> real, reproducible documentation gaps rather than execution failures — see recommendations below.
