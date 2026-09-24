> **Audit record for `bio-differential-expression-deseq2-basics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6900ca0](https://github.com/mrsonord2240/bioSkills/tree/6900ca0bc072c2cf19c33971043bca0bcb6dafa7/differential-expression/deseq2-basics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-differential-expression-deseq2-basics

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@6900ca0bc072c2cf19c33971043bca0bcb6dafa7:differential-expression/deseq2-basics`

This is a corrective final-pass audit. `auditor_independent` is deliberately `false` and its required note is recorded in the JSON report.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|
| 1 | Canonical pseudobulk workflow | 38 | 58 | 96 | 3/3 | ✅ |
| 2 | Batch and paired design | 38 | 57 | 95 | 3/3 | ✅ |
| 3 | padj=NA and tximport edge | 38 | 58 | 96 | 3/3 | ✅ |
| 4 | Interaction and shrinkage | 38 | 58 | 96 | 3/3 | ✅ |
| 5 | Four-level LRT stress test | 38 | 57 | 95 | 3/3 | ✅ |
| 6 | Pseudobulk scope boundary | 37 | 57 | 94 | 3/3 | ✅ |
| 7 | Bare-results adversarial input | 38 | 58 | 96 | 3/3 | ✅ |

**Execution average: 95.4 / 100. Assertion pass rate: 21/21.**

## Environment and clean-exit evidence

All fresh R work ran through WSL distro `science` using `micromamba run -n deseq2-repair-20260923 Rscript`. The isolated environment used R 4.4.3, DESeq2 1.46.0, apeglm 1.28.0, ashr 2.2.63, IHW 1.34.0, and tximport 1.34.0.

- `run/corrective_phase2_suite.R` completed all seven inputs and printed `ALL CORRECTIVE INPUTS PASSED`.
- `run/corrective_phase2_examples.sh` reran each shipped example. `run/corrective_phase2_examples_exit_codes.txt` records `basic_workflow exit=0`, `batch_correction exit=0`, `multi_condition exit=0`, and `ALL SHIPPED EXAMPLES EXITED 0`.
- `run/corrective_phase2_suite.log` and `run/shipped_*.log` retain the output used for this evaluation.

## Detailed outputs

### Input 1 — Explicit-contrast donor pseudobulk workflow

The canonical synthetic count matrix recovered 33 calls from 30 planted genes. `condition_treated_vs_control` was explicit. With `res=res`, apeglm preserved both `pvalue` and `padj`, exactly as the current Standard Workflow says.

Assertions: explicit coefficient PASS; pvalue behavior PASS; padj behavior PASS.

### Input 2 — Batch-adjusted and paired designs

The named condition LFC vector was identical for `~ batch + condition` and `~ condition + batch`. The paired `~ donor + condition` model exposed the named condition coefficient and exited cleanly.

Assertions: batch named contrast PASS; formula-order invariance PASS; paired-design order PASS.

### Input 3 — padj=NA and tximport

`ZERO_IN_CONTROL` was testable, while `ALL_ZERO` had `padj=NA`. IHW returned a `DESeqResults` table, and a synthetic tximport object constructed a `DESeqDataSet` through `DESeqDataSetFromTximport()`.

Assertions: group-zero distinction PASS; all-zero distinction PASS; IHW and tximport execution PASS.

### Input 4 — Interaction and shrinkage

apeglm rejected the arbitrary list contrast as documented. ashr accepted it, and the `~ 0 + group` workaround correlated above 0.999 with the summed contrast.

Assertions: apeglm limitation PASS; ashr workaround PASS; combined-factor agreement PASS.

### Input 5 — Four-level LRT

The omnibus LRT produced adjusted p-values; its `log2FoldChange` exactly equalled the last named Wald coefficient, demonstrating why it must not be reported as a single omnibus effect size.

Assertions: LRT route PASS; LRT-LFC interpretation PASS; adjusted-p-value output PASS.

### Input 6 — Cells are not biological replicates

Eighty synthetic cells were aggregated to eight donor-level columns before fitting. The deterministic null pseudobulk comparison had zero adjusted-significant calls. The Skill’s donor-level pseudobulk routing is appropriate.

Assertions: one column per donor PASS; named condition coefficient PASS; boundary guidance PASS.

### Input 7 — Bare results and threshold FDR claim

On `~ condition + batch`, bare `results(dds)` selected `batch_B_vs_A`, not the intended condition. `results(lfcThreshold=1)` returned a valid threshold-test result, which is distinct from a post-hoc shrunken-LFC filter.

Assertions: bare-results trap PASS; lfcThreshold route PASS; FDR interpretation PASS.

## Source review and gates

The exact branch tip is clean at `6900ca0bc072c2cf19c33971043bca0bcb6dafa7`. Relative to the rejected `e700643` source, the only source changes are the explicit pseudobulk trigger in frontmatter and the compact **What to Report** section. Both are present at the audited tip. All 11 referenced Markdown files exist, all three R examples parse, and `git diff --check` passed.

Structural veto: T1 PASS, T2 PASS, T3 PASS, T4 PASS.

Research veto: M1 PASS, M2 PASS, M3 PASS, M4 PASS. The previous M4 failure was the shared Windows R shutdown fault; it does not reproduce in the isolated WSL environment, where every fresh execution exited 0.

## Final

Static score: 93/100. Dynamic score: 95.4/100. Final score: **94/100**.

**Grade: ⭐ Production Ready. Deployable: true.**

P2 only: consider adding deterministic expected-result assertions to the teaching examples in a future change. No P0 or P1 remains.

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@6900ca0bc072c2cf19c33971043bca0bcb6dafa7:differential-expression/deseq2-basics`
- `auditor_independent:false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@6900ca0bc072c2cf19c33971043bca0bcb6dafa7:differential-expression/deseq2-basics`
- `auditor_independent: false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`
