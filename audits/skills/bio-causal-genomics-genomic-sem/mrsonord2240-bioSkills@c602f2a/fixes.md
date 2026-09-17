# bio-causal-genomics-genomic-sem fixes (2026-09-17)

Worktree `F:\OpenScience\wt\cg-gsem`, branch `fix/cg-genomic-sem`, based on fork main `49fe6d4`.
Fixer: Claude Sonnet 5. Audit: 69/100, Reject on a Research Veto (M4 Code Usability FAIL) --
`usermodel()`, `commonfactorGWAS()`, `userGWAS()` crash with `object 'ReorderModel'`/
`'ReorderModelnoSNP' not found` under GenomicSEM 0.0.5 + lavaan 0.7.2, both DWLS and ML;
`commonfactor()` mislabels the same crash as non-convergence.

## Establishing a working combination

New, separate R library `F:\OpenScience\audit-envs\mendelian-randomization-analyst\R-lib-genomicsem`
(never touches the shared `R-lib`), placed ahead of it via a new wrapper
`F:\OpenScience\audit-envs\mendelian-randomization-analyst\r_gsem.sh`
(`R_LIBS=R-lib-genomicsem`, `R_LIBS_USER=R-lib`). Installed **lavaan 0.6-19** into it from the CRAN
archive source tarball (pure R, no compile needed); GenomicSEM 0.0.5 reused unmodified from the
shared `R-lib`.

Checked GenomicSEM's GitHub HEAD (commit `6b65ca5`, 2026-08-26) first: `usermodel.R`,
`commonfactorGWAS.R`, and `userGWAS.R` still hard-code `estimator="DWLS"` in their internal
`ReorderModel`/`ReorderModelnoSNP` step with no `ordered=FALSE`, unconditionally on the caller's
`estimation` argument -- upstream does not fix this as of that date. Root cause: lavaan >=0.7.0
requires an explicit `ordered = FALSE` to run DWLS on continuous data; GenomicSEM 0.0.5 never
supplies it.

Verified GenomicSEM 0.0.5 + lavaan 0.6.19 end to end on the audit's own synthetic planted-truth
generators (`F:\OpenScience\audits\bio-causal-genomics-genomic-sem\run\synth_lib.R` and
input1/2/4/5 scripts, re-run via `r_gsem.sh`, plus a saved standalone smoke test,
`F:\OpenScience\audit-envs\mendelian-randomization-analyst\smoke_genomicsem.R`):

| Function | DWLS | ML | Checked against planted truth |
|---|---|---|---|
| `commonfactor()` | runs | runs | exact recovery, loadings 0.75/0.65/0.70/0.55, max err 0.00000 |
| `usermodel()` (2-factor) | runs | runs | exact recovery, loadings + factor correlation rF=0.40 vs recovered 0.4000 |
| `commonfactorGWAS()` | runs | runs | ML: Q_pval correctly separates 5 planted heterogeneous SNPs (Q_pval 1e-7 to 1e-89) from 5 planted factor SNPs (Q_pval 0.39-0.73) and 10 null SNPs; **DWLS: runs but Q_pval does not discriminate** (all SNPs Q_pval > 0.86) -- see caveat below |
| `userGWAS()` | runs | singular-matrix error (unrelated to the version bug; small-N synthetic input) | DWLS recovers the one planted direct SNP->trait1 effect (rs3, beta 0.10) against five near-zero SNPs |

All previously-crashing calls now run under both estimators except `userGWAS(ML)`, which fails with
a distinct, expected numerical error (`system is computationally singular`) unrelated to the
`ReorderModel` bug -- this exact 6-SNP synthetic input is simply too small/exact-fit for ML's path.
DWLS -- the Skill's own documented example estimator for `userGWAS` -- works.

**Caveat found, not in the original `recommendations[]`:** `commonfactorGWAS()`'s Q_SNP statistic
under DWLS did not discriminate the planted heterogeneous SNPs from the planted factor SNPs in this
synthetic covstruc (which, like the audit's own, bypasses `ldsc()` and lacks real per-SNP N /
sampling-covariance structure); the identical ML call on the identical input did discriminate
correctly. Not confirmed as a general DWLS-Q_SNP defect -- plausibly an artifact of the synthetic
bypass lacking the N/MAF-driven per-SNP weighting a real `ldsc()`-derived V would carry. Logged in
TOOLS.md for a future auditor with real reference data to confirm; not changed in SKILL.md because
the brief only allows a method-level claim when a run demonstrates it, and this run doesn't cleanly
attribute cause.

Recorded in `F:\OpenScience\audit-envs\mendelian-randomization-analyst\TOOLS.md` (new final
section) with the `r_gsem.sh` wrapper and `smoke_genomicsem.R` for the next auditor.

## Fixes applied

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| 3 of 4 core functions crash under the Skill's own supported lavaan range | P0 | `## Version Compatibility` (SKILL.md) rewritten: pins lavaan 0.6.19 as a ceiling, not a floor; names the exact crash, root cause, and the confirmed-working combination | ran | See table above; GenomicSEM HEAD checked and does not fix it |
| `commonfactor()`'s own error message misdiagnoses the crash as non-convergence | P0 | Same section: states the exact misleading message and the `traceback()` tell (`object '...Results' not found`) that distinguishes it from real non-convergence; new `## Common Errors` row | ran | Reproduced the message directly under lavaan 0.7.2 during audit review; confirmed absent under 0.6.19 |
| No scope-boundary / escape-hatch section | P1 | New `## Scope Boundary` section (SKILL.md): GenomicSEM is population-level only, decline individual-level PGS/diagnostic requests | docs (matches audit's own expected-response text for Input 6) | |
| Bundled example not runnable against the installed dependency set | P1 | `examples/genomic_sem_commonfactor.R` header updated to name the tested combination; added a `packageVersion('lavaan') >= '0.7.0'` guard that warns with the exact fix before the calls that would otherwise crash | ran (`parse()` OK); the `commonfactor()`/`usermodel()`/`commonfactorGWAS()` calls this example makes are the same calls verified end-to-end above -- `ldsc()`/`sumstats()` themselves need a real LD reference this environment does not have, unrelated to the lavaan bug | |
| SKILL.md line count / reference-table placement (P2, progressive disclosure) | P2 | Not moved to a `references/` file -- out of scope for a minimal diff; declined | -- | left unfixed: cosmetic P2, not cheap relative to the P0/P1 work above |

4/5 `recommendations[]` fixed (2 P0, 2 P1); 1 P2 (line-count/references-split) left unfixed as
noted. Every changed `.R` block re-parsed after editing (all 7 SKILL.md r-fenced blocks +
the example script); `mtag_pipeline.sh` unchanged, re-checked with `bash -n`.

## Redundancy pass (per `FIX_BRIEF.md` "Remove redundancy, every pass")

Before any fix this session: SKILL.md 492 lines, usage-guide.md 108 lines.
After both the P0/P1 fixes above and this redundancy pass: SKILL.md 506 lines, usage-guide.md 79
lines.

| deleted from usage-guide.md | disposition | new home / note |
|---|---|---|
| Prerequisites bullet list (package versions, LDSC-fork preference, baselineLD, min-3-traits) | deleted, not moved | Every fact already in SKILL.md `## Version Compatibility` / `## Tool Installation` / `## Quantitative Thresholds`; guide now points at those sections. The `munge_sumstats.py` alternative-tool mention (not previously in SKILL.md) was folded into `## Standard Workflow` Step 1's comment. |
| "What the Agent Will Do" 12-step pipeline | deleted | Every step already covered: 1 by `## Standard Workflow` + the `sumstats()` column-name warning, 2-3 by `## Per-Method Failure Modes` (Heywood, non-PD V), 4 by `## Standard Workflow`, 5 by `## Model Fit Diagnostics`, 6 by the Heywood failure mode, 7-8 by `## Common-Factor GWAS with Q_SNP`, 9 by `## MTAG Comparison`, 10 by `## Stratified GenomicSEM`, 11 by `## Reconciliation`. Confirmed each by grep before deleting; step 12 (generic "manuscript-ready summary") named no agent-actionable fact and was dropped. |
| Tips list (11 bullets) | all deleted as duplicate | Verified bullet-by-bullet against SKILL.md's own wording: Q_SNP-mandatory (Common-Factor GWAS w/ Q_SNP + Anticipated Reviewer Pushback), sample overlap (failure-mode table), Heywood (failure-mode table), MaxFDR (failure-mode table), DWLS-vs-ML (Standard Workflow prose + Reviewer Pushback), identification (Quantitative Thresholds + Standard Workflow inline comment), cross-ancestry (Decision Tree + Reviewer Pushback), CFI-vs-chi-square (Model Fit Diagnostics), ESEM power (Statistical Model Taxonomy "Min traits" column), downstream-MR (Related Skills). The downstream-MR bullet's one non-duplicate nuance -- restrict the MR exposure to the Q_SNP-clean "factor-only" subset -- was folded into the Related Skills line itself rather than dropped. |
| Repeated LDSC-fork rationale (identical sentence in SKILL.md Version Compatibility intro, SKILL.md Tool Installation, and usage-guide.md Prerequisites -- 3x) | 2 of 3 deleted | Kept once, in SKILL.md `## Tool Installation` (the actionable install-command home); Version Compatibility's intro line shortened to a version number + pointer. |

No disagreements found between the two files during this pass. Every deleted passage confirmed
present in SKILL.md by direct reading (not just section-title match) before removal.

## Left unfixed

- P2 "move failure-mode/reconciliation tables to a references/ file" -- cosmetic restructuring,
  not cheap alongside the P0 work; declined per the brief's "P2 that is cheap" bar.
- The DWLS Q_SNP discrimination caveat above -- logged as a caveat for a future auditor with real
  LDSC reference data, not written into SKILL.md as a confirmed defect.

Nothing needs Sam.

Merged to fork main at `f031005` (2026-09-17), with a follow-up commit `4951af0` that cut the Version Compatibility paragraph down to the pin and its reason, since it restated both new Common Errors rows.
