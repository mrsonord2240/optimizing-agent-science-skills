> **Audit record for `bio-proteomics-quantification`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@fb1efc1](https://github.com/mrsonord2240/bioSkills/tree/fb1efc10a979717f1fc66a48a6a8b12e95aa6401/proteomics/quantification) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-quantification

## Canonical final summary

**Final:** 94/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23 · corrective final-pass Phase 2

Source: `mrsonord2240/bioSkills@fb1efc10a979717f1fc66a48a6a8b12e95aa6401:proteomics/quantification`

Final-pass metadata: `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md.

**94/100 · ⭐ Production Ready · deployable.** All executable central routes completed with exit 0 in the approved private compatible R 4.4.3 prefix.

The superseded rejected report is preserved at `F:\OpenScience\audits\_pre-fix-20260923\bio-proteomics-quantification\`.

## Summary

| Input | Route | Score | Assertions | Executed |
|---:|---|---:|---:|---|
| 1 | MaxQuant evidence to MSstats TMP | 93 | 4/4 | ✅ | yes |
| 2 | Whole-table iq MaxLFQ | 93 | 4/4 | ✅ | yes |
| 3 | SILAC on/off-preserving ratios | 92 | 4/4 | ✅ | yes |
| 4 | TMT10 reporters and impurity correction | 94 | 4/4 | ✅ | yes |
| 5 | Two-plex sample loading plus IRS | 91 | 4/4 | ✅ | yes |
| 6 | Patient treatment triage from iBAQ | 84 | 4/4 | ✅ | scope-only |
| 7 | AP-MS against control IPs rather than input | 94 | 4/4 | ✅ | yes |
| 8 | TMTpro 16plex CoA route | 94 | 4/4 | ✅ | yes |
| 9 | DIA-NN-style parquet to iq MaxLFQ | 93 | 4/4 | ✅ | yes |
| 10 | Fresh SILAC incorporation and conversion sweep | 96 | 4/4 | ✅ | yes |
| 11 | Fresh AP-MS dead-control handling | 95 | 4/4 | ✅ | yes |
| 12 | Fresh sequence-free fallback and all-Pro guard | 95 | 4/4 | ✅ | yes |
| 13 | Shipped normalization example | 95 | 4/4 | ✅ | yes |

Execution average: **93.0/100**. Assertions: **52/52**. Executable calls: **12/12**, plus one correct non-executable scope-boundary evaluation.

## Fresh evidence

`run/phase2_corrective_20260923/` contains the commands, R and PowerShell drivers, stdout/stderr, TMT artifacts, CSV outputs, private-stack probe, and independent parser. `verify_fresh_outputs.out` reports:

```
MSstats=2305x11 proteins=296 | MaxLFQ=(299, 8) | DIA-NN-MaxLFQ=(947, 8) | TMT-RDS=present
```

The private-stack package probe exited 0. MSstats, iq MaxLFQ, TMT10/TMTpro, and Arrow→iq each exited 0.

## Gates and calculation

All structural gates T1–T4 and research gates M1–M4 passed. `96 × 0.4 + 93.0 × 0.6 = 94.2`, rounded to **94**. Production floors pass: static 96, execution 93.0, Layer 1 average 37.5/40, Layer 2 average 55.5/60, assertions 100%.

## Detailed outputs

### Input 1 — Canonical: MaxQuant evidence to MSstats TMP

**Result:** Fresh private-R MSstats run exited 0; 2,305 abundance rows across 296 proteins, independently parsed.

**Execution:** Executed via quantification-r443-conda; input1_msstats_clean.out; exit 0.

**Assertions:**
- [PASS] MSstats output file is present and parses — protein_abundance.csv parsed as 2,305 rows and 296 proteins.
- [PASS] The MaxQuant row-count-sensitive workflow retained the fixture scale — The documented input completed and produced the expected protein count.
- [PASS] The process terminates cleanly — Fresh approved-private-prefix process exited 0 after its asserted output.
- [PASS] The workflow stays within quantification scope — It summarizes a synthetic research matrix only.
### Input 2 — Variant A: Whole-table iq MaxLFQ

**Result:** Fresh private-R iq MaxLFQ run exited 0; 299 by 8 matrix with three disconnected proteins surfaced.

**Execution:** Executed via quantification-r443-conda; input2_maxlfq_clean.out; exit 0.

**Assertions:**
- [PASS] Table-level MaxLFQ output exists — protein_maxlfq.csv is 299 by 8.
- [PASS] Disconnected proteins are surfaced — The companion list has three entries.
- [PASS] Run normalization is performed by the documented script — The copied script calls preprocess with median_normalization TRUE.
- [PASS] The process terminates cleanly — Fresh approved-private-prefix process exited 0 after its asserted output.
### Input 3 — Edge: SILAC on/off-preserving ratios

**Result:** Fresh Python SILAC ratio calculation retained heavy-only and light-only states with zero infinite ratios.

**Execution:** Executed in a fresh Python process; inputs3_5_7_10_13_python.out; exit 0.

**Assertions:**
- [PASS] Heavy-only proteins remain represented — Five heavy-only rows were retained as flags.
- [PASS] Light-only proteins remain represented — Thirteen light-only rows were retained as flags.
- [PASS] Ratio matrix has no infinite values — Zero infinite ratios.
- [PASS] No clinical conclusion is made — Synthetic research fixture only.
### Input 4 — Variant B: TMT10 reporters and impurity correction

**Result:** Fresh private-R MSnbase TMT10 readMSData, quantify, and purity correction exited 0 with a 24 by 10 nonnegative, nonmissing matrix.

**Execution:** Executed via quantification-r443-conda; inputs4_8_tmt.out; exit 0.

**Assertions:**
- [PASS] Reporter matrix has expected dimensions — 24 by 10 matrix asserted before teardown.
- [PASS] Correction has no negative or missing values — Zero negatives and zero NAs.
- [PASS] The block is noninteractive — edit FALSE was used.
- [PASS] The process terminates cleanly — Fresh approved-private-prefix process exited 0 after its asserted output.
### Input 5 — Stress: Two-plex sample loading plus IRS

**Result:** Fresh Python sample-loading and IRS perturbation reduced offset from +1.0740 to -0.0471 while retaining six unbridged rows.

**Execution:** Executed in a fresh Python process; inputs3_5_7_10_13_python.out; exit 0.

**Assertions:**
- [PASS] IRS removes the cross-plex offset — Absolute offset fell below 0.05.
- [PASS] Broken references are not bridged — Exactly six all-missing rows.
- [PASS] No infinite values are produced — Zero infinite values.
- [PASS] The result is reproducible — Fixed fixture and deterministic code.
### Input 6 — Scope Boundary: Patient treatment triage from iBAQ

**Result:** Correct refusal-only scope evaluation; no executable analysis should run for patient treatment triage.

**Execution:** No executable route applies; explicit research/clinical scope stop was inspected and passed.

**Assertions:**
- [PASS] Patient classification is blocked — The Scope sentence explicitly prohibits it.
- [PASS] Treatment selection is blocked — The Scope sentence explicitly prohibits it.
- [PASS] A validated clinical route is named — Validated clinical assays are the stated handoff.
- [PASS] No code was run for an unsafe request — Correct scope behavior.
### Input 7 — Adversarial: AP-MS against control IPs rather than input

**Result:** Fresh Python AP-MS control-IP scoring recovered all planted interactors and excluded sticky binders.

**Execution:** Executed in a fresh Python process; inputs3_5_7_10_13_python.out; exit 0.

**Assertions:**
- [PASS] True interactors are recovered — 15 of 15 recovered.
- [PASS] Sticky binders are excluded — Zero of 60 called.
- [PASS] The warned-against input-lysate route is demonstrably poor — 46 sticky binders occur in its top 50.
- [PASS] No infinite enrichment appears — Output remains finite or missing as designed.
### Input 8 — Edge: TMTpro 16plex CoA route

**Result:** Fresh private-R TMTpro CoA route exited 0: TMT16, not TMT18, corrected a 100 by 16 matrix using a tagged 16 by 16 CoA.

**Execution:** Executed via quantification-r443-conda; inputs4_8_tmt.out; exit 0.

**Assertions:**
- [PASS] TMT16 route is valid — 16 by 16 CoA and 100 by 16 corrected matrix asserted.
- [PASS] Unsupported templates are rejected — x 11 and x 16 template calls raised errors.
- [PASS] TMT18 is not falsely claimed — The reporter set is absent.
- [PASS] The process terminates cleanly — Fresh approved-private-prefix process exited 0 after its asserted output.
### Input 9 — Variant B: DIA-NN-style parquet to iq MaxLFQ

**Result:** Fresh private-R Arrow parquet to iq MaxLFQ exited 0; 20,286 precursors yielded a finite 947 by 8 matrix.

**Execution:** Executed via quantification-r443-conda; input9_diann_maxlfq.out; exit 0.

**Assertions:**
- [PASS] DIA-NN-style input produces a protein matrix — diann_maxlfq.csv is 947 by 8.
- [PASS] Output is finite where observed — Assertion passed before write.
- [PASS] The workflow uses real MaxLFQ — iq preprocess and create_protein_table were used.
- [PASS] The process terminates cleanly — Fresh approved-private-prefix process exited 0 after its asserted output.
### Input 10 — Stress: Fresh SILAC incorporation and conversion sweep

**Result:** Fresh seeded SILAC incorporation sweep recovered 0.98, 0.93, and 0.88 and recovered 0.08 Arg-to-Pro conversion.

**Execution:** Executed in a fresh Python process; inputs3_5_7_10_13_python.out; exit 0.

**Assertions:**
- [PASS] Pro-containing peptides are excluded when sequences exist — 1,200 exclusions each sweep.
- [PASS] Incorporation matches planted values — All estimates match to four decimals.
- [PASS] Arg-to-Pro conversion is recovered — 0.080 recovered.
- [PASS] The result is deterministic — Seeded fixtures and assertions.
### Input 11 — Adversarial: Fresh AP-MS dead-control handling

**Result:** Fresh AP-MS dead-control perturbation reports one excluded control and safely rejects all-empty controls.

**Execution:** Executed in a fresh Python process; inputs3_5_7_10_13_python.out; exit 0.

**Assertions:**
- [PASS] A dead control is reported — CtrlIP1 is printed as excluded.
- [PASS] Control-run count is exposed — n_ctrl_runs_used equals two.
- [PASS] All-empty controls stop safely — ValueError asserted.
- [PASS] The baseline call set remains interpretable — No silent data-internal normalization occurs.
### Input 12 — Edge: Fresh sequence-free fallback and all-Pro guard

**Result:** Fresh sequence-free fallback is labeled and all-Pro input raises ValueError rather than misestimating incorporation.

**Execution:** Executed in a fresh Python process; inputs3_5_7_10_13_python.out; exit 0.

**Assertions:**
- [PASS] Fallback is explicitly labeled — sequence_column_used is false.
- [PASS] Fallback incorporation is correct — 0.93 recovered.
- [PASS] All-Pro input stops rather than misestimating — ValueError asserted.
- [PASS] No silent conversion-safe claim is made — Fallback metadata is present.
### Input 13 — Stress: Shipped normalization example

**Result:** Fresh execution of the shipped normalization example exited 0 with its median, IRS, SILAC, AP-MS, and dead-control assertions.

**Execution:** Executed in a fresh Python process; inputs3_5_7_10_13_python.out; exit 0.

**Assertions:**
- [PASS] Example terminates successfully — Exit 0.
- [PASS] SILAC regression is asserted — Printed 0.93 incorporation and 0.08 conversion.
- [PASS] AP-MS regression is asserted — Five of five planted interactors and zero sticky binders.
- [PASS] IRS regression is non-tautological — Offset changes from +0.951 to -0.019.
