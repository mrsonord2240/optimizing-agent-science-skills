# bio-causal-genomics-fine-mapping — 2026-09-17

Worktree: `F:\OpenScience\wt\cg-fm`, branch `fix/cg-fine-mapping`, commit `c5fd9ff`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `coloc.susie` example crashes with a cryptic `data.table` error unless z/LD carry SNP names | P1 | Added a **Precondition** note in "Coloc.susie Integration" explaining `coloc.bf_bf`'s `intersect(colnames(...))` match, added `names(z1) <- names(z2) <- colnames(ld_matrix) <- rownames(ld_matrix) <- snp_ids` to the worked example, and added a Common Errors row | ran | Reproduced the audit's `run/input4_coloc_susie.R` setup (5000 x 250 SNPs, planted shared causal SNP 130) via `r.sh` with susieR 0.14.2 / coloc 5.2.3. Fixed pattern succeeds: max PP.H4 = 1.0000, top hit = rs0000130 (planted). |
| No platform caveat that FINEMAP / SuSiEx / PAINTOR / DAP-G are POSIX-only CLI tools | P1 | Added one consolidated **Platform note** near the top of SKILL.md (before the Algorithmic Taxonomy table, so it precedes every CLI tool's first real mention): no native Windows build, use WSL or `susie_rss`/SuSiE-inf | docs | Matches the audit's Input 6 finding: no finemap/SuSiEx/PAINTOR/dap-g binary exists on this machine or has a Windows build (confirmed by filesystem search in the audit). Single mention chosen over four repeated notes per the redundancy rule. |
| All technical depth sits inline in SKILL.md rather than in `references/` | P2 | Left unfixed | n/a | FIX_BRIEF scopes the "one restructuring" to removing SKILL.md/usage-guide.md duplication, not extracting new reference files; moving the Algorithmic Taxonomy / Quantitative Thresholds / Reviewer Pushback tables is restructuring beyond that, and beyond "keep diffs minimal." Declined. |
| Individual-level and CLI paths lack a genotype-QC checklist | P2 | Left unfixed | n/a | This is new content (no existing checklist text to correct), and FIX_BRIEF's scope excludes new content unless it backs an already-referenced but unbacked executable. Declined. |

## Redundancy pass (every-pass rule, not audit-flagged)

`usage-guide.md`'s `## Tips` section (10 bullets) fully restated `SKILL.md` content:

| Deleted Tips bullet | Now lives in SKILL.md |
|---|---|
| In-sample LD beats reference LD | "LD reference mismatch (most common)" — Fix |
| Always run estimate_s_rss | "Critical LD Diagnostic Block (susie_rss)" |
| Credible set is the unit of inference | "Credible-set misinterpretation" — Fix |
| L is cheap to increase | "L too small" — Fix |
| Purity filter | Quantitative Thresholds table; "Reconciliation" Operational rule |
| PolyFun argument (`prior_weights` not `prior_variance`) | "prior_weights vs prior_variance confusion" |
| Non-sparse loci -> SuSiE-inf | "Non-sparse architecture (biobank scale)" — Fix |
| HLA / chr8 inversion | "HLA and Long-Range LD: When to Stop" |
| PSD violations -> `diag(1e-4)` / `nearPD` | Common Errors, "Negative eigenvalues in LD matrix" row |
| Cross-ancestry -> SuSiEx shrinks credible sets | "Cross-Ancestry Fine-Mapping with SuSiEx" |

Replaced with one pointer sentence naming the four owning SKILL.md sections. Nothing the agent needs was deleted — every fact above already existed verbatim or near-verbatim in SKILL.md before this pass.

## Findings fixed: 2/4 (both P1). Both P2s left unfixed with reasons above, per dispatch scope.

Nothing needs Sam.

---

# bio-causal-genomics-fine-mapping — 2026-09-21

Worktree `F:\OpenScience\wt\causal-genomics-fine-mapping`, branch `fix/causal-genomics-fine-mapping` (from staging `431aa55`). Commits: `e49fd56` (fix + dedup), `dbbf7ea` (split), `4adb8d5` (scripts/ step). Env: `mendelian-randomization-analyst` (R 4.4.3 via `r.sh`, susieR 0.14.2, coloc 5.2.3; plink2 a7.6 in the env's `tools\plink2`).

Audit report read: 3 P2 findings (re-audit of the 2026-09-17 fix). Fixed 1/3 as worded; 1 fixed by the split; 1 left unfixed. Three further defects found while verifying and fixed inline.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| coloc.susie SNP-naming precondition documented but not guarded in code | P2 | `stopifnot(...)` on shared `lbf_variable` colnames placed directly before `coloc.susie()` in the worked example (now in `references/coloc-susie.md`) | ran | Extracted the documented block from SKILL.md and ran it: named input succeeds (PP.H4 = 1, planted SNP rs0020); same block minus the `names()` line stops with the guard message instead of the data.table error. |
| SKILL.md carries all technical depth inline (444 lines) | P2 | Split into 8 `references/` files, SKILL.md 482 -> 296 lines (see table below) | ran (line-by-line comparison, fence parse: 4 bash fences `bash -n`, 6 R fences `parse()`) | 482 was after the dedup pass added Tool Install Notes (+38 lines). |
| Individual-level and CLI paths lack a genotype-QC checklist | P2 | Left unfixed | n/a | See left-unfixed list. |
| `plink --r2 square` given as the in-sample LD recipe | found, not audit-flagged | `--r square` (signed r) with a note that `--r2` writes squared correlations | ran (plink2 a7.6: `--r-unphased square` min -0.13, `--r2-unphased square` min 4.7e-7); docs for PLINK 1.9 | `susie_rss` needs signed R; `examples/finemap_pipeline.sh` already used `--r square`. |
| Reporting schema `L_used = sum(!fit$sets$pruned)` | found | `sum(fit$V > 0)` | ran | `fit$sets$pruned` does not exist in susieR 0.14.2 (`names(fit$sets)` = cs, purity, cs_index, coverage, requested_coverage), so the old formula evaluated to 0. `sum(fit$V > 0)` = 1 on a one-signal fit. |
| kriging_rss comment / threshold row name the wrong quantity | found | Name the real column `z_std_diff` (data.frame: z, condmean, condvar, z_std_diff, logLR) | ran (columns printed; audit scripts already used `z_std_diff`) | Shorthand `|z_obs - z_exp|` kept in prose. |

## Redundancy pass (2026-09-21)

The 2026-09-17 pass had removed the Tips block. Remaining guide content that restated or belonged to SKILL.md:

| Deleted passage (usage-guide.md) | New home | Verified |
|---|---|---|
| `## Prerequisites` (R install, FINEMAP / PolyFun / PAINTOR / SuSiEx / DAP-G / FOCUS / PLINK install commands) | SKILL.md `## Tool Install Notes`, verbatim | grep |
| `## What the Agent Will Do` steps 1-8 | SKILL.md Decision Tree, Critical LD Diagnostic Block, Quantitative Thresholds (purity >= 0.5), Required Reporting Schema, Coloc.susie Integration; VEP annotation is in the guide's Related Skills | grep |

Disagreement logged: the guide said a 1-3 Mb locus window; SKILL.md says +/- 500 kb default (5+ Mb only for long-range LD). SKILL.md kept.

## Split map (SKILL.md 482 -> 296; verbatim moves, only pointer-edited rows changed)

| Old SKILL.md section | New home |
|---|---|
| Algorithmic Taxonomy; Reconciliation table (the Operational rule stays in SKILL.md) | `references/method-comparison.md` |
| Per-Tool Failure Modes > Allele Harmonization with the LD Reference | `references/allele-harmonization.md` |
| Functional Priors with PolyFun (+ Manual Coding-Variant Priors) | `references/polyfun-functional-priors.md` |
| Cross-Ancestry Fine-Mapping with SuSiEx | `references/susiex-cross-ancestry.md` |
| FINEMAP CLI Pattern | `references/finemap-cli.md` |
| Coloc.susie Integration | `references/coloc-susie.md` |
| HLA and Long-Range LD: When to Stop | `references/hla-long-range-ld.md` |
| Anticipated Reviewer Pushback | `references/reviewer-pushback.md` |

Check: every non-blank line of the pre-split SKILL.md is found verbatim in SKILL.md + references/ except 8 decision-tree / Common Errors table rows that gained a `references/...` pointer.

## Runnable code -> scripts/ (Sam, 2026-09-21)

No `scripts/` directory created. Code blocks in SKILL.md and references/: install (3 + 25 lines, not runnable code), LD diagnostic (12), allele harmonize helper (8), PolyFun bash (12) and two R fragments (7, 8), coloc.susie (12), SuSiEx (12), FINEMAP (19). None but FINEMAP reaches ~15 lines, and the FINEMAP and SuSiEx blocks duplicate `examples/finemap_pipeline.sh` and `examples/susiex_multiancestry.sh`.

| Old location | Change |
|---|---|
| `references/finemap-cli.md` 19-line block | Replaced by a pointer to `examples/finemap_pipeline.sh` plus one line keeping the tuning flags (`--n-iterations`, `--n-convergence`) and the file-format notes |
| `references/susiex-cross-ancestry.md` 12-line block | Replaced by a pointer to `examples/susiex_multiancestry.sh` (the one-line form stays in SKILL.md) |

Both examples pass `bash -n`; they could not be run because no FINEMAP or SuSiEx binary exists on this machine (audit Input 6).

## Left unfixed

- **Genotype-QC checklist for the individual-level `susie(X, y)` and CLI paths (P2).** New content (call rate, HWE and MAF thresholds), not a correction: the Skill has no existing QC text to fix, and the thresholds would be unsourced from anything the audit ran.
- FINEMAP / SuSiEx / PAINTOR / DAP-G flags remain checked only against the tools' documentation, not run: no binary exists here (unchanged from the 2026-09-17 audit).

Nothing needs Sam.

---

# bio-causal-genomics-fine-mapping — final pass, 2026-09-21

Worktree `F:\OpenScience\wt\causal-genomics-fine-mapping`, branch `fix/causal-genomics-fine-mapping`
(same branch as above). Env: `mendelian-randomization-analyst`. Phase 1 only (fix, broad install
permission) — full detail in `F:\OpenScience\audits\_final_pass\bio-causal-genomics-fine-mapping\CHECKPOINT.md`.

This pass installed FINEMAP 1.4.2 and SuSiEx 1.1.2 (both bioconda, WSL `science` distro) and built
DAP-G from source (`xqwen/dap` @ `875ba40`, GSL + OpenMP) — none of the three existed on this machine
before, so "FINEMAP / SuSiEx / PAINTOR / DAP-G flags remain checked only against docs" (above) is now
resolved for FINEMAP, SuSiEx, and DAP-G. Real, previously-unverified defects found and fixed by running
each tool end-to-end on synthetic loci with a planted causal SNP:

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| FINEMAP `--prob-tol`/`--n-iterations`/`--n-convergence` don't exist in FINEMAP 1.4.2 | P1 | Renamed to `--prob-conv-sss-tol`/`--n-iter`/`--n-conv-sss` in `SKILL.md`, `references/finemap-cli.md`, `examples/finemap_pipeline.sh` | ran | Old flags aborted with `Cannot recognize flag`; fixed flags ran to completion, planted SNP top-ranked. |
| `plink --r square` writes tab-delimited output; FINEMAP requires spaces | P1 | Added `spaces` modifier everywhere `--r square` feeds a FINEMAP `.ld` file | ran | Without it: `Expected N SNPs in row 1 ... but encountered only 1 SNPs`. |
| FINEMAP writes `<prefix>.cred<k>` per causal-count model, never a plain `<prefix>.cred` | P2 | Fixed Outputs description and `examples/finemap_pipeline.sh`'s report step (loops `locus.cred*`) | ran | Only `locus.cred1` was ever written in this session's runs. |
| SuSiEx 1.1.2 requires `--plink=<path>`, undocumented | P1 | Added to `SKILL.md` one-liner and `examples/susiex_multiancestry.sh` | ran | Omitted: fails inside SuSiEx's own internal PLINK calls with a confusing `No variants remaining after --extract`. |
| SuSiEx's `--ld_file` is an output prefix it computes itself, not a pre-built matrix (Skill said to pre-build with `plink --r square`) | P1 | Corrected `SKILL.md`, `references/susiex-cross-ancestry.md`, `examples/susiex_multiancestry.sh` | ran | Verified on a synthetic 2-population locus, planted shared causal: `CS_PIP = 1.0`. |
| `examples/susie_finemapping.R` crashes under susieR 0.14.2 (`estimated prior variance is unreasonably large`) | P1 | Rewrote z-score generation as `z ~ N(R %*% true_z, R)`; added the Skill's own documented PSD ridge fix (LD matrix wasn't PSD) | ran | Now recovers both planted causals at PIP 1.0000. Also fixed a stray "Reference: ggplot2" header comment (script only uses susieR). |
| DAP-G named throughout (decision tree, method comparison, install notes) with zero runnable code anywhere in the Skill | missing referenced executable | Built DAP-G from source; added `references/dap-g-cli.md` and `examples/dapg_finemap.sh` | ran | Verified against DAP-G's own bundled real example (4 signal clusters) and against the shipped example on the FINEMAP-fix synthetic locus (planted SNP, cluster PIP 0.9998). Also documents a real non-obvious defect: `dap-g` exits status 1 on full success. |
| FINEMAP/SuSiEx install notes pointed at a dead static-download page / source-only build | P2 | Added bioconda as the verified working route for both | verified: ran (installed + smoke-tested) |
| PolyFun `pandas<3` pin never recorded in `SKILL.md` | P2 | Added a one-line pin note in Tool Install Notes | docs (the Skill's own documented `--compute-h2-L2` command does not hit this bug — confirmed by the prior audit's real run; other PolyFun flags might) |

`SKILL.md`: 296 -> 300 lines (added Common Errors rows and a references pointer for DAP-G; trimmed
Tool Install Notes verbosity and merged 3 FINEMAP rows + 2 SuSiEx rows in Common Errors to stay at the
300-line cap).

Also re-ran (no defect, no change) `examples/susie_rss_finemap.R`, `references/allele-harmonization.md`'s
`harmonize_z_to_ref()`, and `references/polyfun-functional-priors.md`'s `build_manual_priors()` against
hand-built assertions — all correct.

## Left unfixed (this pass)

- **PAINTOR**: not on bioconda/conda-forge; two `git clone bogdanlab/PAINTOR_V3.0` attempts under
  background execution both stalled with the clone left in job-control state `T` (stopped) rather than
  completing or erroring — looks like an artifact of this session's background-execution setup (a
  concurrent, unrelated session's own download in the same WSL distro completed normally at the same
  time), not a confirmed network/repo problem. Needs a foreground/interactive retry. Build deps (GSL,
  NLopt, Eigen) confirmed available on conda-forge.
- **Genotype-QC checklist (P2)**: unchanged from above, still new content out of a fixer's scope.

Nothing needs Sam beyond the PAINTOR retry note above.
