# Fix log: bio-data-visualization-lollipop-protein-maps

## 2026-09-23 — backlog correction

Skill `data-visualization/lollipop-protein-maps`, branch
`fix/data-visualization-lollipop-protein-maps`, corrective commits
`e526c0d363d7c07ed2c923074217f6689282564b` and
`4f5e4c0e54f612acdab50562e7a5cb07abb0b6bc` from staging `8c75e1f4`.
Validated with maftools 2.22.0, trackViewer 1.42.0, g3viz 1.2.0, and the
data-visualization R environment.

| finding | priority | change | verification |
| --- | --- | --- | --- |
| Shipped example was incomplete and painted factor-indexed colours incorrectly | P1 | Made inputs explicit, selected a valid mutation-change column, indexed palettes through character values, covered `Translation_Start_Site` and `Nonstop_Mutation`, and labelled trackViewer stems by residue/change. | Exact copied example exits 0 and writes three PDFs plus the g3viz HTML; factor and edge assertions pass. |
| maftools behavior and protein identifier guidance were misstated | P1 | Corrected RefSeq/default transcript selection, bundled CDD domain source, console-count and return-value behavior, fixed-radius heads, recurrence heights, and `AACol` handling. | Checked against maftools 2.22.0 and audit fixtures. |
| TP53 domains and transcript were wrong | P1 | Set UniProt P04637 domains to 1-44, 102-292, 325-356, and 368-387 with inclusive `IRanges(start,end)`; corrected the canonical transcript to `ENST00000269305`. | Domain/transcript assertions pass and plotted boundaries match the declared values. |
| g3viz route called a nonexistent function | P1 | Replaced it with `readMAF(..., protein.change.col=...)`, `g3Lollipop`, and `htmlwidgets::saveWidget`; documented that g3viz 1.2.0 is archived. | HTML export is nonempty (394,088 B) and contains the expected widget data. |
| Protein-change parsing, counts, duplicate rows, and short isoforms were unsafe or unclear | P2 | Added robust one-letter, three-letter, start-loss, and stop-extension parsing with explicit filtering/warnings; documented row-count semantics and deduplication/isoform boundaries. | Parser and edge assertions cover `p.R175H`, `p.Arg175His`, `p.*394Wext`, `p.M1?`, malformed rows, and palette completeness. |
| Stale tools and duplicated guide material | P2 | Removed pyLollipop and unused Bio.PDB/ProteinPaint claims; reduced the guide to prerequisites, prompts, and canonical pointers. | Static checks and `git show --check` pass. |
| The conventional TP53 DNA-binding-core range was presented as a current UniProt feature | P2 | Labeled 102--292 as a supplied conventional range, distinguished the three current UniProt P04637 feature ranges, and required a chosen literature citation when the conventional boundary is used in a publication. | Exact-commit R parse, source-text assertions, and the cached UniProt JSON/reference check pass; the final report has 35/35 passing assertions and no recommendations. |

## Findings left unfixed

None. The shared Windows R `cli` teardown crash occurs after successful output;
validation used the existing process-local cleanup profile and did not install or
embed it in the Skill.
