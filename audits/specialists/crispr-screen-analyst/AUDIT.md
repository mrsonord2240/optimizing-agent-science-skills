# Audit verdict — crispr-screen-analyst (2026-09-16)

Verdict stage only. Scores, deployability, vetoes and P0/P1s below are taken from each Skill's
`eval_report_*_result.json`; surprising items were cross-checked against the corresponding
`eval_viewer_*.md`. Nothing was re-run or re-scored.

## Audited Skills

| # | Skill ID | Role | Category | Mode | N | exec k/N | static | dyn. avg | final | grade | veto | top P1/P0 |
| - | --- | --- | --- | --- | - | --- | --- | --- | --- | --- | --- | --- |
| 1 | bio-crispr-screens-library-design | core — framing/design | Protocol Design | D | 7 | 5/7 | 33.2 | 47.8 | 81 | Limited Release | none | P1: no minimum-spacing/independence filter on candidate guides |
| 2 | bio-crispr-screens-screen-qc | core — QC/validation | Data Analysis | D | 7 | 5/7 | 31.2 | 54.6 | 86 | Production Ready | none | P1: CN-bias Spearman threshold misses focal-amplicon artifacts |
| 3 | bio-crispr-screens-mageck-analysis | core — central operation | Data Analysis | D | 7 | 5/7 | 36.0 | 51.5 | 88 | Limited Release | none | P1: MLE permutation-FDR undocumented-sensitive to `--permutation-round`/covariates |
| 4 | bio-crispr-screens-bagel-essentiality | core — central operation | Data Analysis | D | 5 | 5/5 | 29.2 | 45.4 | 75 | Limited Release | **Skill Veto (T3 Determinism) FAIL** → deployable false | P0: BAGEL2 non-deterministic, undisclosed; P0: `interpret_bagel()` flags 86.5% of genome as tumor-suppressor on a dropout screen |
| 5 | bio-crispr-screens-drugz-chemogenomic | core — central operation | Data Analysis | B | 5 | 5/5 | 30.0 | 42.4 | 72 | Beta Only | none fired, not deployable | P0: essentials-exclusion example silently excludes 0/684 genes (CEGv2.txt parsed wrong — no header skip, no tab split) |
| 6 | bio-crispr-screens-jacks-analysis | core — central operation | Data Analysis | D | 7 | 5/7 | 28.8 | 43.6 | 72 | Beta Only | none fired, not deployable | P0: shipped `analyze_results()` NameError (`output_prefix` undefined); P0: `efficacy_summary()` `KeyError: 'Gene'` — real grna file only has `sgrna, X1, X2` |
| 7 | bio-crispr-screens-copy-number-correction | core — CN-aware hit calling | Data Analysis | D | 7 | 3/7 | 30.0 | 43.4 | 73 | Beta Only | none fired, not deployable | P0: Chronos example unrunnable — wrong readcounts orientation; P0: decision tree wrongly claims Chronos works for one cell line + matched CN |
| 8 | bio-crispr-screens-hit-calling | core — cross-method reconciliation | Data Analysis | D | 7 | 5/7 | 29.2 | 48.8 | 78 | Limited Release | none | P1: BAGEL2 non-determinism unaddressed; P1: three different MAGeCK-FDR/BAGEL-BF threshold pairs across the Skill's own files |
| 9 | bio-workflows-crispr-screen-pipeline | core — end-to-end orchestration | Data Analysis | D | 7 | 4/7 | 30.4 | 45.2 | 76 | Limited Release | **Research Veto (M3 Methodological Ground) FAIL** → deployable false | P0: BAGEL2 non-determinism destabilizes the workflow's own Tier consensus; P0: shipped "Replicate Pearson" QC formula conflates replicate/non-replicate pairs (0.677 naive vs 0.789 true) |
| 10 | bio-crispr-screens-crispresso-editing | core — editing-outcome quantification | Data Analysis | A | 7 | 7/7 | 32.8 | 43.4 | 76 | Limited Release | **Research Veto (M4 Code Usability) FAIL** → deployable false | P0: `parse_crispresso()` crashes on real output (reads `READS_ALIGNED_PERCENTAGE`, a column that does not exist); P0: CRISPRessoPooled silently all-NA on realistic pilot-scale pools |
| 11 | bio-crispr-screens-batch-correction | supporting | Data Analysis | D | 7 | 6/7 | 31.2 | 47.2 | 78 | Limited Release | none | P1: `combat_correct()` crashes on its own "Critical"-covariate usage |
| 12 | bio-experimental-design-batch-design | supporting (reused) | Protocol Design | — | 5 | 5/5 | 32.4 | 49.9 | 82 | Limited Release | none | P1: SVA block fails on matrices with missing values |
| 13 | bio-pathway-go-enrichment | supporting (reused) | Data Analysis | — | 5 | 5/5 | 35.6 | 54.0 | 90 | Production Ready | none | none open |
| 14 | bio-pathway-gsea | supporting (reused) | Data Analysis | — | 7 | 7/7 | 36.4 | 54.0 | 90 | Limited Release | none | P1: `nPerm` accepted and silently downgrades the engine |
| 15 | bio-crispr-screens-base-editing-analysis | supporting — base-editing outcomes | Data Analysis | D | 7 | 6/7 | 26.0 | 28.2 | 54 | Reject | **Research Veto (M4 Code Usability) FAIL** → deployable false | P0×4: `filter_by_editing_efficiency()`, `deconvolute_bystander()`, `aggregate_variant_scores()` all crash (KeyError) on real CRISPResso2/MAGeCK output; `find_be_spacers()` misattributes target/bystander on reverse-strand spacers |
| 16 | bio-crispr-screens-prime-editing-screens | supporting — prime-editing | Data Analysis | D | 7 | 5/7 | 28.0 | 36.1 | 64.1 | Beta Only | **Research Veto (M4 Code Usability) FAIL** → deployable false | P0×3: pegRNA diagram has PBS/RTT in the wrong order (CRISPResso2 silently under-reports editing); `design_pegrna_pridict2.py` crashes and can emit PAM-overlapping PBS; PRIDICT2 batch CLI example broken, then writes an empty file once patched |

`exec k/N` counts inputs where generated code was actually run (reasoning-only, scope-boundary and
adversarial-refusal inputs that require no code are excluded from the denominator's numerator but
counted in N).

## Skills read but not chosen (from SELECTION.md)

- `bio-crispr-screens-combinatorial-screens` — no installable central tool, niche.
- `bio-crispr-screens-in-vivo-screens` — animal-model guidance only, nothing executable.
- `bio-crispr-screens-perturb-seq-analysis` — working tool stack, but belongs to `single-cell-transcriptomics-analyst`'s scope.
- `experimental-design/power-analysis`, `experimental-design/randomization-blocking` — unaudited, breadth control.
- `pathway-analysis/kegg-pathways`, `reactome-pathways`, `wikipathways`, `enrichment-visualization` — unaudited, breadth control.

## Verdict: NOT VIABLE

Fails **gate 3** and **gate 4**.

**Gate 3 (core Skills ≥ 85).** Of 10 Skills marked `core`, only 2 clear the floor: screen-qc (86,
pre-hit-calling QC) and mageck-analysis (88, single-tool hit calling). The candidate's central
step — copy-number-aware, cross-method hit calling (MAGeCK, BAGEL2, drugZ, JACKS) plus the added
editing-outcome operation — has no passing executor outside MAGeCK: bagel-essentiality (75, veto),
drugz-chemogenomic (72), jacks-analysis (72), copy-number-correction (73), hit-calling (78),
the end-to-end pipeline (76, veto) and crispresso-editing (76, veto) all fail. library-design (81)
also falls short.

**Gate 4 (end-to-end coverage).** With only 2 of 10 core Skills passing, there is no passing
framing/design Skill and the "central operation" is reduced to one tool of four, none of which are
copy-number-aware. That does not meet "at least three core Skills covering framing/design, the
domain's central operation, and validation/reporting" as designed.

### Two defects span several Skills

- **BAGEL2 unseeded non-determinism** — bagel-essentiality (Skill Veto T3 FAIL, P0), the
  orchestration pipeline (Research Veto M3 FAIL, P0: destabilizes the workflow's own Tier
  consensus), and hit-calling (P1: named in scope, still unaddressed). Fix: seed BAGEL2's
  bootstrap/BF calculation (or document run-to-run BF variance) in one place all three Skills cite.
- **Bundled parsers keyed to columns/format real tool output does not have** — crispresso-editing
  (`parse_crispresso()` reads `READS_ALIGNED_PERCENTAGE`, a column absent from the real
  CRISPResso2 mapping-statistics file, and mis-parses its key/value shape), base-editing-analysis
  (`filter_by_editing_efficiency()` assumes rows=Position/columns=base; the real
  `Quantification_window_nucleotide_percentage_table.txt` is the transpose; `deconvolute_bystander()`
  and `aggregate_variant_scores()` have the same class of KeyError), jacks-analysis
  (`efficacy_summary()` does `groupby('Gene')` against a real grna-results file whose only columns
  are `sgrna, X1, X2` — contradicting the Skill's own column table two sections earlier), and
  drugz-chemogenomic (the essentials-exclusion example parses `CEGv2.txt` with no header skip and
  no tab split, silently matching 0 of 684 genes). Fix: write one parser per real file format,
  verified against actual tool output, and stop hand-rolling column names from memory.

### Defects that would flip each failing core Skill

- **library-design (81→85+):** add a minimum-spacing/independence filter on candidate guides;
  resolve the SKILL.md vs usage-guide.md contradiction on Azimuth 2.0 usability.
- **bagel-essentiality (veto, 75):** seed/report BAGEL2 determinism (Skill Veto T3); fix or gate
  `interpret_bagel()`'s tumor-suppressor call so it doesn't fire on dropout-only screens.
- **drugz-chemogenomic (72):** fix the CEGv2.txt parser (see above, P0); document the
  `--half_window_size`-vs-guide-count relationship that currently crashes on small libraries.
- **jacks-analysis (72):** fix `analyze_results()`'s undefined `output_prefix`; fix
  `efficacy_summary()`'s `KeyError: 'Gene'` (see above, P0).
- **copy-number-correction (73):** fix the Chronos example's readcounts orientation; correct the
  decision tree's wrong claim that Chronos suits a single cell line with matched CN (or restore a
  working CRISPRcleanR path as the actual answer for that case).
- **hit-calling (78→85+):** address BAGEL2 non-determinism in the reconciliation logic; unify the
  three conflicting MAGeCK-FDR/BAGEL-BF threshold pairs across the Skill's own files; fix the
  Spearman rho audit prompt for the MAGeCK/BAGEL2 sign-scale inversion.
- **workflows-crispr-screen-pipeline (veto, 76):** fix the Replicate Pearson QC formula (P0, see
  above) and the BAGEL2-non-determinism propagation into Tier consensus (P0).
- **crispresso-editing (veto, 76):** fix `parse_crispresso()` (P0, see above); fix
  CRISPRessoPooled's silent all-NA return on realistic pilot-scale pools.

Open P1s (e.g. library-design's guide-spacing gap, batch-correction's `combat_correct()` crash,
gsea's `nPerm` silent downgrade) do not block viability by the brief's rule, but several sit close
enough to the 85 floor that fixing them alone (library-design, hit-calling) could flip a Skill.

## Execution

66 of 100 dynamic inputs across the 16 audited Skills ran real generated code (the rest were
scope-boundary, adversarial-refusal or reasoning-only inputs that require none). Real data used
where available: HAP1 TKOv3 (hart-lab/bagel), JACKS' own bundled Project Score dataset, and
CRISPResso2 2.3.4 via Docker against upstream test fixtures.

## Pending / blocked

Nothing pending — all 16 Skills named in SELECTION.md have finished reports. CRISPRcleanR (the
copy-number-correction Skill's own named primary tool) remains uninstallable on Windows
(VariantAnnotation pthread link failure); only its Chronos alternative path was exercised.
