# bio-pathway-enrichment-visualization fixes (2026-09-17)

Worktree `F:\OpenScience\wt\pw-viz`, branch `fix/pw-viz`, based on `main` @ `10ac5b0`. Fixer:
Claude Sonnet 5. Runtime: R 4.4.3 via `F:\OpenScience\audit-envs\crispr-screen-analyst\r.sh`;
enrichplot 1.26.6, clusterProfiler 4.14.6, ggplot2 4.0.3, org.Hs.eg.db 3.20.0, already installed
there — nothing installed, nothing changed. Verification: scratchpad `isolate_treeplot.R`,
`check_treeplot_ego.R`, `check_cluster_method.R` (isolated treeplot() argument-combination
reproductions against real `compareCluster`/`enrichGO` output built from the audit's own
`gene_data.rds`), and a full re-run of the patched `examples/visualization_ora.R` (exit 0, wrote
a 4-page PDF — verified by counting `/Type /Page` objects, not just exit code).

Commits: `cc5cbe2` fix(pathway-analysis/enrichment-visualization) — the P1/P2 findings below;
`994366d` refactor(pathway-analysis/enrichment-visualization) — the redundancy pass.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `upsetplot()`'s `ggupset` Suggests-only dependency undocumented | P1 | Added `ggupset` to a new SKILL.md Prerequisites install line, the `upsetplot()` code comment, and a new Common Errors row, matching the existing `ggridges`/`ggarchery` pattern | help + audit's own run | the audit's own Input 5 run already produced the exact error text now documented (`ggupset` not installed here either — no install attempted, per the no-version-change rule) |
| `treeplot()` on a `compareClusterResult` crashes under the installed enrichplot/ggplot2 | P1 | Documented as a genuine version incompatibility (not a usage error) in Version Compatibility, the Tool Taxonomy table, the Decision Tree, "Show the Redundancy", and a new Common Errors row — all pointing to `emapplot(pairwise_termsim(ck))` as the verified-working alternative for that class | ran | `isolate_treeplot.R`: the default call, `nCluster=5`, `cluster.params=list(n=...)`, and four `showCategory=` values on real `compareCluster(list(Up=..., Down=...), fun='enrichGO')` output all throw the identical ggplot2 "Aesthetics must be either length 1 or the same as the data" error inside ggtree's `geom_cladelab`/`fortify()` path — including the package's own `?treeplot` documented example (`treeplot(xx)` with no arguments). 100% failure across every combination tried; not a usage error |
| No guidance for zero surviving terms/sets | P2 | New "Zero surviving terms or sets" entry in Per-Method Failure Modes + matching Common Errors row | docs (mirrors the shipped `examples/visualization_gsea.R`'s own `if (nrow(...) > 0)` guard, which already existed) | |
| Skill's own `treeplot()` examples use deprecated `nCluster=` | P2 | SKILL.md's "Show the Redundancy" code block and `examples/visualization_ora.R` switched to `cluster.params=list(n=5)` | ran | `check_treeplot_ego.R`: both `nCluster=5` and `cluster.params=list(n=5)` render correctly on a plain `enrichResult` (only the former emits enrichplot's own deprecation warning); patched `examples/visualization_ora.R` re-run end-to-end, exit 0, `ora_visualization_test.pdf` (26,694 bytes) contains 4 page objects matching the 4 plots the script emits (dot, fold, emap, tree) |

**Found while fixing, not in the dispatch — fixed inline per "Fix. Don't Report":** the Quantitative
Thresholds table's `treeplot(nCluster=5, cluster_method='ward.D')` used `cluster_method=`, which is
not a real `treeplot()` argument name at all (the real one is `cluster.params=list(method=...)` or
the deprecated top-level `hclust_method=`). `check_cluster_method.R` confirmed R's `...` silently
swallows the bogus `cluster_method=` with no warning — the example "worked" only because the default
clustering method already happens to be `ward.D`. Replaced with the correct
`cluster.params=list(n=5, method='ward.D')`, confirmed working by execution.

All 4 dispatched findings fixed (2 P1, 2 P2), plus the `cluster_method=` defect found in the same
section while verifying the P2 nCluster fix. Nothing left unfixed.

## Redundancy pass (2026-09-17)

Scope: `usage-guide.md` only, per the brief's "Remove redundancy, every pass" rule (SKILL.md had no
internal repetition to collapse). Lines: SKILL.md 221 -> 255 (net +34: the P1/P2 fixes above, plus a
new Prerequisites section absorbing usage-guide.md's install commands — new content, not previously
in SKILL.md). usage-guide.md 95 -> 47 (net -49, then -1 after this pass's own edits: pointers added
where sections were deleted).

**Deleted passage -> new home** (every deletion verified present at destination before commit):

| Deleted from usage-guide.md | New home in SKILL.md | Note |
|---|---|---|
| "Prerequisites" R install block (`BiocManager::install(...)`, `install.packages(c('ggridges','ggarchery'))`) | New "Prerequisites" section (top of file) | verbatim install commands, plus `ggupset` added per the P1 fix above — new content, not previously in SKILL.md |
| "Prerequisites" conceptual bullets (input object types, ridgeplot/goplot Suggests deps, ggtangle churn, pairwise_termsim requirement, no-barplot-for-gseaResult, offline-once-built) | Already stated in "Object Model", "Version Compatibility", "GSEA Plots", "Specialized Views", "Missing pairwise_termsim" and "Barplot on gseaResult" failure modes | deleted, no unique content except the offline-once-built note, kept verbatim in the new Prerequisites section |
| "What the Agent Will Do" (5-step workflow) | Already stated in "The Single Most Important Modern Insight" and "Tool Taxonomy" | deleted, no unique content |
| "Plot-by-Class Quick Reference" table | Already stated, more completely, in "Tool Taxonomy" (which additionally covers goplot/simplify/REVIGO) | deleted, strict subset |
| "Tips" (9 bullets) | Already stated in "Decision Tree", "Show the Redundancy", "Dotplot", "Default-ordering misread", "GeneRatio read as effect size", "Barplot on gseaResult", "Over-trimmed showCategory", "All Outputs Are ggplot Objects", "Common Errors" | deleted, no unique content — all 9 bullets independently checked against SKILL.md before deletion |

No disagreements found between the two files' copies before deletion.
