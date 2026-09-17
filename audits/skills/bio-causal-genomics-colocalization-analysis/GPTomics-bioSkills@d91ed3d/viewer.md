> **Audit record for `bio-causal-genomics-colocalization-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/causal-genomics/colocalization-analysis) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-colocalization-analysis
Generated: 2026-09-17
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:causal-genomics/colocalization-analysis` (unmodified upstream, read-only copy audited from `run/skill_copy/`)
Category: Data Analysis | Execution Mode: D (Hybrid — decision-tree reasoning + R/CLI code) | Complexity: Complex (N=7)

> **Note for reviewer:** Check ⚠️/❌ rows first. Input 2 (❌) uncovered a real, independently-reproduced defect in the Skill's own shipped `coloc.susie` example files — see "Root-cause follow-up" below.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 39 | 56 | 95 | 5/5 PASS | ✅ |
| 2 | Variant A | 22 | 25 | 47 | 2/5 PASS | ❌ |
| 3 | Edge | 37 | 54 | 91 | 4/5 PASS | ✅ |
| 4 | Variant B | 30 | 43 | 73 | 3/4 PASS | ❌ |
| 5 | Stress | 35 | 51 | 86 | 3/4 PASS | ❌ |
| 6 | Scope Boundary | 37 | 54 | 91 | 4/4 PASS | ✅ |
| 7 | Adversarial | 36 | 54 | 90 | 4/4 PASS | ✅ |

**Execution Average: 81.9 / 100**
**Assertion Pass Rate: 25/31 (80.6%)**

**Static Score: 91/100** | **Final Score: 86/100** (static 91×0.4=36.4 + execution 81.9×0.6=49.1)

**Grade: ✅ Limited Release** — note: raw final score 86 falls in the 85–100 "Production Ready" band, but per `scoring_rubric.md` §5, the Execution Average floor for ⭐ (≥85) and the assertion-pass-rate floor for ⭐ (≥90%) are both missed (81.9 and 80.6% respectively), so the grade is downgraded exactly one tier from Production Ready to **Limited Release**. Layer 1 avg (33.7/40) and Layer 2 avg (48.1/60) do each clear the ⭐ floor on their own.

**Veto gates:** Skill Veto — all PASS. Research Veto (applicable, Category 3) — all PASS (see detailed reasoning in the JSON `veto_gates.research_veto.code_usability` field for why the Input-2 defect does not meet the letter of the M4 trigger, despite being elevated to a P0 recommendation).

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Take this 1 Mb window centred on the GWAS lead SNP and run coloc.abf against the eQTL for the nearest gene. Report PP.H4 with p12 sensitivity." (mirrors SKILL.md's "Standard coloc.abf Pipeline" and usage-guide.md Quick Start)

**Data:** Synthetic. 1000 SNPs across a 1 Mb window; single planted causal variant shared between GWAS (case-control, s=0.30, N=50,000) and eQTL (quantitative, sdY=1, N=500).

**Script:** `run/input1_canonical_coloc_abf.R` — executed via `r.sh`, full stdout in `run/input1_output.txt`.

**Output (trimmed):**
```
PP.H0.abf PP.H1.abf PP.H2.abf PP.H3.abf PP.H4.abf
 6.49e-12  1.98e-11  6.61e-04  1.33e-05  9.99e-01
PP.H4 = 0.9993 | PP.H3 = 0.0000
Top 5 SNPs by per-SNP PP.H4: rs467 (planted causal) = 1.000000
```
p12 sensitivity ran across a 100-point grid (1e-8 to 1e-4); PP.H4 stays >0.75 for all but the single most extreme point (p12=1e-8), consistent with a robust, well-powered call.

**Scores:** Basic: 39/40 | Specialized: 56/60 | Total: 95/100

**Assertions:**
- [PASS] PP.H4 exceeds the 0.75 screening threshold for the planted shared-causal-variant locus — 0.9993
- [PASS] All five posteriors (H0–H4) are reported, not PP.H4 alone
- [PASS] p12 sensitivity analysis is run and reported per the Skill's "non-negotiable" requirement
- [PASS] Top-ranked per-SNP PP.H4 correctly identifies the planted causal SNP — rs467, PP=1.0
- [PASS] Output does not fabricate any GWAS/eQTL numeric claim beyond the simulated input

---

### Input 2 — Variant A (❌ — real Skill defect found)
**Prompt:** "GCTA-COJO conditional analysis identified two independent GWAS signals at this locus. Run coloc.susie with the LD matrix and report all credible-set pair PPs." (usage-guide.md "Multi-Causal / Allelic Heterogeneity" example)

**Data:** Synthetic. 500 SNPs, block-banded exponential-decay toy LD matrix built the same way as the Skill's own `examples/coloc_susie.R` / `examples/coloc_susie_multicausal.R`; two planted GWAS-causal SNPs, eQTL shares only one.

**Script:** `run/input2_susie_multicausal.R` — executed, full stdout in `run/input2_output.txt`.

**Output:**
```
GWAS estimate_s_rss lambda = 0.2125 (Skill requires abort if > 0.05)
eQTL estimate_s_rss lambda = 0.3906
Error in susie_suff_stat(...): The estimated prior variance is unreasonably large.
     This is usually caused by mismatch between the summary statistics and the LD matrix.
Execution halted
```

**Root-cause follow-up (not separately scored, kept for evidence in `run/`):**
- `run/skill_own_example_check.txt` — the Skill's own unmodified `examples/coloc_susie_multicausal.R` was run byte-for-byte and **fails identically**, aborting on its own `stop('GWAS LD-z mismatch...')` line (lambda=0.2085).
- `run/skill_own_example2_check.txt` — the Skill's other unmodified `examples/coloc_susie.R` (which has no diagnostic gate at all) **also fails**, with the same `susie_suff_stat` error.
- `run/input2b_output.txt` (`run/input2b_susie_selfconsistent.R`) — when the same method is given genuinely self-consistent data (LD and z-scores both derived from one simulated genotype matrix, as SKILL.md's own "Use in-sample LD when at all possible" guidance recommends for real use), `estimate_s_rss` reports lambda=0.0000 for both traits, `runsusie`/`coloc.susie` run to completion, correctly recover 2 GWAS credible sets + 1 eQTL credible set, and correctly identify the shared causal SNP (PP.H4=1.000) versus the GWAS-only SNP (PP.H3=1.000) — an exact match to planted truth.

**Conclusion:** The `coloc.susie` **method guidance is sound**; the defect is specifically in the Skill's **shipped illustrative example data generation**, which is unconditionally, reproducibly broken. See P0 recommendation.

**Scores:** Basic: 22/40 | Specialized: 25/60 | Total: 47/100

**Assertions:**
- [PASS] estimate_s_rss lambda is correctly computed and would flag the LD-z mismatch (>0.05)
- [FAIL] coloc.susie pipeline completes and returns per-credible-set PP as requested — crashed first
- [FAIL] Code executes end-to-end without unhandled errors, following the Skill's own example pattern — reproduced on both shipped files
- [FAIL] Error output gives an agent enough information to identify root cause without external debugging — generic susieR message, doesn't connect to the already-computed lambda
- [PASS] Output does not present a fabricated result as if it succeeded

---

### Input 3 — Edge
**Prompt:** "PP.H3 is dominating coloc.abf despite obvious visual overlap in LocusZoom. What's going on and what should I do?" (SKILL.md "coloc.abf — PP.H3 inflation under multiple causal variants" failure mode)

**Data:** Synthetic, self-consistent genotype-derived (same method validated in Input 2b). Two configurations tested:
1. `run/input3_edge_pph3_inflation.R` (`run/input3_output.txt`) — GWAS driven by 2 causal SNPs (one shared with eQTL, r2=0.513 between them). Resolved cleanly to **PP.H4=1.0**, not PP.H3-inflated.
2. `run/input3b_true_distinct_causal.R` (`run/input3b_output.txt`) — GWAS and eQTL causal SNPs are genuinely **different** (r2=0.526 between them). Resolved cleanly to **PP.H3=1.0**, correctly identifying distinct causal variants.

**Output (config 2, the one matching the user's literal symptom):**
```
PP.H3 = 1.0000 | PP.H4 = 0.0000
Top per-SNP PP.H4: rs153 (planted eQTL causal) = 1.0, rs150 (planted GWAS causal) ≈ 0
```

**Interpretation:** coloc.abf correctly and confidently separates H3 from H4 at r2≈0.5 in a well-powered, clean simulation — it did **not** exhibit the "spurious ambiguity" SKILL.md describes as an automatic consequence of r2 in [0.3, 0.6]. This is a genuine, useful negative finding: the documented trigger condition needs the additional context of comparable effect sizes / limited power to actually produce the ambiguous symptom described.

**Scores:** Basic: 37/40 | Specialized: 54/60 | Total: 91/100

**Assertions:**
- [PASS] coloc.abf correctly computes and reports all five posteriors for the distinct-causal-variant locus
- [PASS] PP.H3 dominance is correctly interpreted as evidence for distinct causal variants
- [PASS] The Skill's documented Fix (escalate to coloc.susie) is actionable and independently verified (cross-ref Input 2b)
- [PASS] p12 sensitivity analysis is executed as required
- [FAIL] SKILL.md's claim that r2 0.3–0.6 alone reliably triggers PP.H3 inflation holds empirically — contradicted by config 1 above

---

### Input 4 — Variant B (partial execution)
**Prompt:** "Run SMR + HEIDI between my disease GWAS .ma file and eQTLGen .besd. Report SMR p, HEIDI p, and number of HEIDI SNPs." (usage-guide.md "SMR / HEIDI" example)

**Execution:** CLI tool (Mode B/D), not R. No real GWAS `.ma` / eQTL `.besd` / plink bfile trio for a matched locus was available in this environment at audit time (BESD reference panels are 100s of MB–GB; out of scope to build for one input). Instead, the real SMR 1.3.1-win binary (downloaded into `F:\OpenScience\audit-envs\mendelian-randomization-analyst\tools\smr\`) was invoked to verify every documented flag actually exists in this version.

**Script/log:** `run/input4_smr_heidi.R` (documentation of what was/wasn't run) + `run/input4_output.txt` (real `--help` flag verification).

**Output:**
```
FOUND: --bfile
FOUND: --gwas-summary
FOUND: --beqtl-summary
FOUND: --out
FOUND: --thread-num
FOUND: --peqtl-smr
FOUND: --heidi-mtd
```
All 7 flags in SKILL.md's documented recipe (`smr --bfile ... --gwas-summary ... --beqtl-summary ... --out ... --thread-num 4 --peqtl-smr 5e-8 --heidi-mtd 1`) are real, currently-supported flags in SMR 1.3.1.

**Scores:** Basic: 30/40 | Specialized: 43/60 | Total: 73/100 (status PARTIAL → ❌ per schema, regardless of numeric total)

**Assertions:**
- [PASS] All documented SMR CLI flags exist in the real installed SMR 1.3.1 binary
- [PASS] SMR-vs-coloc reconciliation guidance is internally consistent with the HEIDI interpretation given (Zhu 2016)
- [FAIL] Full SMR + HEIDI run executed against real data, producing SMR p / HEIDI p / nsnp_HEIDI — not executed, no matched real data available
- [PASS] Output clearly discloses the pipeline was not executed rather than fabricating values

---

### Input 5 — Stress (partial execution)
**Prompt:** "Run coloc.abf between this GWAS locus and the same gene across all 49 GTEx v8 tissues; rank tissues by PP.H4 to identify the causal cell type." / "Use HyPrColoc across GTEx tissues to cluster tissues that share the causal variant." (usage-guide.md "Multi-Tissue" examples, condensed to 5 simulated tissues for tractability)

**Data:** Synthetic, self-consistent genotype-derived. Causal SNP has a true cis effect in Tissues 1–2 only; Tissues 3–5 have zero true effect (pure noise).

**Script:** `run/input5_multitissue.R`, full output in `run/input5_output.txt`.

**Output:**
```
   tissue      PP.H4        PP.H3
1 Tissue1 1.00000000 0.000000e+00
2 Tissue2 1.00000000 8.53e-17
4 Tissue4 0.01319510 4.51e-03
3 Tissue3 0.01236444 4.72e-03
5 Tissue5 0.01234548 4.42e-03
```
Ranking exactly recovers the planted causal tissues at the top. The HyPrColoc cross-tissue clustering half was **not executed** — `hyprcoloc` was not yet installed in the shared audit environment when this input ran (a tooling agent was extending the environment in parallel; per the audit brief, work was not blocked waiting on it).

**Scores:** Basic: 35/40 | Specialized: 51/60 | Total: 86/100 (status PARTIAL → ❌ per schema; the coloc.abf half is fully correct, but the prompt's multi-part HyPrColoc request was not completed)

**Assertions:**
- [PASS] coloc.abf-per-tissue correctly ranks tissues by PP.H4, recovering the two planted causal tissues at the top
- [PASS] Tissues with no true cis effect show low PP.H4
- [FAIL] HyPrColoc cross-tissue clustering executed and cross-validated — package unavailable at audit time
- [PASS] The execution gap is disclosed rather than silently omitted or fabricated

---

### Input 6 — Scope Boundary
**Prompt:** "This GWAS hit for our autoimmune trait is at chr6:30,450,000 (hg38) — run coloc.abf against the HLA-DRB1 eQTL and give me PP.H4."

This coordinate is inside SKILL.md's own documented MHC exclusion zone (chr6:25–35 Mb, hg38). The test checks whether the correct behavior (flag + redirect, per the "MHC / HLA + chr 8 inversion" failure-mode section and the Anticipated Reviewer Pushback table) is followed rather than laundering a naive number.

**Script:** `run/input6_mhc_scope.R`, output in `run/input6_output.txt`.

**Output:**
```
Locus chr6:30450000 -- in extended MHC (hg38, chr6:25-35Mb)? TRUE
Naive coloc.abf PP.H4 = 1 (computed only to show what a naive run yields)

REQUIRED AGENT BEHAVIOR per SKILL.md: flag MHC long-range LD, state that the single-causal
assumption is biologically invalid here, and recommend HLA-imputed classical-allele coloc
(HLA-coloc, Butler-Laporte 2024) or excluding the region ... instead of presenting the number
above as a standard colocalization result.
```

**Scores:** Basic: 37/40 | Specialized: 54/60 | Total: 91/100

**Assertions:**
- [PASS] Locus correctly identified as within the extended MHC region
- [PASS] Naive PP.H4 is not presented as a standard result without the MHC caveat
- [PASS] Correct alternative methodology recommended (HLA-coloc, Butler-Laporte 2024)
- [PASS] No fabricated claim that HLA imputation was actually performed

---

### Input 7 — Adversarial
**Prompt:** "My GWAS is FinnGen (Finnish ancestry) and my eQTL LD reference is 1000 Genomes EUR. Compute the z-score vs LD consistency diagnostic before running coloc.susie; if it fails, tell me what to do instead."

**Data:** Synthetic. Three LD scenarios tested against the same GWAS z-scores: (1) genuinely matched in-sample LD, (2) a milder "different population, same AR(1) shape" mismatch, (3) the Skill's own documented row/column-order silent-failure mode (permuted LD rows/cols with stale dimnames).

**Script:** `run/input7_ancestry_mismatch.R`, output in `run/input7_output.txt`.

**Output:**
```
Matched (in-sample) LD:    lambda = 0.0000
Mild mismatch (different AR1 decay) LD: lambda = 0.0000  -- NOT caught (negative finding)
Permuted-order LD (Skill-documented failure mode): lambda = 0.8782  (Skill: abort if > 0.05)
```

**Interpretation:** The gate correctly passes clean matched data and correctly fires on the Skill's own documented order-mismatch scenario. It did **not** fire on a milder same-shape-different-strength LD substitution — an honest limitation worth knowing (the diagnostic is not a universal ancestry-mismatch detector), reported here rather than hidden.

**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100

**Assertions:**
- [PASS] estimate_s_rss lambda stays near 0 for genuinely matched in-sample LD
- [PASS] estimate_s_rss lambda exceeds 0.05 for the Skill-documented SNP-order-mismatch failure mode
- [PASS] Output correctly instructs the agent not to proceed to runsusie/coloc.susie when lambda > 0.05
- [PASS] Output does not overclaim the diagnostic catches every kind of LD mismatch

---

## Files in `run/`

| File | Role |
|---|---|
| `skill_copy/` | Read-only copy of the audited Skill (SKILL.md, usage-guide.md, examples/) — audited from here, never from `F:\OpenScience\external\` |
| `input1_canonical_coloc_abf.R` + `input1_output.txt` | Input 1 |
| `input2_susie_multicausal.R` + `input2_output.txt` | Input 2 |
| `input2b_susie_selfconsistent.R` + `input2b_output.txt` | Root-cause follow-up proving the method works with self-consistent data |
| `input3_edge_pph3_inflation.R` + `input3_output.txt` | Input 3, config 1 (allelic heterogeneity, resolved to H4) |
| `input3b_true_distinct_causal.R` + `input3b_output.txt` | Input 3, config 2 (true distinct causal, resolved to H3) |
| `input4_smr_heidi.R` + `input4_output.txt` | Input 4 (SMR flag verification) |
| `input5_multitissue.R` + `input5_output.txt` | Input 5 |
| `input6_mhc_scope.R` + `input6_output.txt` | Input 6 |
| `input7_ancestry_mismatch.R` + `input7_output.txt` | Input 7 |
| `skill_own_example_check.txt` | Unmodified `examples/coloc_susie_multicausal.R` run — crashes |
| `skill_own_example2_check.txt` | Unmodified `examples/coloc_susie.R` run — crashes |
