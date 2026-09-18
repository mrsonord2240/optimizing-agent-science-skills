> **Audit record for `bio-causal-genomics-colocalization-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@9da81ea](https://github.com/mrsonord2240/bioSkills/tree/9da81ea758e0b0d631f72199a4679211dc89f5d4/causal-genomics/colocalization-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-18 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-colocalization-analysis (RE-AUDIT)
Generated: 2026-09-18
Source: `mrsonord2240/bioSkills@9da81ea758e0b0d631f72199a4679211dc89f5d4:causal-genomics/colocalization-analysis` (fork, branch `fix/cg-coloc`, worktree `F:\OpenScience\wt\cg-coloc`, audited from a copy at `run/skill_copy/`, never executed in place)
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=7)
Prior audit (pre-fix): `F:\OpenScience\audits\_pre-fix-20260918\bio-causal-genomics-colocalization-analysis\` — score 86, Limited Release, 2026-09-17
Fix log (claims only, independently re-verified below, not taken on faith): `F:\optimizing-agent-science-skills\fixes\bio-causal-genomics-colocalization-analysis.md`

> **Re-audit method:** every open finding from the pre-fix audit was re-run as a regression test with fresh data/parameters (not the fixer's own scratch files, which this auditor never had access to), plus 2 new inputs (6, 7) probing things the fixer was not specifically told about. All 7 inputs executed; none were skipped or simulated.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 2 | Variant A (P0 regression) | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 3 | Edge (P0 regression) | 39 | 59 | 98 | 5/5 PASS | ✅ |
| 4 | Variant B (P1 regression + extension) | 39 | 56 | 95 | 5/5 PASS | ✅ |
| 5 | Stress (P1 regression, new data) | 37 | 59 | 96 | 5/5 PASS | ✅ |
| 6 | Scope Boundary (new) | 35 | 55 | 90 | 3/5 PASS | ✅ |
| 7 | Adversarial (new) | 38 | 56 | 94 | 4/5 PASS | ✅ |

**Execution Average: 95.3 / 100**
**Assertion Pass Rate: 32/35 (91.4%)**
**Static Score: 97/100** | **Final Score: 96/100** (static 97×0.4=38.8 + execution 95.3×0.6=57.2)

**Grade: ⭐ Production Ready** — up from 86 (✅ Limited Release) pre-fix. All per-layer floors for the ⭐ tier clear: Static ≥80 (97), Execution Average ≥85 (95.3), Layer 1 avg ≥32 (38.0), Layer 2 avg ≥48 (57.3), Assertion pass rate ≥90% (91.4%, clears by a narrow margin).

**Veto gates:** Skill Veto — all PASS (unchanged). Research Veto (applicable, Category 3) — all PASS. `code_usability` is now a clean PASS with no hedging: the pre-fix report's M4 reasoning explained why the two crashing examples didn't meet the *letter* of an automatic FAIL despite being elevated to a P0; that P0 is now independently confirmed closed.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Take this 1 Mb window centred on the GWAS lead SNP and run coloc.abf against the eQTL for the nearest gene. Report PP.H4 with p12 sensitivity." (fresh synthetic locus, chr10, independent of the pre-fix audit's Input 1)

**Script:** `run/input1_canonical_coloc_abf.R`, output `run/input1_output.txt`.

**Output (trimmed):**
```
PLANTED TRUTH: shared causal SNP = rs501
Region flag (expect NA for this chr10 synthetic locus): NA
PP.H0.abf PP.H1.abf PP.H2.abf PP.H3.abf PP.H4.abf
1.62e-208 2.05e-147  1.58e-64  0.00e+00  1.00e+00
Top per-SNP PP.H4: rs501 (planted causal: rs501) match=TRUE
PP.H4 stays > 0.75 across 100 / 100 grid points
```
Also exercises `flag_excluded_region()` inline (verbatim from SKILL.md's Standard coloc.abf Pipeline) to confirm it does not falsely fire on a non-excluded locus.

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100 — 5/5 assertions PASS.

---

### Input 2 — Variant A (P0 regression: shipped `coloc_susie.R`)
**Prompt equivalent:** re-run the Skill's own first shipped `coloc.susie` example, unmodified, exactly as an agent following SKILL.md's "coloc.susie Multi-Causal Pipeline" pointer to `examples/` would.

**Script:** the shipped `examples/coloc_susie.R` itself (copied to `run/skill_copy/examples/`, executed unmodified), output `run/input2_coloc_susie_shipped_output.txt`.

**Output:**
```
PLANTED TRUTH: shared causal SNP index 149
GWAS credible sets found: 1 (planted truth: 1)
eQTL credible sets found: 1 (planted truth: 1)
Best CS pair: rs149 x rs149 | PP.H4 = 1.000 (planted causal: rs149)
```
Pre-fix, this exact file crashed with `susie_suff_stat(): the estimated prior variance is unreasonably large`. It now runs clean to completion with exact planted-truth recovery — **independently confirmed, not re-run from the fixer's own patched copy but from the file as it now ships in the fork.**

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100 — 5/5 assertions PASS.

---

### Input 3 — Edge (P0 regression: shipped `coloc_susie_multicausal.R`)
**Prompt equivalent:** re-run the Skill's second shipped `coloc.susie` example (allelic heterogeneity), unmodified.

**Script:** the shipped `examples/coloc_susie_multicausal.R` itself, executed unmodified, output `run/input3_coloc_susie_multicausal_shipped_output.txt`.

**Output:**
```
PLANTED TRUTH: causal1 idx 79 (shared GWAS+eQTL), causal2 idx 198 (GWAS-only)
GWAS estimate_s_rss lambda = 0.0000
eQTL estimate_s_rss lambda = 0.0000
GWAS credible sets: 2 (planted truth: 2) | eQTL credible sets: 1 (planted truth: 1)
   idx1  idx2   hit1   hit2   PP.H3.abf   PP.H4.abf
1:     1     1   rs79   rs79 1.09e-10 1.00e+00
2:     2     1  rs198   rs79 1.00e+00 9.19e-29
```
Pre-fix, lambda was 0.2085 (well above the 0.05 abort threshold) and the file `stop()`ped on its own gate before ever reaching `coloc.susie()`. It now shows lambda=0.0000 for both traits and correctly separates the shared-causal pair (PP.H4=1.0) from the GWAS-only pair (PP.H3=1.0), exact match to planted truth.

**Scores:** Basic 39/40 | Specialized 59/60 | Total 98/100 — 5/5 assertions PASS.

---

### Input 4 — Variant B (P1 regression + extension: `flag_excluded_region()`)
**Prompt equivalent:** "This GWAS hit is at chr6:30,450,000 / chr8:9,000,000 / [7 more coordinates] — is this locus excluded from standard coloc?"

**Script:** `run/input4_mhc_gate.R` (the gate function extracted verbatim from SKILL.md's Standard coloc.abf Pipeline code block), output `run/input4_output.txt`.

**Output (9 cases + 2 integration checks, all correct):**
```
chr6:30450000  -> MHC            PASS
chr8:9000000   -> chr8_inversion PASS
chr1:1000000   -> NA             PASS
chr6:24000000  -> NA             PASS
chr6:25000000  -> MHC            PASS   (new: exact lower boundary)
chr6:35000000  -> MHC            PASS   (new: exact upper boundary)
chr6:35000001  -> NA             PASS   (new: one bp past boundary)
'chr8':8100000 -> chr8_inversion PASS   (new: 'chr' prefix)
chr8:11900001  -> NA             PASS   (new: one bp past boundary)
build="hg19"   -> Correctly stopped: liftover to hg38 first...
full gate block -> Correctly stopped pipeline: Locus is in the MHC exclusion zone...
```
The first 4 cases regression-test the fixer's own test coordinates; the remaining 5 are new boundary/robustness cases this auditor added. All pass, including confirming the gate is a real `stop()` that would actually abort a pipeline, not just an inspectable flag.

**Scores:** Basic 39/40 | Specialized 56/60 | Total 95/100 — 5/5 assertions PASS.

---

### Input 5 — Stress (P1 regression: real SMR + HEIDI, independent data)
**Prompt equivalent:** "Run SMR + HEIDI between my GWAS and eQTL. Report SMR p, HEIDI p, and nsnp_HEIDI" for two scenarios: (a) the eQTL and GWAS share the same causal SNP, (b) the eQTL's causal SNP is a different SNP in LD with the GWAS causal SNP (linkage, not shared causality).

**Data:** Fresh liability-threshold-simulated genotypes (n=2500, 50 SNPs, AR(1) rho=0.80) — independent seed, sample size, and SNP count from the fixer's own `tmp_smr_test/`. Built a full PLINK bfile via `plink2 --pedmap --make-bed`, and two real `.besd` eQTL files via `smr --eqtl-flist ... --make-besd`, then ran the exact documented recipe: `smr --bfile ... --gwas-summary ... --beqtl-summary ... --peqtl-smr 5e-8 --heidi-mtd 1`.

**Scripts:** `run/input5_smr_prep.R` (data generation + file writing), `run/smr_test/smr_run_output.txt` (the actual `plink2`/`smr` CLI invocations and full logs), `run/smr_test/result_shared.smr`, `run/smr_test/result_linkage.smr`.

**Output:**
```
[shared]  topSNP=rs9025  p_SMR=4.580844e-45  p_HEIDI=9.932894e-01  nsnp_HEIDI=9
[linkage] topSNP=rs9027  p_SMR=1.359792e-08  p_HEIDI=9.083979e-12  nsnp_HEIDI=9
```
Planted causal SNP was rs9025 (GWAS) and rs9025 (shared eQTL) / rs9027 (linkage eQTL) — both scenarios recover the correct top SNP exactly. Shared scenario: significant SMR + non-rejecting HEIDI (p=0.993) → correctly interpreted per SKILL.md as pleiotropy/shared-causal. Linkage scenario: significant SMR but HEIDI rejects (p=9.08e-12) → correctly interpreted as linkage, not shared causality. This independently reproduces the fixer's own claimed result pattern (their shared-scenario p_HEIDI=0.749, linkage p_HEIDI=1.8e-5) with completely different underlying data.

**Caveat (test artifact, not a Skill defect):** `nsnp_HEIDI=9` in both runs, one below SKILL.md's own documented `>= 10 for HEIDI reliability` floor — an artifact of this test's smaller 50-SNP panel (vs. the fixer's 60), not a flaw in the recipe. The qualitative conclusion is robust regardless (11 orders of magnitude apart in p_HEIDI).

**Scores:** Basic 37/40 | Specialized 59/60 | Total 96/100 — 5/5 assertions PASS.

---

### Input 6 — Scope Boundary (NEW — probes the revised PP.H3 trigger text itself)
**Prompt equivalent:** "PP.H3 is dominating coloc.abf at moderate LD (r2~0.5) with comparable, modestly-powered effect sizes at both signals — is this the trigger condition SKILL.md now describes?"

This input was not derived from anything the fixer was told; it directly tests whether the *revised* trigger clause ("comparable effect sizes / limited power") — added to fix the pre-fix P1 that r2-alone was overstated — is itself empirically accurate.

**Script:** `run/input6_pph3_revised_trigger.R`, output `run/input6_output.txt`.

**Output:**
```
PLANTED: causal1 idx 150, causal2 idx 152, r2=0.505
[N=150] PP.H0=2.35e-07 PP.H1=0.9430 PP.H2=6.87e-09 PP.H3=0.0275 PP.H4=0.0295
[N=400] PP.H1=0.8606 PP.H3=0.0450 PP.H4=0.0944
```
At r2=0.505 (squarely in the documented 0.3-0.6 band) with comparable modest effect sizes (both β=0.12) and two different underpowered eQTL sample sizes, **PP.H1 (GWAS-only), not PP.H3, dominates** in both cases. PP.H3 never exceeds 0.05. This partially contradicts the revised trigger text: the added "limited power" clause, as currently worded, does not reliably reproduce the claimed PP.H3-dominant symptom in this auditor's independent testing — see the P1 recommendation. (PP.H3 and PP.H4 are at least closely matched to each other at N=150, a weak partial echo of "ambiguity," but both are dwarfed by PP.H1.)

**Scores:** Basic 35/40 | Specialized 55/60 | Total 90/100 — 3/5 assertions PASS (2 FAILs are the genuine finding, not scoring artifacts).

---

### Input 7 — Adversarial (NEW — probes the redundancy-pass move for corruption/gaps)
**Prompt equivalent:** "Harmonise these two summary-stat tables, including a SNP that's coded on the complementary strand" — exercising the `harmonise()` function that this fix pass moved from `usage-guide.md` into SKILL.md's "Allele Harmonisation" section.

**Script:** `run/input7_harmonise_test.R`, output `run/input7_output.txt`.

**Output:**
```
Harmonised rows kept: rs1, rs2, rs6
ASSERTION [kept set matches expectation]: PASS
ASSERTION [rs2 flip-coded SNP beta sign correctly negated, -0.28 -> 0.28]: PASS (got 0.280)
ASSERTION [rs6 palindromic-but-low-MAF SNP kept and flip-corrected]: PASS
ASSERTION [rs3, allele-mismatched SNP with no A1/A2 overlap, is dropped not silently mis-flipped]: PASS
FINDING [rs4, non-palindromic strand-complement mismatch (A/G vs T/C), silently dropped -- no strand-flip resolution, no pitfall callout]: CONFIRMED
```
The function's core same/flip/palindromic-drop logic is intact and correct after the move — no corruption, nothing lost. A new, previously-unflagged minor gap was found: a SNP pair on complementary strands without being palindromic (e.g. `A/G` vs its complement `T/C`) is neither "same" nor "flip" under the function's literal definition, so it is silently dropped — and none of the "Harmonisation pitfalls to watch for" bullets warn about this specific case (they cover build mismatch and palindromic-at-high-MAF only). See P2 recommendation.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100 — 4/5 assertions PASS.

---

## Files in `run/`

| File | Role |
|---|---|
| `skill_copy/` | Copy of the audited Skill (fork commit 9da81ea), executed from here — never in place in the worktree |
| `input1_canonical_coloc_abf.R` + `input1_output.txt` | Input 1 |
| `input2_coloc_susie_shipped_output.txt` | Input 2 — output of the shipped, unmodified `examples/coloc_susie.R` |
| `input3_coloc_susie_multicausal_shipped_output.txt` | Input 3 — output of the shipped, unmodified `examples/coloc_susie_multicausal.R` |
| `input4_mhc_gate.R` + `input4_output.txt` | Input 4 |
| `input5_smr_prep.R` + `input5_prep_output.txt` | Input 5 — data/file generation |
| `smr_test/` | Input 5 — plink bfile, `.ma`/`.esd`/`.flist`, real `.besd` files, `smr_run_output.txt`, `result_shared.smr`, `result_linkage.smr` |
| `input6_pph3_revised_trigger.R` + `input6_output.txt` | Input 6 |
| `input7_harmonise_test.R` + `input7_output.txt` | Input 7 |

**Note on the pre-fix audit's own `run/` scripts:** this working directory already held the pre-fix audit's scripts and outputs (`input2_susie_multicausal.R`, `input2b_*`, `input3_edge_*`, `input5_multitissue.R`, `input6_mhc_scope.R`, `input7_ancestry_mismatch.R`, the two `skill_own_example*_check.txt` files, etc.) — the pre-fix report itself had only been archived as JSON+viewer, not its `run/` folder. Those files were moved (not deleted) to `F:\OpenScience\audits\_pre-fix-20260918\bio-causal-genomics-colocalization-analysis\run\` to complete that archive, keeping this directory's contents an accurate record of only this re-audit's own runs.
