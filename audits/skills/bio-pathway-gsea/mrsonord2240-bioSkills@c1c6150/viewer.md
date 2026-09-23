> **Audit record for `bio-pathway-gsea`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c1c6150](https://github.com/mrsonord2240/bioSkills/tree/c1c6150cba5570abc754866e90d09ee536917b07/pathway-analysis/gsea) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-gsea

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@c1c6150cba5570abc754866e90d09ee536917b07:pathway-analysis/gsea`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 58 | 96 | 3/3 | ✅ |
| 2 | Variant A | 38 | 57 | 95 | 3/3 | ✅ |
| 3 | Edge | 37 | 57 | 94 | 3/3 | ✅ |
| 4 | Variant B | 38 | 57 | 95 | 3/3 | ✅ |
| 5 | Scope Boundary | 38 | 57 | 95 | 3/3 | ✅ |
| 6 | Variant C | 38 | 56 | 94 | 3/3 | ✅ |
| 7 | Matrix/design | 37 | 54 | 91 | 2/3 | ✅ |

Execution average: **94.3 / 100**. Assertion pass rate: **20/21 (95.2%)**.

## Execution evidence

All seven inputs were executed through the isolated documented Linux R runtime. Each output ends with `exit=0`.

1. **GO preranked GSEA:** shipped `gsea_go.R` produced 31 terms; planted GO:0006260 had NES 3.0484.
2. **MSigDB Hallmark:** shipped `gsea_msigdb.R` produced the planted OXPHOS hallmark with NES 3.0540.
3. **nPerm and ranking guards:** `nPerm` emitted the expected fgseaSimple fallback warning; the post-call guard, unsorted-list rejection, and duplicate-ID rejection all passed.
4. **Per-sample scores:** parameter-object GSVA/ssGSEA returned finite 3x16 score matrices; planted deltas were +0.7376 and -0.8415.
5. **ID matching:** symbol TERM2GENE returned 50 terms; the mismatched Entrez TERM2GENE call was rejected.
6. **KEGG and Reactome:** live KEGG plus local ReactomePA calls completed with 311 and 924 terms, respectively.
7. **Matrix/design:** CAMERA with `inter.gene.cor=NA` and fry both completed; planted UP/DOWN sets were significant (FDR 5.26e-08). The synthetic `factor()` default placed `Case` before `Control`, so the observed directions were inverted relative to the informal set names; this exposed that the Skill should show explicit reference-level ordering for a case-vs-control contrast.

## Detailed output evaluation

### Input 1 — Canonical GO preranked GSEA

**Prompt:** Run GO biological-process GSEA on a DESeq2-style Entrez-ranked vector, report adjusted p-values, NES, and leading-edge genes.

**Output:** The shipped example ran and reported 31 enriched terms, a positive planted DNA-replication result (NES 3.0484), BH-adjusted p-values, and a 38-gene leading edge.

**Assertions:**

- [PASS] The example exits successfully and returns an enriched result — evidence ends `exit=0` and has 31 terms.
- [PASS] The planted GO term is positive and reported — GO:0006260 NES is 3.0484.
- [PASS] The output includes NES, BH adjustment, and leading-edge interpretation — all appear in the printed result and example.

### Input 2 — MSigDB Hallmark

**Prompt:** Run Hallmark GSEA on an Entrez-ranked human vector and identify an enriched hallmark.

**Output:** The shipped example completed; the planted OXPHOS hallmark was the significant positive result (NES 3.0540).

**Assertions:**

- [PASS] The msigdbr collection API and `ncbi_gene` TERM2GENE route execute — completed with exit 0.
- [PASS] The planted Hallmark is recovered with BH-adjusted significance — OXPHOS passed the example's assertion.
- [PASS] The result preserves direction through NES — positive and negative sections are emitted by the example.

### Input 3 — nPerm and invalid rankings

**Prompt:** Check how the Skill handles deprecated `nPerm`, unsorted ranks, and duplicate gene identifiers.

**Output:** The fallback warning appeared, the post-call `nPerm` guard fired as intended, and the two invalid vectors were rejected.

**Assertions:**

- [PASS] `nPerm` fallback is detected rather than silently accepted — fgseaSimple warning and guard succeeded.
- [PASS] Unsorted vectors are rejected — expected decreasing-sort error was detected.
- [PASS] Duplicate names are rejected — expected duplicate-ID error was detected.

### Input 4 — GSVA and ssGSEA

**Prompt:** Turn a continuous expression matrix into GSVA and ssGSEA pathway scores.

**Output:** Both parameter-object calls returned finite 3x16 matrices and recovered the planted up/down score shifts.

**Assertions:**

- [PASS] Current GSVA parameter-object API executes — both calls completed with exit 0.
- [PASS] Score matrices have the requested set-by-sample shape — both are 3x16.
- [PASS] The planted biological direction is recovered — GSVA deltas are +0.7376 and -0.8415.

### Input 5 — ID mismatch boundary

**Prompt:** Run symbol-ranked MSigDB GSEA and verify that a mismatched Entrez TERM2GENE mapping is refused.

**Output:** The correct symbol mapping gave 50 terms; the mismatched mapping emitted `No gene can be mapped` and was classified as rejected.

**Assertions:**

- [PASS] Symbol-ranked input works with `gene_symbol` — 50 terms were returned.
- [PASS] An ID mismatch is not silently interpreted as zero enrichment — the call errored as documented.
- [PASS] The failure is actionable — the output identifies mapping, matching the Common Errors guidance.

### Input 6 — KEGG and Reactome

**Prompt:** Run KEGG and Reactome preranked GSEA with Entrez identifiers.

**Output:** KEGG fetched its dated live annotation and returned 311 terms; local ReactomePA returned 924 terms.

**Assertions:**

- [PASS] Both advertised pathway routes execute in the documented isolated runtime — each exited 0.
- [PASS] KEGG's live-service behavior is visible and documented — REST annotation fetch messages were captured.
- [PASS] Reactome uses a local annotation route and returns structured results — 924 terms were materialized.

### Input 7 — Matrix + design competitive and self-contained tests

**Prompt:** Test pathway differences in a case/control expression matrix while accounting for correlation.

**Output:** CAMERA with `inter.gene.cor=NA` and fry returned significant planted UP/DOWN sets. The output also showed that R's default factor-level ordering makes the coefficient `Control - Case` unless the reference level is explicitly fixed.

**Assertions:**

- [PASS] CAMERA is called with `inter.gene.cor=NA` and returns PValue/FDR/Direction — all columns and significant planted sets were observed.
- [PASS] fry runs on the same indexed pathways — it returned three rows.
- [FAIL] The documented case-vs-control contrast explicitly fixes coefficient orientation — the snippet uses `factor(Control, Case)` without `relevel()` or `levels=`, and default lexical ordering inverted the observed directions.

## Veto assessment

Skill veto: PASS. Research veto: PASS. The code is executable in the stated isolated runtime, uses seeded stochastic calls, avoids PHI/credential handling, and makes no diagnostic or treatment recommendation. The factor-direction ambiguity is a P2 clarification issue, not a methodological redline because the code exposes Direction and a caller can set factor levels.

## Recommendation

**P2 — Make case/control coefficient orientation explicit.** In the Matrix + Design block, set `group <- factor(group, levels = c('Control', 'Case'))` (or state the desired reference level) before `model.matrix(~ group)`, and say that Direction is relative to that coefficient.
