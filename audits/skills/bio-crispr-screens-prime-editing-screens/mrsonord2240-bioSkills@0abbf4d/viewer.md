> **Audit record for `bio-crispr-screens-prime-editing-screens`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0abbf4d](https://github.com/mrsonord2240/bioSkills/tree/0abbf4d40d0df260ca60b346a9d6dc307b80fa5d/crispr-screens/prime-editing-screens) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-prime-editing-screens

## Canonical final summary

**Final:** 95/100 — ⭐ Production Ready; deployable: true.

Source: `mrsonord2240/bioSkills@0abbf4d40d0df260ca60b346a9d6dc307b80fa5d:crispr-screens/prime-editing-screens`
Auditor independent: `false`
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

Generated: 2026-09-23 | Source: `mrsonord2240/bioSkills@0abbf4d40d0df260ca60b346a9d6dc307b80fa5d:crispr-screens/prime-editing-screens`

This is the required final-pass exception: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.
Prior canonical audit bundle preserved at `F:\OpenScience\audits\_pre-fix-20260923\bio-crispr-screens-prime-editing-screens` before this report replaced the active record.

## Verdict

**95/100 — Production Ready — deployable: true.** Both structural and research veto gates pass. All 9/9 dynamic inputs executed; all 28/28 assertions passed.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 57 | 95 | 3/3 | ✅ |
| 2 | Variant A | 39 | 57 | 96 | 4/4 | ✅ |
| 3 | Edge | 37 | 57 | 94 | 3/3 | ✅ |
| 4 | Variant B | 38 | 56 | 94 | 3/3 | ✅ |
| 5 | Stress | 38 | 58 | 96 | 3/3 | ✅ |
| 6 | Adversarial | 38 | 58 | 96 | 3/3 | ✅ |
| 7 | Scope Boundary | 38 | 57 | 95 | 3/3 | ✅ |
| 8 | Stress | 37 | 57 | 94 | 3/3 | ✅ |
| 9 | Variant B | 38 | 57 | 95 | 3/3 | ✅ |

Execution average: **95.0/100**. Layer 1 mean: **37.9/40**. Layer 2 mean: **57.1/60**.

## Static evaluation

- **functional_suitability: 12/12** — All central claims were exercised: PRIDICT2 single and batch, candidate generation, filtering, concordance, CRISPResso2 PE mode, and ePRIDICT light model.
- **reliability: 11/12** — The failure modes accurately cover the reproduced second-run guard and empty-summary handling. One point is reserved for the intentionally unrun full ePRIDICT model.
- **performance_context: 7/8** — Progressive references keep SKILL.md compact and disclose ePRIDICT light/full download sizes; the full model remains a large optional resource.
- **agent_usability: 15/16** — Decision tree, command blocks, exact real output columns, and recovery messages are actionable. The full-model path cannot be live-tested in a normal audit footprint.
- **human_usability: 8/8** — Usage guide now points to SKILL.md for operational detail and clearly distinguishes PE, BE, and Cas9 decisions.
- **security: 12/12** — Static inspection found no raw eval/exec, credentials, or unbounded user-command interpolation in shipped Python.
- **maintainability: 11/12** — Runnable helpers are separate, parse cleanly, and their expected columns are checked. The example intentionally retains a documented simulation placeholder rather than calling PRIDICT2 itself.
- **agent_specific: 18/20** — Strong trigger precision, references, failure recovery, and handoffs. Full-model resource planning remains an explicit escape hatch rather than a fully executable low-footprint path.

## Dynamic evidence

### Input 1 — PRIDICT2 five-fold single-mode pegRNA scoring

**Executed:** `True`. **Execution note:** Fresh upstream-README single-mode input; 5-fold run written under run/phase2/input1_single.

Scores: Basic 38/40 | Specialized 57/60 | Total 95/100.

- [PASS] Single-mode invocation produces a non-empty per-pegRNA CSV — 765 rows
- [PASS] Real PRIDICT2 score columns are present and non-NaN — ['PRIDICT2_0_editing_Score_deep_K562', 'PRIDICT2_0_editing_Score_deep_HEK']
- [PASS] The documented five-fold option completes — mode banner observed

### Input 2 — Fresh two-edit PRIDICT2 batch recipe at the documented core cap

**Executed:** `True`. **Execution note:** Fresh two-edit batch run from an initially empty audit directory; exact --cores 3 and --summarize K562 recipe executed.

Scores: Basic 39/40 | Specialized 57/60 | Total 96/100.

- [PASS] Literal documented input/ and fresh predictions/ batch recipe completes — completion banner observed
- [PASS] Summary contains real prediction rows — 6 rows
- [PASS] Documented real output columns are present — missing=[]
- [PASS] K562 scores are numeric and non-NaN — all rows populated

### Input 3 — Second --summarize run into a nonempty output directory

**Executed:** `True`. **Execution note:** Regression of the documented no-CSV-in-output-dir precondition; deliberately expected failure was observed.

Scores: Basic 37/40 | Specialized 57/60 | Total 94/100.

- [PASS] A second --summarize into an occupied CSV directory fails — rc=1
- [PASS] Failure gives the documented remediation signal — Output directory is not empty
- [PASS] The first-run summary remains parseable — (6, 52)

### Input 4 — Shipped pegRNA example with constructible and no-PAM variants

**Executed:** `True`. **Execution note:** Copied shipped example ran on a new two-variant fixture, including a no-PAM edge case.

Scores: Basic 38/40 | Specialized 56/60 | Total 94/100.

- [PASS] A constructible variant yields a filtered library entry — rows=2
- [PASS] No-PAM variants are skipped rather than crashing the batch — No PE-designable PAM/PBS/RTT window for 1 variant(s): ['no_pam'] -- excluded before PRIDICT2 scoring, not a script error.
- [PASS] Every emitted extension is RTT then PBS — rowwise equality

### Input 5 — Shipped summary filter on real and literal-empty summaries

**Executed:** `True`. **Execution note:** Copied shipped filtering script checked against fresh real PRIDICT2 summary and a literal empty-summary sentinel.

Scores: Basic 38/40 | Specialized 58/60 | Total 96/100.

- [PASS] Filter script retains top one per sequence on a real summary — rows=2
- [PASS] Output has the two input sequence names — ['deletion1', 'insertion1']
- [PASS] A literal empty PRIDICT2 summary exits nonzero with guidance — clear guard observed

### Input 6 — Shipped PE/BE concordance against planted truth

**Executed:** `True`. **Execution note:** Copied shipped cross-validation script executed on a newly planted four-shared-variant fixture.

Scores: Basic 38/40 | Specialized 58/60 | Total 96/100.

- [PASS] Only shared variants are inner-joined — rows=4
- [PASS] Exactly the two planted same-sign FDR-passing variants are high confidence — ['v1', 'v4']
- [PASS] Discordant sign and failed FDR are excluded — v2/v3 false

### Input 7 — ePRIDICT light model at the documented K562 locus

**Executed:** `True`. **Execution note:** run_epridict_phase2.sh, launched in the mandated WSL login shell, ran ePRIDICT single at chr3:44843504. It returned score 42.53 and K562 percentile 62.02%, and wrote the documented chr3_44843504.csv output.

Scores: Basic 38/40 | Specialized 57/60 | Total 95/100.

- [PASS] The documented single-locus command completes in the provisioned ePRIDICT environment — Exited 0 in WSL science/epridict.
- [PASS] The output contains a numeric light-model score and genomewide K562 percentile — 42.53 and 62.02%, respectively.
- [PASS] The result is presented as K562-specific chromatin context rather than a cross-cell-line guarantee — Reference file states this boundary explicitly.

### Input 8 — All six ePRIDICT light-model bigWig inputs

**Executed:** `True`. **Execution note:** run_epridict_phase2.sh opened every light-model bigWig with pyBigWig at chr3:44843504 and counted non-null signal values. Each of the six tracks yielded 200/200 non-null values.

Scores: Basic 37/40 | Specialized 57/60 | Total 94/100.

- [PASS] All six light-model ENCODE bigWigs parse — ENCFF139KZL, 601JGK, 834SEY, 954LGE, 959YJV, and 972GVB opened successfully.
- [PASS] Every parsed bigWig has signal at the documented test locus — Each had 200/200 non-null values.
- [PASS] The check detects a data artifact rather than trusting a downloader exit code — It opens each file and asserts observed signal.

### Input 9 — CRISPResso2 PE quantification with planted reference and edited reads

**Executed:** `True`. **Execution note:** run_crispresso_phase2.ps1 built a 500-read synthetic FASTQ (240 prime-edited, 260 reference) and ran the copied SKILL.md command through pinellolab/crispresso2:latest. The nested report path existed and contained three amplicon rows with 240 reads assigned to Prime-edited.

Scores: Basic 38/40 | Specialized 57/60 | Total 95/100.

- [PASS] The documented nested CRISPResso2 output path exists — CRISPResso_on_sample_id/CRISPResso_quantification_of_editing_frequency.txt was produced.
- [PASS] The correct RTT-then-PBS extension creates a Prime-edited amplicon row — The report has Reference, Prime-edited, and Scaffold-incorporated rows.
- [PASS] All 240 planted edited reads are assigned to Prime-edited — Prime-edited Reads_aligned = 240 of 500 input reads.

## Veto review

- **T1 Stability:** PASS — completed commands yielded parsed, checked outputs; the intentionally invalid second-run test failed clearly.
- **T2 Contract:** PASS — required frontmatter and all referenced copied files exist.
- **T3 Determinism:** PASS — repeated PRIDICT2 recipe and fixed-format planted inputs yielded stable parseable results.
- **T4 Security:** PASS — no raw eval/exec or credential handling in shipped Python.
- **M1 Scientific integrity:** PASS — source citation metadata was cross-checked against Nature/PubMed or the publisher-hosted PRIME record; no fabricated result was emitted.
- **M2 Practice boundaries:** PASS — research-only workflow, no diagnosis or treatment advice.
- **M3 Methodological baseline:** PASS — tool constraints and independent biological validation are explicit.
- **M4 Code usability:** PASS — copied shipped Python parsed and executed; Docker/WSL requirements were exercised rather than assumed.

## Open issue

- **P2:** the optional ePRIDICT full model remains unexecuted because its 455 tracks require approximately 624 GB. The default light model was fully executed and verified; no P0 or P1 remains.

## Artifacts

- Fresh scripts and logs: `run/phase2/`
- Synthetic CRISPResso2 fixture: `run/phase2/input9_crispresso/`
- Prior report and evidence: `_pre-fix-20260923/bio-crispr-screens-prime-editing-screens/`
