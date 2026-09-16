# `untargeted-metabolomics-analyst` -- audit record (2026-09-16)

**Verdict: NOT VIABLE.** Fails gate 3 (core Skills Production Ready) and gate 4 (end-to-end
coverage). Four of the five core Skills that make up the central LC-MS pipeline are not
deployable; only metabolite annotation clears the bar.

## Audited Skills

| Skill ID | Role | Category | Mode | N | Executed | Static | Exec avg | Final | Grade | Veto | Top open P0/P1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `bio-metabolomics-xcms-preprocessing` | core -- entry | Data Analysis | A | 7 | 4/7 | 95 | 86.7 | **90** | Beta Only | PASS | P1: 79.3% assertion pass rate caps grade at Beta Only despite a 90 raw score |
| `bio-metabolomics-normalization-qc` | core -- QC/drift/normalization | Data Analysis | A | 7 | 7/7 | 87 | 86.6 | **87** | Production Ready (nominal) | **FAIL** (research veto, methodological ground) | P0: QRILC imputation on non-log intensities silently returns negative (impossible) values |
| `bio-metabolomics-metabolite-annotation` | core -- annotation | Data Analysis | D | 5 | 4/5 | 93 | 81.6 | **86** | Limited Release | PASS | P1: Common Errors table misdescribes the missing-precursor_mz failure |
| `bio-metabolomics-statistical-analysis` | core -- statistics | Data Analysis | A | 7 | 5/7 | 78 | 88.0 | **84** | Limited Release (nominal) | **FAIL** (skill veto, stability) | P0: OPLS-DA (ropls) silently returns an empty, unusable model in ~40% of runs |
| `bio-metabolomics-pathway-mapping` | core -- pathway, terminal step | Data Analysis | A | 5 | 4/5 | 80 | 77.0 | **78** | Beta Only | PASS | P0 x2: documented background-correction ORA path is unrunnable; MetaboAnalystR silently sends compound lists to a remote API, undisclosed |
| `bio-metabolomics-msdial-preprocessing` | supporting -- alternate preprocessing (DIA/GC-MS) | Data Analysis | D | 5 | 4/5 | 76 | 73.2 | **74** | Beta Only | PASS | P1: documented MsdialConsoleApp `lcmsdda`/`lcmsdia` commands do not exist |
| `bio-metabolomics-lipidomics` | supporting -- lipidomics branch | Data Analysis | A | 7 | 3/7 | 92 | 84.1 | **87** | Limited Release | PASS | P1: Goslin honest-downgrade pattern crashes on sum-composition/ether names |
| `bio-workflows-metabolomics-pipeline` | supporting -- orchestration | Data Analysis | D | 7 | 3/7 | 78 | 70.7 | **74** | Beta Only | PASS | P1: Stage2->Stage4 hand-off crashes on real multi-batch data (imputation is a comment, not code) |
| `bio-experimental-design-batch-design` (reused) | supporting -- framing/design | Protocol Design | A | 5 | 5/5 | 81 | 83.2 | **82** | Limited Release | PASS | P1: SVA block fails on matrices with missing values |

Nine Skills, 55 inputs, 39 executed (71%; execution counts for the six reports that record
per-input evidence only in free-text notes rather than a structured `executed` field were read
from those notes). Only three Skills pass gate 2 outright (deployable, no veto, no open P0,
score >= 75): `metabolite-annotation` (86), `lipidomics` (87), and the reused `batch-design` (82).

## Verdict against the gates

- **Gate 2 -- every bundled Skill audited and deployable.** Fails for 6 of 9 Skills.
  `normalization-qc` and `statistical-analysis` both fire a veto (research veto /
  methodological-ground on the former, skill veto / stability on the latter), forcing
  `deployable: false` regardless of raw score. `xcms-preprocessing` scores 90 but its grade is
  capped at Beta Only by a 79.3% assertion pass rate, which also forces `deployable: false`.
  `pathway-mapping` (78), `msdial-preprocessing` (74) and `workflows-metabolomics-pipeline` (74)
  are Beta Only with open P0s. Only `metabolite-annotation`, `lipidomics` and `batch-design` pass.
- **Gate 3 -- core Skills Production Ready (>= 85).** Fails. Of the five Skills marked `core`,
  only `metabolite-annotation` (86) clears 85. `xcms-preprocessing` (90 raw, Beta Only/not
  deployable), `normalization-qc` (87 raw, veto FAIL), `statistical-analysis` (84, veto FAIL) and
  `pathway-mapping` (78) do not. The central pipeline's entry, QC/normalization, statistics and
  pathway-mapping steps are all unusable as audited; only the annotation step is solid.
- **Gate 4 -- end-to-end coverage.** Fails as a consequence of gate 3. A single passing core Skill
  (annotation only) cannot cover framing/design, the central operation, and validation/reporting.
  Framing is covered only by a reused *supporting* Skill (`batch-design`), which gate 4 explicitly
  says may not stand in for a missing core step.
- **Gate 7 -- research scope.** Pass across all nine reports. Every `practice_boundaries` check
  passed; adversarial patient-level requests (statistical-analysis Input 6, lipidomics Input 7,
  pathway-mapping Input 5) were correctly declined and redirected.
- **Gate 8 -- shipped means present.** No report flagged a missing primary script or reference set
  as a P0; this appears satisfied on the evidence in hand, but was not independently re-verified
  file-by-file at the verdict stage.

## What would flip the verdict

The core pipeline needs real fixes, not re-scoring, at four points:

1. `bio-metabolomics-normalization-qc` -- stop `impute.QRILC` from being run on raw (non-log)
   intensities per the Skill's own documented pipeline order (step 5 imputation before step 7
   log/glog transform), or add a floor/warning so it cannot silently emit negative intensities.
   This alone fired the research veto.
2. `bio-metabolomics-statistical-analysis` -- fix or guard the ~40% silent empty-model failure in
   the Skill's own bundled OPLS-DA (ropls) example; this fired the skill veto (operational
   stability).
3. `bio-metabolomics-xcms-preprocessing` -- raise the assertion pass rate above whatever floor
   caps it at Beta Only (currently 79.3%); no single defect is vetoed, so this is a documentation/
   completeness gap (see the P1s in `eval_report_bio-metabolomics-xcms-preprocessing_result.json`).
4. `bio-metabolomics-pathway-mapping` -- make the documented background-corrected ORA path
   actually run, and disclose (or route around) MetaboAnalystR's undisclosed remote API call to
   fix its two open P0s.

Only after those four clear their respective bars would gate 3 (>= 85 on all five core Skills) and
gate 4 (three-plus core Skills covering entry through terminal step) have a chance of passing.

## Skills read but not chosen

See `SELECTION.md` for the full list and reasoning; summary: `bio-metabolomics-isotope-tracing`
and `bio-metabolomics-targeted-analysis` are supporting-only per `CANDIDATES.md` scope; the six
`bio-pathway-*` gene-list Skills operate on Entrez/ENSEMBL/SYMBOL identifiers, not metabolites, and
are out of scope; `bio-experimental-design-sample-size` (veto fired) and
`bio-experimental-design-multiple-testing` (not deployable) are excluded per the brief;
`bio-experimental-design-power-analysis` targets count-model (RNA-seq-style) data, not continuous
LC-MS intensities; `bio-experimental-design-randomization-blocking` is redundant with the more
specific `batch-design`.

Reports live in `F:\OpenScience\audits\<skill-id>\`.
