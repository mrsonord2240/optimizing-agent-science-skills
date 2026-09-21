> **Audit record for `bio-data-visualization-color-palettes`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/color-palettes) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-color-palettes (FIRST AUDIT)

Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/color-palettes` (unmodified upstream; extracted with `git archive` to `run\skill\`, all four files `diff --strip-trailing-cr` identical to the clone; nothing written in the clone, no `__pycache__`).
Env: `F:\OpenScience\audit-envs\data-visualization` (R 4.4.3 via `r.sh`: ggplot2 4.0.3, viridis 0.6.5, RColorBrewer 1.1.3, scico 1.5.0, khroma 1.17.0, ggsci 5.2.0, colorspace 2.1.2, scales 1.4.0; Python 3.12 via `py.sh`: matplotlib 3.11.2, cmcrameri 1.10, colorcet 3.2.1, colorspacious 1.1.2, seaborn 0.13.2).
Category: Data Analysis (3), result visualization | Mode A (agent writes code from the Skill's patterns; two shipped examples) | Complexity: Moderate (4 task types: sequential/diverging/cyclic/categorical + CVD and grayscale checks; 4 files) -> 5 inputs
Data: ALL SYNTHETIC (seed 20260920), saved in `data\`: `synthetic_umap_celltypes.csv`, `synthetic_skewed_lfc.csv`, `synthetic_spatial_expr.npy`, `synthetic_phd_df.csv`, `synthetic_phd_de_df.csv`. The palettes themselves are the real package output.
Method: every claim about a colour was asserted by computation, with two independent methods where possible (CIELab L* in R `colorspace` and Python `colorspacious`; CVD by `colorspace::deutan/protan/tritan` and `colorspacious` `sRGB1+CVD`; the pairwise distance is CAM02-UCS dE, min over all pairs; ggplot_build fill values for mapping questions). Figures were opened with Read and pixel-checked.

## Result

| | |
|---|---|
| Static | **71** / 100 |
| Execution average | **72.4** / 100 (L1 avg 29.8/40, L2 avg 42.6/60) |
| Final | **71.8** (28.4 + 43.4) |
| Grade | **Beta Only** |
| Deployable | **false** (grade below Limited Release) |
| Vetoes | none (Skill veto PASS, Research veto PASS) |
| Open P0 / P1 / P2 | 0 / 6 / 3 |
| Assertions | 12/25 (48%) |
| Executed | 5/5 |

Grade note: 71.8 is Beta Only. Limited Release floors missed: execution avg 72.4 < 75 and assertion pass rate 48% < 80% (static 71, L1 29.8 and L2 42.6 pass). No safety-assertion failure and no P0.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: 7 cell types, Okabe-Ito, grey for unassigned | 30 | 41 | 71 | 2/5 | warn |
| 2 | Variant A: vik LFC heatmap, symmetric, zero white | 32 | 48 | 80 | 3/5 | pass |
| 3 | Edge: grayscale + CVD audit of candidate palettes | 28 | 39 | 67 | 2/5 | warn |
| 4 | Variant B: jet migration, signed and cyclic data (Python) | 31 | 46 | 77 | 3/5 | pass |
| 5 | Stress: both shipped examples, 15 groups, journal palettes | 28 | 39 | 67 | 2/5 | warn |

Static breakdown: functional 8/12, reliability 7/12, performance/context 5/8, agent usability 10/16, human usability 7/8, security 11/12, maintainability 7/12, agent-specific 16/20 (notes in the JSON).

## Skill veto and shipped-means-present

- T1-T4 PASS: no eval/exec/shell/network, no credentials, deterministic (palette functions are pure; rerunning `i2_diverging.R` printed identical output; the examples seed with `set.seed(42)`); frontmatter has `name`, `description`, `license`.
- Gate 8: folder ships `SKILL.md`, `usage-guide.md`, `examples/palettes_phd.R`, `examples/palette_examples.R`; nothing points at a `references/`, `scripts/` or `assets/` file. All four Related Skills exist in staging.
- Gate 7: figure-colour Skill, nothing diagnostic or prescriptive.
- Citations: Crameri 2020 (Nat Commun 11:5444), Nunez 2018 (PLOS ONE 13:e0199239), Wong 2010/2011, Gehlenborg and Wong 2012, Harrower and Brewer 2003, Borland and Taylor 2007, Light and Bartlein 2004 are real; none fabricated.

## Existence and signature checks (run/i0_api.R, i6_exist.R, i7_skill_blocks.R)

```
scico 1.5.0 names: batlow lipari vik roma bam romaO vikO  -> all TRUE       viridis options incl. turbo: OK (6/6 drawn)
scale_fill_scico formals: ... alpha begin end direction palette midpoint   ggsci npg/aaas/lancet/jama/jco/nejm: 6/6 exist
palette.colors(8,'Okabe-Ito') = 000000 E69F00 56B4E9 009E73 F0E442 0072B2 D55E00 CC79A7 (+ 999999 as 9th)
brewer.pal(8,'Dark2') 8, (9,'YlOrRd') 9, (11,'RdBu') 11: OK      display.brewer.all(colorblindFriendly=TRUE): draws
cvd_emulator formals: file, overwrite, shiny.trace   <- takes an image file, NOT a palette
Diverging centres:  vik #EBE5E0 (L* 91.3) | roma #C0E9C2 | bam #F5F0F0 | RdBu #F7F7F7   bam ends #65014B (magenta) .. #0C4C00 (green)
```

## Palette computation (run/i1_metrics.py, 256-step ramps; L* = CIELab; frac = share of steps in the dominant L* direction; stepCV = CAM02-UCS step-size variation)

```
cmap        L0    L1   Lmin  Lmax  monotonic  frac   stepCV
viridis    14.9  90.9  14.9  90.9   True     1.0    0.012
magma       0.1  97.8   0.1  97.8   True     1.0    0.009
cividis    13.9  91.2  13.9  91.2   True     1.0    0.055
batlow     12.2  87.2  12.2  87.2   True     1.0    0.089
lipari      5.5  96.4   5.5  96.4   True     1.0    0.102
turbo      12.0  24.5  12.0  90.9   False    0.506  0.359
jet        12.9  25.4  12.9  95.9   False    0.569  0.429
rainbow    40.8  53.2  40.1  91.5   False    0.51   0.311
```
R cross-check (10 steps, `colorspace`): `turbo L* 12 46 67 81 90 89 79 62 45 24` (mono=FALSE); `viridis 15 24 33 42 50 59 67 75 83 91` (TRUE).

CVD, minimum pairwise CAM02-UCS dE (run/i2_cvd.py; >= 10 comfortably distinct, < 5 hard to tell):

```
palette                normal   deutan   protan   tritan
Okabe-Ito 7            20.8     14.8     14.0     11.0
Tol bright 7           23.4     16.2     15.6      7.4
npg 8                  10.8      7.8      9.5      9.4
aaas 8                 10.0      5.9      6.1      3.1
lancet 8               18.5      7.4     13.4      7.4
jco 8                  21.3      9.1     15.7     15.7
nejm 8                 17.8     10.5      5.1      7.2
Set1 (first 5)         25.3      4.7      7.7     13.6
Dark2 8                16.7      3.7      2.2      6.9
Sequential ramp shift under deutan sim (mean dE): cividis 0.7, batlow 10.7, viridis 15.4, magma 20.0, turbo 19.2
```

## Detailed Outputs

### Input 1 - Canonical: CVD-safe categorical palette, grey for unassigned
**Prompt:** "Assign one CVD-safe Okabe-Ito color to each of these 7 cell types, reserve grey for ambient/unassigned (usage-guide prompt). My UMAP has T, B, NK, monocyte, dendritic, platelet and erythroid cells plus unassigned cells; I'll also show a subset without the T cells."
**Run:** `run\i1_categorical.R` (Skill Okabe-Ito block verbatim, then named-vector variant; 1,270 SYNTHETIC cells), `run\i1b_grey_conflict.py`. Figures: `figs\i1_categorical_full_vs_subset.png`, `figs\i1_categorical_cvd.png` (both opened).
**Printed (trimmed):**
```
Skill hexes as set == palette.colors(8,'Okabe-Ito') set: TRUE ; same ORDER: FALSE (palette.colors starts with #000000)
A (Skill, unnamed): Unassigned -> #000000 (black)
B (same code, T cells removed): B cell E69F00 (was 56B4E9) NK 56B4E9 (was 009E73) Monocyte 009E73 ... Unassigned CC79A7
cell types whose colour CHANGED between A and B (unnamed vector): 7 of 7
Named vector (grey #999999 for Unassigned): mapping identical across full and subset: TRUE
cvd_emulator(pal, type='deutan') -> ERROR: unused argument (type = "deutan")
deutan(pal): Erythroid #9498A5, NK #8A8676, Unassigned #999999
deutan min dE with grey: Erythroid 6.5, NK cell 9.8 (all others >= 23.6)
```
**Reading:** in the figure the 8th level is black, and in panel B every colour has moved one step; in the deuteranopia panel NK and Erythroid sit on the grey Unassigned cloud. The named vector fixes the shift, and the palette itself is right.
**Scores:** Basic 30/40 | Specialized 41/60 | Total 71/100
**Assertions:** 2/5 (see JSON): PASS hexes equal; PASS 7-colour deutan min 14.8; FAIL unnamed mapping stable; FAIL cvd_emulator as written; FAIL Okabe-Ito 7 + grey separable under deutan.

### Input 2 - Variant A: diverging LFC heatmap with vik, zero pure white
**Prompt:** "Use a diverging Crameri vik palette for a log-fold-change heatmap with symmetric bounds at +/- the 99th percentile of |LFC|. Zero must map to pure white." (usage-guide prompt, verbatim)
**Run:** `run\i2_diverging.R` (SKILL block, `palettes_phd.R` block 2, range-based default and custom ramp; 480 SYNTHETIC cells with right skew, min -2.94, max 8.12, one exact zero). Figure `figs\i2_diverging_heatmaps.png` (opened).
**Printed:**
```
fill of the EXACT-ZERO cell:  A vik midpoint=0 -> #EBE5E0 | B vik midpoint=0, +-q99 squish -> #EBE5E0 | C vik default -> #3B85AC | D custom #0072B2/white/#D55E00 -> #FFFFFF
vik centre scico(255)[128] = #EBE5E0 ; RdBu brewer midpoint #F7F7F7 ; q99 |lfc| = 4.81 ; squished cells 5/480
```
**Reading:** panel C (default) shows the Skill's failure mode, the whole matrix blue. A and B are correct diverging maps, zero anchored, but the zero colour is a warm off-white that the Skill's own rule would call a failure; panel D is truly white.
**Scores:** Basic 32/40 | Specialized 48/60 | Total 80/100
**Assertions:** 3/5: PASS vik centre at zero; PASS symmetric q99 example; FAIL "pure white" with vik; FAIL rule vs recommended palettes (centre L* 91.3 vs banned #EEEEEE 94.1); PASS custom ramp white.

### Input 3 - Edge: grayscale and CVD audit
**Prompt:** "Run colorspace::cvd_emulator on the current palette and report whether the categories remain distinguishable under deuteranopia; also verify it prints correctly in grayscale. Candidates: viridis, cividis, batlow, turbo, rainbow."
**Run:** `run\i3_cvd_gray.R` (SKILL blocks verbatim + L* in R), `run\i1_metrics.py`, `run\i3_python_snippet.py`. Figures `figs\i3_showcol_gray.png`, `figs\i3_demoplot.png` (opened).
**Printed (trimmed):**
```
L* mono: viridis TRUE, cividis TRUE, magma TRUE, batlow TRUE, turbo FALSE, rainbow FALSE
L* grey ramp 0 10 24 36 48 59 70 80 90 100 | viridis 15 24 33 42 50 59 67 75 83 91 | desaturate(viridis) 15 24 34 42 50 59 67 74 83 91
max |L*(viridis) - L*(grey ramp)| = 14.9 ; vs desaturate = 0.2
cvd_emulator(palette, type='deutan'|'protan'|'tritan') -> ERROR: unused argument (type = t)
python: from colorspacious import cspace_converter -> import ok (nothing simulated); working call cspace_convert(..., {"name":"sRGB1+CVD",...}) returns sim
plt.style.use('colorblind') -> OSError ; 'seaborn-v0_8-colorblind' cycle: 0072B2 009E73 D55E00 CC79A7 F0E442 56B4E9
```
**Reading:** `show_col` panels: the grey ramp (top middle) is a different ramp from `desaturate(viridis)` (top right); `desaturate(rainbow)` shows light-dark-light banding, `desaturate(turbo)` peaks in the middle. `demoplot` heatmaps: batlow keeps its dark-to-light order under deutan/protan, rainbow collapses to yellow/blue.
**Scores:** Basic 28/40 | Specialized 39/60 | Total 67/100
**Assertions:** 2/5: PASS viridis/cividis/batlow monotonic; PASS rainbow/jet fail; FAIL turbo passes own test; FAIL CVD call runs; FAIL grey ramp is the equivalent.

### Input 4 - Variant B: jet migration, signed and cyclic data (Python)
**Prompt:** "Find every plot in this notebook that uses cmap='jet' and replace it; the spatial map, the signed log-ratio panel and the phase panel are all affected."
**Run:** `run\i4_python_migration.py` (SYNTHETIC 120x160 field with two peaks). Figures `figs\i4_jet_migration.png`, `figs\i4_diverging_python.png`, `figs\i4_cyclic.png` (jet migration and cyclic opened).
**Printed (trimmed):**
```
vik, vmin/vmax = data min/max : zero maps to 0.155 of the colour range -> #044f88 (centre #ece5e0)
vik symmetric (Skill fix)     : zero maps to 0.500 -> #ece5e0 ; RdBu_r vmin=-2,vmax=2 -> 0.500 #f7f6f6 ; pixels beyond +-2 saturated: 0.084
seam dE: viridis 92.1 | twilight 0.2 | cm.romaO 0.6 | cm.vikO 0.6
batlow lipari vik roma bam romaO vikO all present in cmcrameri.cm
rank corr(data, L* of rendered pixel): jet 0.996 rainbow 0.997 turbo 0.978 viridis 1.000 batlow 1.000   <- did NOT separate jet on this smooth field; not used as evidence
```
**Scores:** Basic 31/40 | Specialized 46/60 | Total 77/100
**Assertions:** 3/5: PASS Crameri names and blocks; PASS symmetric vs min/max; PASS cyclic seams; FAIL jet to turbo is monotonic/uniform; FAIL `colorblind` style.

### Input 5 - Stress: shipped examples, many groups, journal palettes
**Prompt:** "Run the shipped examples, then color 15 clusters and tell me whether npg/aaas/lancet are safe for the reviewers."
**Run:** `run\ex\palette_examples.R` verbatim (plus a PNG copy `palette_examples_png.R`), `palettes_phd.R` verbatim and via `run\i5c_phd_harness.R` (SYNTHETIC `df`, `de_df`), `run\i5e_many_groups.R`, `run\i5f_many_groups.py`. Figures `figs\i5_palette_examples.png` (opened), `figs\i5_phd_03.png` (opened), 15 harness pages pixel-checked (non-white 0.42-0.77).
**Printed (trimmed):**
```
palette_examples.R: Saved: palette_examples.pdf (34,737 B)
palettes_phd.R verbatim: ggplot2 error "data cannot be a function" (df is stats::df)
harness: 24/24 expressions OK (incl. scale_fill_scico(midpoint=0, limits, oob=squish), romaO, deutan/protan demoplot, desaturate show_col, scale_color_npg)
min dE normal / deutan (pairs<10 under deutan):  tab20 n=20 11.3 / 2.9 (16) | Paired 12 15.9 / 3.6 (6) | Polychrome 36 first 15 19.8 / 2.0 (6) | Okabe-Ito 8 20.8 / 14.8 (0)
```
**Reading of palette_examples.png:** the "Custom Diverging" panel has near-zero points white on white and the light blue arm much weaker than the red arm; the qualitative panels use Set1 and NPG-style hexes, which the Skill says not to use when CVD matters.
**Scores:** Basic 28/40 | Specialized 39/60 | Total 67/100
**Assertions:** 2/5: PASS example 1 runs; FAIL example 2 as shipped; PASS journal palettes CVD-imperfect; FAIL examples follow own advice; FAIL 9-20 group palettes CVD-safe.

## Findings (see JSON for root cause and fix)

- P1 turbo called perceptually uniform and offered as the rainbow fix; fails L* monotonicity and uniformity (3, 4).
- P1 `cvd_emulator(palette, type=)` errors; Python CVD block simulates nothing (1, 3).
- P1 pure-white midpoint rule contradicts vik/roma/bam/RdBu centres; the guide's prompt cannot be met with vik (2, 4).
- P1 unnamed Okabe-Ito vector recolours groups on subsetting, gives black to the 8th level, no grey path; Okabe-Ito + grey collides under deutan (1).
- P1 grayscale block uses a generic grey ramp, and is billed as the CVD check (3).
- P1 shipped examples contradict the Skill (Set1/NPG, invisible white points) and `palettes_phd.R` does not run without `df` (5).
- P2 9-20 group palettes are not CVD-safe (5); small factual errors (`colorblind` style, viridis default since 2.0, bam colours, roma description, RdBu called uniform, RdBu_r +-2 hard-coded, even-N colorRampPalette has no white); usage-guide duplicates SKILL.md and lists unused khroma/colorcet.

## Files

`run\` holds every script and its `.out` (`i0_api.R`, `i1_categorical.R`, `i1_metrics.py`, `i1b_grey_conflict.py`, `i2_cvd.py`, `i2_diverging.R`, `i3_cvd_gray.R`, `i3_python_snippet.py`, `i4_python_migration.py`, `i5c_phd_harness.R`, `i5d_png_check.py`, `i5e_many_groups.R`, `i5f_many_groups.py`, `i6_exist.R`, `i7_skill_blocks.R`, `finalize_report.py`, `ex\` copies of the shipped examples), the extracted Skill at `run\skill\`; `data\` synthetic inputs and palette lists; `figs\` all PNGs.
