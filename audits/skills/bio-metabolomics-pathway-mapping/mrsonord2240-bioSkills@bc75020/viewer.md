> **Audit record for `bio-metabolomics-pathway-mapping`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@bc75020](https://github.com/mrsonord2240/bioSkills/tree/bc7502038043b387617e236ee116d251c4bd5b50/metabolomics/pathway-mapping) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-pathway-mapping

## Canonical final summary

**Final:** 92.3/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23

Exact source: `mrsonord2240/bioSkills@bc7502038043b387617e236ee116d251c4bd5b50:metabolomics/pathway-mapping`
Mode: D (scripts plus interpretive guidance) · Category: Data Analysis · Complexity: Complex (7 inputs)

The prior 2026-09-16 report was preserved at `F:\OpenScience\audits\_pre-fix-20260922\bio-metabolomics-pathway-mapping\` before this fresh Phase 2 report replaced the current record. This directed final pass sets `auditor_independent: false`; see `F:\OpenScience\audits\_final_pass\bio-metabolomics-pathway-mapping\CHECKPOINT.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical Local-Only ORA | 37 | 55 | 92 | 5/5 | ✅ |
| 2 | Full-table PSEA, twice | 38 | 56 | 94 | 5/5 | ✅ |
| 3 | Significant-only PSEA boundary | 38 | 54 | 92 | 4/4 | ✅ |
| 4 | FELLA diffusion | 37 | 57 | 94 | 4/4 | ✅ |
| 5 | Interpretive stress case | 37 | 55 | 92 | 4/4 | ✅ |
| 6 | Unknown-name mapping boundary | 34 | 52 | 86 | 4/5 | ⚠️ |
| 7 | Disclosed remote API alternative | 35 | 53 | 88 | 4/4 | ⚠️ |

Execution average: **91.1/100** · Assertions: **30/31 (96.8%)** · Layer 1 average: **36.6/40** · Layer 2 average: **54.6/60**
Static: **94/100** · Final: **92.3/100 — Production Ready — deployable** · Vetoes: **none**.

## What ran

All source scripts were parsed first by `run/final_pass_static_parse.R`: five R scripts, three references, and required frontmatter passed. Dynamic commands and their logs are in `run/final_pass_execute.ps1`, `run/final_pass_remaining.ps1`, and `run/final_pass_input8_local_execute.ps1`.

1. `map_compounds.R input1_ora_compounds.txt hsa name ...` printed `Mapped 12 of 12 compounds to KEGG IDs`.
2. `local_ora.R` on those IDs and the 320-ID synthetic assay background wrote a parseable CSV; `hsa00020` had p `9.372143e-11` and FDR `3.327111e-09`.
3. `mummichog_psea.R` twice on the entire 1500-row table (5 ppm, negative, p-cutoff 0.2, 200 permutations) wrote two equal 15-row CSVs. Logs show 11/111/11/11 duplicate merges and completed 200 permutations.
4. The 70-row significant-only file logged `There are too few m/z features` and wrote no result CSV. It then produced a secondary raw R error because the script does not guard the validation return value.
5. `fella_diffusion.R` on six KEGG IDs wrote 206 results. `getExcluded()` was `character(0)` and `hsa00020` was top at p-score `7.400315e-06`.
6. A new 11-name file containing one unknown name exposed the P1: `map_compounds.R` printed `Mapped 11 of 11` but wrote ten KEGG IDs and literal `NA`; a fresh paired Local-Only ORA still returned `hsa00020` from the valid IDs.
7. `ora_api.R` made the disclosed remote attempt and logged `Failed to connect to the API Server!` and `Failed to perform pathway analysis!`; it wrote no output CSV. The R status 2 appears as 2816 (`0xB00`) through the Windows Git-bash wrapper.

The compact cross-run assertions are in `run/final_pass_assertions.R` and its log. They confirmed canonical mapping, the observed literal-NA defect, both TCA ORA outputs, deterministic PSEA, FELLA output, and no API result CSV.

## Detailed assessment

### Inputs 1–2 — primary analyses

The primary default is sound: mapping precedes Local-Only ORA, the background is explicit, and the expected TCA pathway appears. The PSEA instructions use the complete feature table rather than a significant-only subset and the code's `set.seed(123)` made two fresh outputs equal. These are real computed results, not values reused from the fix log.

### Inputs 3–4 — defensive boundary and mechanism

Rejecting the too-small significant-only table is scientifically correct; no invalid enrichment result was emitted. The useful validation message is obscured only by a subsequent secondary error, yielding P2 rather than a veto. FELLA's cached graph loaded and its diffusion route returned pathways, modules, and an explicit unmapped-compound result.

### Inputs 5–7 — interpretation, mapping coverage, and remote alternative

The interpretive guidance preserves the necessary limits: annotation uncertainty, assay background, hub effects, and steady-state pools are not mistaken for flux. The new mapping boundary found a real P1: the literal string `NA` is counted and written as a KEGG ID. The remote API route remains a clearly disclosed, known-failing alternative and is not the default; the local default succeeds.

## Veto review

- T1 Stability: PASS — all primary workflows completed; guarded errors do not produce false results.
- T2 Contract: PASS — required frontmatter, scripts, and referenced files are present.
- T3 Determinism: PASS — seeded PSEA outputs were equal across fresh runs; FELLA uses analytic normality approximation.
- T4 Security: PASS — no raw code execution or secrets; remote transfer and reference downloads are disclosed.
- M1 Scientific integrity: PASS — fresh calculations and no fabricated evidence.
- M2 Practice boundaries: PASS — research framing, no diagnosis/prescription.
- M3 Methodological baseline: PASS — background, annotation, topology, and flux pitfalls are actively guarded.
- M4 Code usability: PASS — scripts parse and core workflows execute; the P1/P2 defects are bounded and documented above.

## Recommendations

1. **P1 — filter literal `NA` mappings.** In `scripts/map_compounds.R`, exclude both R `NA` and `trimws(kegg_ids) == 'NA'` before writing and counting; report the unknown name as unmapped.
2. **P2 — stop after failed mummichog validation.** Test whether `SanityCheckMummichogData` returned numeric 0, print `current.msg`, and quit nonzero before `SetPeakEnrichMethod`.

## Canonical final-pass metadata

- Source: `mrsonord2240/bioSkills@bc7502038043b387617e236ee116d251c4bd5b50:metabolomics/pathway-mapping`
- `auditor_independent:false`
- Note: `final pass: fixed and audited under one brief, see CHECKPOINT.md`
