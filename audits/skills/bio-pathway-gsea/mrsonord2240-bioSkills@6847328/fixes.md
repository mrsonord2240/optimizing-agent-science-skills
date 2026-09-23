# bio-pathway-gsea — fix log (2026-09-16)

Commit `30b5b16` on `fix/r2-crispr-a`. Candidate: crispr-screen-analyst. Scope: all 7 open
findings (3 P1, 4 P2) per Sam's 2026-09-16 override.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `nPerm` claimed "an argument error"; actually accepted with a warning, silently downgrades `fgseaMultilevel` to `fgseaSimple` | P1 | Rewrote the Stale-nPerm failure mode, the Common Errors row, the frontmatter description; added a `'nPerm' %in% names(gse@params)` post-call guard | ran — reproduced independently on clusterProfiler 4.14.6 with a real-Entrez-ID Hallmark GSEA: two warnings, no error, `gseaResult` with 50 rows | audit ran this on 4.14.6 too; re-verify wording holds on 4.18.4+ as claimed in frontmatter |
| `pmax(pvalue, 1e-300)` clamp makes exact-zero p-values ~75x the strongest measured gene's weight, >16% of total ranking weight, erasing planted down-regulated biology | P1 | Changed the clamp to `1e-30` in SKILL.md (2 places) and usage-guide.md (1 place); added a Quantitative Thresholds row explaining the clamp is a ranking weight | ran — reproduced independently (own synthetic 14,000-gene vector, 4 planted zero-p): 1e-300 gives 76.5x/16.5% share, 1e-30 gives 7.6x/1.9% share, closely matching the audit's 71x/16.05% | did not re-run the full gseGO recovery-of-planted-signal comparison (audit's Input 3) to save the ~150s budget; the weight-math reproduction is the load-bearing check |
| Bare `limma::camera(...)` inherits limma's preset `inter.gene.cor = 0.01`, giving no protection | P1 | Added `inter.gene.cor = NA` everywhere CAMERA is mentioned: Decision Tree, Tool Taxonomy, the correlation failure-mode Fix, usage-guide Tips | ran — reproduced independently on a synthetic 50-gene correlated set (true ρ ≈ 0.87): default preset PValue 8.9e-15 (false confidence), `inter.gene.cor=NA` estimated 0.866 and gave PValue 0.14 | own repro used a different data setup than the audit's (true correlation 0.87 vs audit's 0.31); direction and magnitude of the failure match |
| Both shipped examples rank by `rnorm()` under a fixed seed — a null by construction, 0 terms every run, dead code inside their result-reporting branches | P2 | Planted a ~1 SD shift on the real member genes of GO:0006260 (`gsea_go.R`) and `HALLMARK_OXIDATIVE_PHOSPHORYLATION` (`gsea_msigdb.R`) | ran both end-to-end via `r.sh` from the candidate env — `gsea_go.R`: 31 GO BP terms, top hit GO:0006260 NES 3.05; `gsea_msigdb.R`: 1 Hallmark (the planted OXPHOS set), NES 3.05, p.adjust 3.1e-22 | `gsea_go.R` takes ~155s genome-wide; ran once after the edit |
| Unsorted/duplicated `geneList` documented as "silently wrong ES"; it is a hard clusterProfiler error | P2 | Corrected the symptom text in the failure-mode section to the two actual error strings (`geneList should be a decreasing sorted vector...`, `Duplicate values in names(stats) not allowed`) | docs — taken from the audit's own Input 3 block A output, not independently re-run (short, low-risk textual correction) | |
| ID-mismatch Common Errors row omits the follow-on error | P2 | Added `'organism' is not a slot in class "NULL"` to that row | docs — taken from the audit's Input 3 output | |
| No runtime expectation for a genome-wide `gseGO` run | P2 | Added a Quantitative Thresholds row: ~155s / 14,000 genes | ran — matches this fixer's own `gsea_go.R` run (see above) and the audit's 154.8s | |

No findings left unfixed.

---

# bio-pathway-gsea — fix log (2026-09-21)

Branch `fix/pathway-gsea` in `F:\OpenScience\wt\pathway-gsea` (commit hash in the dispatch report). Evidence:
`F:\OpenScience\comparisons\gsva-vs-gsea\COMPARISON.md`. Env: mass-spec-proteomics-analyst (R 4.4.3, clusterProfiler
4.14.6, fgsea 1.32.4, limma 3.62.2, GSVA 2.0.7, msigdbr 26.1.0). SKILL.md 218 -> 252 lines (under 300, no split).

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| Default preranked GSEA calls 9/20 co-regulated null sets, the Skill's own CAMERA `NA` advice 0/20 | P1 (comparison) | Decision tree: new first row, matrix + design -> `camera(..., inter.gene.cor = NA)` is the DEFAULT, preranked GSEA is for "only a ranked vector" and is labelled screening; Insight #2 and the correlation failure mode now carry the measured 9 / 0 / 7 / 1 numbers; new section "Matrix + Design" with a runnable CAMERA/fry block (ids2indices, size filters) | ran: reproduced the comparison's `q1_ours.R` in scratch (GSEA t 9/20, 68 sig; CAMERA NA 0/20, 41 sig; CAMERA default 7/20; planted cell cycle NES +3.66 / OXPHOS -4.11, CAMERA FDR 3e-17 / 2e-17); then ran the new SKILL.md block: camera NA 0/20, fry 1/20 (54 sig) | the comparison's 24-sample synthetic set only; no real-data check |
| "GSVA is not installed in the reference environment" | P2 | Sentence deleted; version block now names GSVA 2.0.7 as checked; `gsvaParam`/`ssgseaParam` block given `minSize/maxSize` (defaults 1/Inf) | ran: `gsva(gsvaParam(..., kcdf='Gaussian', minSize=10, maxSize=500))` and `ssgseaParam` gave 186x24 score matrices on the comparison data | |
| Snippet uses `ncbi_gene` against symbol-named data | P2 | Added the rule "TERM2GENE column must match the ranked vector's IDs (`ncbi_gene` vs `gene_symbol`)" with a symbol example and the KEGG `CP:KEGG_LEGACY` subcollection form | ran: `ncbi_gene` t2g on a symbol-named vector fails with `No gene can be mapped` / `'organism' is not a slot in class "NULL"` (not a silent 0 terms, text says so); `gene_symbol` t2g gave 16 Hallmarks, OXPHOS NES -3.34 | |
| kcdf undocumented (audit P2) | P2 | Added kcdf paragraph: only on `gsvaParam` (`ssgseaParam` has none, unlike the audit's suggestion), Gaussian for continuous log data, Poisson for counts, log it | help: `args(gsvaParam)` / `args(ssgseaParam)` on GSVA 2.0.7 | |
| fgsea "ties in the preranked stats" warning undocumented (audit P2) | P2 | Common Errors row (high % = degenerate metric, few % benign) | ran: stat rounded to 1 decimal gave "92.85% of the list" on fgsea 1.32.4 | benign-threshold wording rests on the audit's runs |
| Version claim "clusterProfiler 4.18.4+, fgsea 1.36+" never run (audit P2) | P2 | Version block and both example headers changed to what was run (clusterProfiler 4.14.6 etc.), plus a note that newer releases were not run | ran `gsea_msigdb.R` (Hallmark OXPHOS planted, NES 3.05, p.adjust 3.1e-22); both examples `parse()` | `gsea_go.R` (~155 s) only comment-edited, not re-run |
| Per-sample section said "no contrast test" while limma on scores works | P2 | Added a limma-on-scores line and softened the sentence | ran: GSVA+limma cell cycle FDR 2.7e-21, OXPHOS 3.7e-21, 1/20 nulls (matches comparison) | |
| Phenotype-permutation GSEA named with no runnable code (Missing referenced executables) | P2 | Chose delete-the-claim: row now says concept only, Broad desktop/CLI not run here, use CAMERA | n/a | Broad GSEA is a Java desktop tool, absent from the env |
| CAMERA and fry named without code (Missing referenced executables) | P2 | Chose write-it: "Matrix + Design" block | ran, see row 1 | |

## Redundancy removed (2026-09-21 rule)

| deleted passage | where its content now lives |
|---|---|
| usage-guide Prerequisites (install block, ranked-vector/ID/KEGG-live/set.seed notes) | SKILL.md Version Compatibility "Install" line; ID and live-KEGG and seed content already in SKILL.md |
| usage-guide "What the Agent Will Do" | SKILL.md sections (procedure) |
| usage-guide "GSEA vs Over-Representation" table | SKILL.md decision-tree ORA row (now also says ORA finds strong individual changes, GSEA coordinated subtle shifts) |
| usage-guide "Choosing a Ranking Statistic" table | SKILL.md "Build the Ranked Vector" table (identical) and clamp paragraph / Thresholds |
| usage-guide "Interpreting NES" | SKILL.md gseaResult paragraph (sign), tiny-leading-edge failure mode (FDR first), Thresholds `pAdjustMethod` row (BH vs 0.25; the "reserve 0.25 for exploratory, say which" clause moved there) |
| usage-guide "Tips" (7 bullets) | SKILL.md Insight, nPerm/GSVA failure modes, msigdbr comments; "no terms enriched" moved to a Common Errors row |
| SKILL.md Common Errors rows for nPerm and GSVA `method=` | the "Stale nPerm" and "Stale GSVA call" failure modes (now note the error text) |
| SKILL.md clamp explanation in the ranked-vector paragraph | Quantitative Thresholds clamp row; paragraph keeps a pointer |
| SKILL.md "Treat p.adjust as BH..." tail of the nPerm failure mode | Thresholds `pAdjustMethod` row |
| stale `# GSVA >= 1.50` code comment | Approach sentence above the block |

Disagreement logged: usage-guide gave the edgeR clamp as `1e-30` with the "1e-300 can give >16%" figure; SKILL.md carries the same numbers in its Thresholds row, kept.

## Left unfixed

- **Re-verification on clusterProfiler 4.18.4+ / fgsea 1.36+** (audit P2): the env has 4.14.6 / 1.32.4 and a fixer may not install into the shared library; the version claim was instead narrowed to what ran.
- **`gsea_go.R` not re-run**: only its header comment changed; a full run is ~155 s and its logic was verified on 2026-09-16.
- **CAMERA/GSEA guidance validated on one synthetic dataset** (24 samples, 20 nulls): no real-data set with known truth exists in the corpus; 9/20 vs 0/20 is a single run, not a rate estimate.
- **Phenotype-permutation GSEA has no runnable path**: needs the Broad Java tool, not installed and outside this Skill's R scope; claim reduced to concept.

---

# bio-pathway-gsea — Phase 1 corrective (2026-09-23)

Branch `fix/pathway-gsea`; rejected source tip `d6ecbe33cfc1aa0e9635f83ae2f0b98832557dbe`.

| finding | change | verified | notes |
|---|---|---|---|
| Successful GSEA output was followed by exit `2816`, making shipped code unusable in the native Windows runtime | Added an explicit isolated-runtime requirement and fresh micromamba command; documented that a nonzero exit is failure even when results were printed | ran — Linux R 4.5.3 / Bioconductor 3.22 exited 0 for shipped GO/MSigDB and representative nPerm/ID/GSVA/KEGG/Reactome paths | Native R 4.4.3 / Bioc 3.20 package loading reproduced `2816` for clusterProfiler, GSVA, msigdbr, org.Hs.eg.db, and ReactomePA; SerialParam did not help |
| Package-version claims were stale after the runtime move | Updated SKILL.md compatibility block and both shipped example headers to execution-verified versions | ran — clusterProfiler 4.18.4, fgsea 1.36.2, org.Hs.eg.db 3.20.0, msigdbr 26.1.1, limma 3.66.0, GSVA 2.4.9, ReactomePA 1.54.0, reactome.db 1.95.0 | The isolated org.Hs.eg.db payload was seeded from the pre-existing local 3.20.0 package only; no shared library mutation |

Evidence: `F:\OpenScience\audits\_final_pass\bio-pathway-gsea\verify_r45_all_paths.out` ends `ASSERT kegg_reactome=ok kegg=311 reactome=924` and `exit=0`.

Source commit: `c1c6150cba5570abc754866e90d09ee536917b07` (`fix(pathway-analysis/gsea): document verified isolated R runtime`). Push was attempted and rejected because remote `GPTomics/bioSkills` is archived/read-only (HTTP 403); no publish, merge, or score was attempted.
