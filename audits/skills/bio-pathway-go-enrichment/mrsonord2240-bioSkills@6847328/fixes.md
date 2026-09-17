# bio-pathway-go-enrichment — fix log (2026-09-16)

Commit: `f683355` on `fix/r2-crispr-b` (worktree `F:\OpenScience\wt\crispr-b`).
Scope: all 3 open P2s (no P0/P1; score 90). Sam's 2026-09-16 "fix every known deficiency" override applied — no further defects found beyond the three plus one claim checked and confirmed correct.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| `enrichResult` column list stale (missing RichFactor/FoldEnrichment/zScore) | P2 | Added the three columns to SKILL.md and usage-guide.md's column table; pointed the two "read fold enrichment" instructions at the `FoldEnrichment` column instead of a manual computation | ran | Ran the `enrichGO` block on this machine (clusterProfiler 4.14.6, org.Hs.eg.db 3.20.0): printed columns were exactly `ID,Description,GeneRatio,BgRatio,RichFactor,FoldEnrichment,zScore,pvalue,p.adjust,qvalue,geneID,Count`. Cross-checked against `DOSE::enricher_internal`'s source: `FoldEnrichment <- RichFactor * N/n`, i.e. `(k/n)/(M/N)` — matches the Skill's own formula. |
| `simplify()` on `ont='ALL'` — Skill predicted "redundancy not removed, or an error" | P2 | Rewrote the failure-mode entry, the Common Errors table row, and the usage-guide.md tip to state it silently keeps only the first ontology's terms (BP) and drops the rest, no error/warning | ran | Built an `ont='ALL'` `enrichResult` (36 terms: BP 15/CC 13/MF 8) on this machine and called `simplify()` on it directly: returned 15 terms, all BP — confirms the actual (undocumented) behaviour and that no error is raised. |
| `examples/go_all_ontologies.R` reads an unshipped `de_results.csv`, cannot run standalone | P2 | Rewrote to draw foreground/universe from `org.Hs.eg.db` directly via `keys()`/`head()`, the same self-contained pattern `go_enrichment_basic.R` already uses; kept the per-ontology `enrichGO` + `simplify()` loop and CSV output | ran | Ran the rewritten script end-to-end on this machine: exit 0, `BP : 51 terms after simplify`, `MF : 23 terms after simplify`, `CC : 5 terms after simplify`, writes `go_all_simplified.csv` to `tempdir()`. |

## Checked, not changed

- usage-guide.md's claim about the `enrichment_force_universe` R option (default intersects the universe with annotated genes; `force_universe=TRUE` keeps the universe as given, including unannotated genes) — read `DOSE::enricher_internal`'s actual source (`getOption("enrichment_force_universe", FALSE)`, `if (force_universe) extID <- universe else extID <- intersect(extID, universe)`). The Skill's description matches the code exactly. No change made.

## Left unfixed

None — all three P2s fixed, and everything else found while reading the Skill checked out.
