> **Audit record for `bio-data-visualization-distribution-plots`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/distribution-plots) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-distribution-plots
Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/distribution-plots` (unmodified upstream; SKILL.md, usage-guide.md, examples/raincloud_phd.R; no references/ dir, nothing referenced is missing)
Category: Data Analysis (3) | Mode: A | Complexity: Moderate -> N = 5 | Env: `F:\OpenScience\audit-envs\data-visualization` (r.sh = ggplot2 4.0.3, r-gg35.sh = ggplot2 3.5.2 + gghalves, py.sh = seaborn 0.13.2 / ptitprince 0.3.1 / matplotlib 3.11.2)

## Result

**Static 70 x 0.4 = 28.0 | Execution avg 69.2 x 0.6 = 41.5 | FINAL 69.5 - Beta Only.** No veto fired, no P0. Below the Limited Release floors (execution avg 75). 12/24 assertions passed. 5/5 inputs executed.

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: every R block, planted 2-group data | 32 | 45 | 77 | 4/5 | OK (raincloud fails on ggplot2 4.x) |
| 2 | Variant A: Python ptitprince / seaborn blocks | 34 | 48 | 82 | 2/4 | OK |
| 3 | Edge: zero-inflated / ties / small N / notch / N snippet / bandwidth claims | 26 | 33 | 59 | 2/5 | defects |
| 4 | Variant B: REAL ALL microarray, split violin, missing cell | 28 | 42 | 70 | 2/5 | defects |
| 5 | Stress: shipped example raincloud_phd.R | 24 | 34 | 58 | 2/5 | defects |

Layer averages: basic 28.8/40, specialized 40.4/60. All numbers below are from `run/out/*.log`; every figure named was opened.

## Static (25 criteria, 70/100)

Functional 8/12, Reliability 5/12, Performance 6/8, Agent usability 11/16, Human usability 7/8, Security 11/12, Maintainability 7/12, Agent-specific 15/20 (notes in the JSON).

## Input 1 - Canonical (R blocks verbatim, planted data)

**Prompt:** "Compare a biomarker between Control (n=25) and Treated (n=80). Show every point, the distribution and the summary; don't use bars."

Data (SYNTHETIC, `run/data/i1_synthetic_2group.csv`, seed 20260920): Control N(5,1); Treated 50/50 mixture N(3,0.5)+N(7,0.5). Means 4.990 / 4.968, medians 5.186 / 4.875.

Code: `run/i1_blocks.R` (SKILL blocks pasted verbatim, then `layer_data()` assertions).

```
ggplot2 4.0.3
[PASS] box medians equal data medians 5.186/4.875
[PASS] box fill order Control=#0072B2 Treated=#D55E00
[PASS] jitter shows every point (25 + 80)
[PASS] SJ violin: Control unimodal, Treated bimodal (prominent modes) 1/2
[PASS] trim=FALSE: violin extends past data range  y [0.61, 9.18] vs data [1.69, 8.09]
[PASS] quasirandom draws all 105 points ...  crossbar y equals group median 5.186/4.875
[PASS] quasirandom deterministic / y values are the data values
BLOCK ERROR raincloud : Caused by error in `fun()`: ! argument "layout" is missing, with no default
letter-value M row 5.186 / 4.875 = data medians   [PASS]
--- r-gg35.sh (ggplot2 3.5.2)
[PASS] raincloud half-points: 105 raw points, y equals data  n per group 25/80
[PASS] raincloud box medians equal data medians       (lv block: could not find function "gg_par", lvplot built for 4.0.3)
```

Opened `out/i1_raincloud_gg35.png`: horizontal raincloud, blue Control (unimodal), orange Treated (two humps at 3 and 7), boxes in the gap-median, points beneath. `out/i1_raincloud_gg4.png` is a 1.5 KB blank. `out/i1_violin_gg4.png`: Treated bimodal, Control unimodal, colours in group order. `out/i1_quasi_gg4.png`: crossbar for Treated at 4.875 sits in the empty band between the two point clusters (the bar-of-mean insight). ggdist raincloud on 4.0.3 (`out/i1b_ggdist_raincloud_gg4.png`) renders with medians 5.186/4.875.

Also: default (nrd0) violin already shows two prominent modes on this well-separated data, so "default oversmooths bimodality" is not visible here (it is at smaller separations, see Input 3).

**Scores:** Basic 32/40, Specialized 45/60, Total 77. Assertions 4/5 (raincloud on 4.0.3 FAIL).

## Input 2 - Variant A (Python)

**Prompt:** "Same data in Python: horizontal raincloud with ptitprince, a boxen plot, and standard seaborn box/violin/swarm/strip."

Code: `run/i2_py.py`, `run/i2b_bw.py`.

```
seaborn 0.13.2 matplotlib 3.11.2 pandas 3.0.6
-- i2_raincloud_verbatim: ran; FutureWarning palette-without-hue; MatplotlibDeprecationWarning vert (removed in 3.13)
-- i2_boxen: ran; FutureWarning palette-without-hue (removed in seaborn 0.14)
[verbatim x=group,y=value,orient=h] scatter collections [1, 1, 25, 80]; ylabel='group' xlabel='value'; box medians x = ..., 4.875, 5.186, ...
scott: bw=0.869 valley/lower-peak density = 0.346 | Sheather-Jones (R): bw=0.363 -> 0.028 | Treated points between 4 and 6: 3 of 80
```

Opened `out/i2_raincloud_verbatim.png`: correct groups and colours, 25 and 80 points, Treated violin bimodal but the valley is filled in; points overlap the box (the Skill promises no occlusion). `out/i2_boxen.png`: Treated central box spans the gap.

**Scores:** Basic 34/40, Specialized 48/60, Total 82. Assertions 2/4.

## Input 3 - Edge

**Prompt:** "Violin of gene X per cluster for single-cell data (many zeros), 5 to 300 cells per cluster, with Sheather-Jones bandwidth; add N; use a notch."

Code: `run/i3_edge.R`, `run/i3b_bw.R` (synthetic, seeds set).

```
bw.nrd0 0.7916  bw.nrd 0.9323  ratio 1.1778
[FAIL] SKILL claim 'nrd (Scott) oversmooths less than Silverman(nrd0)' is TRUE
SKILL violin recipe geom_violin(trim=FALSE, bw='SJ') on zero-inflated clusters ... warnings: Computation failed in `stat_ydensity()`.
   Caused by error in `stats::bw.SJ()`: ! sample is too sparse to find TD
   bw.SJ(C1: n=300) -> 0.0325   C2 n=250 -> 0.1075   C3 n=5 -> 0.7497   C4 (all zeros, n=40) -> ERROR
default violin same data: error = none
[FAIL] trim=FALSE keeps violin within physically possible range (>=0)  min drawn y = -1.628
violin at n=5/3/1: 'Groups with fewer than two datapoints have been dropped.'
notch=TRUE n=8: "Notch went outside hinges" [PASS]; notch limits = median +/- 1.58*IQR/sqrt(n) [PASS]
stat_summary(geom='text', fun.data=function(x) data.frame(label=...)) -> `geom_text()` requires the following missing aesthetics: y   [FAIL]
tick-label N 'Control (n=12)', 'Drug (n=20)' [PASS]
Simulation (300 draws x 12 cells): SJ better than nrd0 in 10, equal 2, worse 0; nrd at least as good in 1/12
```

Opened `out/i3_sc_sj.png`: the panel is empty (axes only) although ggsave exited 0. `out/i3_sc_default.png`: all four clusters drawn (C4 flat line at 0). Without the all-zero cluster SJ works (`out/i3b_sc_sj_no_allzero.png`, 3 groups drawn); on 90% ties bw.SJ still errors.

**Scores:** Basic 26/40, Specialized 33/60, Total 59. Assertions 2/5.

## Input 4 - Variant B (REAL data)

**Prompt:** "Split violin of the most B-vs-T discriminating probe per disease stage, B and T on the two halves, SJ bandwidth, n per group on the axis."

Data: Bioconductor `ALL` 1.48.0 (Chiaretti 2004), probe 38319_at (|t| = 34.4). Cells: B 19/36/23/12, T 1/15/10/2 (stages 1-4). Code: `run/i4_real_split.R`, `run/i4c_side.R`.

```
[PASS] box medians equal per-(stage,lineage) data medians 4.54,4.61,4.71,4.9,8.58,9.36,9.64,9.9
[PASS] 8 boxes drawn ; N per cell in tick labels equals table
Warning: Groups with fewer than two datapoints have been dropped.   (T stage 1, n=1)
with stage-2 B removed: violin group ids 1,3,4,5,6,7 ; halves drawn (odd = left): B left at stage 1, B right / T left at stages 2-4
[FAIL] T (orange) is always drawn on the right half, also when the paired B is missing
```

Opened `out/i4_split_n.png` (all cells, correct tick labels "Stage 2 (B n=36, T n=15)") and `out/i4c_side_gg4.png` / `out/i4_split_missingB.png`: B jumps from the left of the centre line at stage 1 to the right at stages 2-4 while its box stays on the left; T is drawn on the left. The half is chosen by group-id parity in introdataviz, so an empty cell shifts every later cluster. A T n=2 cell still gets a KDE violin, against the Skill's own N rule.

**Scores:** Basic 28/40, Specialized 42/60, Total 70. Assertions 2/5.

## Input 5 - Stress: shipped example

**Prompt:** "Run the shipped raincloud_phd.R and give me the 89 mm PDF."

Code: `run/i5_example.R`, `run/i5_pdf.py`, `run/i5c_trim.R`.

```
(1) as shipped -> no applicable method for 'count' applied to an object of class "function"     (df is stats::df)
ggplot2 4.0.3 with prelude -> ggsave: argument "layout" is missing ; raincloud.pdf left at 1,031 bytes, no fonts (run/out/i5/raincloud_gg4_FAILED.pdf)
ggplot2 3.5.2 with prelude -> ran ; raincloud.pdf 34,209 B, MediaBox 252 x 198 pt = 88.90 x 69.85 mm, 1 TrueType, 0 Type3   [PASS]
p_small x labels: Ctrl (n=80) | Low (n=80) | High (n=80)   over 15 points per group           [FAIL]
LV M = medians (2.79, 5.06, 3.84) ; F fourths within 0.4% ; k=5 -> 5 levels per group          [PASS]
split-violin box medians = per-cell medians                                                     [PASS]
High (lognormal, min 4.4): raincloud half-violin y-range -0.98 .. 43.75 (trim=FALSE, bw='SJ')
```

Opened `out/i5/p_small.png` (labels n=80 under 15 dots each) and `out/i5/p_raincloud.png` (three correctly coloured rainclouds; the High violin runs below 0 and out to 44 with an SJ tail wiggle; no n shown).

**Scores:** Basic 24/40, Specialized 34/60, Total 58. Assertions 2/5.

## Veto gates

Skill veto PASS (stability, contract, determinism, security). Research veto PASS: no fabricated numbers (all five citations verified as real), no practice-boundary content, no principled fallacy, code parses and runs on a working stack. Noted but not vetoed: the raincloud block fails on current ggplot2 and there is a working substitute.

## Recommendations (P0: none)

- P1 gghalves (headline raincloud) broken on ggplot2 4.x and archived; add a ggdist raincloud (verified) and a version ceiling.
- P1 `bw='SJ'` blanks the entire violin panel on tied / all-zero data, the single-cell case the usage guide names.
- P1 Split violin swaps sides when a cluster x condition cell is empty; boxes end up on the wrong half; n < 30 rule not enforced.
- P1 Shipped example not standalone; N labels from the wrong frame; leaves a blank PDF on failure.
- P2 nrd/Scott sentence wrong; N-label `stat_summary` snippet errors; `trim=FALSE` on bounded data; Python bandwidth `scott` oversmooths; inconsistent N thresholds; deprecations and unseeded jitter; usage-guide duplicates SKILL.md.

Scripts: everything in `run/` (see `run_all.sh`).
