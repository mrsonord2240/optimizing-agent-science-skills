# Fix log — bio-microbiome-differential-abundance

2026-09-19. Fixer for `microbiome/differential-abundance` (skill-id `bio-microbiome-differential-abundance`,
audited at 87/100, Limited Release, deployable, no open P0). Audit evidence originally filed under
`bio-differential-abundance-microbiome`, since corrected to match the frontmatter `name`.

Worktree `F:\OpenScience\wt\mb-da`, branch `fix/mb-diff-abundance`, commit `aeee6e0`.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| LinDA section's own code crashes on a real phyloseq object (`invalid class "sample_data" object`) | P1 | `meta <- as.data.frame(sample_data(ps))` -> `meta <- data.frame(as(sample_data(ps), 'data.frame'))`; added a Common Errors row | ran | Ran fixed `linda()` end to end against `phyloseq_object.rds` via `rr.sh` (R 4.4.3, MicrobiomeStat 1.4) — completed, real output columns. |
| (found while fixing the above) the LinDA formula `~ Group + Age + (1 \| SubjectID)` also crashes independently of the coercion bug — `phyloseq_object.rds` is cross-sectional, so `SubjectID` has as many levels as observations, and `linda()` errors "number of levels of each grouping factor must be < number of observations" | P1 (self-found, same code block) | Changed the shown default formula to `~ Group + Age` (fixed effects only) with a comment showing how to add `+ (1 \| SubjectID)` for repeated/paired designs — mirrors the existing `rand_formula = NULL` pattern already used in the ANCOM-BC2 section | ran | Verified the fixed-effects formula runs end to end on `phyloseq_object.rds`. The mixed-model path itself was already independently confirmed working (no crash) by the audit's own Input 3 run against `long_phyloseq.rds` once the coercion is fixed, so the "native mixed models" claim in the prose stays true — only the single shown code example was misleading for the fixture it sits next to. |
| `GUniFrac::ZicoSeq()` crashes outright on zero-variance features; no SKILL.md code or warning | P1 | Added a runnable ZicoSeq code block that drops zero-variance features first (`apply(otu, 1, function(x) length(unique(x)) > 1)`); added a Common Errors row | ran | Ran against `phyloseq_object.rds` (GUniFrac 1.9): 20 significant, TP=17/17 planted taxa, FP=3. |
| 4 of 8 frontmatter-named tools (ZicoSeq, MaAsLin3, LEfSe, DESeq2) had no runnable code anywhere in the Skill | P2 | See per-tool rows below | mixed | ZicoSeq covered by the P1 row above. |
| — MaAsLin3 has no code example | P2 | Wrote a `maaslin3()` code block (auto-detects feature/sample orientation; results in `fit_data_abundance$results`, gated on `qval_individual`) | ran | maaslin3 1.5.7 (GitHub `biobakery/maaslin3`, TOOLS.md had only load-verified it). Ran end to end on the fixture: 18 significant, TP=17/17, FP=1. |
| — DESeq2 has no code example | P2 | Added the one recipe SKILL.md already names as the minimum mitigation (`estimateSizeFactors(type='poscounts')`) as a short caveat-only block inside the existing DESeq2/edgeR Failure Mode entry — SKILL.md already frames DESeq2 as "a caveat, not a recipe," so this is bounded to exactly that claim, not a general recommendation | ran | DESeq2 1.46.0. Ran end to end: 20 significant, TP=17/17, FP=3. |
| — LEfSe has no code example | P2 | Added the CLI invocation (`lefse-format_input.py` -> `run_lefse.py`), flags checked against real `--help` output from the WSL `lefse` env; framed explicitly as exploratory/non-FDR per the Skill's own existing Tool Taxonomy row | help output only, not a clean full run | Attempted a real end-to-end run (exported the fixture to LEfSe format, ran both scripts): `run_lefse.py` (LEfSe 1.1.1, WSL `science` distro env `lefse`) crashed with `AttributeError`/`TypeError` on a `None` return from its internal R/rpy2 LDA step, **and** the same failure mode when switched to `-r svm`. This reproduces on any input — a real bug in that env's LEfSe build (likely an rpy2/R-version mismatch), not something a SKILL.md code example can route around. Verified the command syntax against `--help` instead, per FIX_BRIEF's fallback. Flagging for the tooling record: `microbiome-metagenomics-analyst`'s `lefse` env needs a rebuild/pin fix before any Skill's LEfSe example can be execution-verified. |
| ALDEx2 example never calls `set.seed()`, so Monte-Carlo output isn't bit-reproducible | P2 (cheap, general rule) | Added `set.seed(42)` before `aldex()` with a one-line note | parsed + ran (part of the combined ALDEx2/LinDA canonical path, unaffected functionally by seeding) | Trivial, in scope under "any P2 that is cheap." |
| Mandatory redundancy pass | — | Moved usage-guide.md's install commands into a new SKILL.md "Installation" section (single home for install notes). Deleted usage-guide.md's "What the Agent Will Do" and "Tips" sections — both were fully restated from SKILL.md's Decision Tree / Per-Method Failure Modes / Common Errors / Quantitative Thresholds tables — replaced with a one-line pointer. usage-guide.md now holds only Overview, Prerequisites (trimmed to a pointer), Quick Start, Example Prompts, Related Skills. | — | Nothing deleted was unique; every fact now lives once, in SKILL.md. |

## Left unfixed

- **LEfSe's own execution could not be verified in this environment** (see row above) — a
  pre-existing bug in the shared `microbiome-metagenomics-analyst` WSL `lefse` env, not a
  defect introduced by or fixable from this Skill. Worth a tooling-pass follow-up on that env.

## Verification method

All new/changed R blocks were re-run together, verbatim as they now appear in SKILL.md, in one
script against the audit's real fixture (`phyloseq_object.rds`, 200 taxa x 40 samples, 17
planted DA taxa) via the env's `rr.sh` wrapper (R 4.4.3, private `R-lib`) — no shared library or
package version touched. The LEfSe bash block passed `bash -n`. All 10 R code blocks in the
final SKILL.md were also parsed together with `parse()` to confirm syntax validity.

## Final-pass correction — 2026-09-24

Source worktree `F:\OpenScience\worktrees\bio-microbiome-differential-abundance-finalpass`,
branch `agent/finalpass-bio-microbiome-differential-abundance-20260924`, exact source commit
`55c385dd6480e12d6f648af57dd2eb5ba7503fe8`.

| finding | priority | change | verified |
|---|---|---|---|
| MaAsLin2's displayed `random_effects = c('SubjectID')` silently produced zero usable Group rows on the canonical cross-sectional fixture, because all 40 subject IDs occurred once | P1 | Removed the default random effect; restricted the documented escape hatch to datasets with repeated observations; added the exact grouping-level warning and repair to Common Errors | `finalpass_20260924_maaslin2_regression.R`: cross-sectional run wrote 188 Group rows |
| The numeric MaAsLin2 example could be interrupted by an optional ggplot2 plotting incompatibility after writing results | P2 | Set `plot_heatmap = FALSE, plot_scatter = FALSE` in the example and explained that tables, not optional plots, are its primary output | Fresh cross-sectional run completed with 188 Group rows; archived multi-tool panel reached `ALL BLOCKS COMPLETED WITHOUT ERROR` |

Fresh repeated-measures evidence used `long_phyloseq.rds` (12 subjects x 3 visits) and the same
documented `random_effects = c('SubjectID')` route; it wrote 191 Arm rows. The fixture emitted
visible singular-fit warnings, but did not suppress output. Final audit artifacts are
`F:\OpenScience\audits\bio-microbiome-differential-abundance\eval_report_bio-microbiome-differential-abundance_result.json`
and its viewer; they are self-audit evidence (`auditor_independent: false`) for the exact commit.
