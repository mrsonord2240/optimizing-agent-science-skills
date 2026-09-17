# Cross-reference — design, statistics, databases and the remainder (2026-09-17)

Slice: 72 published (non-bio) Skills not claimed by the other three agents. Read-only analysis; no Skill file was edited.

Framing per brief: Skill IDs never collide at install time. The risk is (a) ambiguous routing when a
Specialist loads both, and (b) a future Specialist bundling the weaker of two Skills that do overlapping
work. Every `duplicate`/`partial` verdict below says which one to bundle and why.

A structural pattern worth stating once instead of per-row: every published Skill here (author "AIPOCH",
source `github.com/aipoch/medical-research-skills`) is a prompt-engineered template — frontmatter,
workflow steps, "Input Validation" / "Error Handling" boilerplate repeated near-verbatim across the
corpus. The `mendelian-randomisation` and `adaptive-trial-simulator` skills claim an executable
`scripts/main.py`; the rest are pure protocol-writing/checklist prompts with no code. Every bioSkills
Skill compared below is a citation-grounded, versioned, method-specific execution skill (R/Python/CLI
code, decision trees, failure modes, primary literature). That asymmetry — planning prompt vs. executing
tool — is the dominant finding and recurs through almost every `partial` verdict.

## Tier 1 — full cross-reference

| Published Skill | bioSkills counterpart(s) | Verdict | Bundle | Reason |
|---|---|---|---|---|
| `mendelian-randomisation` | `bio-causal-genomics-mendelian-randomization` | **duplicate** | bio | bio covers the same 4 core estimators (IVW/Egger/weighted-median/weighted-mode) plus MR-RAPS, CAUSE, GSMR-HEIDI, MR-PRESSO, MVMR, MR-Clust, LCV, LHC-MR, MRlap, with a scenario decision tree and per-method citations; published executes only the 4-estimator core. |
| `qtl-colocalization-study-planner` | `bio-causal-genomics-colocalization-analysis` | **partial** | bio (execution) + published (scoping only) | Published never runs colocalization — it outputs a 4-tier study-design memo. bio runs coloc.abf/coloc.susie/HyPrColoc/SMR-HEIDI/eCAVIAR/PWCoCo/moloc with documented failure modes (PP.H3 inflation, LD mismatch, MHC/HLA breakage). |
| `mendelian-randomization-protocol-designer` | `bio-causal-genomics-mendelian-randomization` | **partial** | bio (execution) | Same planning-vs-execution split as above; this and the next two skills are internally near-duplicates of each other (same AIPOCH template family) before even reaching bio. |
| `two-sample-mr-exposure-screening-reference-grounded` | `bio-causal-genomics-mendelian-randomization` | **partial** | bio (execution) | Same pattern. |
| `bidirectional-multi-phenotype-mr-research-planner` | `bio-causal-genomics-mendelian-randomization`, `bio-causal-genomics-genetic-correlation` | **partial** | bio (execution) | Same pattern; bidirectional/multi-phenotype framing maps onto bio's genetic-correlation + MR skills used together. |
| `mr-scrna-research-planner` | `bio-causal-genomics-mendelian-randomization` | **partial** | bio (execution) | Same pattern; scRNA linkage is a planning framing bio doesn't template but doesn't need to — it composes with `single-cell/*` bioSkills directly. |
| `gwas-database` | *(no direct counterpart)* — thematically adjacent to `bio-population-genetics-association-testing` | **distinct** | published (for this function) | `gwas-database` queries the published NHGRI-EBI GWAS Catalog (a lookup tool); `bio-population-genetics-association-testing` *runs* a new GWAS (plink2/SAIGE/regenie/GEMMA/BOLT-LMM on genotypes). Different function, not competing. bioSkills has no GWAS-Catalog query tool — a real gap (see Gaps). |
| `clinicaltrials-database` | *(none)* | **distinct** | published | Live ClinicalTrials.gov API v2 client. No bioSkills folder touches trial-registry querying. Gap in bioSkills. |
| `experiment-design` | `bio-experimental-design-{randomization-blocking, batch-design, power-analysis, sample-size, multiple-testing}` | **partial** | bio, with a caveat | Published is a shallow, domain-general template (RCT/factorial/A-B/survey, closed-form power formulas only). bio is genomics-specific and far deeper, **but** its own `sample-size` sub-skill scored 67/Reject (vetoed) and `multiple-testing` scored 82/Beta-Only (not deployable) — see note below. |
| `randomization-gen` | `bio-experimental-design-randomization-blocking` | **partial** | both, layered | Published is a turnkey block/stratified sequence generator with a concrete output format (sealed list). bio supplies the design theory it lacks (experimental-unit choice, pseudoreplication, split-plot error strata) but has no equivalent "generate the list" entry point. Bundle bio first for correctness, `randomization-gen` for the concrete artifact. |
| `sample-size-basic` | `bio-experimental-design-sample-size` (score 67, **Reject, veto** — not deployable) | **duplicate in scope, but bio side is unusable** | published | Rare case where the bioSkill loses on deployability, not method. `sample-size-basic`'s closed-form t-test/chi-square/proportion formulas are the same territory `bio-experimental-design-sample-size` covers (biological replicate counts for genomics) — but that bioSkill is vetoed. For a Specialist needing *any* basic sample-size answer today, `sample-size-basic` is the only deployable option in either corpus, despite being the thinner tool. |
| `sample-size-and-power-planning-assistant` | `bio-clinical-biostatistics-power-and-sample-size` | **partial** | bio | Published explicitly refuses to output a number ("not a fake-precision calculator") and produces an assumption-audit memo instead. bio computes real numbers (Schoenfeld/Lakatos survival, TOST equivalence, FDA NI-margin M1/M2 framework, group-sequential) with citations and working code. For a Specialist that must deliver a defensible N, bundle bio; the published assistant's assumption-quality gate is a reasonable pre-flight check layered in front of it. |
| `confounder-and-bias-control-planner` | *(no dedicated counterpart)* | **distinct — real gap, fill favors published** | published | bioSkills has computational adjustment tools (`clinical-biostatistics/logistic-regression`, `subgroup-analysis`) that execute a control strategy once chosen, but nothing that classifies variable roles (confounder/mediator/collider/effect-modifier) or pressure-tests a protocol before execution. This is the most defensible non-overlap in the slice. |
| `epidemiology` | `bio-epidemiological-genomics/*` (pathogen surveillance, phylodynamics, transmission inference); conceptual overlap only with `bio-clinical-biostatistics/{effect-measures, logistic-regression, categorical-tests}` | **distinct** | published (for classic epi) | Published triggers on SIR/SEIR compartmental modeling, R0 from case counts, outbreak curves — none of which bioSkills covers. bio's "epidemiological-genomics" folder is pathogen *genomic* epidemiology (AMR calling, lineage assignment, transmission trees from sequences) — a different data source and method for a partly-overlapping concept (Re vs R0). Not competing skills. |
| `clinical-data-cleaner` | `bio-clinical-biostatistics-cdisc-data`, `bio-clinical-biostatistics-missing-data` | **duplicate, bio wins on correctness** | bio | Both claim SDTM domain validation and CDISC compliance for regulatory submission. bio is current to SDTM 2.0/SDTMIG 3.4, ADaM v1.3, Define-XML 2.1 (FDA-required since March 2023), Pinnacle21/CORE validation, `admiral` derivation. Published's default missing-value strategies are `mean/median/mode/forward/drop` — the exact naive approaches NRC 2010 Rec. 10 (cited by bio's own missing-data skill) says to reject. This is a genuine quality gap in the published Skill, not just a coverage gap. |
| `table-1-generator-advanced` | `bio-reporting-publication-tables` | **duplicate, bio wins on correctness** | bio | Published always computes a t-test/chi-square p-value column for Table 1. bio's skill explicitly documents this as a known anti-pattern for randomized trials (Senn 1994; CONSORT 2010 item 15 — a "significant" baseline p-value in a randomized trial is a Type-I error by construction) and recommends SMD instead. Same functional target, bio is methodologically correct where published is not. |
| `reporting-guideline-compliance-checker` | `bio-clinical-biostatistics-trial-reporting` | **partial** | both, different strengths | Published is a broad but shallow multi-guideline checker (CONSORT/STROBE/PRISMA/TRIPOD in one generic template). bio is deep but CONSORT/ICH E9(R1)-only, current to CONSORT 2025 + SPIRIT 2025 + FDA 2023 covariate-adjustment guidance, with the 5 ICH E9(R1) estimand strategies and executable MMRM/estimand code. Bundle bio for CONSORT/estimand-heavy work; keep published for STROBE/PRISMA/TRIPOD breadth bio doesn't have. |
| `reproducibility-check` | Mode A (Methods audit, pre-registration, FAIR): *no counterpart*. Mode B (code/environment sharing): partially `bio-reporting-{quarto-reports, rmarkdown-reports, jupyter-reports}` | **distinct (Mode A) / partial (Mode B)** | published (Mode A), bio (Mode B execution) | bioSkills has no Methods-completeness auditor, no FAIR/pre-registration guidance skill. It does have real parameterized, containerizable reproducible-report tooling (papermill, Quarto engines) that Mode B only gestures at in prose. |
| `validation-strategy-designer` | `bio-machine-learning-model-validation` (score 93, **Limited Release, deployable**) | **partial** | bio | Published is a non-executing protocol-stage memo (internal/external/temporal/functional validation tiers). bio is a deployable, leakage-aware execution skill (nested CV, group/temporal splits, calibration, decision-curve net benefit, TRIPOD+AI) — one of the few bioSkills in this cross-reference with a passing audit grade. Bundle bio for any Specialist that actually validates a model; published's tier-planning framing is a legitimate front-end, not a substitute. |
| `prognostic-biomarker-protocol-designer` | `bio-machine-learning-biomarker-discovery`, `bio-machine-learning-model-validation` | **partial** | bio (execution) + published (planning front-end, no bio equivalent) | bio's discovery skill (Boruta/mRMR/elastic-net/stability selection with leakage-safe pipelines) and validation skill do the actual work better than anything published offers computationally. But bioSkills has no "prognostic biomarker protocol" planning layer (endpoint family, follow-up horizon, time-scale framing) — that half of published is a genuine complement, not a duplicate. |
| `adaptive-trial-simulator` *(promoted from Tier 2 — see note)* | `bio-clinical-biostatistics-adaptive-designs` | **partial, bio wins decisively** | bio | Published is a generic Monte-Carlo script (group-sequential / adaptive-reestimate, O'Brien-Fleming default, promising-zone) with no regulatory citation and default parameters (effect size 0.3, sample size 200). bio covers 12+ adaptive-design families (blinded/unblinded SSR, RAR, seamless Phase 2/3, Bayesian platform trials) current to FDA 2019/2022, ICH E20 Step 2b/3 draft (2025-2026), and FDA's January 2026 Bayesian methodology draft, with per-method citations and `rpact`/`gsDesign` code. |

**Note on the promotion:** the brief listed `clinical-trial-protocol-designer` as a Tier 2 "expected distinct" family. `adaptive-trial-simulator` (one of its 7 Skills) turned out to have a strong, specific bioSkills counterpart (`bio-clinical-biostatistics-adaptive-designs`), so per the brief's own instruction it is promoted and treated above. The family's other 5 Skills (SOP writing, eligibility-criteria text, endpoint-definition text) remain Tier 2 — see below.

**Note on `sample-size`/`multiple-testing` veto status:** the brief flagged that `bio-experimental-design-sample-size` (score 67, Reject) and `bio-experimental-design-multiple-testing` (score 82, Beta Only, not deployable) are excluded from Specialists. Where `experiment-design` and `sample-size-basic` touch that ground, the published Skill is — despite being the thinner tool — the only *deployable* option today. This is the more useful finding than raw overlap: bioSkills' genomics sample-size and multiple-testing methodology is superior on paper but currently unshippable, so a Specialist assembled today has no choice but to lean on the published (weaker but working) Skill for that slice, or on `bio-clinical-biostatistics-power-and-sample-size` (deployable, no audit record, clinical-trial framing rather than genomics-replicate framing).

### Audit status of every bioSkill cited above

Only 4 of the ~15 bioSkills cited have an audit report under `F:\OpenScience\audits\`:
- `bio-experimental-design-batch-design` — score 87, grade **Production Ready**, deployable.
- `bio-experimental-design-multiple-testing` — score 82, grade **Beta Only**, **not deployable** (assertion pass rate below the Limited-Release floor).
- `bio-experimental-design-sample-size` — score 67, grade **Reject**, veto override, **not deployable**.
- `bio-machine-learning-model-validation` — score 93, grade **Limited Release**, deployable.

`bio-causal-genomics-mendelian-randomization`, `bio-causal-genomics-colocalization-analysis`,
`bio-causal-genomics-genetic-correlation`, `bio-experimental-design-{randomization-blocking, power-analysis}`,
`bio-population-genetics-association-testing`, `bio-clinical-biostatistics-{trial-reporting, missing-data,
power-and-sample-size, cdisc-data, adaptive-designs}`, `bio-reporting-publication-tables`, and
`bio-machine-learning-biomarker-discovery` have **no audit report anywhere in `F:\OpenScience\audits\`** —
their quality claims above rest on reading the Skill text itself (depth, citation density, working code),
not on a scored evaluation. Say so plainly rather than inferring a grade that doesn't exist.

The published (non-bio) Skills have no audit reports of any kind — there is no scoring pipeline for them
in this repo, so their quality assessment above is qualitative (template-boilerplate density, presence/
absence of executable code, correctness of embedded statistical claims like the Table 1 p-value issue).

## Tier 2 — confirmed distinct, grouped by specialist family

Confirmed by (a) bioSkills top-level folder listing (no `manuscript/`, `grant/`, `critical-appraisal/`,
`clinical-trial-protocol/`, `pharmacovigilance/` folder exists) and (b) targeted grep for
`FAERS|pharmacovigilance|adverse event report`, `IACUC|ARRIVE`, `clinicaltrials.gov|NCT ID` across every
bioSkills `SKILL.md` — zero or near-zero hits, none of them a real functional match.

| Specialist family | Skills (count) | Verdict |
|---|---|---|
| `manuscript-revision-specialist` | arxiv-preflight, author-response-builder, blind-review-sanitizer, claim-strength-calibrator, consistency-checker-across-manuscript, cover-letter-drafter, figure-reference-checker, journal-recommender, paper-sprint-review, rebuttal-letter-strategist, reference-integrity-checker, response-letter, response-tone-polisher, revision-strategy-planner (14) | **distinct** — bioSkills is a computational-analysis corpus with no manuscript-writing or journal-submission skills of any kind. |
| `critical-appraisal-specialist` | contradictory-findings-resolver, diagnostic-study-quality-assessment-quadas-2, figure-first-paper-reader, high-value-paper-screener, medical-research-literature-reader-pro, methods-reverse-engineer, paper-to-claim-verifier, rct-bias-assessment-rob2, result-reliability-checker, retraction-watcher, scientific-critical-thinking, study-design-identifier (12) | **distinct** — no paper-appraisal, risk-of-bias, or literature-reading skill exists in bioSkills; it operates on data/genotypes, not on published papers. |
| `research-grant-proposal-specialist` | aim-and-hypothesis-designer, feasibility-aware-study-planner, grant-budget-justification, grant-mock-reviewer, grant-proposal-assistant, grant-specific-aims-writer, novelty-vs-feasibility-assessor (7) | **distinct** — no grant-writing skill exists in bioSkills. |
| `clinical-trial-protocol-designer` (remainder, after `randomization-gen`/`clinicaltrials-database`/`adaptive-trial-simulator` promoted to Tier 1) | clinical-trial-protocol-skill, endpoint-definition-designer, inclusion-exclusion-criteria-builder, sop-writer, tooluniverse-clinical-trial-design (5) | **distinct** — protocol/SOP/eligibility-criteria text generation; bioSkills has no administrative trial-document skills. |
| `pharmacovigilance-signal-designer` (remainder, after `confounder-and-bias-control-planner` treated in Tier 1) | active-comparator-single-soc-faers-safety-comparison, faers-pharmacovigilance-disproportionality-research-planner, single-drug-faers-safety-profile-research-planner (3) | **distinct** — zero FAERS/pharmacovigilance hits anywhere in bioSkills. |
| `preclinical-validation-designer` (remainder, after `experiment-design`/`sample-size-basic` treated in Tier 1) | animal-and-cell-validation-planner, mechanism-to-validation-planner, methodology-extractor, translational-study-blueprint (4) | **distinct** — these are non-executing planning templates; bioSkills' closest material (CRISPR/omics execution skills) belongs to the other agents' assigned slice and answers a different question (how to run an assay, not how to plan a validation study). |
| `real-world-evidence-epidemiologist` (remainder, after `clinical-data-cleaner`/`epidemiology`/`table-1-generator-advanced` treated in Tier 1) | case-control-study-planner, clinical-cohort-protocol-designer, nhanes-clinical-retrospective-biomarker-research-planner, real-world-evidence-study-designer (4) | **distinct** — cohort/case-control study-design planning templates; already-covered Tier 1 themes (design, Table 1, data cleaning) are the closest bioSkills gets. |
| `tumor-immune-microenvironment-analyst` (remainder, after the 11 skipped execution Skills) | pcd-immune-oncology-research-planner, tumor-immune-infiltration-diagnostic-ml-research-planner (2) | **distinct** — these plan a study around methods (CIBERSORT, GSVA, etc.) that exist in bioSkills only as execution tools, already assigned to another agent's slice; the *planning* layer itself has no counterpart. |

## Gaps — themes one corpus covers and the other has nothing for

**Published covers, bioSkills has nothing:**
- Manuscript revision, peer-review response, cover letters, journal selection (14 Skills, `manuscript-revision-specialist`).
- Literature critical appraisal / risk-of-bias / retraction checking (12 Skills, `critical-appraisal-specialist`).
- Grant proposal writing (7 Skills, `research-grant-proposal-specialist`).
- Live ClinicalTrials.gov registry querying (`clinicaltrials-database`) — bioSkills' `database-access/*` never touches trial registries.
- GWAS Catalog (NHGRI-EBI) querying as a lookup service (`gwas-database`) — bioSkills runs its own GWAS but never queries the published-associations catalog.
- Protocol-stage confounder/bias taxonomy and variable-role classification (`confounder-and-bias-control-planner`) — bioSkills only executes an adjustment once one is chosen.
- FAERS pharmacovigilance signal design (3 Skills).
- Classic disease-transmission modeling — SIR/SEIR, R0 from case counts (`epidemiology`) — bioSkills' epidemiological-genomics folder is pathogen genomics (Re from sequence data), a different method entirely.
- Pre-registration / FAIR-data / open-science compliance auditing (`reproducibility-check` Mode B) — bioSkills has reproducible-report *tooling* (Quarto/R Markdown/Jupyter) but no compliance-audit skill.

**bioSkills covers, published has nothing (or only a weak/non-executing version):**
- Actual execution of Mendelian randomization (8+ estimators including MR-RAPS/CAUSE/MVMR/LHC-MR) — published only plans or runs the 4-estimator basic core.
- Actual colocalization execution (coloc.abf/susie/HyPrColoc/SMR-HEIDI/eCAVIAR) — published only plans it.
- CDISC SDTM/ADaM regulatory data handling current to 2024-2026 standards (Define-XML 2.1, Pinnacle21/CORE) — published's cleaner uses outdated naive imputation.
- ICH E9(R1) estimand framework and regulatory-grade missing-data sensitivity analysis (MMRM, reference-based MI, tipping-point) — published's compliance checker doesn't reach this depth.
- Leakage-aware model validation and biomarker feature-selection methodology with citations — published's designers describe validation tiers in prose without the machinery to execute them correctly.
- Adaptive trial design current to FDA 2019/2022 and ICH E20 2025-2026 drafts, 12+ design families — published's simulator is a generic, uncited Monte-Carlo script.
