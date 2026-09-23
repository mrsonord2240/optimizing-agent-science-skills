> **Audit record for `bio-differential-expression-deseq2-basics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@e700643](https://github.com/mrsonord2240/bioSkills/tree/e70064331a8091df08a09ebee3368302bc0f622e/differential-expression/deseq2-basics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-differential-expression-deseq2-basics

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@e70064331a8091df08a09ebee3368302bc0f622e:differential-expression/deseq2-basics`

Final-pass metadata: `auditor_independent: false`; `note: final pass: fixed and audited under one brief, see CHECKPOINT.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Execution |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical pseudobulk | 32 | 49 | 81 | 3/4 | PARTIAL: validated output, exit 139 |
| 2 | Batch, sex, paired | 25 | 35 | 60 | 2/4 | PARTIAL: paired regression ended early |
| 3 | padj=NA edge cases | 31 | 47 | 78 | 3/4 | PARTIAL: validated output, exit 139 |
| 4 | Interaction/shrinkage | 32 | 50 | 82 | 3/4 | PARTIAL: validated output, exit 139 |
| 5 | LRT stress | 32 | 49 | 81 | 3/4 | PARTIAL: validated output, exit 139 |
| 6 | Cell-level scope boundary | 33 | 52 | 85 | 3/4 | PARTIAL: validated output, exit 139 |
| 7 | Adversarial inference | 32 | 49 | 81 | 3/4 | PARTIAL: validated output, exit 139 |

Execution average: **78.3/100**. Assertion pass rate: **20/28**.

The output-level scientific checks passed. The Research Veto is nevertheless **FAIL** at M4 because the declared R runtime exits with code 139 after every DESeq2 route, including a minimal `library(DESeq2)` script that printed `minimal DESeq2 load: PASS` before exiting 139.

## Inputs and observed output

### 1 — Canonical: donor-level CD14 pseudobulk DE

Prompt: “Run treated-versus-control pseudobulk DE for CD14 monocytes from eight donors, preserving the requested FDR.”

Executed: `run/input1.R` → `run/input1_p2.log`.

Observed: `19` calls, all `19` injected true positives; the named coefficient was `condition_treated_vs_control`. `lfcShrink()` preserved `pvalue`, did not preserve `padj` without `res = res`, and bare `results()` changed meaning with formula order. The log reached `DONE`; the DESeq2 R process did not exit cleanly.

Assertions: PASS explicit reference; PASS named contrast; PASS pvalue/padj distinction; FAIL clean R exit.

### 2 — Variant A: nuisance terms and pairing

Prompt: “Control for batch and sex, then use a donor-paired DE design.”

Executed: `run/input2.R` → `run/input2_p2.log`.

Observed before the process ended: `~ condition` yielded 19 calls (19 true); `~ batch + condition` yielded 25 calls (24 true); `~ batch + sex + condition` yielded 24 calls (24 true); the named condition contrast remained stable when batch was last. The paired-data segment did not finish under the unstable R process.

Assertions: PASS named nuisance formulas; PASS named contrast independent of formula order; FAIL paired regression completion; FAIL clean R exit.

### 3 — Edge: three padj=NA mechanisms

Prompt: “Explain and recover a biologically relevant gene with `padj=NA`.”

Executed: `run/input3.R` → `run/input3_p2.log`.

Observed: independent filtering recovered `MASTER_TF` at padj `0.008`; disabling Cook’s cutoff exposed `ONE_SAMPLE_GENE`; IHW (`nbins=4`, per env note) recovered `MASTER_TF` at `0.00225`. The group-zero `ZERO_IN_CONTROL` gene was testable (`padj=0`), consistent with the fixed source text. The log reached `DONE`, then R exited 139.

Assertions: PASS separated causes; PASS group-zero diagnosis; PASS IHW inspected; FAIL clean R exit.

### 4 — Variant B: interaction and LFC shrinkage

Prompt: “Test whether treatment differs by sex, then report shrunken treatment effect within males.”

Executed: `run/input4.R` → `run/input4_p2.log`.

Observed: the reference-level treatment effect had 11 calls; the true-null interaction had 0; the male summed contrast had 6. apeglm produced the documented `only for use with 'coef'` error for the list contrast; ashr and the `~ 0 + group` workaround agreed at correlation `1`. R then exited 139.

Assertions: PASS level-specific interpretation; PASS documented apeglm limitation and ashr route; PASS combined-factor agreement; FAIL clean R exit.

### 5 — Stress: four-level omnibus LRT

Prompt: “Find any difference among four groups and provide interpretable effect sizes.”

Executed: `run/input5.R` → `run/input5_p2.log`.

Observed: the LRT LFC equalled the last named Wald coefficient and did not equal the first; the valid `reduced = ~ batch` form returned 25/25 true calls. The log reached `DONE`, then the DESeq2 session failed at exit.

Assertions: PASS LRT omnibus route; PASS no omnibus-LFC misreport; PASS reduced model preserves batch; FAIL clean R exit.

### 6 — Scope boundary: cells are not replicates

Prompt: “Treat 1,184 cells as independent replicates instead of aggregating by donor.”

Executed: `run/input6.R` → `run/input6_p2.log`.

Observed on a constructed null split: cell-level Wilcoxon returned 78 false positives, cell-level DESeq2 returned 30, and donor-level pseudobulk returned 0 (smallest padj `1.00`). On the real contrast, cell-level Wilcoxon precision was `0.523`; pseudobulk was `1.000`. The route is scientifically correct, but R exited 139 after output.

Assertions: PASS refusal/alternative; PASS null measurement; PASS donor aggregation; FAIL clean R exit.

### 7 — Adversarial: invalid FDR claim and bare results

Prompt: “Use bare `results(dds)`, filter `|shrunken LFC| > 1`, and call it a 5% FDR result.”

Executed: `run/input7.R` → `run/input7_p2.log`.

Observed: post-hoc shrinkage filtering was rejected in favor of `lfcThreshold`; bare `results()` on `~ condition + batch` returned batch and gave precision `0.017`, versus `1.000` for the named condition coefficient; stored alpha changed the summary count from 19 at 0.05 to 22 at 0.1. The log reached `DONE`, then R exited 139.

Assertions: PASS valid threshold alternative; PASS bare-results demonstration; PASS alpha demonstration; FAIL clean R exit.

## Additional Phase 2 coverage

Two new post-fix checks were run beyond the seven regression inputs:

- `run/p2_input5_shipped_examples.R` sourced all three shipped examples. Each printed its PASS assertion and returned expected 1,000-row results before the shared R runtime exit fault.
- `run/p2_input6_reference_blocks.R` executed interaction/ashr, LRT, all-zero versus group-zero, `poscounts`, VST, and `tximport()` → `DESeqDataSetFromTximport()` routes. Every assertion printed PASS before the same exit fault.
- `run/p2_input7_pydeseq2.py` executed the Python reference block successfully: 80 result rows and 80 non-null adjusted p-values. `py_compile` also passed.
- `run/p2_r_shutdown_smoke.R` printed `minimal DESeq2 load: PASS` and exited 139, independently demonstrating an environment-level R failure.

## Static review and gates

Structural veto: T1 PASS, T2 PASS, T3 PASS, T4 PASS. All eleven referenced markdown files and all three shipped examples are present. The source worktree remained clean at the requested tip.

Research veto: M1 PASS; M2 PASS; M3 PASS; **M4 FAIL** (declared R environment exits 139). The audit cannot mark the Skill deployable from this environment.

Static score: **90/100**. Dynamic score: **78.3/100**. Numeric result before veto: **83/100**. Veto override: **true**. Final: **❌ Reject; deployable false**.

## Recommendations

1. **P0:** Repair or rebuild the declared `single-cell-transcriptomics-analyst` R runtime, then rerun the saved scripts. This is an environment defect, not a source edit authorized in this audit.
2. **P1:** Reconcile `CHECKPOINT.md`: it claims a frontmatter pseudobulk trigger and what-to-report section that are absent at the pinned tip.
3. **P2:** Add a pseudobulk trigger to frontmatter.
4. **P2:** Add the compact reporting fields claimed by the checkpoint.
