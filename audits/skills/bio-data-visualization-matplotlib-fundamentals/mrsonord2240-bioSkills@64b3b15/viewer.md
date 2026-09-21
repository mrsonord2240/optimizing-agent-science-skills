> **Audit record for `bio-data-visualization-matplotlib-fundamentals`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/matplotlib-fundamentals) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-matplotlib-fundamentals (first audit)

Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/matplotlib-fundamentals` (extracted with `git archive` into `run\skill\`; nothing written into the repo; `find -name __pycache__` in the clone: none).
Env: `F:\OpenScience\audit-envs\data-visualization\` via `py.sh` (Python 3.12.13, matplotlib **3.11.2**, seaborn 0.13.2, numpy 2.5.3, pandas **3.0.6**, cmcrameri; Arial present, Helvetica absent). The Skill says "tested with matplotlib 3.8+, pandas 2.2+".
Category: Data Analysis (result visualization) | Mode: A (Skill's own code blocks exec-ed verbatim, plus the shipped example) | Complexity: Moderate, 5 inputs. All data is synthetic and labelled so in each script.

## Result

| | |
|---|---|
| Static | **76** |
| Execution average | **73.6** |
| Final | **75** (30.4 + 44.2 = 74.6) |
| Grade | **Beta Only**, not deployable |
| Assertions | 15/24 (62.5%) |
| Vetoes | none (Skill veto PASS, Research veto PASS) |
| Open P0 / P1 / P2 | 0 / 6 / 6 |

Grade note: 75 is numerically Limited Release. It drops one tier because two floors in `scoring_rubric.md` section 5 are missed: execution average 73.6 < 75 and assertion pass rate 62.5% < 80%. Floors met: static 76 (>=70), Layer 1 average 30.8/40, Layer 2 average 42.8/60.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Executed |
|---|---|---|---|---|---|---|
| 1 | Canonical: 89 mm PCA scatter, TrueType PDF | 35 | 51 | 86 | 3/5 | yes |
| 2 | Variant A: 2x3 multipanel (Common Chart Types) | 30 | 41 | 71 | 3/4 | yes |
| 3 | Edge: seaborn volcano into a pre-made Axes, objects API, FacetGrid | 28 | 38 | 66 | 3/5 | yes |
| 4 | Variant B: axis formatting, colour, PDF/PNG/TIFF/SVG | 30 | 41 | 71 | 3/5 | yes |
| 5 | Stress: 100k-cell UMAP + every Failure Modes claim + shipped example | 31 | 43 | 74 | 3/5 | yes |

Executed 5/5. Reproduce in `run\`: `env_check.py`, `i1_pca.py`, `i2_charts.py`, `i2b_box.py`, `i3_seaborn.py`, `i4_axis_color_save.py`, `i5a_example` (copy of the shipped example run in `run\scratch`, then `i5a_check.py`), `i5b_failure_modes.py`, `finalize_report.py`. Helpers: `blocks.py` (extracts SKILL.md python blocks so they run verbatim), `pdfcheck.py` (PDF fonts, page size, image XObjects, font sizes from the raw PDF; `pdftotext` for text). Raw outputs: `i1.out`, `i2.out`, `i2b.out`, `i3.out`, `i4.out`, `i5a_example.out`, `i5b.out`; figures in `run\out\`.

## What was checked and what came out

**Input 1 (blocks 0 and 1 verbatim).** Ran with no error or warning. PDF: `size_mm (89.42, 70.42)`, fonts `ArialMT` TrueType x1, Type 3 x0, font sizes {6, 7} pt, 2 image XObjects (rasterized scatter), `pdftotext` returns `PC1 (34.6%)` and tick labels. PNG 1056x831, 300 dpi. Opened `run\out\pca_true.png`: three clusters, top/right spines off, correct labels. The Skill's typed label `PC1 (45%)` is not what PCA gave (34.6%). The requested 89 mm becomes 89.42 mm because `savefig.bbox: tight` resizes the page.

**Input 2 (block 2 segment by segment).** Scatter, line, bar, histogram ran. `ax.boxplot(..., labels=[...])` -> `TypeError: Axes.boxplot() got an unexpected keyword argument 'labels'` (removed; `tick_labels=` works, verified in `i2b.out`). Heatmap segment -> `NameError: vmax`. After supplying vmax and `tick_labels`, the assembled 2x3 figure (`multi2x3.png`, opened) is correct: bar heights 3.1/4.7/2.2, histogram counts sum to 2000, boxplot medians 0.074/0.915/2.033 identical to `np.median`, colorbar labels Expression and Z-score, heatmap clim +/-2.657 = 99th percentile. Multipanel PDF 179.97 x 100.42 mm, Type 3 x0.

**Input 3 (block 3 verbatim).** Draws 5000/5000 rows. The list palette `['#999999','#0072B2','#D55E00']` was applied in first-appearance order: legend `Up=#999999, NS=#0072B2, Down=#D55E00`; opened `volcano_sns.png`: upregulated genes grey, non-significant genes blue. A dict palette gave the intended colours. The `seaborn.objects` snippet returns an unrendered `Plot` (needs `.save()`/`.plot()`); `pl.save` then works. `sns.displot` returns `FacetGrid` with no `set_xlabel` (AttributeError), `set_axis_labels` works: the Skill's gotcha is correct.

**Input 4 (blocks 4, 5, 6).** Log, sci-notation (offset `x10^6`), date and grid snippets work. Tick snippet: `NameError: np`, then with np `ValueError: The number of FixedLocator locations (5) ... does not match the number of labels (3)`. Colour block needs `data`. Okabe-Ito list equals the published 8 hexes; symmetric clim (-7.710, 7.710) equals `np.quantile(abs, 0.99)`. Saving: PNG 300 dpi, TIFF 300 dpi `tiff_lzw`, PDF Type-42, SVG has **0 `<text>` elements** (28 paths; `svg.fonttype` default `path`), so the claim "SVG for editable vector" holds only for shapes, not text.

**Input 5 (Failure Modes + shipped example).**
- 100,000-point scatter PDF: vector 2,000,274 B in 11.9 s; `rasterized=True` 363,890 B in 2.1 s (the Skill's "50 MB" is not reproduced; the direction is right).
- Colorbar `shrink=0.6, aspect=20`: height ratio 0.60, no overlap with axes. `umap_cb.png` opened: 12 clusters, labelled UMAP1/UMAP2, colorbar 'Gene X'.
- `rcParamsDefault['figure.constrained_layout.use'] = False`: the Skill's "constrained_layout ... is the default in matplotlib 3.6+" is false.
- `fig.set_rasterization_zorder(0)` -> `AttributeError`; `ax.set_rasterization_zorder(0)` works.
- `tight_layout()` + colorbar: no warning, no clipped axes on 3.11.2 (claim not reproduced).
- `fig.set_constrained_layout(True)` works with a `PendingDeprecationWarning`.
- Default PDF has Type 3 x1, TrueType x0 (Skill correct); with the fix Type 3 x0.
- `figsize=(89,70)` -> 8900x7000 px at 100 dpi (Skill correct).
- 12 clusters with the 8-colour Okabe-Ito list: seaborn cycles (8 distinct colours), warning only; the Skill says nothing about >8 categories.
- Shipped `examples/matplotlib_phd.py` (run from a copy, seaborn emits `Pandas4Warning` on pandas 3): writes `pca.pdf` (91.96 x 72.96 mm), `multipanel.pdf` (182.72 x 112.96 mm, 12 images), `heatmap.pdf` (91.78 x 92.96 mm), `volcano_sns.pdf`, `volcano_so.pdf`. All: Type 3 x0, text extractable. `volcano_so.pdf` is 162.56 x 121.92 mm with 11-12 pt text and no raster layer: the `seaborn.objects` recipe ignores the Nature setup the Skill sets up above it. The pca example hard-codes `PC1 (45.2%)` over random data.

## Gate 8 (shipped means present)

Every path the Skill points at exists at the commit: `data-visualization/{color-palettes,multipanel-figures,distribution-plots,heatmaps-clustering,volcano-and-ma-plots}` and `reporting/figure-export` each have a SKILL.md. The Skill has no `references/` or `scripts/` files; `examples/matplotlib_phd.py` exists and runs. No P0.

## Research veto

M1 PASS (placeholders are labelled illustrative, flagged P1), M2 PASS (no individual-level content), M3 PASS, M4 PASS with findings (example runs; 3 fragment lines fail on 3.11.2 or need undefined names). Skill veto T1-T4 PASS (seeded example is deterministic; no injection surface).

## Recommendations

P0: none.

P1 (fix before production):
1. `boxplot(labels=)` removed in matplotlib 3.11: use `tick_labels=`.
2. `fig.set_rasterization_zorder` does not exist: use `ax.set_rasterization_zorder`.
3. "constrained_layout is the default in 3.6+" is false: must be requested.
4. List palette maps by appearance order: Up rendered grey, NS blue. Use a dict palette with `hue_order`.
5. Hard-coded PC variance labels (45%, 45.2%) over data whose variance differs: compute from `explained_variance_ratio_`.
6. "89 mm" is 89.42 mm (Skill rcParams) or 91.96 mm (example) after `bbox tight`; the `seaborn.objects` example is 162 mm wide with 11-12 pt text.

P2: fragments not self-contained (np, data, vmax, tick/label mismatch, objects snippet never renders); SVG text not editable without `svg.fonttype='none'`; 180 mm vs 183 mm and unsourced journal rules and "50 MB"; no guidance for >8 categories or overplotting order; deprecation/warning debt (`set_constrained_layout`, `Pandas4Warning`, unreproduced tight_layout claim); no When-Not-To-Use section.

Full detail and fixes: `eval_report_bio-data-visualization-matplotlib-fundamentals_result.json`.
