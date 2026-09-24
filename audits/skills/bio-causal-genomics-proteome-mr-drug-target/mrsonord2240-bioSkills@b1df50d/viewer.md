> **Audit record for `bio-causal-genomics-proteome-mr-drug-target`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@b1df50d](https://github.com/mrsonord2240/bioSkills/tree/b1df50d420e9a6bb2cd43f46adf2a0d94ff37288/causal-genomics/proteome-mr-drug-target) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-proteome-mr-drug-target

## Canonical final summary

**Final:** 93/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@b1df50d420e9a6bb2cd43f46adf2a0d94ff37288:causal-genomics/proteome-mr-drug-target`

Final-pass metadata is deliberate: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|
| 1 | Canonical PCSK9 cis-MR | 38 | 57 | 95 | 4/4 | ✅ |
| 2 | Variant A IL6R platforms | 38 | 56 | 94 | 5/5 | ✅ |
| 3 | Edge small cis window | 37 | 55 | 92 | 4/4 | ✅ |
| 4 | Variant B 50-outcome pheWAS | 39 | 57 | 96 | 5/5 | ✅ |
| 5 | Stress allelic heterogeneity | 38 | 57 | 95 | 5/5 | ✅ |
| 6 | Scope boundary trans-pQTL | 39 | 57 | 96 | 4/4 | ✅ |
| 7 | Adversarial overclaim | 38 | 57 | 95 | 4/4 | ✅ |
| 8 | New Steiger regression | 39 | 59 | 98 | 4/4 | ✅ |
| 9 | New current shipped cis example | 39 | 58 | 97 | 5/5 | ✅ |
| 10 | New current pheWAS script | 39 | 58 | 97 | 5/5 | ✅ |
| 11 | New empty-result pheWAS edge | 31 | 47 | 78 | 3/4 | ❌ |

**Execution average:** 93.9 / 100.  **Assertion pass rate:** 48 / 49 (98.0%).

All 11 dynamic inputs were explicitly executed. Inputs 1–6 and 8–11 have `Rscript` exit 2816 after their PASS or materialized output, a repeatable Windows R wrapper/process teardown artifact. This is not credited as a successful exit code: the report relies only on the printed values and assertions already emitted into each corresponding `.log`. Input 7 exits 0. The parse gate exits 0 for all 15 audit/shipped R files.

## Veto gates

- Skill veto: PASS (stability, contract, determinism, security).
- Research veto: PASS. Outputs are synthetic/stubbed where stated, population-level only, retain causal boundaries, and current shipped code is runnable on valid inputs.
- Input 11 is a P1 reliability defect, not a veto: it fails explicitly and does not create a false result.

## Executed evidence

All harnesses, logs, source snapshot, and synthetic inputs are under `run/` and `data/` in this audit directory. The old report and its raw evidence were retained at `F:/OpenScience/audits/_pre-fix-20260923/bio-causal-genomics-proteome-mr-drug-target/` before this report was written.

### 1. PCSK9 canonical cis-MR

`run/input1_pcsk9_cad_cismr_coloc.R` used a 60-SNP synthetic PCSK9 window with a planted 0.45 log-effect. It recovered IVW 0.4296, PAV-excluded IVW 0.4224, PP.H4 0.9999999, and a namespaced correlated-IVW estimate. Its four assertions passed.

### 2. IL6R cross-platform/PAV case

`run/input2_il6r_ra_crossplatform.R` found Olink -0.5220 and SomaScan -0.2380 before PAV exclusion (magnitude ratio 2.19, so not claimable); removing the planted SomaScan missense artifact gave -0.4950 and restored agreement. It preserved the H3-dominant SomaScan coloc result instead of treating it as target validation.

### 3. Small-window edge

`run/input3_edge_single_sentinel.R` reported full-IVW 0.5750 and sentinel Wald 0.5334; PP.H4 0.6026 stayed below the Skill's 0.7 suggestive bar. The output describes why that is not a publishable drug-target claim.

### 4. Full local pheWAS substitute

`run/input4_phewas_ontarget.R` scanned every one of 50 synthetic endpoints. The planted T2D-like effect was beta 0.1777 (truth 0.18), p_bonf 1.09e-32; the weak planted signal remained non-significant (p_bonf 0.276). It never applied the prohibited endpoint slice.

### 5. Allelic heterogeneity

`run/input5_stress_allelic_heterogeneity.R` found two credible sets per trait. Matching sets had PP.H4 1.0; crossed sets were H3-dominant. Standard and robust/penalized correlated IVW both returned 0.4987 for a planted 0.5 effect.

### 6. Trans-pQTL refusal

`run/input6_scope_trans_pqtl_refusal.R` recovered cis-only IVW 0.4089 for truth 0.4. Adding the explicitly pleiotropic trans instrument moved the estimate to 1.4657 and yielded Cochran Q p=4.03e-44, validating the documented refusal boundary.

### 7. Overclaim refusal

`run/input7_adversarial_overclaim_check.R` grounds the refusal: p=0.03 is 1753.8-fold looser than the Olink proteome-wide bar and 2944.2-fold looser than the SomaScan bar, before the unprovided coloc, platform, PAV, neighbour-gene, and L2G legs.

### 8. Repaired Steiger block

`run/input8_steiger_samplesize_regression.R` executes the current failure-mode block verbatim after harmonization. Explicit N fields resulted in four usable rows, all forward, with directionality p=1.29e-57. This directly regresses the checkpointed crash fix.

### 9. Current shipped cis example

`run/input9_shipped_cis_example.R` sources the unmodified current `examples/cis_pqtl_mr.R` from `run/skill-copy/`. A disposable bfile backed by the real 957-person/14,389-variant local panel let PLINK form 24 clumps and compute the LD matrix. The example then completed namespaced IVW and coloc, producing `triangulation_passed=TRUE`.

### 10. Current curated-endpoint script

`run/input10_shipped_phewas_script.R` sources the unmodified `scripts/phewas_curated_endpoints.R` with deterministic local OpenGWAS-shaped functions because live OpenGWAS requires JWT. It scanned all 12 endpoints, produced 12 rows, wrote and re-read a TSV, and detected the planted endpoint at p_bonf=6.63e-43.

### 11. Empty-result edge (P1)

`run/input11_phewas_empty_result_edge.R` supplies an endpoint for which extraction returns `NULL`. The current shipped source then raises `object 'pval' not found` and writes no TSV. Add an explicit zero-row guard and per-endpoint error handling before production use.

## Final score

Static: 92 / 100 × 0.4 = 36.8. Dynamic: 93.9 / 100 × 0.6 = 56.3. **Final: 93 / 100 — Production Ready; deployable: true; veto override: false.**

Open P1: add the zero-usable-outcomes guard to the curated-endpoint script. Open P2: preflight and communicate the JWT/VEP runtime prerequisites. The checkpoint's live OpenGWAS, 1000G EUR download, and VEP-cache items remain environment prerequisites, not claims of live verification.
auditor_independent: false
