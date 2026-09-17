# Cross-reference — bioSkills vs the published OpenScience Skills (2026-09-17)

Written for: Sam, deciding what to bundle in future Specialists and what to fix in already-published ones.

## Scope

561 bioSkills (`optimizing-agent-science-skills/skills/bioSkills`, export `f5ad8c5`) against the
**98 non-`bio-` Skill IDs** published in `mrsonord2240/openscience-specialists`. The marketplace also
ships 45 `bio-*` Skills already; those are the same corpus and are not cross-referenced against
themselves.

Four agents took a themed slice each, reading both `SKILL.md` files (and shipped `scripts/`) before
judging. Detail lives in `slice-pathway.md`, `slice-expression.md`, `slice-ml.md`, `slice-design.md`.
The headline defect claims below I re-verified myself at the call site; those are marked **[verified]**.

## The thing to understand first

Skill IDs differ on both sides (`gsea` vs `bio-pathway-gsea`), so **none of this causes an
install-time byte conflict**. This is not a repeat of today's proteomics problem. The real costs are:

1. **Routing ambiguity** — an agent holding both Skills has two plausible answers to one request.
2. **Bundling the weaker of two equivalents** into a future Specialist.

And the answer to "which is better" is genuinely per-pair. A consistent pattern runs through all four
slices: **the published Skills ship runnable, tested code; the bioSkills encode the statistical
guardrails.** Neither side wins outright.

## Verdicts

| slice | published Skills | duplicate | partial | distinct / no counterpart |
| --- | --- | --- | --- | --- |
| Pathway & enrichment | 4 | 1 | 3 | 0 |
| Expression & clustering | 8 | 1 | 5 | 2 |
| ML, survival & validation | 14 | 0 | 13 | 1 |
| Design, databases, remainder (Tier 1) | 21 | 4 | 11 | 6 |
| Manuscript / grant / peer-review (Tier 2) | 51 | 0 | 0 | 51 |
| **total** | **98** | **6** | **32** | **60** |

Only 6 strict duplicates out of 98. The two corpora are far more complementary than redundant.

## Defects found in already-published Skills, ranked

These are not overlap findings — they are things wrong in Skills we have shipped.

### 1. `gokegg-analysis` runs ORA with no background set **[verified]**
`scripts/functions.R` calls `enrichGO()` and `enrichKEGG()` with **no `universe` argument**, and the
string `universe` appears **zero times** anywhere in the Skill — SKILL.md, scripts, references. The
bioSkills counterparts mention it 21 and 22 times. clusterProfiler then silently defaults the
background to every annotated gene in the OrgDb, which inflates enrichment whenever the measured
background is narrower — i.e. every RNA-seq experiment. Nothing discloses this.
*Severity: real defect. Fix the Skill; bundle `bio-pathway-go-enrichment` (90) + `bio-pathway-kegg-pathways`.*

### 2. `batch-effect-correction` points users into the Nygaard failure mode **[verified]**
No cautions section anywhere in its 17 files. Its only mention of downstream testing,
`references/algorithm.md:109`, reads *"QC plots should be reviewed before downstream differential
expression or clustering analysis"* — which directs the reader toward running DE on the
ComBat-corrected matrix. Its scope clause excludes "differential expression without batch labels" but
says nothing about this. `bio-differential-expression-batch-correction` makes it the top section:
*"never run ComBat (or ComBat-seq, or removeBatchEffect, or SVA-subtract-then-test) and then run DE on
the corrected matrix"*, citing Nygaard, Rødland & Hovig 2016.
*Severity: real gap, actively misleading. Add the warning; keep the published Skill for its runnable code.*

### 3. `table-1-generator-advanced` always emits a significance test **[verified]**
`scripts/main.py` computes a t-test/ANOVA/chi-square p-value **unconditionally** whenever `--group` is
given, and there is **no CLI flag to suppress it** (only `--data`, `--group`, `--vars`, `--output`).
No CONSORT or Senn 1994 caution anywhere. Testing baseline balance is a Type-I error by construction
in a randomised trial.
*Severity: real defect. Make the column opt-in; the bio counterpart is the methodologically correct one.*

### 4. `clinical-data-cleaner` offers only single imputation, with the caveats filed away **[verified]**
`scripts/main.py` offers `mean`, `median` and `mode` imputation and nothing else. But the agent's
framing — "exactly what NRC 2010 Rec. 10 rejects" — is too harsh: the Skill *does* warn that
"Ignoring missing patterns → MNAR data treated as MCAR" (`references/common-patterns.md:261`) and
does say "Consider multiple imputation" (`references/troubleshooting.md:45`). The problem is
placement, not ignorance: both caveats sit in reference files while `common-patterns.md:73` tells the
reader to "Impute missing values with median" as a workflow step.
*Severity: weak default, correctly caveated in the wrong place. Move the caveat to the point of use.*

### Not a defect, despite looking like one
`univariate-multivariable-cox-regression` has no `cox.zph`/Schoenfeld check — but
`references/algorithm.md:134` **explicitly declares it out of scope** ("does not automatically test
proportional hazards assumptions") and line 129 lists PH appropriateness as a user-owned assumption.
That is an honest limitation, not a hidden fault. **[verified]** The bioSkill
(`bio-clinical-biostatistics-survival-analysis`, whose core teaching is "PH Almost Never Holds")
complements it rather than superseding it. Pair them; don't replace.

## Where the published Skill is the better bundle

Worth stating because it inverts the usual assumption:

- **GSVA / ssGSEA / immune infiltration** — `bio-pathway-gsea`'s per-sample section is thin and flagged
  as not installed in the reference environment. The published Skills ship full tested pipelines
  (limma differential step, heatmaps, correlation matrices).
- **Genomics sample size and multiple testing** — `bio-experimental-design-sample-size` scored 67
  (Reject, veto) and `bio-experimental-design-multiple-testing` is 82 but **not deployable**. The
  thinner published `sample-size-basic` / `experiment-design` are the only deployable option today.
- **`sample-group-sankey-plot`** — true duplicate of `bio-data-visualization-flow-and-transition-plots`
  (`ggalluvial` in both), and the published one ships a runnable CLI plus tests.

## Coverage gaps, both directions

**bioSkills has nothing for** — manuscript writing, peer review, grant writing (33 published Skills
with no counterpart at all); bulk-RNA-seq immune deconvolution (CIBERSORT/ESTIMATE have no bioSkills
equivalent — checked `immunoinformatics`, `single-cell`, `systems-biology`); consensus clustering.

**The published side has nothing for** — actual execution of Mendelian randomisation, colocalisation,
or CDISC/ADaM regulatory data handling. It carries planning prose around work that bioSkills actually
runs.

## Unprompted find: published-vs-published duplication

The sharpest routing problem is not between corpora, it is **inside one shipped Specialist**.
`gsva-analysis-and-visualization`, `immune-pathway-analysis` and `ssgsea-immune-infiltration-analysis`
are near-identical `GSVA::gsva()` wrappers differing only in which gene-set file is plugged in — three
Skills competing for one request inside `tumor-immune-microenvironment-analyst@1.0.0`.

Similarly, six published model Skills (LASSO, elastic-net, XGBoost, LightGBM, RF, SVM) each fit one
family with no held-out validation, leakage guard or batch-shortcut check. Two of them are **not**
redundant with bioSkills — LightGBM and SVM-RFE are only *named* in bioSkills, never implemented.

## Suggested actions

1. Fix `gokegg-analysis` (`universe=`), `batch-effect-correction` (Nygaard warning) and
   `table-1-generator-advanced` (opt-in p-value). All three are small, evidenced edits to Skills we own.
2. Move `clinical-data-cleaner`'s MNAR and multiple-imputation caveats out of the reference files and
   next to the imputation step itself.
3. Decide whether the three GSVA wrappers collapse into one Skill in a future
   `tumor-immune-microenvironment-analyst` version.
4. For future candidate selection, use the per-pair bundling column in the slice files rather than
   preferring bioSkills by default — for GSVA, sample-size and Sankey plots the published Skill wins.
5. Consider auditing the published non-bio Skills. None of the 98 has an audit report; every quality
   judgement above rests on reading the files, not on executed evidence.
