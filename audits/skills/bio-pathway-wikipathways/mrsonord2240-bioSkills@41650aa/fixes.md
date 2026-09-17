# bio-pathway-wikipathways fixes (2026-09-17)

Worktree `F:\OpenScience\wt\pw-wiki`, branch `fix/pw-wiki`, based on `main` @ `d9971f6`. Fixer:
Claude Sonnet 5. Runtime: R 4.4.3 via `F:\OpenScience\audit-envs\crispr-screen-analyst\r.sh`;
clusterProfiler 4.14.6, rWikiPathways 1.26.0, org.Hs.eg.db 3.20.0, tidyr 1.3.2, already installed
there, no version changes made, nothing new installed. All calls were to the public,
unauthenticated WikiPathways API/archive (data.wikipathways.org).

Commits: `95b0121` fix(pathway-analysis/wikipathways) - the P1/P2 findings below;
`41650aa` refactor(pathway-analysis/wikipathways) - the redundancy pass.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| SKILL.md's/usage-guide.md's worked reproducibility example and the shipped `examples/wikipathways_explore.R` hardcode `downloadPathwayArchive(date='20240310', ...)`, which 404s because the live archive retains only the last 12 months | P1 | Replaced the literal date everywhere with `archive_date <- format(Sys.Date() - 60, '%Y%m10')` (archives publish on the 10th of each month; confirmed live via the folder listing at data.wikipathways.org - entries run `20260910...20260110`, then jump to a stray `20230810`); added a retention-window note + the Zenodo GMT/GPML archive as the citable fallback for older dates | ran | Ran the patched SKILL.md code block against the audit's synthetic DE data (`de_results_synthetic.csv`): recovered WP554 (p.adjust 6.44e-11) and WP430 (p.adjust 8.90e-22) from the pinned `20260710` archive, matching the audit's own manually-substituted-date run. Ran the patched `examples/wikipathways_explore.R` end-to-end (`Rscript`, exit 0) against the live archive |
| Fixing the date exposed a second, previously undiscovered defect: `examples/wikipathways_explore.R`'s last block referenced `entrez_ids`/`all_entrez`, never defined in that file (comment claimed they come from `wikipathways_ora.R`, but the two files are not sourced together) | (found while verifying P1) | Made the script self-contained: reuse the WP554 genes already fetched via `getXrefList()` earlier in the same file as the query set, and the pinned archive's own gene union as the universe | ran | Confirmed the undefined-variable halt first (re-ran the date-only fix, got `Error: object 'entrez_ids' not found`), then fixed and re-ran: completes, recovers WP554 as top hit (p.adjust 2.7e-51, 17/17 genes) |
| `enrichWP()`/`gseWP()` return `NULL` silently on a wrong organism string (e.g. `'zebrafish'` vs `'Danio rerio'`), reproduced live by the audit, but undocumented | P2 | Added a Common Errors table row: verify with `listOrganisms()`/`get_wp_organisms()` first | docs (matches audit's own live reproduction of the symptom, Input 6) | |

Both dispatched findings fixed (1 P1, 1 P2), plus the one defect the P1 fix exposed. Nothing left
unfixed.

## Redundancy pass (2026-09-17)

Scope: `SKILL.md` and `usage-guide.md`, per the brief's "Remove redundancy, every pass" rule.
Lines: SKILL.md 209 -> 250 (net +41: absorbed usage-guide.md's install block, agent workflow,
results-column table - none previously in SKILL.md - plus the WikiPathways-vs-KEGG/Reactome
comparison table, which had unique data not present anywhere in SKILL.md). usage-guide.md
100 -> 37 (net -63).

**Deleted passage -> new home** (every deletion verified present at destination with grep before
commit):

| Deleted from usage-guide.md | New home in SKILL.md | Note |
|---|---|---|
| "Prerequisites" R install block (`BiocManager::install(...)`) | "Version Compatibility" | verbatim, new content not previously in SKILL.md |
| "Prerequisites" conceptual bullets (ID types, universe, live-query, CC0/no-review) | Already stated in "The Single Most Important Modern Insight", "Common Errors" | deleted, no unique content |
| "Quick Start" one-liner prompts | Deleted -- duplicated the same 3 scenarios already spelled out in "Example Prompts" | usage-guide.md keeps one prompt section, not two |
| "What the Agent Will Do" numbered workflow | New "Agent Workflow" section (after Decision Tree) | verbatim |
| "Understanding Results" column table | New "Understanding Results" section (before Per-Method Failure Modes) | verbatim |
| "WikiPathways vs Other Databases" table | New "WikiPathways vs KEGG/Reactome" section (after Tool Taxonomy) | verbatim, new content not previously in SKILL.md |
| "Tips" section (11 bullets) | Already stated in "The Single Most Important Modern Insight", "Other Organisms", "Reproducible Analysis with a Dated GMT", "Per-Method Failure Modes", "Common Errors", "Tool Taxonomy", "Decision Tree", "Related Skills" | deleted, no unique content |

No disagreements found between the two files' copies before deletion.

## Unfixed
None.
