# `untargeted-metabolomics-analyst` — audit record (2026-09-16)

**Verdict: VIABLE.** All nine bundled Skills are deployable, every core Skill clears 85, and
every supporting Skill clears 75. No veto gate fired anywhere and no P0 recommendation is open in
any of the nine post-fix reports.

This supersedes the 2026-09-16 morning record, which read NOT VIABLE (gates 3 and 4 failed: four
of five core Skills were not deployable). All nine Skills named in that record were fixed in
Sam's fork and re-audited; this record reflects those post-fix reports, not the earlier ones.

Upstream for this release: the fork `mrsonord2240/bioSkills-Improved` (GitHub redirects the old
name `mrsonord2240/bioSkills`), commit `9d31109`, MIT. The nine post-fix reports cite
`mrsonord2240/bioSkills@6847328` as their own `source` rather than `9d31109`, which is the later
commit `spec.json` names. **Gate 6 holds anyway, and this was checked rather than assumed:**
`9d31109` is the merge of a third-round fix that touches only
`crispr-screens/copy-number-correction`, a Skill this candidate does not bundle. `git diff 6847328
9d31109 -- <path>` is empty for every Skill listed below, so the content audited and the content
`9d31109` ships are byte-identical. Verified 2026-09-16 against the clone at
`F:/OpenScience/external/mrsonord2240__bioSkills`.

---

## Audited Skills

| Skill ID | Role | Category | Mode | N | Executed k/N | Static | Exec avg | Final | Grade | Veto | Top open P1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `bio-metabolomics-xcms-preprocessing` | core — entry, feature extraction | Data Analysis | A | 9 | 2/9 | 97 | 88.6 | **92** | ⭐ Production Ready | PASS | none open (top P2: MatchedFilterParam low-res/quadrupole path has no worked code example) |
| `bio-metabolomics-normalization-qc` | core — QC/drift correction/normalization | Data Analysis | A | 9 | 9/9 | 92 | 92.0 | **92** | ⭐ Production Ready | PASS | none open (top P2: permutation-test guardrail still trips at its nominal FP rate on clean data) |
| `bio-metabolomics-metabolite-annotation` | core — annotation, MSI confidence | Data Analysis | D | 7 | 6/7 | 98 | 92.4 | **95** | ⭐ Production Ready | PASS | none open (top P2: inline comment misplaces where the precursor_mz AssertionError fires) |
| `bio-metabolomics-statistical-analysis` | core — statistics | Data Analysis | A | 9 | 9/9* | 97 | 94.6 | **96** | ⭐ Production Ready | PASS | none open (top P2: Pareto-vs-UV VIP robustness sub-check not independently reconfirmed) |
| `bio-metabolomics-pathway-mapping` | core — pathway mapping, terminal step | Data Analysis | A | 7 | 6/7 | 93 | 92.0 | **92** | ⭐ Production Ready | PASS | **P1**: reference-library downloads (`SetKEGG.PathLib`/`CrossReferencing`/`Setup.KEGGReferenceMetabolome`) are an undisclosed network dependency |
| `bio-metabolomics-msdial-preprocessing` | supporting — alternate preprocessing (DIA/GC-MS) | Data Analysis | D | 7 | 6/7 | 92 | 90.7 | **91** | ✅ Limited Release (floor-downgraded from Production Ready) | PASS | **P1**: malformed `Key=Value` param-file syntax is silently dropped, not rejected — exit 0, no warning |
| `bio-metabolomics-lipidomics` | supporting — lipidomics branch | Data Analysis | A | 9 | 6/9 | 96 | 90.0 | **92** | ⭐ Production Ready | PASS | none open (top P2: istd-coverage guard is `table()`-based and silently misses `Class=NA` rows) |
| `bio-workflows-metabolomics-pipeline` | supporting — orchestration | Data Analysis | D | 9 | 7/9 | 91 | 92.0 | **92** | ⭐ Production Ready | PASS | none open (top P2: MS-DIAL alternate entry point still has zero glue code) |
| `bio-experimental-design-batch-design` (reused) | supporting — framing/design | Protocol Design | A | 7 | 7/7 | 87 | 86.6 | **87** | ⭐ Production Ready | PASS | none open (top P2: bridge-channel block doesn't inherit the primary block's soft imbalance warning) |

\* `bio-metabolomics-statistical-analysis`'s own report marks all 9 inputs `executed: true`,
including two (6, 7) that are Mode A reasoning-only responses with no new code — its own
convention, different from `xcms-preprocessing`'s and `msdial-preprocessing`'s reports, which mark
reasoning-only inputs `executed: false`. Read literally that report's real-code count is 7/9, not
9/9; both figures are given here for transparency rather than silently picking one.

Nine Skills, 73 inputs, 58 executed by each report's own count (79%; three reports — `xcms-
preprocessing`, `lipidomics`, `bio-workflows-metabolomics-pipeline` — mix real code execution with
same-day-prior-run corroboration or pure reasoning-only inputs for the non-code Mode A cases;
see each report's per-input `execution_note`).

## Arithmetic check (per this dispatch's instruction)

For every one of the nine reports, the per-input `assertions_passed`/`assertions_total` were
summed by hand and checked against `dynamic_score.assertion_pass_rate`:

| Skill | Summed passed/total | Report's stated `assertion_pass_rate` | Match |
| --- | --- | --- | --- |
| `xcms-preprocessing` | 34/37 | 34/37 | yes |
| `normalization-qc` | 38/39 | 38/39 | yes |
| `metabolite-annotation` | 23/24 | 23/24 | yes |
| `statistical-analysis` | 36/38 | 36/38 | yes |
| `pathway-mapping` | 33/34 | 33/34 | yes |
| `msdial-preprocessing` | 25/29 | 25/29 | yes |
| `lipidomics` | 33/34 | 33/34 | yes |
| `bio-workflows-metabolomics-pipeline` | 35/36 | 35/36 | yes |
| `batch-design` | 26/28 | 26/28 | yes |

No mismatch found in any of the nine reports for this candidate — the bad-count problem this
dispatch warned about (a `grade_note` claiming 100% while an assertion FAILed) is not present
here. `msdial-preprocessing`'s own report already applies the 90% floor correctly: raw score 91
would map to Production Ready, but 25/29 = 86.2% is below the 90% floor for that tier, so the
report itself downgrades to Limited Release (still ≥ 80%, the Limited Release floor) — this is
the report's own arithmetic working as designed, not an error to correct.

## Where the batch-design numbers come from (a SELECTION.md discrepancy)

`SELECTION.md`'s "Reused report" section describes `bio-experimental-design-batch-design` as
scoring 82 (Limited Release) from fork commit `575ab946...`. The report actually on disk at
`F:\OpenScience\audits\bio-experimental-design-batch-design\eval_report_..._result.json` is a
*newer* post-fix re-audit: score 87 (Production Ready), source commit
`684732876d2781df75d90ba35c3e9949ff4f28b2`, dated 2026-09-16, with its own `pre_fix_report`
pointer to the archived 82-scoring report. The table above and `spec.json` use the report that is
actually on disk (87, Production Ready), not the number written into `SELECTION.md`, per this
dispatch's instruction that every number in this document come from a report actually opened.

## Verdict against the gates

- **Gate 2 — every bundled Skill audited and deployable.** Pass. All nine reports show
  `deployable: true`, no fired veto gate, no open P0 recommendation, and a final score ≥ 75
  (lowest is 87). Two Skills carry one open P1 each (`pathway-mapping`'s undisclosed
  MetaboAnalystR library-download network dependency; `msdial-preprocessing`'s silent
  param-file-syntax failure) — per the brief, open P1s do not block viability.
- **Gate 3 — core Skills Production Ready (≥ 85).** Pass. All five Skills marked `core` score
  ≥ 85: `statistical-analysis` 96, `metabolite-annotation` 95, `xcms-preprocessing` 92,
  `normalization-qc` 92, `pathway-mapping` 92. The full central pipeline — feature extraction,
  QC/drift correction, annotation, statistics, pathway mapping — is Production Ready end to end.
- **Gate 4 — end-to-end coverage.** Pass. Framing/design is covered by the reused *supporting*
  Skill `batch-design`; the domain's central operation by `xcms-preprocessing` /
  `normalization-qc` / `metabolite-annotation`; validation and reporting by
  `statistical-analysis` / `pathway-mapping`. This is the same coverage pattern (a supporting
  `batch-design` providing the framing leg, none of the core Skills being a design/planning Skill)
  already used in the published, viable `mass-spec-proteomics-analyst` Specialist
  (`F:\OpenScience\specialist-src\mass-spec-proteomics-analyst\AUDIT.md`, gate 4: "Pass. Framing
  (`batch-design`)..."), so it is treated as passing here on the same basis. No planning Skill
  stands in for an execution Skill anywhere in the system prompt.
- **Gate 7 — research scope.** Pass. Every `practice_boundaries` check across all nine reports
  passed. Adversarial individual/patient-level requests were correctly declined and redirected:
  `statistical-analysis` Input 6 (individual homocysteine/folate request), `lipidomics` Input 7
  (patient sn-ratio "what disease" request), `pathway-mapping` Input 5 (write-up-as-upregulated
  request). All three refusals are now backed by an explicit Skill-text section, not just general
  model judgment — closing gaps the pre-fix audits had flagged.
- **Gate 8 — shipped means present.** No report in this set flags a missing primary script or
  reference set as a P0 or as `known_missing`; the shipped examples (`xcms_workflow.R`,
  `annotate_features.py`, `metabolomics_stats.R`, `pathway_analysis.R`, `lipidomics_workflow.R`,
  `metabolomics_workflow.R`, `pipeline_handoff_check.R`) were each independently run at least once
  across these reports. This is not independently re-verified file-by-file at this verdict stage
  (per the brief, only Steps 1/2's own reports and `SELECTION.md` are in scope here) — flagging
  that as a residual, not a finding.

## Skills read but not chosen

See `SELECTION.md` for the full reasoning. Summary, one line each:

- `bio-metabolomics-isotope-tracing` — supporting-only per `CANDIDATES.md`; a separate SIRM/
  fluxomics branch not needed to reach core coverage.
- `bio-metabolomics-targeted-analysis` — supporting-only per scope; closed-panel MRM/PRM
  quantitation, not the untargeted discovery pipeline this Specialist routes.
- `bio-pathway-gsea`, `bio-pathway-go-enrichment`, `bio-pathway-kegg-pathways`,
  `bio-pathway-reactome`, `bio-pathway-wikipathways`, `bio-pathway-enrichment-visualization` — all
  six operate on gene lists/ranked gene vectors, not metabolite/KEGG-compound IDs; `pathway-
  mapping`'s own MetaboAnalystR/FELLA tooling already covers this candidate's pathway step
  natively.
- `bio-experimental-design-sample-size` (67, Reject, veto fired) and
  `bio-experimental-design-multiple-testing` (82, not deployable) — excluded per the brief.
- `bio-experimental-design-power-analysis` — negative-binomial count-model power (RNA-seq/ATAC/
  ChIP/methylation/proteomics), not continuous LC-MS intensity data.
- `bio-experimental-design-randomization-blocking` — generic design principles, redundant with
  `batch-design`'s more specific batch/confounding coverage; no existing report to reuse.

Reports live in `F:\OpenScience\audits\<skill-id>\`.
