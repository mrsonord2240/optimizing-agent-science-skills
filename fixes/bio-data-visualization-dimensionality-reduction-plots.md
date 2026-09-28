# bio-data-visualization-dimensionality-reduction-plots

## 2026-09-27 — backlog correction

Source branch: `fix/backlog-dimensionality-reduction`, based on shelf commit `c6d06ae53e0be79b792aa5082d0d1d8b781acd55`. Scope: all 12 recommendations in the 2026-09-20 audit (6 P1, 6 P2).

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| Rtsne silently ignores `seed=42` | P1 | Replaced the generalized seed rule with `set.seed(42)` immediately before `Rtsne()`; kept `seed=` only for uwot. | Audit regression evidence reproduced the ignored argument; corrected text checked in `SKILL.md` and `references/method-recipes.md`. | Rtsne accepts the unsupported value through `...`, so no error is sufficient evidence. |
| Scikit-learn PCA was called deterministic although `auto` selected a randomized solver | P1 | Qualified PCA reproducibility and specified `svd_solver="full"` (or a fixed seed) in the Python recipe. | The prior audit's wide-matrix regression found a max score difference of 15.3; source assertions confirm the deterministic recipe. | Scanpy's explicit PCA seed remains recorded in the runnable example. |
| Shipped example and prerequisites were incomplete | P1 | Turned `embedding_phd.py` into a CLI, documented the raw-count/shape/metadata contract, added `scikit-misc` and `igraph` prerequisites, and selected Scanpy's igraph Leiden flavor. | `py_compile`; 3 focused tests; full run on the audit's 1,200-cell/3,000-gene synthetic H5AD completed. | Verification used task-local `scikit-misc==0.5.2`; the shared environment was not modified. |
| `seurat_v3` HVG ran after normalization/log1p | P1 | Moved `highly_variable_genes(..., flavor="seurat_v3", subset=True)` before normalization and added a raw-integer input validator. | Focused tests accept raw counts and reject fractional/log values; full example run emitted no raw-count warning. | Input contract requires at least 2,000 genes. |
| Library-size and batch guidance was inaccurate | P1 | Required library-size normalization before log/scale; replaced PC1/PC2-only batch diagnosis with PC1-PC5 R2 plus kNN batch mixing; removed the claim that UMAP hides batch. | Text checked against the audit's planted library-size and PC4 batch regressions. | UMAP is treated as a display, not a batch statistic. |
| Example dropped plots, lacked a categorical legend, and printed literal `{n}` | P1 | Saved PCA, scree, UMAP, t-SNE, and PHATE with exact paths; added condition/Leiden legends; made the caption an f-string. | Full run wrote five non-empty PDFs (13,378-254,649 bytes); every first page was rendered and opened. Caption printed `N=1200`. | PCA also shows five strongest loading arrows. |
| openTSNE defaults were misstated | P2 | Documented that openTSNE 1.0 already defaults to PCA initialization and `learning_rate="auto"` (n/12); explicit values now record provenance. | Full openTSNE run completed with the corrected explicit contract. | Removed claims that openTSNE defaults to random initialization or learning rate 200. |
| Local-neighborhood preservation was overstated | P2 | Reworded the claim to partial preservation, added a reusable kNN-overlap procedure, and printed measured retention in the example caption. | Full run measured 15-neighbor retention at 16.5%. | `tests/test_embedding_phd.py` confirms identical embeddings yield retention 1.0. |
| Low PC1/PC2 variance was called noise | P2 | Scoped that warning to bulk sample QC and stated that low percentages are normal for sparse single-cell data. | Checked against the audit example: PC1/PC2 approximately 1.1% with planted clusters recovered. | No universal variance cutoff is asserted. |
| Perplexity heading contradicted its body | P2 | Renamed it to “too high for sample size” and distinguished Rtsne's error from openTSNE's warning/clamp. | Checked against audit runs at n=60. | The `< n/3` validity rule remains. |
| Python lacked loadings/legend code; Scanpy seed/save notes were stale | P2 | Added loading arrows and categorical legends to the example, scoped seed behavior by implementation, and replaced deprecated `save=` usage with `show=False` plus `figure.savefig`. | Full Scanpy run produced labeled PCA/UMAP outputs and exact-path PDFs; rendered outputs were opened. | Scanpy's deterministic default is acknowledged while an explicit seed is still recorded. |
| `usage-guide.md` duplicated `SKILL.md` | P2 | Deleted the repeated Tips rules and replaced them with a pointer to the canonical method/failure-mode sections. | Diff review plus link checks. | Method blocks moved from `SKILL.md` to `references/method-recipes.md`; neighborhood/batch validation moved to `references/neighborhood-validation.md`. Nothing needed by the agent was removed. |

### Structural pass

- `SKILL.md` decreased from 326 to 220 lines.
- Detailed PCA, t-SNE, UMAP, Scanpy-save, and PHATE material moved to `references/method-recipes.md`, indexed under **Reference Files** and linked from the decision flow.
- Neighborhood-retention and batch-mixing validation moved to `references/neighborhood-validation.md`.
- The complete runnable workflow remains in `examples/embedding_phd.py`, where runnable examples are exempt from duplication with the concise recipes.
- Unfixed recommendations: none (12/12 addressed).

## 2026-09-27 — independent re-audit follow-up

Source branch: `fix/backlog-dimensionality-reduction`. Scope: all three P2 recommendations from the independent 93/100 re-audit of shelf commit `f3de5bc6421ca81d37ca532c1771e533a9af5cdf`.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| Fixed `tab10` reused colors for 12 conditions | P2 | Added one-to-one `tab20` colors for 1-20 categories and a hard stop requiring faceting or a documented alternative above 20; applied the same guard to condition and Leiden legends. | Added a unique-RGBA regression for 12 categories and an above-20 failure check; ran the full example on the archived 100-cell, 12-condition fixture and visually inspected its PCA PNG. | The boundary PCA showed 12 distinct legend colors; no palette recycling remains. |
| `SKILL.md` said the example saved four figures | P2 | Corrected the example summary to five saved figures. | Existing filename regression checks all five exact outputs; both archived boundary and 1,200-cell runs produced PCA, scree, UMAP, t-SNE, and PHATE previews. | The executable already produced five; only the stale summary changed. |
| PCA loading labels could collide | P2 | Replaced fixed offsets with deterministic candidate placement that tests rendered text boxes and accepts only non-overlapping labels. | Added a five-label coincident-anchor non-overlap regression with deterministic offset assertions; ran and visually inspected PCA output on both archived 100-cell and 1,200-cell fixtures. | All five labels were distinct and readable in both visual checks. |

- TDD: the two new focused tests first failed because the palette and collision helpers did not exist, then passed after implementation.
- Verification: `py_compile` passed for the changed example and test; all 7 focused tests passed.
- Unfixed recommendations: none (3/3 addressed).
