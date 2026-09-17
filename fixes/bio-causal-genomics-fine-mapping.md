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
