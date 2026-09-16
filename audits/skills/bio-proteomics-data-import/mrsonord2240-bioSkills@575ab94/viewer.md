> **Audit record for `bio-proteomics-data-import`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@575ab94](https://github.com/mrsonord2240/bioSkills/tree/575ab946989a7029d235eb0ab711e47b08edbcb0/proteomics/data-import) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Skill Audit Viewer — `bio-proteomics-data-import` (re-audit)

**Date:** 2026-09-15 · **Source:** `mrsonord2240/bioSkills@575ab946989a7029d235eb0ab711e47b08edbcb0:proteomics/data-import`
**Pre-fix report:** `F:\OpenScience\audits\_pre-fix-20260915\bio-proteomics-data-import\` (2026-09-11 — static 79, execution 76.8, final 78, ⚠️ Beta Only, not deployable)

| | Pre-fix (2026-09-11) | Re-audit (2026-09-15) |
|---|---|---|
| Static | 79 | **84** |
| Execution average | 76.8 (N=5) | **86.0 (N=8)** |
| Assertions | 17/25 (68%) | **35/40 (87.5%)** |
| Final | 78 ⚠️ Beta Only | **85.2 ✅ Limited Release** |
| Deployable | no | **yes** |

Raw 85.2 maps to ⭐ Production Ready; the assertion pass rate (87.5%) is under the 90% floor, so the grade drops exactly one tier. Every other floor is met (static 84 ≥ 80, execution 86.0 ≥ 85, Layer 1 35.6 ≥ 32, Layer 2 50.4 ≥ 48).

**Category:** 3 — Data Analysis. **Mode:** A. **Complexity:** Moderate → N = 5; 8 were run (5 pre-fix inputs as regression + 3 new).

---

## Environment and data

pyOpenMS 3.5.0 · pandas 3.0.5 · numpy 2.5.3 · R 4.4.3 with QFeatures 1.16.0 · DIA-NN 2.6.1 and msconvert 3.0.26253 (to produce the real inputs).

*Synthetic* (labelled as such in every script that makes or uses it): MaxQuant `proteinGroups.txt` (1560 rows, 8 LFQ runs, 60 bookkeeping rows); `proteinGroups_failed.txt` (Intensity / iBAQ / LFQ families with a deliberately under-loaded run T4 and a truth table); a DIA-NN `report.parquet` (8 runs, 60 `LOWCONF` groups that pass run-level q-values and fail `Global.PG.Q.Value`); `synthetic_mixed.mzML` (DDA, DIA windows, a scan with offsets not written, an all-ion scan, plus a truth table); and two tables written for this re-audit — a MaxQuant TMT10 `proteinGroups.txt` and a FragPipe `combined_protein.tsv`.
*Public:* PXD070049 (CC0, Van Puyvelde et al. 2026) — one Orbitrap Astral DIA mzML (20,409 spectra) and a real DIA-NN 2.6.1 `report.parquet` from three Astral runs, submitter SDRF.

---

## Veto gates

**Skill veto (T1–T4): PASS.** All four code blocks completed on every input the Skill declares support for, including a real 20k-spectrum file and a real DIA-NN report. Deterministic, read-only. The two crashes seen are on a format the Skill does not claim (FragPipe) and on a quant column family it does not route (TMT); both are recommendations below, not stability failures.

**Research veto (M1–M4): PASS.** References real and now correctly attributed — the pyOpenMS misattribution to Chambers 2012 is fixed and Rost 2014 *Proteomics* 14(1):74–77 is cited. No diagnostic or prescriptive content. The methodological core (missingness structure) is right and was confirmed against real data. All code ran verbatim.

---

## Input 1 — Canonical: MaxQuant → clean log2 LFQ matrix ✅ 93/100 (5/5)

Block `b02` run verbatim:

```
warnings: []
rows read 1560 | kept after flag filter 1500 | final matrix (1445, 10) | all-NaN rows 0 | -inf 0
surviving REV__/CON__ IDs: 0 | blank leading_gene: 40
groups with Razor + unique peptides < 2 still in matrix (threshold documented as not applied): 16
no-LFQ table -> ValueError: No LFQ intensity columns: LFQ was not enabled in MaxQuant; use Intensity and normalize explicitly
```

The pre-fix FAIL — 55 rows with no valid LFQ value passing silently into the matrix — is fixed: `matrix[matrix[lfq_cols].notna().any(axis=1)]` now drops them, 0 remain. The `≥2 peptides` threshold is still not applied, and the thresholds table now says so explicitly, which is the honest form.

## Input 2 — Variant A: DIA-NN `report.parquet` → protein × run matrix ✅ 91/100 (5/5)

```
report rows 23020 | after filter 20170 | matrix (887, 8) | -inf 0 | NaN cells 589
LOWCONF groups in raw: 60 | surviving in matrix: 0
zero PG.MaxLFQ cells among filtered rows: 202 | max distinct PG.MaxLFQ per group x run: 1
Lib.PG.Q.Value column present (1.9.x MBR alternative): True
```

Both pre-fix FAILs fixed. `Global.PG.Q.Value <= 0.01` now excludes all 60 groups that pass only within single runs, and `np.log2(matrix.replace(0, np.nan))` removes the 61 `-inf` cells the pre-fix block produced. The filter now matches the sibling `dia-analysis` Skill, so an agent running both gets one definition of 1% FDR rather than two.

## Input 3 — Edge: mzML with an all-ion scan, then a real 20k-spectrum file ✅ 91/100 (5/5)

Synthetic mixed file:

```
Skill loop: completed over 20 spectra
printed by the block: controllerType=0 controllerNumber=1 scan=18: isolation offsets not written (width unknown, not 0 Th)
 i  ms  n_peaks  prec_mz   z   lo   hi                   flag
17   2       60 733.3812 2.0  0.0  0.0    offsets not written
18   2      400      NaN NaN  NaN  NaN no precursor (all-ion)
19   2       80 650.1234 3.0  0.5  1.5
```

Pre-fix this raised `IndexError: list index out of range` at spectrum 18 and reported spectrum 17's window as 0 Th without comment. Both fixed, and the extracted values match the truth table row for row.

Real Astral DIA mzML:

```
Skill block completed in 16 s over 20409 spectra
lines printed by the block (offsets not written): 0
MS levels: {1: 1361, 2: 19048} | MS2 without precursor: 0
isolation widths (Th): {20.01: 19048} | distinct window centres: 20
```

The new guard costs nothing on a well-formed file: no false warnings across 19,048 MS2 scans.

## Input 4 — Variant B: Intensity vs LFQ vs iBAQ, and the R route ⚠️ 86/100 (4/5)

```
complete-case proteins: 657 | true nulls among them: 613
Intensity      T4 - mean(other runs) median -1.33 | true-null median T/C log2FC -0.424
iBAQ           T4 - mean(other runs) median -1.33 | true-null median T/C log2FC -0.424
LFQ intensity  T4 - mean(other runs) median +0.00 | true-null median T/C log2FC -0.066
max within-protein SD of log2(iBAQ/Intensity) across samples: 0.0
```

The Skill's central quant-column teaching is exactly right and the data show it: the deliberately under-loaded run is invisible in LFQ and 1.33 log2 low in the other two; iBAQ carries raw `Intensity`'s between-sample ratios identically.

The R route is still a name with no code — the fix log records this as deliberately out of scope. Running it:

```
readQFeatures formals: assayData,colData,quantCols,runCol,name,removeEmptyCols,verbose,ecol,...
features read: 1560
filterFeatures with MaxQuant column names as-is: ERROR: 'Potential contaminant' is/are absent from all rowData.
'Reverse' found in 1 out of 1 assay(s)
'Potential.contaminant' found in 1 out of 1 assay(s)
after filter + zeroIsNA + log2: 1500 8 | -Inf: FALSE | NA %: 19.8
```

`readQFeatures` applies `make.names()`, so the MaxQuant names with spaces must be dotted. An agent hits this on the first attempt. **FAIL.**

## Input 5 — Stress: DDA + DIA missingness ✅ 91/100 (5/5)

```
DDA MaxQuant LFQ : missing 14.5% | corr(abundance, #missing) -0.619
DIA DIA-NN       : missing  8.3% | corr(abundance, #missing) -0.495
DIA missing % by TRUE abundance quartile: {'Q1 low': 21.9, 'Q2': 4.3, 'Q3': 3.6, 'Q4 high': 3.4}
Skill still says DIA is MCAR / tolerates standard imputers: False
Skill DIA decision-tree row routes by diagnostic: True
```

The pre-fix contradiction — the Skill's own diagnostic giving DIA an MNAR signature while its decision tree sent DIA to "MCAR / standard imputers" — is gone. Both pre-fix FAILs on this input are fixed.

## Input 6 — New: MaxQuant TMT10 `proteinGroups.txt` ❌ 71/100 (3/5)

```
Skill block -> ValueError: No LFQ intensity columns: LFQ was not enabled in MaxQuant; use Intensity and normalize explicitly
Intensity columns per sample available (the suggested fallback): [] | single column: True
agent route: reporter-corrected matrix (390, 10) | corr(FC, true) = 0.897
```

The new error is a real improvement over the pre-fix silent ID-only matrix — but it sends a TMT user to a column family that does not exist in a TMT table. The channels are in `Reporter intensity corrected 1..10`, and the Skill mentions reporter ions nowhere, while its taxonomy row advertises "DDA label-free / TMT search results". Two FAILs.

## Input 7 — New: FragPipe `combined_protein.tsv` ❌ 72/100 (3/5)

```
Skill block -> KeyError True
agent route: contam_ removed 8 | matrix (292, 6) | -inf 0 | missing % 15.1
```

FragPipe is genuinely outside the Skill's declared formats, so refusing is correct — but `KeyError: True` names nothing. The cause is a defect in the guard the Skill itself documents. Reproduced minimally on a four-column frame:

```
mask when all three flag columns are absent -> True bool
b02 on a flagless table -> KeyError: True
```

With one or two flag columns present the mask stays a Series and `.get()` works as advertised. With all three absent, each `.get(col, '')` returns the scalar `''`, `'' != '+'` is a Python bool, and `pg[True]` raises. The Common Errors row that recommends `.get()` as the fix for a missing flag column does not hold in the case it is written for. Two FAILs.

## Input 8 — New, public data: real DIA-NN report + missingness diagnostic ✅ 93/100 (5/5)

```
[b03 verbatim on REAL DIA-NN 2.6.1 output] matrix (4376, 3) | -inf 0 | NaN 1717 (13.1%)
[b04 verbatim] total missing 13.1% | abundance-missingness corr -0.444 | missing per run {'A': 565, 'B': 428, 'C': 724}
missing % by mean-abundance quartile: {'Q1 low': 29.8, 'Q2': 13.9, 'Q3': 6.7, 'Q4 high': 1.7}
```

This is the input the pass-1 P1 fix most needed: the rewritten missingness claim was verified on synthetic tables only. On a real Orbitrap Astral DIA matrix the Skill's own `assess_missingness`, run verbatim, returns exactly the structure the fixed text describes — fewer missing values than the DDA table, still strongly intensity-dependent, with a 17× gradient from the lowest to the highest abundance quartile. One replicate per condition in this dataset, so no within-condition CV is claimed anywhere.

---

## What pass 1 fixed, verified by execution

| Pre-fix finding | Priority | Now |
|---|---|---|
| DIA-NN import omits `Global.PG.Q.Value` | P1 | **Fixed** — 0/60 LOWCONF survive |
| DIA missingness labelled MCAR against its own diagnostic | P1 | **Fixed** — and confirmed on real Astral data (−0.444) |
| DIA block keeps `PG.MaxLFQ` zeros (−inf after log2) | P1 | **Fixed** — 0 −inf on synthetic and real |
| mzML loop crashes on MS2 scans without precursor | P1 | **Fixed** — 20/20 synthetic spectra, 20,409 real spectra |
| Silent failure modes in the MaxQuant block | P2 | **Fixed** — ValueError raised, 0 all-NaN rows |
| pyOpenMS misattributed to Chambers 2012 | P2 | **Fixed** — Rost 2014 cited |
| R route named but no QFeatures code | P2 | **Not fixed** (declared out of scope) — still a FAIL on Input 4 |

## Open recommendations

- **P1** — Add a TMT route (`Reporter intensity corrected`) and make the no-LFQ error name the columns the table actually has.
- **P2** — Rebuild the flag mask as a Series so it cannot collapse to `KeyError: True`, and correct the Common Errors row that recommends the broken guard.
- **P2** — Ship the QFeatures R block, with the `make.names()` caveat.
- **P2** — Add runnable examples for the DIA-NN and mzML blocks (the two that changed most and have none).
- **P2** — Have the cleaning blocks report what they removed, for the methods record.

## Evidence on disk

`F:\OpenScience\audits\bio-proteomics-data-import\rerun\` — `blocks/` (Skill code extracted verbatim), `in1_maxquant`, `in2_diann`, `in3_mzml`, `in3b_public_mzml`, `in4_columns`, `in4_qfeatures.R`, `in5_stress`, `in6_mq_tmt`, `in7_fragpipe`, `in8_real_dia_missingness` (each `.py`/`.R` with its `.out`), `make_new_tables.py`, `ex_load_maxquant.out`, `work*/`.
Real inputs: `F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\public-work\mzml\dia\` and `...\diann_predlib_mzml\diann_out\report.parquet`.
