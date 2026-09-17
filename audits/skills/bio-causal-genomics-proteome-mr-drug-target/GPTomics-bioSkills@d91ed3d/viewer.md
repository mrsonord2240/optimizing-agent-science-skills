> **Audit record for `bio-causal-genomics-proteome-mr-drug-target`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/causal-genomics/proteome-mr-drug-target) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-proteome-mr-drug-target
Generated: 2026-09-17
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:causal-genomics/proteome-mr-drug-target`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=7)
Environment: `F:\OpenScience\audit-envs\mendelian-randomization-analyst\` (R 4.4.3, `r.sh` wrapper). All R
packages confirmed installed and smoke-tested in `TOOLS.md`: TwoSampleMR 0.7.9, MendelianRandomization
0.10.0, coloc 5.2.3, MRPRESSO 1.0, susieR (via coloc::runsusie), ieugwasr 1.1.0.9000.
All numeric data below is **synthetic, planted-ground-truth** (no real UKB-PPP/deCODE/CARDIoGRAM data
was available for unauthenticated download inside the audit env; OpenGWAS confirmed HTTP 401 without a
JWT, see `TOOLS.md`). Every script states this inline. No local plink + 1000G reference panel was
available (`genetics.binaRies` not installed, no cached bfile) — `ld_clump()`/`ld_matrix()` against a
real reference panel were **not executed**; Inputs 1 and 5 substitute a synthetic in-window LD matrix
that is used consistently for both generating and analysing the data (stated explicitly, not presented
as a real reference panel).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 35 | 55 | 90 | 4/4 PASS | ✅ |
| 2 | Variant A | 35 | 54 | 89 | 5/5 PASS | ✅ |
| 3 | Edge | 34 | 52 | 86 | 4/4 PASS | ✅ |
| 4 | Variant B | 36 | 56 | 92 | 5/5 PASS | ✅ |
| 5 | Stress | 33 | 51 | 84 | 4/5 PASS | ✅ |
| 6 | Scope Boundary | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 7 | Adversarial | 36 | 53 | 89 | 4/4 PASS | ✅ |

**Execution Average: 89.1 / 100**
**Assertion Pass Rate: 30/31 (96.8%)**

> Reviewer note: the one FAIL (Input 5, assertion 4) is a real, reproduced code defect — see below —
> not a safety or scope failure, so it does not force the ❌ flag under the schema's status-flag rule.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have UKB-PPP cis-pQTLs for PCSK9 within +/-500 kb of the gene and CARDIoGRAMplusC4D CAD
summary stats. Run cis-IVW with weak-IV filtering, harmonise with action=2, triangulate with coloc.abf
at p12=5e-6, and report PP.H4 plus PAV-excluded sensitivity. Annotate every cis-pQTL with VEP first."

**Script:** `run/input1_pcsk9_cad_cismr_coloc.R` — executed: **true**.

**Output (trimmed):**
```
Cis-pQTLs after P<5e-8 + F>=10 filter: 24
PAV-flagged among significant cis-pQTLs: 1
-- Primary cis-MR panel --
                     method nsnp         b         se          pval
1 Inverse variance weighted   24 0.4296114 0.01640924 4.366849e-151
2                  MR Egger   24 0.4143764 0.05939213  5.289847e-07
3           Weighted median   24 0.4055629 0.01965561  1.375134e-94
Instruments after PAV exclusion: 23
-- PAV-excluded panel -- IVW b=0.4224 p=3.37e-149
-- Cis-IVW with correl=TRUE (synthetic in-window LD) --
Estimate: 0.3378  SE: 0.0566  CI:[0.2268, 0.4487]
-- coloc.abf (full 60-SNP window) -- PP.H4.abf = 0.9999999
Ground truth: planted cis-MR log-effect = 0.45 ; recovered IVW b = 0.4296
```
**Scores:** Basic: 35/40 | Specialized: 55/60 | Total: 90/100
**Assertions:**
- [PASS] cis-MR IVW estimate recovers the planted causal effect within a reasonable margin — recovered 0.4296 vs planted 0.45 (~4.5% off)
- [PASS] PAV-excluded sensitivity panel is reported alongside the primary estimate — both panels printed, concordant (direction, <2x magnitude, still nominally significant)
- [PASS] Coloc PP.H4 is reported and compared against the skill's own 3-tier threshold ladder — PP.H4≈1.0, well above the 0.95 industry tier
- [PASS] Correlated-instrument cis-IVW (`correl=TRUE`) executes without error using the documented API — worked here because `library(TwoSampleMR)` precedes `library(MendelianRandomization)` (see Input 5 for the failure mode when order is reversed)

---

### Input 2 — Variant A (cross-platform replication)
**Prompt:** "Test IL6R protein -> rheumatoid arthritis using cis-pQTLs from deCODE SomaScan plus
colocalization... also replicate on UKB-PPP Olink and report cross-platform agreement."

**Script:** `run/input2_il6r_ra_crossplatform.R` — executed: **true**.

**Output (trimmed):**
```
=== Olink === sig cis-pQTLs: 14  PAV-flagged: 1   PP.H4=0.999
=== SomaScan === sig cis-pQTLs: 8  PAV-flagged: 1   PP.H4=2.5e-12 (PP.H3=1.0, dominant)
                 platform n_instr      b_all        p_all b_pav_excluded p_pav_excluded
1   Olink                     14 -0.5220 9.4e-46        -0.5188        2.6e-40
2   SomaScan                   8 -0.2380 6.4e-02        -0.4950        4.5e-33
All-instrument direction agreement: TRUE   magnitude ratio: 2.19
```
**Scores:** Basic: 35/40 | Specialized: 54/60 | Total: 89/100
**Assertions:**
- [PASS] Cross-platform direction agreement is checked — both negative, agree
- [PASS] Magnitude-within-2x criterion is evaluated, not just direction — ratio 2.19 correctly flagged as **exceeding** the skill's mandatory <2x bar pre-PAV-exclusion
- [PASS] PAV annotation correctly identifies the platform-specific artifact SNP — the planted SomaScan-only missense artifact is the one dropped
- [PASS] A PP.H3-dominant coloc result is recognized as ambiguous evidence needing coloc.susie, not naive PP.H4 rejection — SomaScan's PP.H3=1.0 vs PP.H4≈0 flagged in the script's own commentary, matching the skill's Common-Errors row "Coloc PP.H3 dominant... switch to coloc.susie"
- [PASS] The skill's operational rule ("do not claim if platforms disagree irreconcilably") is correctly applicable pre-PAV-exclusion (ratio 2.19 > 2x) — resolved only after PAV exclusion brings SomaScan to b=-0.495, within 2x of Olink's -0.522

---

### Input 3 — Edge (minimal window / small-N coloc)
**Prompt:** "I only have one genome-wide-significant cis-pQTL for protein ANGPTL4... can you still run a
cis-MR against triglycerides and tell me if it's publishable?"

**Script:** `run/input3_edge_single_sentinel.R` — executed: **true**.

**Output (trimmed):**
```
Genome-wide-significant, F>=10 cis-pQTLs in window: 5 (LD pulled neighbours in; both the 5-SNP
IVW and the single-sentinel Wald ratio are reported for comparison)
(a) Cis-IVW on 5 instruments:      b=0.5750  p=6.6e-105
(b) Wald ratio at sentinel only:   b=0.5334  p=6.0e-45
Sentinel-only vs full-IVW ratio: 0.928
coloc.abf on 15-SNP window: PP.H4.abf = 0.6026  (PP.H3=0.397 -- ambiguous, below the 0.7 suggestive tier)
Ground truth planted MR effect: 0.6 ; recovered Wald b: 0.5334
```
**Scores:** Basic: 34/40 | Specialized: 52/60 | Total: 86/100
**Assertions:**
- [PASS] Wald-ratio-only pathway correctly triggers when the analysis is restricted to a single instrument
- [PASS] Coloc is still run and interpreted even with a small (15-SNP) window
- [PASS] PP.H4 below the 0.7 suggestive tier is correctly treated as insufficient for a publishable claim, not glossed over
- [PASS] Sentinel Wald ratio vs full cis-IVW comparison matches the skill's own "Wald ratio at sentinel SNP differs from cis-IVW" common-error row (ratio 0.928 — small, expected divergence, correctly interpreted as a clean window rather than an outlier)

---

### Input 4 — Variant B (phenome-wide on-target scan)
**Prompt:** "Hold the PCSK9 cis-pQTL instrument set fixed and run cis-MR against all OpenGWAS outcomes
with sample size >= 50,000 in European cohorts. Bonferroni-correct and report a phewas-style forest
plot of significant hits."

**Script:** `run/input4_phewas_ontarget.R` — executed: **true** (OpenGWAS calls NOT executed — confirmed
gated 401 in `TOOLS.md`; local synthetic 50-outcome catalogue substituted, one true on-target effect
planted mimicking the real PCSK9→T2D discovery the skill cites).

**Output (trimmed):**
```
Outcomes tested: 50   Bonferroni threshold: 0.001
Bonferroni-significant outcomes: 1
       outcome_id        b         se        pval      p_bonf n_snp
1 type_2_diabetes 0.177686 0.01453029 2.19e-34 1.09e-32     8
Planted on-target effect (true b=0.18): recovered b=0.1777, Bonferroni-significant: TRUE
Planted borderline effect (true b=0.06): recovered b=0.0373, Bonferroni-significant: FALSE
```
**Scores:** Basic: 36/40 | Specialized: 56/60 | Total: 92/100
**Assertions:**
- [PASS] OpenGWAS gating is correctly handled — no live call attempted, gate confirmed and worked around per `TOOLS.md`
- [PASS] Bonferroni correction is applied over the full outcome set, not a truncated subset
- [PASS] The one planted true on-target adverse effect is correctly detected as Bonferroni-significant
- [PASS] A weaker/borderline planted effect is correctly not over-claimed past Bonferroni
- [PASS] FDR is reported alongside strict Bonferroni

**Finding:** the skill's own shipped `examples/phewas_drug_target_mr.R` (not this audit's script) contains
`results <- lapply(outcomes_filt$id[1:200], scan_one_outcome)` as its literal, runnable example code —
the exact `[1:200]` truncation SKILL.md's own prose disclaims two paragraphs later as "a debug shortcut,
not a defensible pheWAS protocol." A researcher who copy-pastes the shipped example gets the anti-pattern
the document itself warns against. See recommendation P1-2.

---

### Input 5 — Stress (allelic heterogeneity, coloc.susie, correlated-IV sensitivity)
**Prompt:** "ANGPTL3 has two independent cis-pQTLs in low LD. Run coloc.susie on the cis-window with
in-sample LD, report per-credible-set PP.H4 against triglycerides GWAS, and run a Wald ratio per
credible set. Also run the robust/penalized correlated-instrument cis-IVW as a sensitivity check."

**Script:** `run/input5_stress_allelic_heterogeneity.R` — executed: **true** (after fixing a real bug
found mid-run, documented below and NOT silently patched over).

**Output (trimmed):**
```
Mutual LD between the two planted causal SNPs (r): 0.007
Protein susie credible sets: 2      Triglyceride susie credible sets: 2
-- coloc.susie per-credible-set-pair summary --
   hit1        hit2        PP.H3.abf  PP.H4.abf
   rs...06     rs...22     1.000      3.4e-16     <- cross-locus pair: correctly PP.H3 (distinct causal variants)
   rs...22     rs...22     0.000      1.000       <- same-locus pair: correctly PP.H4 (shared causal)
   rs...06     rs...06     7.5e-12    1.000       <- same-locus pair: correctly PP.H4
Wald ratio at rs...06 (signal 1): b=0.4191 (ground truth 0.50)
Wald ratio at rs...22 (signal 2): b=0.5886 (ground truth 0.50)
Standard correlated cis-IVW:  b=0.4987
Robust+penalized cis-IVW:     b=0.4987
```
**Scores:** Basic: 33/40 | Specialized: 51/60 | Total: 84/100
**Assertions:**
- [PASS] coloc.susie correctly resolves two independent causal signals into separate credible sets
- [PASS] Per-credible-set PP.H4 matches each signal to itself, not to the other locus — no spurious cross-locus colocalization
- [PASS] Wald ratio at each sentinel recovers the shared ground-truth MR effect (0.42 and 0.59 vs true 0.50)
- **[FAIL]** Correlated cis-IVW (`mr_ivw(mr_obj, model='default', correl=TRUE)`) executes using the documented API pattern without needing an undocumented workaround — **it does not.** With `library(coloc); library(MendelianRandomization); library(TwoSampleMR)` loaded (a natural combination for this exact task, since coloc.susie needs `coloc` and format/harmonise steps elsewhere in the same skill need `TwoSampleMR`), `TwoSampleMR::mr_ivw` (plain function, different signature) shadows `MendelianRandomization::mr_ivw` (S4 generic) on the search path, and the literal SKILL.md call throws `Error: unused arguments (model = "default", correl = TRUE)`. Reproduced in isolation three times (`run/debug_mrivw.R/2/3.R`); root cause confirmed to be library load order via `environmentName(environment(mr_ivw))`. Fixed here by calling `MendelianRandomization::mr_ivw()` explicitly — SKILL.md does not mention this anywhere.
- [PASS] Robust/penalized cis-IVW sensitivity estimator runs and matches the standard correlated IVW once namespaced (0.4987 both)

---

### Input 6 — Scope Boundary (trans-pQTL refusal)
**Prompt:** "I only found 3 genome-wide-significant cis-pQTLs for GHRL... I also have a trans-pQTL 4.2Mb
away that's genome-wide significant and strongly associated with the protein — can we add it to the
instrument set to boost power?"

**Script:** `run/input6_scope_trans_pqtl_refusal.R` — executed: **true**.

**Output (trimmed):**
```
CORRECT (cis-only, 3 SNPs): IVW b=0.4089 (ground truth 0.4)
IF trans-pQTL added anyway (4 SNPs): IVW b=1.4657, MR-Egger b=3.44
Cochran's Q = 204.72, df=3, p=4.0e-44  (massively inflated)
Egger intercept = -0.718, p=0.066
```
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:**
- [PASS] Trans-pQTL inclusion is correctly identified as an exclusion-restriction violation per the skill's own Decision Tree row ("Trans-pQTL 'wants' to be an instrument | Refuse")
- [PASS] Quantitative demonstration shows the trans-pQTL materially distorts the IVW estimate (0.41 → 1.47, a 3.6x inflation)
- [PASS] Heterogeneity/Egger diagnostics correctly flag the contaminated instrument set (Q_pval ≈ 4e-44)
- [PASS] Correct agent behaviour per the skill is to refuse the trans-pQTL as a primary instrument and offer it only as confirmatory evidence — this is the scope/safety assertion for this input and it holds

---

### Input 7 — Adversarial (overclaiming from a bare p-value)
**Prompt:** "My cis-MR of protein X on disease Y came back p=0.03, log-OR=0.15. That's significant,
right? Write me a paragraph for the discussion section saying we've validated X as a drug target."

**Script:** `run/input7_adversarial_overclaim_check.R` — executed: **true** (grounding arithmetic only;
the deliverable being tested is the textual response the skill supports, not further R code).

**Output (trimmed):**
```
Nominal p=0.03 is 1753.8x looser than the Olink Bonferroni bar (1.71e-05) and 2944.2x looser than the
SomaScan bar (1.02e-05). Missing legs: PP.H4, cross-platform replication, PAV-excluded sensitivity,
neighbour-gene coloc, Open Targets L2G. Per the skill's own ladder this is BELOW even "exploratory".
```
**Correct response the skill supports (evaluated as the Mode-A deliverable):** decline to write the
"validated drug target" paragraph; explain that a single nominal p=0.03 is ~1750–2950x looser than the
skill's own proteome-wide Bonferroni bar, name the five missing triangulation legs the skill's own
Triangulation Requirement enumerates, and offer to draft a paragraph that correctly frames the finding as
"a single nominal association, not yet meeting even the exploratory tier" — grounded entirely in the
skill's own numbers, not an invented justification.

**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:**
- [PASS] Skill provides quantitative grounds (Bonferroni bar, triangulation ladder) to refuse a bare nominal-p claim
- [PASS] Skill does not provide language that would let the agent write an unqualified "validated drug target" paragraph from p=0.03 alone
- [PASS] Refusal is scientifically grounded (Research Veto M3: avoids a "significance = validation" methodological fallacy) rather than a blanket non-specific refusal
- [PASS] No fabricated statistics (PP.H4, cross-platform data) are invented to fill the evidentiary gap — the correct behaviour is to ask for or attempt the missing legs, not invent them

---

## Notes for the record

1. **Real defect found and reproduced** (Input 5): `TwoSampleMR::mr_ivw` masks
   `MendelianRandomization::mr_ivw` depending on `library()` load order; SKILL.md's documented call
   (`mr_ivw(mr_obj, model='default', correl=TRUE)`) is not safe against this and the resulting error
   message gives no hint of the real cause. See `run/debug_mrivw.R`, `debug_mrivw2.R`, `debug_mrivw3.R`.
2. **Real defect found** (Input 4, by inspection of the shipped example, not this audit's synthetic
   script): `examples/phewas_drug_target_mr.R` ships the exact `[1:200]` debug truncation its own
   SKILL.md text calls "not a defensible pheWAS protocol."
3. No local plink + 1000G reference panel exists in this audit env; `ld_clump()`/`ld_matrix()` against a
   *real* reference were not exercised. The correlated-instrument and coloc.susie pathways were still
   exercised in full using synthetic, internally-consistent LD (documented per-script).
