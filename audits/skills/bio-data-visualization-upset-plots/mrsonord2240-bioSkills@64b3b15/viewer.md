> **Audit record for `bio-data-visualization-upset-plots`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/upset-plots) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-data-visualization-upset-plots
Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/upset-plots` (unmodified upstream). Auditor stage: first audit.
Category: Data Analysis (3), execution mode A, complexity Moderate, N = 5. Scripts: `run/`. Raw logs: `run/out/*.log`. Figures: `run/out/*.png`.

Method note: a figure that ran is not a figure that is right. Every input below reads what was drawn (ComplexUpset: `ggplot_build` layer data of each patchwork panel; UpSetR: the grob trees of `Main_bar`/`Matrix`/`Sizes`; upsetplot: matplotlib patches, scatter offsets and colours) and compares it with a set-operation truth computed a second, independent way (R base `intersect/setdiff` and Python `set` algebra, which agreed on all 19 combinations of the planted data). 11 PNGs were opened with Read.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: ComplexUpset block 1 + planted 8 sets | 33 | 49 | 82 | 4/5 PASS | ✅ |
| 2 | Variant A: queries, annotations, sorts, filters | 27 | 38 | 65 | 3/5 PASS | ⚠️ |
| 3 | Variant B: Python upsetplot, block + shipped example | 24 | 36 | 60 | 2/5 PASS | ❌ |
| 4 | Stress: UpSetR, shipped R example, reconciliation | 29 | 44 | 73 | 2/5 PASS | ⚠️ |
| 5 | Scope: REAL Hallmark 10 sets, NA IDs, claims | 28 | 42 | 70 | 2/5 PASS | ⚠️ |

**Execution Average: 70.0 / 100** (L1 avg 28.2/40, L2 avg 41.8/60). **Assertion Pass Rate: 13/25 (52%).**
**Static: 71/100.** **Final = 71 x 0.4 + 70.0 x 0.6 = 70.4 -> Beta Only, not deployable.** No veto fired, no P0 open (Python route is a borderline M4, recorded as P1).

Floors: static 71 >= 70 ok; execution 70.0 < 75; L1 28.2 >= 28 ok; L2 41.8 < 42; assertions 52% < 80%. Limited Release is out of reach on three floors.

## Step 1 - Skill Veto

| | | |
|---|---|---|
| T1 Stability | PASS | R route is stable; Python route fails on the installed stack but a documented workaround exists (P1) |
| T2 Contract | PASS | `name`, `description`, `tool_type`, `primary_tool`, `license` present; `SKILL.md`, `usage-guide.md`, `examples/upset_gene_sets.R`, `examples/upset_python.py` all exist (shipped means present, no `references/` are pointed at) |
| T3 Determinism | PASS | Examples set seeds; drawn numbers identical on re-run |
| T4 Security | PASS | No eval, shell, network or credentials |

## Step 2 - Static score (25 criteria) = 71/100

Functional 8/12 (3,2,3), Reliability 7/12 (2,2,3), Performance/Context 5/8 (2,3), Agent usability 11/16 (3,2,3,3), Human usability 6/8 (4,2), Security 11/12, Maintainability 7/12 (2,3,2), Agent-specific 16/20 (4,3,3,4,2). Per-criterion reasons are in the JSON.

## Test data

- SYNTHETIC planted sets (`data/planted_sets.tsv`, `data/planted_truth.tsv`, made by `run/d0_make_planted.py`): 8 sets A..H, sizes 30 23 17 7 13 7 6 0; **D is a strict subset of A, H is empty**; 14 non-empty exclusive intersections (A 12, B 9, C 7, E 6, A-B 6, A-D 5, B-C 4, E-F 4, A-C 3, E-F-G 3, G 2, A-B-D 2, A-B-C 2, C-G 1); union 66.
- The Skill's own 4-set toy (every gene has a unique membership: 8 exclusive intersections, all of size 1).
- The shipped example's simulated 6 sets (seed 42; sizes 172 145 201 125 90 200; 56 non-empty exclusive intersections).
- REAL: MSigDB Hallmark, 10 immune/inflammatory sets via msigdbr 26.1.0 (`data/hallmark10_sets.tsv`; union 1,211; 137 non-empty exclusive intersections).

---

## Input 1 - Canonical: ComplexUpset block 1, verbatim, then on planted sets

**Prompt:** "Make an UpSet plot of overlap across my gene sets with ComplexUpset, sorted by intersection size, counts on the bars. (4 toy sets, then my 7 result sets plus one empty one.)"

**Code:** SKILL.md ComplexUpset block verbatim (`run/i1_canonical_complexupset.R`), same arguments on the planted table (`run/i1b_planted_cardinality.R`); helper `run/helpers.R::extract_cu`.

**What it printed (trimmed):**
```
drawn bars (4-set toy):  SetD 1 | SetC-SetD 1 | SetB-SetC 1 | SetB 1 | SetA-SetD 1 | SetA-SetC 1 | SetA-SetB-SetC-SetD 1 | SetA-SetB 1
A1..A6 all TRUE; distinct heights in this example: 1          <- the toy cannot show sorting
planted: heights 12 9 7 6 6 5 4 4 3 3 2 2 2 1 == truth sorted (B1-B7 TRUE)
set-size bars A30 B23 C17 D7 E13 F7 G6 == list lengths; D only drawn with A (B7 TRUE)
matrix rows: G,D,F,E,C,B,A     <- H (empty) is not there; warnings seen: only the ggplot2 linewidth deprecation
```
PNG `out/i1b_planted_card.png` opened: counts on top of bars, dot matrix and set-size bars consistent with the numbers above; default x label "group".

**Scores:** Basic 33/40, Specialized 49/60, Total 82/100.
**Assertions:** [PASS] toy bars == truth; [PASS] 14 planted bars == truth and cardinality-descending; [PASS] set sizes and D within A respected; [PASS] count labels == heights; [FAIL] empty set H is silently dropped (no message).

## Input 2 - Variant A: queries, attribute panels, sort and filter options

**Prompt:** "Highlight A-and-B in orange and A-B-D in blue, add a log2FC boxplot and a significant-fraction bar above the intersections, then show the same by degree instead of size, drop 1-set intersections."

**Code:** SKILL.md blocks 3 and 4 verbatim, then the same patterns on planted data with synthetic per-gene `log2FC` (seed 20260920) and `significant` (`run/i2_queries_sort_annotations.R`, `i2a_query_break.R`, `i2g_query_geometry.R`, `i5a/i5b` for the ggplot2 3.5.2 private build).

**What it printed (trimmed):**
```
[block3 verbatim, both queries] ggsave -> ERROR: Problem while setting up geom aesthetics. Error occurred in the 3rd layer ... Aesthetics must be either length 1 or the same as the data (1)
   (query 2 = SetA-SetC-SetD, whose exclusive size in the toy is 0; each query alone renders)
[block4 verbatim on df without log2FC/significant] -> ERROR: object 'log2FC' not found
C4 boxplot medians == independent per-intersection medians: TRUE (14 boxes)
C5 stacked-fraction 'significant' == independent proportion: TRUE (14 columns)
[degree, descending] degrees L->R: 3 3 3 2 2 2 2 2 2 1 1 1 1 1 ; [degree, ascending]: 1 1 1 1 1 2 2 2 2 2 2 3 3 3
[min_degree=2] 9/9  [min_size=4] 8/8  [n_intersections=5] top-5 TRUE  [intersections=list(AB,ABD,EF)] heights == truth TRUE
[mode='intersect'] A = 30 (= |A|), bars == INCLUSIVE truth TRUE, 1-set bars remain first
two queries A-B and A-B-D (planted): highlight layer widths 0.9 and 6.3      (ggplot2 4.0.3)
                                    same on ggplot2 3.5.2 with ComplexUpset 1.3.3 built against it
```
PNGs opened: `i2c_block4_annotations.png` (panels correct), `i2f_queries_planted.png` and `i5b_gg35_2q.png` (an orange rectangle spans the 9, 7, 6, 6, 5, 4, 4 bars and a blue one spans the last four; the highlighted numbers are unreadable), `i2a_block3_query1_only.png` (single query fine).

**Scores:** Basic 27/40, Specialized 38/60, Total 65/100.
**Assertions:** [PASS] annotation panels == independent statistics; [PASS] filters == filtered truth; [PASS] a single query highlights exactly the requested bar; [FAIL] two-query block renders a correct figure; [FAIL] the documented 1-set remedies (degree sort as written, mode='intersect') behave as described.

## Input 3 - Variant B: Python upsetplot

**Prompt:** "upsetplot.UpSet from a dict of contents, sort by cardinality, show counts; export PDF. Then run the shipped example."

**Code:** SKILL.md Python block verbatim (`run/i3_python_upsetplot.py`, `PYENV=venv-pd2` and main venv), root cause (`i3b_showcounts_rootcause.py`), planted-data checks (`i3c_python_planted.py`), shipped `upset_python.py` verbatim and a `show_counts=False` copy (`out/ex_py/`), metadata part (`i3d_example_metadata_part.py`).

**What it printed (trimmed):**
```
pandas 2.3.3 / numpy 2.5.3 / matplotlib 3.11.2
VERBATIM block: savefig FAILS -> TypeError only 0-dimensional arrays can be converted to Python scalars
float(np.array([1.0])) -> TypeError  (same message)
show_counts=True   savefig FAILS | show_counts=False savefig OK | show_counts='{:d}' FAILS | show_percentages=True FAILS
(main venv, pandas 3.0.6)  ValueError: Invalid RGBA argument: nan
shipped upset_python.py VERBATIM -> same TypeError, no PNG written; with show_counts=False: 2 PNGs written, then
AttributeError: 'DataFrame' object has no attribute 'to_frame'
show_counts=False, planted 8 sets: Q1 bars == truth TRUE; Q2 non-increasing TRUE; totals == sizes (H drawn as a 0 row) TRUE; Q5 D only with A TRUE
sort_by=degree -> degrees 1 1 1 1 1 2 2 2 2 2 2 3 3 3 (within a degree not size-sorted); -degree -> 3..1
min_subset_size=4 8 cols, max_subset_rank=5 5 cols, min_degree=2 9, max_degree=1 5: all heights == truth
[intersection_plot_elements=3] 14 columns still drawn; bar panel height 0.183 vs 0.496 at 15  -> it is a height
[style_subsets(present=[A,B])] orange: (A,B) (A,B,D) (A,B,C);  with absent=[rest]: (A,B) only
[duplicates in A] from_contents raises ValueError 'Got duplicate ids in a category'
from_memberships == truth TRUE; from_indicators == truth TRUE
```
PNGs `out/ex_py/upset_basic.png` (an empty stray axes with ticks 0..1 is drawn over the left half) and `upset_customized.png` (all 31 intersections drawn although the comment says `intersection_plot_elements=15` is the max) opened.

**Scores:** Basic 24/40, Specialized 36/60, Total 60/100.
**Assertions:** [FAIL] Skill block runs verbatim; [FAIL] shipped example runs to completion; [PASS] with `show_counts=False` all bars, totals, orders and filters == truth; [PASS] constructors and duplicate handling; [FAIL] `style_subsets(present=...)` highlights only the specific intersection.

## Input 4 - Stress: UpSetR, shipped R example, reconciliation

**Prompt:** "Migrate this UpSetR figure to ComplexUpset and make sure both give the same counts; my list has 7 sets and some elements are repeated."

**Code:** `run/i4_upsetr_and_reconcile.R` (namespaced `UpSetR::upset` / `ComplexUpset::upset`), shipped `upset_gene_sets.R` (run verbatim in `out/ex_R/`, three PDFs), grob extraction helpers in `run/helpers.R`.

**What it printed (trimmed):**
```
[SKILL UpSetR block, 4 sets] 8 columns, U1..U3 TRUE
[planted 7 sets, Skill's nsets = 4] rows drawn: A,B,C,E ; heights 17 13 9 8 8 4 3 2 ; sum 64 vs union 66  (truth A-only = 12)
[planted 7 sets, nsets=7] 14 columns == truth (12 9 7 6 6 5 4 4 3 3 2 2 2 1)
[fromList with an empty set H] rows drawn: A,B,C,E,F,D,G
[shipped example] sizes Treatment_vs_Control=172 Timepoint_6h=145 Timepoint_24h=201 Drug_A=125 Drug_B=90 Combined_Treatment=200
  basic (40 of 56 possible): U1-U3 TRUE ; customized (30): U1-U3 TRUE
[queries] highlighted: col1 Combined_Treatment 47 (#E64B35); col12 Timepoint_6h-Timepoint_24h 12 (#4DBBD5); nothing else
[UpSetR vs ComplexUpset, shipped 6 sets, 40 intersections] common combos agree TRUE; 4 combos only in one (ties at the rank-40 cut)
[duplicates: 6 in A, 3 in B] UpSetR bars == de-duplicated truth TRUE ; ComplexUpset via %in% TRUE   <- no inflation
```
Loading ComplexUpset after UpSetR makes the Skill's UpSetR block fail: `unused arguments (nsets = 4, nintersects = 20, order.by = "freq", ...)`. PNGs `i4c_example_queries.png` (47 red, 12 blue, legend at bottom) and `i4b_upsetr_nsets4_on7.png` (only rows A,B,C,E; 17 on the first bar) opened.

**Scores:** Basic 29/40, Specialized 44/60, Total 73/100.
**Assertions:** [PASS] shipped R example runs, three PDFs 17,127 / 14,414 / 17,213 B; [PASS] every UpSetR bar and query highlight == truth; [FAIL] `nsets = 4` is safe to reuse on more than 4 sets; [FAIL] duplicates inflate `fromList` counts; [FAIL] empty set shown or reported.

## Input 5 - Scope boundary: real Hallmark sets, identifier hygiene, the Skill's claims

**Prompt:** "Compare 10 Hallmark inflammation/immune gene sets. Is the plot going to be 1,023 columns? Also some of my lists contain NA and empty strings."

**Code:** `run/i5_real_hallmark_scale.R` (REAL msigdbr data), `i5c_python_hallmark.py`, `v5_pkgdates.R`, `i6_pdf_fonts.py`.

**What it printed (trimmed):**
```
hallmark sizes 200 200 87 200 97 200 200 199 161 200 ; union 1211 ; possible 2^10-1 = 1023 ; non-empty exclusive intersections: 137
ComplexUpset n_intersections=20: heights 144 135 132 106 91 90 87 56 39 25 16 9 9 9 8 7 7 7 6 6 == truth top-20; sets sizes right; 0.8 s
UpSetR nintersects=20: identical 20 values ; upsetplot max_subset_rank=20: same values (+ one extra 6 from a rank tie, 21 bars)
n_intersections=Inf: 137 columns, 0.5 s
[NA and '' in the lists] 6 elements counted (1 NA row, 1 blank row); bars S1-S2:3 S1-S3:2 S2-S3:1 in ComplexUpset and UpSetR (true genes: S1&S2 share TP53 only -> 1)
ComplexUpset 1.3.3  Packaged: 2021-12-10  (installed from CRAN and rebuilt from source today);  UpSetR 1.4.0  Packaged: 2019-05-09
matplotlib default pdf.fonttype = 3 ; Skill code never sets 42 or cairo_pdf ; R example uses pdf()
```
PNG `i5_hallmark10_top20.png` opened: the first eight bars are single-set (144 P53 ... 56), the real multi-set overlaps are 39 (IFN-g with IFN-a) and below.

**Scores:** Basic 28/40, Specialized 42/60, Total 70/100.
**Assertions:** [PASS] three implementations agree with truth on real data; [PASS] single-set exclusives dominate; [FAIL] 10 sets with `n_intersections=Inf` gives 1,023 columns; [FAIL] NA/blank IDs do not create false overlaps; [FAIL] maintenance and ggplot2 4.0 claims hold.

---

## Code usability (Research Veto M4) evidence

R route: the ComplexUpset block, sorting, filters, annotations (columns present), UpSetR block and `upset_gene_sets.R` ran and were asserted correct. Python route: syntax parses, imports exist (`from_contents, UpSet, plot`), but the runtime fails on numpy 2.5.3 / pandas 3 and the example has the `to_frame()` bug (P1). Verdict: PASS with a note (see JSON).

## Optimization Recommendations

- **[P1] Python upsetplot route does not run as shipped** (Input 3): `show_counts=True` fails on numpy 2.5.3, pandas 3 fails earlier, the example calls `data.to_frame()`.
- **[P1] Query highlighting breaks and the Skill blames the wrong cause** (Input 2): two non-adjacent queries draw a 6.3-wide bar on ggplot2 4.0.3 and 3.5.2; the empty-intersection query in block 3 crashes render; block 4 needs columns that df lacks.
- **[P1] Silent data-loss patterns not warned about** (Inputs 1, 4, 5): `nsets = 4` on more sets, empty sets, NA and blank IDs.
- **[P1] Several stated behaviours are false or unreproduced** (Inputs 2 to 5): duplicates inflating `fromList`, ComplexUpset "active through 2025-07", ggplot2 4.0 breaking `upset()`, `mode='intersect'` as a 1-set fix, degree sort with 'descending', `style_subsets(present=)`, `intersection_plot_elements`, 1,023 columns.
- **[P2] Toy example cannot show anything** (all bars 1; second query target empty).
- **[P2] Package masking, stray axes, x label 'group', export claims (cairo_pdf/Type-42) not implemented.**
- **[P2] SKILL.md and usage-guide.md duplicate the same tips.**

## Not verified

Medians of the repaired `add_catplot` box plot (Python); `sanbomics`-style third-party tools are not part of this Skill; ComplexUpset behaviour on numpy/pandas versions other than the audit stack; the `{'True':..}` fill mapping legend in block 4 was only inspected visually.
