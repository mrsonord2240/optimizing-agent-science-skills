# bio-differential-expression-deseq2-basics fix log

## 2026-09-21 (first fix pass, from audit score 92)

Worktree `F:\OpenScience\wt\differential-expression-deseq2-basics`, branch `fix/differential-expression-deseq2-basics`.
Commits: `b73350b` (fixes), `e700643` (split). Env: `single-cell-transcriptomics-analyst` (R 4.4.3 via `tools\rs.sh`;
DESeq2 1.46.0, apeglm 1.28.0, ashr 2.2.63, PyDESeq2 0.5.4). Data: the audit's `pseudobulk_cd14_mono.rds`.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| "all-zero in a group" listed as a padj=NA cause | P2 (audit) | Now "all-zero across every sample"; added that group-zero genes are tested and give huge LFCs | ran: 0,0,0,0,300,300,300,300 -> LFC 10.88, padj 5e-22; all-zero row -> baseMean 0, NA | |
| lfcShrink "preserves the p-value" but padj differs | P2 (audit) | Insight section: pvalue carried, padj recomputed at alpha 0.1; Standard Workflow and `examples/basic_workflow.R` now pass `res = res` | ran: pvalue identical for apeglm/ashr/normal; padj differs without `res=` (max diff 0.154, metadata alpha 0.1); identical with `res = res` | root cause is lfcShrink's own default alpha, not a re-fit |
| Common-errors row said `summary()` defaults to alpha 0.1 regardless of `results(alpha=)` | found | Row rewritten: `summary(res)` uses the stored alpha (0.05 here); an lfcShrink object stores 0.1 unless `res = res` | ran: summary(res) reported padj < 0.05 after `results(alpha=0.05)` | the audit's input 7 printed the counts but never called summary() |
| `type='normal'` table contradicted itself (`coef=` or `contrast=` vs `coef=` only) and claimed it gives shrunken p-values | found | Both rows aligned: accepts `coef=` or `contrast=`, pvalue still unshrunken Wald, errors on interaction designs | ran: contrast= worked, pvalue identical to results(), interaction design error text confirmed; help page agrees | shrunken p-values need `DESeq(betaPrior=TRUE)` |
| `vst()` "uses the 1000 most-variable genes" | found | Genes span the range of mean normalized count; errors when fewer than nsub rows | help(vst) + ran (500 genes -> error; nsub=200 -> ok) | |
| Prokaryotic and betaPrior sections dead weight (~60 lines) | P2 (audit) | Moved to `references/` with the rest of the split | line-compare + fence parse | |
| SKILL.md 339 lines | brief 2026-09-21 | Split to 176 lines + 11 reference files; Reference Files index; decision-tree and Common-errors pointers | every moved non-blank line found in new files (9 lines differ only by added pointers or the emptied "Per-Method Failure Modes" header); 6 R fences parse, 1 Python fence compiles | |
| Examples | - | `basic_workflow.R` edited; all three run | ran on DESeq2 1.46.0 | |

Redundancy pass (usage-guide.md vs SKILL.md):

| deleted from usage-guide.md | now lives in |
| --- | --- |
| Prerequisites (BiocManager install) | SKILL.md "Version Compatibility" (Install line, plus ashr/IHW/tximport, pydeseq2) |
| "What the Agent Will Do" 6-step list | SKILL.md Standard Workflow (guide points to it) |
| Tips (replicates, prefilter, apeglm/coef, vst vs rlog, reference level, resultsNames, LRT, shrunken LFC vs Wald p, prokaryotic, PyDESeq2) | SKILL.md decision tree, Standard Workflow, Insight, LRT/shrinkage/transform references |
| Input Requirements "rownames must match" | one line added to SKILL.md Standard Workflow (table stays in the guide) |

Disagreement logged: usage-guide "use vst over rlog for >100 samples" vs SKILL.md "rlog only if n<30 and size factors vary >4x"; kept SKILL.md.

## Left unfixed

- **IHW segfaults at default `nbins` in this env (audit note).** Local build issue in the audit env, not a Skill defect; not written into the Skill.

## 2026-09-23 (corrective Phase 1 after M4/P0 rejection)

Worktree `F:\OpenScience\wt\differential-expression-deseq2-basics`, branch `fix/differential-expression-deseq2-basics`.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| Shared Windows R runtime exits 139 after every DESeq2 route, including `library(DESeq2)` | P0 | Created isolated WSL micromamba env `deseq2-repair-20260923` (R 4.4.3, DESeq2 1.46.0, apeglm 1.28.0); no shared runtime or shared package version was changed | `wsl.exe -d science -u sci -- bash -lc 'bash /mnt/openscience/audit-scratch/deseq2-runtime-check/wsl_run_isolated_checks.sh'`: minimal `library(DESeq2)` and unchanged shipped `examples/basic_workflow.R` both exited 0; workflow asserted 1,000 rows and non-NA adjusted p-values, reporting 58 significant genes | The failed F-mounted scratch prefix was removed after verification; the verified env lives under the WSL user's micromamba env root. |
| Source did not match the existing checkpoint/rejection recommendations for pseudobulk discovery and reporting | P1/P2 | Added an explicit pseudobulk trigger to frontmatter and a compact What to Report section | source review; covered workflow exits cleanly in the isolated env | Keeps scope to DESeq2 result reporting; no method expansion. |
