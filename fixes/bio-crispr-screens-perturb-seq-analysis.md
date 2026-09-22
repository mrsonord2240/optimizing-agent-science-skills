# Fix log: bio-crispr-screens-perturb-seq-analysis (2026-09-19)

Fresh fixer. Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:crispr-screens/perturb-seq-analysis`.
Fork branch: `fix/cs-perturbseq` off `main` at `a93661e`, worktree `F:\OpenScience\wt\cs-perturbseq`. Commit `1a3068b`.
Audit: `F:\OpenScience\audits\bio-crispr-screens-perturb-seq-analysis\` (83, Limited Release, deployable, no P0, 3 P1s, 3 P2s).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| `PyDESeq2.test_contrasts()`/result columns stale for pertpy >=1.0 (`contrast=(col,group,baseline)` tuple + `log2FoldChange`/`padj`) | P1 | SKILL.md's Pertpy Unified Framework block and `examples/run_pertpy.py`: use `de.contrast(column, baseline, group_to_compare)` -> `de.test_contrasts(...)`; read `log_fc`/`p_value`/`adj_p_value`; noted in Version Compatibility | ran | crispr-screen-analyst env, pertpy 1.3.0. Ran end-to-end twice: (1) a controlled synthetic dataset with a planted true effect + 3 planted nulls, recovering all 20 planted DE genes at padj<1e-60 (same method the auditor used for the original P1); (2) the fixed `examples/run_pertpy.py` in full on the real `pt.dt.papalexi_2021()` dataset (20,729 cells, 18,649 genes) -- completed the full Mixscape -> PyDESeq2 fit -> 26-way contrast loop with no errors, producing a 466,225x9 result table with correctly named `log_fc`/`adj_p_value` columns and biologically sensible top hits (e.g. MYC, SPI1 -- both real ECCITE-seq perturbation targets in this dataset) |
| (found while fixing the above, not in the audit) `pert_key='perturbation'`/`design='~perturbation'` -- papalexi_2021()'s RNA modality has no `perturbation` obs column at all; the real label (`gene_target`, control='NT') lives on the top-level MuData.obs only | P1-adjacent (same code path) | Merge `mdata.obs['gene_target']` into `adata.obs` before use; `pert_key`/`design` changed to `gene_target` throughout | ran | Confirmed the original code raises `KeyError: 'perturbation'` on real data; fixed version runs Mixscape cleanly |
| (found while fixing the above) `pt.tl.PyDESeq2(...)` called on log-normalized `adata.X`, not raw counts -- pertpy 1.3.0's `_check_counts()` raises `ValueError: Non-zero elements of the matrix must be close to integer values.` | P1-adjacent (same code path) | Save `adata.layers['counts']` before normalizing; pass `layer='counts'` to `PyDESeq2(...)` | ran | Reproduced the exact `ValueError` on real `papalexi_2021()` data with the pre-fix code (crash, not silent corruption -- pertpy's own check catches it); confirmed it disappears and the fit proceeds with the layer fix |
| Multiomic RNA+ATAC section is a 4-line non-functional stub despite frontmatter promising multiome coverage | P1 | Wrote a real workflow: propagate per-perturbation `mixscape_class` from RNA to ATAC modality via shared `obs_names`, then `sc.tl.rank_genes_groups` on normalize_total+log1p ATAC counts (not TF-IDF -- see note) | ran | Chose **write it**: muon 0.1.9 + scanpy + pertpy already installed. Verified on synthetic planted-signal RNA+ATAC data (800 cells, 100 genes, 60 peaks): 5/5 planted DE genes and 5/5 planted differential peaks recovered in each top-5. Also verified TF-IDF+binarize (the "standard" scATAC route) actively destroys the planted peak signal here via a compositional/library-size confound -- documented that finding inline so the choice isn't silently wrong |
| Genome-scale cost/channel figures ($50-100K/10-30 channels) don't scale-check against a literal ~19,000-gene request | P1 | Anchored the figures explicitly to Replogle 2022's ~9,866-gene scope; added the linear scaling ratio (~1.9x -> ~$95-190K/~19-57 channels for 19,000 genes) and a `cells_needed = genes x cells_per_pert / cells_per_channel` formula | arithmetic, checked by hand | 19000/9866 = 1.926 ~= 1.9x; 50-100K x 1.9 = 95-190K; 10-30 x 1.9 = 19-57 |
| Unseeded `pynndescent` call in `perturbation_signature()` -- 5/2000 cells drifted across reruns | P2 (cheap) | Added `random_state=0` to all three `perturbation_signature()` call sites (SKILL.md x2, example) | ran | 2 identical seeded runs on a 2000-cell synthetic dataset: `X_pert` byte-identical (0/2000 cells differed, max abs diff 0.0), `mixscape_class_global` identical |
| No Escape Hatches / clinical-scope statement anywhere in the Skill | P2 (cheap) | Added a `## Scope` section to SKILL.md (single home, matches the pattern used in sibling `crispr-screens/combinatorial-screens`) | n/a (prose) | Short, one paragraph |
| Bundled example (`examples/run_pertpy.py`) fails as shipped (same root cause as the PyDESeq2 P1) | P2 | Fixed by the same edits as the P1 above, plus the two additional bugs found along the way | ran | See first three rows |
| NTC vs NT inconsistency across code blocks (P2, observed 1,4) | P2 (cheap) | Left 'NTC' as the general placeholder (MOI/assign_sgrna/Mixscape-generic sections); added an explicit inline note at the one real-data call site (`papalexi_2021()`) that its actual label is 'NT', not a placeholder -- can't rename real data | n/a (prose) | Matches the audit's second suggested option ("explicitly note that the label must match whatever the user's own data uses") |

## Redundancy pass (every fix, per FIX_BRIEF)

- `usage-guide.md`'s **Validation Checklist** restated SKILL.md's Quantitative Thresholds numbers near-verbatim -> collapsed to a one-line pointer; the one checklist fact not already in SKILL.md (NTC ~5% of library) moved into SKILL.md's Quantitative Thresholds table before deleting.
- `usage-guide.md`'s **Architecture Cheat Sheet** duplicated SKILL.md's Decision rule -> deleted; its two mappings not already covered (CROP-seq for low-cost, ECCITE-seq for hashed cells) folded into SKILL.md's Decision rule. Dropped the table's third unique row ("scAR-Trac (Tracr-RNA-barcoded)") rather than migrate it -- not corroborated anywhere else in the Skill or its references, so not carried into SKILL.md's own voice.
- `usage-guide.md`'s **Cell-per-Pert Targets** table duplicated part of SKILL.md's Quantitative Thresholds row -> deleted; its finer per-resolution breakdown (focused/single-pert-deep/combinatorial) merged into that row.
- `usage-guide.md`'s **Tips** section: 7 of 9 bullets restated Failure Modes/SCEPTRE/Quantitative Thresholds/MOI sections verbatim -> collapsed to a pointer; kept the one non-duplicate bullet (combinatorial-screen pairing); migrated the one unique data point (MOI 0.5 -> 9% multi-sgRNA) into SKILL.md's MOI section.
- No fact was deleted outright -- each now lives once, in SKILL.md.

## Unfixed

None of the 6 audit recommendations were left unfixed. Two extra defects found during the P1 fix (missing `gene_target` merge; log-normalized data fed to PyDESeq2) were fixed inline under "Fix. Don't Report" rather than just noted, since they sit on the exact code path the P1 already required touching and verifying.

Nothing needs Sam.

## 2026-09-21 (structure)

Resumed fixer (previous agent died mid-task from a server error, not bad work). Worktree
`F:\OpenScience\wt\crispr-screens-perturb-seq-analysis`, branch `fix/crispr-screens-perturb-seq-analysis`,
env `crispr-screen-analyst`.

**Mixscape filter fix (`0096224`, plain corrections, no open audit findings -- score 93):**
- SKILL.md Mixscape block: a trailing comment swallowed `].copy()` -- a `SyntaxError`. Moved the
  comment above the line; block now parses and ran on synthetic data (294 KO cells).
- SKILL.md Pertpy block and `examples/run_pertpy.py`: both filtered on `mixscape_class` (per-gene
  labels like `'GENE_A KO'`) for the bare string `'KO'`, matching no cells -- the filter never
  filtered. Fixed to `mixscape_class_global` (values `KO`/`NP`/`NT`). Ran on real
  `papalexi_2021()` (20,729 cells): 7,081 kept (4,695 KO + 2,386 NT), sensible top hits
  (STAT1/IFNGR1/JAK2/IRF1 -> IFN genes; MYC -> ribosomal genes).
- "KO retention among perturbed" used the wrong denominator (kept/all cells, not kept/perturbed) --
  fixed; 25.6% on real data, 21.0% on synthetic, both checked.

**Split (`f03e575`):** SKILL.md 208 lines -> `references/` (factor-decomposition.md,
genome-wide-perturb-seq.md, multiomic-perturb-seq.md, sceptre-low-moi.md), no content lost.

**Scripts (`f82c507`):** moved four runnable blocks (SKILL.md x2, references x2) to
`scripts/`, each run against real invocations before committing:

| old location | script | ran on | result |
| --- | --- | --- | --- |
| SKILL.md sgRNA-assignment block | `scripts/assign_sgrna.py` | audit's `synthetic_sgrna.h5ad` | sane none/multiplet/per-sgRNA fractions |
| SKILL.md Mixscape block | `scripts/mixscape_filter.py` | audit's `synthetic_perturbseq.h5ad` (normalize_total+log1p'd first, raw counts as shipped) | 294/2000 cells kept, 100% `mixscape_class_global == KO` -- confirms the `0096224` filter fix holds through the script |
| `references/multiomic-perturb-seq.md` block | `scripts/multiome_differential.py` | synthetic MuData built for this run (audit data has no ATAC modality): planted a signal on 5/50 peaks for GENE_A KO cells | recovered exactly those 5 peaks as the top hits by adjusted p-value |
| `references/sceptre-low-moi.md` block | `scripts/run_sceptre.R` | sceptre's own bundled `--example` data via the env's `r.sh` | 2000-row real output table (`p_value`, `fold_change`, `significant`) |

No script code changes were needed -- all four ran correctly exactly as extracted. Nothing stayed
inline; nothing needs Sam.

## 2026-09-22 (final pass, Phase 1)

Final-pass agent. Worktree `F:\OpenScience\wt\crispr-screens-perturb-seq-analysis`, branch
`fix/crispr-screens-perturb-seq-analysis`. Every runnable block in SKILL.md, all four
`references/*.md`, all four `scripts/*` and `examples/` was walked and actually run this pass -- a
block that parses is not verified.

**Sparse-layer crash in `scripts/assign_sgrna.py` (found this pass):** the script was fine on the
audit's dense `synthetic_sgrna.h5ad`, but a sparse sgRNA count layer -- the normal 10X /
FeatureBarcode case -- crashed it. Sparse `.sum(axis=1)` / `.argmax(axis=1)` return `(cells, 1)`
matrices, so the threshold mask reached `.obs` as a 2-D array (`pyarrow.lib.ArrowInvalid`) and the
per-cell `np.where` mask raised `numpy.exceptions.AxisError`. Ravelled both. Verified three ways:
dense output unchanged (none 0.250 / sg_NTC1 0.150 / sg_GENE_B_1 0.144 / sg_GENE_A_2 0.138 /
sg_GENE_A_1 0.138 / sg_NTC2 0.130 / multiplet 0.050 over 500 cells); the same data as a CSR layer
gives 0 assignment mismatches vs dense; and both match an independent recompute from `sgrna_counts.npy`.

**`references/multiomic-perturb-seq.md` API error:** `muon.atac.pp.add_peak_annotation` does not exist
in muon 0.1.9, and the note claimed the gene / distance / peak-type annotations become columns of
`sc.get.rank_genes_groups_df`. Corrected to `muon.atac.tl.add_peak_annotation` and to the real
semantics (`.uns['rank_genes_groups']`, keyed by group). Ran both calls on synthetic MuData: raises as
written, correct after the fix.

**`references/factor-decomposition.md` wrong FR-Perturb flags:** the documented invocation used
`--input` / `--perturbations`, which the tool does not have. Replaced with the real argparse flags
(`--input-h5ad`, `--input-perturbation-matrix` / `--perturbation-column-name`, `--out`), switched the
comment-only python fence to `bash`, and dropped the unused `import pertpy as pt`.

**`usage-guide.md` redundancy:** "What the Agent Will Do" restated three SKILL.md numbers verbatim
(>=10 reads; 39-92% across four guides; 1,000+ iterations). Removed; items 8 and 10 now point at
SKILL.md's Quantitative Thresholds. K=20 kept -- it is not a duplicate.

**`examples/run_pertpy.py` deprecation:** `sc.tl.pca(..., use_highly_variable=True)` is deprecated on
scanpy 1.12 -- the very version SKILL.md:12 claims the examples were checked on. Changed to
`mask_var='highly_variable'`; verified byte-identical `X_pca` on real `papalexi_2021()` (max abs diff
0.0) and re-ran the example end-to-end after the edit.

**Newly run this pass (previously only parse-checked, or never exercised):** `scripts/run_sceptre.R`'s
file-input branch -- built `input.rds` from the bundled `lowmoi_example_data` + a 3-row
`discovery_pairs`: 3 rows, p 0.74 / 0.812 / 0.892, all `significant = FALSE`, correct for null pairs;
`scripts/multiome_differential.py` -- 5/5 planted peaks recovered, and a permuted ATAC feature order
gives byte-identical `pvals_adj`, so the propagation is index-aligned rather than positional;
`scripts/mixscape_filter.py` -- 297 KO, 21.2% of perturbed, denominator correct;
`examples/run_pertpy.py` in full on real `papalexi_2021()` -- 186,490 rows (10 perturbations x 18,649
genes) x 9 columns; SKILL.md's inline PyDESeq2 fragment verbatim -- documented columns asserted
present, 22 genes at `adj_p_value < 0.05`, top 20 by `adj_p_value` = exactly the 20 planted effect
genes; SKILL.md:12's version floors checked against the env (pertpy 1.3.0, scanpy 1.12.4, anndata
0.13.3, pandas 3.0.5, numpy 2.5.3, scipy 1.18.1, muon 0.1.9 -- all satisfied).

**Left as-is on purpose:** `references/genome-wide-perturb-seq.md`'s ```python fence is comment-only
(design arithmetic -- library elements vs cells), not a tool claim, so there is nothing to run.

**Blocked (see `CHECKPOINT.md`):** FR-Perturb cannot be executed in this seat -- `python-spams` exists
only on Anaconda's `defaults`/`anaconda` channel, and `spams` has no py3.12 wheel and needs
`numpy.distutils`. Seurat is not installed in the env's R library, so `Seurat::MixscapeLDA` /
`?Seurat::PrepLDA` (SKILL.md:18,28) were confirmed from published docs, not by loading the package.
