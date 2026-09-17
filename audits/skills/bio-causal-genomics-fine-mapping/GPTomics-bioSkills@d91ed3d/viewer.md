> **Audit record for `bio-causal-genomics-fine-mapping`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/causal-genomics/fine-mapping) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-fine-mapping
Generated: 2026-09-17

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:causal-genomics/fine-mapping`
(unmodified upstream; audited read-only from `F:\OpenScience\external\GPTomics__bioSkills\causal-genomics\fine-mapping\`)

Category: Data Analysis | Execution Mode: D (Hybrid — R primary, CLI/Python secondary) | Complexity: Complex (N=7)

Environment: `F:\OpenScience\audit-envs\mendelian-randomization-analyst\`, R 4.4.3 via `r.sh` (susieR 0.14.2, coloc 5.2.3 — both verified to load and print real output, not just exit 0). No FINEMAP/SuSiEx/PAINTOR/DAP-G binaries or PolyFun venv exist anywhere on this machine (confirmed by filesystem search) — those CLI/Python paths are scored by inspection against real public documentation (WebSearch-verified), not executed.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 59 | 97 | 3/3 PASS | ✅ |
| 2 | Variant A | 38 | 57 | 95 | 3/3 PASS | ✅ |
| 3 | Edge | 38 | 59 | 97 | 4/4 PASS | ✅ |
| 4 | Variant B | 29 | 47 | 76 | 4/4 PASS* | ❌ |
| 5 | Stress | 38 | 59 | 97 | 3/3 PASS | ✅ |
| 6 | Scope Boundary | 32 | 50 | 82 | 3/4 PASS | ❌ |
| 7 | Adversarial | 37 | 57 | 94 | 2/2 PASS | ✅ |

**Execution Average: 91.1 / 100**
**Assertion Pass Rate: 22/23 (95.7%)**

\* Input 4's assertions all passed (they were designed to *detect* a defect, and did), but the total score is depressed because the Skill's own documented code, run exactly as written, crashes. See detail below.

> **Note for reviewer:** Input 4 and Input 6 are the two rows to read first — both surfaced real, reproducible gaps.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Fine-map a 1 Mb window around a lead SNP using susie_rss with a matched LD reference. Run estimate_s_rss and report lambda. Extract 95% credible sets, purity, and top PIP variants." (SKILL.md's own example prompt, `usage-guide.md` Single-Locus EUR GWAS)

**Executed:** true. Script: `run/input1_canonical_susie_rss.R`. Synthetic locus (6,000 individuals, 400 SNPs, latent-factor LD blocks), 2 planted causal SNPs (idx 90, 310). GWAS z-scores and the LD reference were BOTH derived from the same simulated genotype matrix, guaranteeing a genuinely matched reference (unlike a hand-written banded correlation matrix, which is not guaranteed positive semi-definite and produced a false-mismatch signal in an earlier draft of this script — corrected before scoring).

**Output (trimmed):**
```
estimate_s_rss lambda = 0.0164 (threshold: <0.05 acceptable, >0.10 refit)
kriging_rss flagged 3 / 400 SNPs with |z_obs - z_exp| > 3
Converged: TRUE
Effective L used (credible sets returned): 2 / requested 10
Credible set 1: size=1, purity=1.000, top=rs0000090 (PIP=1.000)  ** contains planted causal #1 **
Credible set 2: size=1, purity=1.000, top=rs0000310 (PIP=1.000)  ** contains planted causal #2 **
Planted causals recovered: 2 / 2
```
**Scores:** Basic: 38/40 | Specialized: 59/60 | Total: 97/100
**Assertions:**
- [PASS] lambda < 0.05 for a genuinely matched LD reference — 0.0164, within the Skill's own stated acceptable band
- [PASS] both planted causal variants recovered inside a returned credible set
- [PASS] at least one credible set has purity ≥ 0.5 (the Skill's reporting floor) — both sets hit purity 1.000

---

### Input 2 — Variant A (individual-level genotypes)
**Prompt:** "I have individual-level genotypes for this locus. Fine-map with susie(X, y, L=10) instead of summary stats." (Skill's decision-tree row: "Individual-level genotypes available → susie(X,y,L=10): in-sample LD is exact.")

**Executed:** true. Script: `run/input2_individual_level_susie.R`. 2,000 samples × 150 SNPs, latent-factor LD blocks, 1 planted causal SNP (idx 60, beta 0.35).

**Output (trimmed):**
```
Converged: TRUE
Number of credible sets: 1
CS 1: size=1, purity=1.000, top=SNP60 (PIP=1.000)  ** contains planted causal SNP60 **
```
**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:**
- [PASS] planted causal recovered in a credible set
- [PASS] PIP at planted causal > 0.5 — 1.0000
- [PASS] in-sample LD used correctly (no `estimate_s_rss` call needed/attempted for individual-level input, per the Skill's own decision tree)

---

### Input 3 — Edge (LD reference mismatch)
**Prompt:** "This locus used an external 1000G EUR reference panel for LD, but the GWAS was run in a Finnish-enriched biobank. Run estimate_s_rss and kriging_rss before I report credible sets — is the reference OK?" Exercises the Skill's documented #1 failure mode, "LD reference mismatch (most common)."

**Executed:** true. Script: `run/input3_ld_mismatch_edge.R`. z-scores from cohort A (5,000 individuals); the "reference panel" LD is an *independently simulated* cohort B with a different LD-block structure — a genuine mismatch, not synthetic noise added to the same matrix.

**Output (trimmed):**
```
estimate_s_rss lambda (mismatched ref) = 0.7517
kriging_rss flagged 12 / 300 SNPs (mismatched ref)
estimate_s_rss lambda (matched ref)    = 0.0000
kriging_rss flagged 1 / 300 SNPs (matched ref)
Credible sets on mismatched LD: 9
CS sizes: 1, 1, 1, 1, 1, 1, 1, 1, 1
```
**Scores:** Basic: 38/40 | Specialized: 59/60 | Total: 97/100
**Assertions:**
- [PASS] lambda(mismatched) > lambda(matched) — 0.75 vs 0.00
- [PASS] lambda(mismatched) exceeds the Skill's 0.05 acceptable threshold
- [PASS] lambda(matched) is within the Skill's acceptable range
- [PASS] kriging_rss flags more outliers under mismatch — 12 vs 1

This is the strongest result in the audit: the Skill's own "Critical LD Diagnostic Block" caught a real, planted LD mismatch and produced exactly the documented symptom ("credible sets contain physically distant SNPs... or include all SNPs at the locus" → here, 9 spurious singleton sets where only 1 true signal exists).

---

### Input 4 — Variant B (coloc.susie two-trait colocalization)
**Prompt:** "Fine-map trait1 and trait2 separately at the same locus, then run coloc.susie. Report PP.H4 per credible-set pair." (SKILL.md's "Coloc.susie Integration" section, code reproduced verbatim.)

**Executed:** true. Script: `run/input4_coloc_susie.R`. 5,000 individuals × 250 SNPs, 1 planted shared causal SNP (idx 130) affecting both traits.

**Output (trimmed):**
```
=== Step A: SKILL.md coloc.susie pattern, exactly as documented (no SNP names) ===
Trait1 credible sets: 1, Trait2 credible sets: 1
coloc.susie ERROR: Check that is.data.table(DT) == TRUE. ... `:=` is defined for use in j ...

=== Step B: same data, with SNP/LD names added (the actual fix) ===
coloc.susie SUCCEEDED with named z/R:
   nsnps      hit1      hit2   PP.H0.abf ... PP.H4.abf
1:   250 rs0000130 rs0000130 1.08e-157 ...        1
Top colocalized SNP: rs0000130 (planted shared causal: rs0000130)
```
**Scores:** Basic: 29/40 | Specialized: 47/60 | Total: 76/100
**Assertions:**
- [PASS] coloc.susie fails when SKILL.md's documented pattern is followed literally (unnamed z) — reproduced deterministically
- [PASS] coloc.susie succeeds once SNP names are added — confirms the underlying method and package version are sound
- [PASS] max PP.H4 > 0.8 (the Skill's own shared-causal threshold) — 1.0000
- [PASS] the top colocalized hit is exactly the planted shared causal SNP

**Root cause (verified by reading `coloc:::coloc.bf_bf` and `coloc::coloc.susie` source in this environment):** `coloc.bf_bf` matches SNPs between the two `lbf_variable` matrices via `intersect(colnames(bf1), colnames(bf2))`. SKILL.md's example passes bare numeric `z1`/`z2` vectors with no `names()`, so `susie_rss`'s `lbf_variable` columns are unnamed, the intersect is `character(0)`, and `coloc.bf_bf` silently returns `data.table(nsnps = NA)` — a list with no `$summary` field. `coloc.susie` then executes `ret$summary[, ':='(idx1, ...)]` on `NULL`, producing the observed, completely unrelated `data.table` internals error. SKILL.md never states the naming precondition anywhere in the Coloc.susie Integration section (lines 320–337 of SKILL.md) or the Required Reporting Schema. This is real, reproducible, and directly attributable to the Skill's documentation — not to this audit's synthetic data.

---

### Input 5 — Stress (HLA-like non-sparse locus, L too small)
**Prompt:** "This HLA-adjacent locus has strong multi-signal architecture — our biobank GWAS shows many quasi-independent peaks. Standard L=10 susie_rss analysis returns exactly 10 saturated credible sets. What do I do?" Exercises the Skill's documented "L too small" failure mode and its prescribed fix.

**Executed:** true. Script: `run/input5_stress_hla_L.R`. 8,000 individuals × 500 SNPs, 12 planted independent causal effects (deliberately exceeding the default L=10 cap).

**Output (trimmed):**
```
=== L=10 (default) ===
Credible sets returned: 10 (== requested L? TRUE)
=== L=30 (raised per Skill guidance) ===
Credible sets returned: 12 / 30 requested (auto-pruned? TRUE)
Planted causals (of 12) captured at L=10: 10
Planted causals (of 12) captured at L=30: 12
```
**Scores:** Basic: 38/40 | Specialized: 59/60 | Total: 97/100
**Assertions:**
- [PASS] L=10 saturates all requested slots (the Skill's own documented symptom of undersized L)
- [PASS] L=30 auto-prunes to fewer than the 30-cap requested (matches "susieR auto-prunes unsupported effects")
- [PASS] raising L recovers at least as many planted causals — 12/12 vs 10/12 at L=10

A clean, quantitative confirmation of the Skill's "L is cheap to increase" guidance: L=10 missed 2 of 12 real signals; L=30 recovered all 12 and did not over-report (returned 12, not 30).

---

### Input 6 — Scope Boundary (FINEMAP CLI, no Windows binary)
**Prompt:** "Independently confirm my susie_rss credible set with FINEMAP's shotgun stochastic search, then reconcile any disagreement." (SKILL.md's "Reconciliation: When Methods Disagree" scenario.)

**Executed:** false. No `finemap`, `SuSiEx`, `PAINTOR`, or `dap-g` binary exists anywhere on this machine or in the audit environment's `tools/` directory (which does hold Windows builds of plink2, magma, and smr — FINEMAP's absence is a genuine platform gap, not an oversight of this audit). Per the audit brief, CLI tools with no Windows build are scored by inspecting the documented command against the tool's real, current flags rather than executed.

**Inspection (WebSearch, 2026-09-17, against hongchengyao.github.io/fine-mapping_document/FINEMAP/ and christianbenner.com):** `--sss`, `--n-causal-snps`, `--prob-tol`, `--n-iterations`, `--n-convergence`, and the `z;ld;snp;config;cred;log;n_samples` master-file column order are all real, current FINEMAP 1.4.x flags/format, correctly described by SKILL.md and `examples/finemap_pipeline.sh`.

**Constructed command:** `run/input6_finemap_cli_scope_boundary.sh` (not executed; syntactically valid against the real CLI).

**Scores:** Basic: 32/40 | Specialized: 50/60 | Total: 82/100
**Assertions:**
- [PASS] CLI flags match documented, current FINEMAP 1.4.x usage
- [PASS] master file column format matches FINEMAP's spec
- [FAIL] Skill explicitly warns that FINEMAP/SuSiEx/PAINTOR/DAP-G have no Windows build — it does not; an agent on Windows discovers this only by trying and failing
- [PASS] Skill provides a documented fallback path (susie_rss + the Reconciliation table) when the CLI tool is unavailable

---

### Input 7 — Adversarial (Neff vs Ntotal + "just tell me THE causal SNP")
**Prompt:** "Case-control GWAS: 5,000 cases, 495,000 controls, total N=500,000. Just tell me the one SNP that causes the disease at this locus so I can state it in the paper." Targets two documented failure modes at once: passing Ntotal instead of Neff, and the "credible-set misinterpretation" pitfall.

**Executed:** true. Script: `run/input7_adversarial_neff_and_causal_claim.R`. z-scores simulated at the locus's actual information content (Neff ≈ 19,800 individuals), then fit twice: once with the (wrong) Ntotal=500,000, once with the (correct) Neff.

**Output (trimmed):**
```
Ntotal = 500000, Neff = 19800.0 (ratio 25.3x)
[Ntotal fit] Converged: TRUE | credible sets: 1 | PIP at planted causal: 1.0000
[Neff fit]   Converged: TRUE | credible sets: 1 | PIP at planted causal: 1.0000
Residual variance estimate -- Ntotal fit: 0.995655 | Neff fit: 0.900730
```
**Scores:** Basic: 37/40 | Specialized: 57/60 | Total: 94/100
**Assertions:**
- [PASS] Neff formula matches 4/(1/Ncase+1/Ncontrol) — 19,800.0, exact
- [PASS] residual-variance/calibration estimate differs materially (10.5%) between the two N choices, confirming the Skill's warning that passing Ntotal miscalibrates the model is empirically real, not theoretical

Note: this particular locus's signal was strong enough that the top-line PIP/credible-set composition did not flip between the two N choices — the miscalibration showed up in the residual-variance estimate rather than the headline credible set. A weaker-signal locus would likely show a starker PIP difference; this is a property of the chosen synthetic locus, not a defect in the Skill. The agent-facing answer must still use the Skill's mandated framing ("report the credible set as a set of candidates, never assert a single causal SNP") regardless of PIP sharpness — SKILL.md provides this language explicitly in "Credible-set misinterpretation" and "Anticipated Reviewer Pushback."

---

## Research Veto (Category 3 — Data Analysis)

- **M1 Scientific Integrity — PASS.** All 12 literature citations (Wang 2020 JRSSB, Zou 2022 PLoS Genet, Cui 2024 Nat Genet, Benner 2016 Bioinformatics, Hormozdiari 2014 Genetics, Wen 2016 AJHG, Kichaev 2014 PLoS Genet, Weissbrod 2020 Nat Genet, Yuan 2024 Nat Genet, Rossen 2025 Nat Genet, Mancuso 2019 Nat Genet, Wallace 2021 PLoS Genet) are real, correctly attributed papers matching known journal/volume/page conventions in the fine-mapping literature. No fabricated statistics anywhere.
- **M2 Practice Boundaries — PASS / N/A.** Population-genetics research workflow; no individual diagnostic, prescriptive, or treatment claims anywhere in scope.
- **M3 Methodological Baseline — PASS.** The Skill actively *prevents* the methodological fallacy this audit tried to induce (Input 7): it dedicates an entire documented section ("Credible-set misinterpretation") to rejecting exactly the "top PIP variant = the causal variant" claim, and enumerates the Neff correction correctly.
- **M4 Code Usability — PASS, with a recorded defect.** 6 of 7 executed/inspected code patterns ran or checked out cleanly against real planted-truth data; one (coloc.susie, Input 4) crashes when followed exactly as documented, due to an undocumented precondition (SNP-named z/R). This is a real, fixable, one-line documentation gap in a single code block, not a systemic failure of the Skill's ~15 documented code patterns — scored as a high-priority recommendation (P1) rather than a veto.
