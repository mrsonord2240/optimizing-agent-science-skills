# gsva-vs-gsea: three Open Science GSVA wrappers vs `bio-pathway-gsea` (2026-09-21)

**Verdict: partial.** The three Open Science (OS) Skills are one pipeline with three input defaults; `bio-pathway-gsea` is a different job (ranked-list GSEA plus statistical guardrails) that also carries a 4-line per-sample snippet.

## What each side claims
| Skill | Claim |
|---|---|
| `gsva-analysis-and-visualization` | CLI `main.R`: GSVA/ssGSEA of a bulk matrix against MSigDB (fetched by `msigdbr`), limma case-vs-control on the scores, heatmap. |
| `immune-pathway-analysis` | Same CLI, but gene sets come from a local long table (bundled: 41 immune Reactome sets); adds `--focus_genesets`, custom column names, a written fallback when nothing passes FDR. |
| `ssgsea-immune-infiltration-analysis` | Same scoring core, bundled 28-cell-type immune table, then per-cell-type Wilcoxon, Spearman correlation matrix, 4 PDFs; `--gene_id_case` normalisation. |
| `bio-pathway-gsea` | Prose, no scripts. Preranked GSEA (`gseGO/gseKEGG/GSEA`) on a signed statistic; CAMERA/ROAST; GSVA/ssGSEA as "per-sample matrix, not a contrast test"; failure modes. |

## Data and env
Synthetic, `data/expr.csv`: 8,288 human symbols x 24 samples (12 Case/12 Control), made by `run/make_data.R` (truth in `data/truth.json`). Planted: KEGG_CELL_CYCLE +1.2, KEGG_OXIDATIVE_PHOSPHORYLATION -1.0, REACTOME_INTERFERON_GAMMA_SIGNALING +1.2, "Activated CD8 T cell" (OS table) +1.2; zero gene overlap among the four. Plus 20 KEGG sets with a shared per-sample latent factor and NO group effect (co-regulated nulls). Fair to both: real gene symbols so every Skill's gene-set source resolves; a truth is known. Env: `audit-envs/mass-spec-proteomics-analyst` (GSVA 2.0.7, limma 3.62.2, fgsea 1.32.4, clusterProfiler 4.14.6, msigdbr 26.1.0, optparse, pheatmap); nothing installed.

**Requests.** Q1: KEGG pathway case-vs-control. Q2: which immune pathways/cell types are higher in Case. Q3: only a ranked DE table, no matrix.

## Results (request x side)
| Req | Side | executed | key output | asserted |
|---|---|---|---|---|
| Q1-Q2 as shipped | all 3 OS | **false** | `out/q1_theirs_asis.txt`: `gsva(expr=,gset.idx.list=,method=)` is defunct in GSVA 2.0.7 (Bioc 3.20); `closure` error x2; msigdbr `subcategory="KEGG"` also unknown | none possible |
| Q1 shimmed* | gsva skill | true | 42/186 sets FDR<.05; cell cycle up 2.7e-21, OXPHOS down 3.7e-21 (`shim/gsva-analysis-and-visualization/out_q1/table/GSVA_diff.csv`) | direction + FDR of both planted: pass |
| Q1 shimmed* | immune-pathway (KEGG table fed in) | true | **byte-identical** diff table to gsva skill: max abs dlogFC = 0, dP = 0 (`out/q1_summary.csv`, `run/q1_eval.R`) | pass |
| Q1 shimmed* | ssgsea skill (KEGG table as "cell_type") | true | Wilcoxon: cell cycle 1.4e-5, OXPHOS 1.4e-5, 46 sig (`.../ssgsea_group_compare.csv`) | pass |
| Q1 | ours GSEA on limma t | true | cell cycle NES +3.66, OXPHOS NES -4.11, 68 sig (`out/ours_q1_gsea_t.csv`) | pass |
| Q1 | ours CAMERA `inter.gene.cor=NA` | true | 41 sig (`out/ours_q1_camera_NA.csv`) | pass |
| Q2 shimmed* | ssgsea skill | true | Activated_CD8_T_cell up, FDR 2.1e-5, rank 1 of 28, the only hit (`out/q2_summary.txt`) | pass |
| Q2 shimmed* | immune-pathway | true | IFNG up, FDR 8.8e-23, rank 1 of 41 | pass |
| Q2 shimmed* | gsva skill (C2 Reactome) | true | IFNG up, FDR 2.0e-18, rank 1 of 1,815; 195 sig | pass |
| Q2 | ours GSEA (Reactome; and OS cell table as TERM2GENE) | true | IFNG NES>0 FDR 5.5e-65 rank 1; CD8 T FDR 3.3e-12 rank 1 | pass |
| Q3 | all 3 OS | **false** | needs matrix + group file; ranked table gives `SKILL_EMPTY_DATA` / `SAMPLE_MISMATCH` (`out/q3_theirs.txt`) | unsupported |
| Q3 | ours | true | `out/q3_ours.txt` | see below |

*Shim (`run/make_shim.py`): 3-line swap of the `gsva()` call to `gsvaParam/ssgseaParam` (+ msigdbr `collection/subcollection`, `CP:KEGG_LEGACY`), applied to copies in `shim/`. No statistics changed.

**Executed as shipped:** OS 0/3 each (all fail on current GSVA; Q3 unsupported anyway); OS 2/3 each after shim; ours 3/3.

## What only one side can do
- **Only OS:** ready CLI with tables, `.rda/.rds`, heatmap PDFs, run/manifest logs; limma moderated t on scores (gsva, immune); Wilcoxon + cell-type correlation + immune table (ssgsea); `--gene_id_case upper` rescued a lower-case matrix (`out/q4_idcase.txt`: ssgsea skill completed; the other two failed loudly, none silently wrong).
- **Only ours:** ranked-vector GSEA with no matrix; warns and demonstrates the failure modes. Executed in `out/q3_ours.txt`: ranking by `-log10 p` without sign reports the planted DOWN set OXPHOS as **NES +1.96, FDR 1.1e-35**, and all 44 significant sets have NES>0; `nPerm=1000` runs to completion with only two warnings and `nPerm` retained in `@params` (engine downgrade, as the Skill says); unsorted input errors.
- **Co-regulation guardrail (`out/q1_summary.csv`), 20 co-regulated null sets:** GSEA on t calls **9/20** at FDR<.05; CAMERA `NA` 0/20; CAMERA default preset 7/20; GSVA+limma (gsva/immune skills) 1/20. The Skill's own advice (CAMERA `NA`) fixes what its default GSEA path gets wrong; the OS pipeline is inherently robust here because the test runs on per-sample scores.

## Which to use
- Per-sample pathway scores + case/control contrast + plots from a matrix: gsva skill (MSigDB) or immune-pathway (own table). **They compete for the same request** (identical output given the same sets/method); pick by where the gene sets live. immune-pathway subsumes gsva (any table).
- Immune cell-type infiltration table + correlation: ssgsea skill (different statistic, Wilcoxon, ssGSEA default).
- Ranked DE list, no matrix, or need a correlation-honest test, seed/version guardrails: `bio-pathway-gsea`. Its per-sample section is a snippet, not a pipeline: no contrast, no plots, no immune sets.

## Defects hit
- All 3 OS: unrunnable on GSVA >=1.50 (old `gsva()` signature); their recorded baseline is GSVA 1.42. Env has a fixable 3-line fix.
- gsva skill: `--subcategory KEGG` fails on msigdbr >=10 (`CP:KEGG_LEGACY`); CLI docs use `category/subcategory`.
- ssgsea skill: renames cell types (`Activated CD8 T cell` -> `Activated_CD8_T_cell`); auto-picked scatter gene is an arbitrary top-correlate (`OR51E1`).
- ours: says GSVA is "not installed in the reference environment" (stale here); uses `ncbi_gene` in the snippet while data were symbols (used `gene_symbol`, trivial).
- Caveat: "clean-null" sets share genes with the co-regulated nulls (`out/q1_clean_null.txt`: ours GSEA 9/67), so use the 20-null row as the clean signal.
