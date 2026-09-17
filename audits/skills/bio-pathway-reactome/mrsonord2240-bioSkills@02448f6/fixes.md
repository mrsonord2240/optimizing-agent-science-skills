# bio-pathway-reactome fixes (2026-09-17)

Worktree `F:\OpenScience\wt\pw-react`, branch `fix/pw-react`, based on `main` @ `d9971f6`. Fixer:
Claude Sonnet 5. Runtime: R 4.4.3 via `F:\OpenScience\audit-envs\crispr-screen-analyst\r.sh`;
ReactomePA 1.50.0, reactome.db 1.89.0, clusterProfiler 4.14.6, org.Hs.eg.db 3.20.0 (matches the
audit env, no version changes made, nothing new installed).

Commits: `a58596e` fix(pathway-analysis/reactome-pathways) — the 4 dispatched P2 findings;
`02448f6` refactor(pathway-analysis/reactome-pathways) — the redundancy pass.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `examples/reactome_gsea.R` ranked every gene by `rnorm()`, null by construction — 0 enriched terms every run, plotting branch dead code | P2 | Planted a real +1.5 shift on `R-HSA-877300` (Interferon gamma signaling)'s own member genes over a realistic ~3000-gene background (same pathway the audit itself planted) | ran via `r.sh` | 54 rows returned, `R-HSA-877300` recovered at rank 1; the `gseaplot2` branch now executes. `ridgeplot()` then errors because `ggridges` is not installed in this shared audit env (not in `TOOLS.md`) — this was previously masked by the 0-row null-by-construction bug and is a pre-existing gap, not something I introduced; left unfixed per "install nothing" (not one of the 4 dispatched findings) |
| `examples/reactome_ora.R`'s `universe` was every SYMBOL in `org.Hs.eg.db` (~20,000+ genes) — almost the same size as the implicit ~11,200-gene default, so the example never visibly demonstrated the universe/background point SKILL.md stresses | P2 | Sampled a realistic ~3000-gene background instead (significant genes + random noise) | ran via `r.sh` | `BgRatio` denominator now 193 (vs. the near-whole-genome universe before), materially different from the implicit default — the example now shows `universe=` changing the result |
| SKILL.md's Per-Method Failure Modes and Common Errors described the SYMBOL/ENSEMBL-without-`bitr` failure as "zero rows"/"0 rows"; the audit's own run showed `enrichPathway` returns `NULL`, not a 0-row `enrichResult` | P2 | Reworded both to "returns `NULL`" with the console message quoted, and to guard with `is.null(result)` rather than `nrow(result) == 0` | docs — taken from the audit's Input 3 output (`eval_viewer_bio-pathway-reactome.md`) | |
| No line addressing diagnostic/prescriptive misuse of a pathway result — Input 7's correct refusal came entirely from base-model alignment, not Skill guidance | P2 | Added a one-paragraph "Practice Boundaries" section (pattern matches the existing one in `metabolomics/lipidomics/SKILL.md`) | docs | |

All 4 dispatched findings fixed. Not fixed / not in scope: the 5th audit P2 (7-organism
ceiling not independently verifiable — `org.Mm.eg.db`/`org.At.tair.db` absent from the shared
audit env) was not in the dispatch list and needs a package install the "install nothing" rule
forbids; left as-is.

## Redundancy pass (2026-09-17)

Scope: `SKILL.md` and `usage-guide.md`, per the brief's "Remove redundancy, every pass" rule.
Lines: SKILL.md 205 -> 237 (net +32: absorbed usage-guide.md's install command block and the
results-column table, plus the P2 fixes above). usage-guide.md 107 -> 48 (net -59).

**Deleted passage -> new home** (every deletion verified present at destination before commit):

| Deleted from usage-guide.md | New home in SKILL.md | Note |
|---|---|---|
| "Prerequisites" `BiocManager::install()` block | "Version Compatibility" | verbatim, new content not previously in SKILL.md |
| "Prerequisites" conceptual bullets (ENTREZ-only, universe, organism-7, DE-list source) | Already stated in "Decision Tree", "Per-Method Failure Modes", "Tool Taxonomy" | deleted, no unique content |
| "Quick Start" 4 one-liner prompts | Deleted — duplicated the same scenarios already spelled out in "Example Prompts" | usage-guide.md keeps one prompt section, not two |
| "What the Agent Will Do" 6-step workflow | Already stated as Goal/Approach prose under "Over-Representation Analysis", "GSEA", "viewPathway", "ReactomeGSA" | deleted, no unique content |
| "Understanding Results" `enrichResult`/`gseaResult` column tables | New "Understanding Results" section in SKILL.md (before Per-Method Failure Modes) | verbatim |
| "Tips" (9 bullets) | Already stated in "Decision Tree", "Per-Method Failure Modes", "Common Errors", "ReactomeGSA" | deleted, no unique content; the one non-duplicate line (pointer to enrichment-visualization) kept as one line in usage-guide.md |

Kept in usage-guide.md as non-duplicate, human-facing content: the "Reactome vs KEGG"
comparison table (not present anywhere in SKILL.md; aids choosing this Skill over the sibling).

No disagreements found between the two files' copies before deletion.
