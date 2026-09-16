> **Audit record for `bio-metabolomics-msdial-preprocessing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/metabolomics/msdial-preprocessing) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-msdial-preprocessing
Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:metabolomics/msdial-preprocessing`
Category: Data Analysis | Execution Mode: D (Hybrid — CLI console + R/Python code) | Complexity: Moderate (N=5)

## Environment

Ran against the real, already-installed MS-DIAL console at
`F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\tools\msdial-console\MSDIALCUI.exe`
(v5.5.260820), and R/Python code via `rs.sh` / `Scripts\python.exe` in the same candidate env.
No raw LC-MS/GC-MS instrument files were available for a full end-to-end MS-DIAL run (per
TOOLS.md, only the CLI banner/help and the R/Python parsing paths are testable without vendor
raw data), so the console was exercised for its documented commands and help text, and the
import/filter code was exercised on independently-generated synthetic AlignResult-style exports
(distinct from the Skill's own bundled `examples/process_msdial_output.R`), saved under
`data/` and `run/` in this audit folder.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 32 | 49 | 81 | 4/5 PASS | ✅ |
| 2 | Variant A | 30 | 43 | 73 | 2/4 PASS | ⚠️ |
| 3 | Edge | 25 | 37 | 62 | 2/4 PASS | ⚠️ |
| 4 | Variant B | 29 | 41 | 70 | 3/4 PASS | ⚠️ |
| 5 | Stress | 31 | 49 | 80 | 4/5 PASS | ✅ |

**Execution Average: 73.2 / 100**
**Assertion Pass Rate: 15/22**
**Static Score: 76/100** | **Final Score: 74/100 — Beta Only ⚠️ (not deployable, below the supporting floor of 75)**
**Skill Veto: PASS | Research Veto: PASS (not fired — findings below are documentation/version-currency defects, not fabrication, practice-boundary or unrunnable-code issues)**

> Reviewer note: read Inputs 2, 3, 4 first — all three failures trace back to the Skill's core
> "Run MS-DIAL Headless" commands and confidence-level logic not having been re-verified against
> the actually-installed, current MS-DIAL release.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have LC-MS DDA raw data converted to mzML in a folder. Build the MsdialConsoleApp headless command to process it, then show me how to parse the resulting AlignResult.txt into R with correct header handling and filter to keep only Fill% >= 70% features with MS/MS support."

**Executed: true.**

Console verification (`MSDIALCUI.exe` with no args):
```
Commands:
  gcms          Run GC-MS data processing
  lcms          Run LC-MS data processing
  lcimms        Run LC-IM-MS data processing
  dims          Run DI-MS data processing
  imms          Run IC-MS data processing
  msn / eic / rtcorrection / imagegen
```
No `lcmsdda` token exists. `MSDIALCUI.exe lcms --help` confirms the real flags: `-i/-o/-m/-p/-t`.
SKILL.md's exact command (`MsdialConsoleApp lcmsdda -i ./LCMS_DDA/ -o ./LCMS_DDA_out/ -m ./Msdial-lcms-dda-Param.txt`)
therefore fails twice over: wrong binary name, and a subcommand that does not exist in this
build. The corrected command is `MSDIALCUI.exe lcms -i ./LCMS_DDA/ -o ./LCMS_DDA_out/ -m ./Msdial-lcms-dda-Param.txt`.

R import + filter (run verbatim from SKILL.md against an independently-generated synthetic
export, `run/input1_import_filter.R`):
```
Parsed 45 rows x 18 cols. meta_cols found: 8 | sample_cols found: 10
PASS: row/col counts match the synthetic ground truth ( 45 features, 10 samples).
Fill% >= 70 kept 15 / 45 features
MSI level table (all features, before fill filter):
   2    3 <NA>
  10   12   23
PASS: every row kept by keep_fill truly has Fill% >= 70 -> TRUE
```

**Scores:** Basic: 32/40 | Specialized: 49/60 | Total: 81/100
**Assertions:**
- [FAIL] The documented `MsdialConsoleApp lcmsdda` command runs against the installed console as written — real binary is `MSDIALCUI.exe`, real token is `lcms`.
- [PASS] Skill instructs verifying the installed console's real subcommands before trusting the documented command (Version Compatibility section).
- [PASS] R import correctly splits metadata vs. sample columns on a real 4-header-row export — 45/45 rows, 10/10 sample cols, exact match to ground truth.
- [PASS] Fill% >= 70 filter keeps only features that truly meet the threshold — ground-truth check TRUE.
- [PASS] Output excludes gap-filled/low-confidence features before treating them as measurements.

---

### Input 2 — Variant A (DIA/SWATH)
**Prompt:** "My run is a SWATH/DIA acquisition converted from vendor raw. What MS-DIAL console command and input format do I need, and how is DIA distinguished from DDA in MS-DIAL's console?"

**Executed: true** (console help commands; no code generation to run beyond that).

`MSDIALCUI.exe lcms --help` shows one `lcms` command shared by both DDA and DIA — there is no
`lcmsdia` token, and nothing in the help output or SKILL.md explains that DDA vs. DIA is
actually selected via a setting inside the `-m` method/param file. SKILL.md's ABF-only-input
claim for DIA is plausible and undisputed by anything found here (the console help has no
input-format flag to check it against), so that specific claim is credited as correct.

**Scores:** Basic: 30/40 | Specialized: 43/60 | Total: 73/100
**Assertions:**
- [FAIL] Documented `lcmsdia` console token exists in the installed console — confirmed absent.
- [PASS] Skill correctly states DIA requires ABF-format input, not mzML.
- [PASS] Skill correctly explains why DIA/SWATH needs MS2Dec deconvolution (chimeric spectra).
- [FAIL] SKILL.md documents how DDA vs. DIA is actually distinguished in the real console — it does not; an agent following the Skill has no path to a working DIA invocation.

---

### Input 3 — Edge (GC-EI on MS-DIAL 5)
**Prompt:** "I have GC-EI (70 eV) raw data. Can I process it in MS-DIAL 5 console, and how does retention alignment work?"

**Executed: true.**

```
$ MSDIALCUI.exe gcms --help
Description:
  Run GC-MS data processing
Options:
  -i, --input <input> (REQUIRED)
  -o, --output <output> (REQUIRED)
  -m, --method <method> (REQUIRED)
  -p, --project
```
This is a real, working subcommand in the installed MS-DIAL 5.5.260820 console, backed by its
own `MsdialGcMsApi.dll` in the same install. SKILL.md's "Why GC-EI Is Different (and stays in
MS-DIAL 4)" section and its Common Errors row ("No GC-MS option in MS-DIAL 5 | 5-alpha excludes
GC-MS | Use a MS-DIAL 4 build's gcms token") are directly contradicted by this evidence: the
researcher's already-installed 5.x console has a working `gcms` mode and does not need a
separate MS-DIAL 4 build. The retention-index (Kovats/FAME) alignment rationale itself is
accurate and well-sourced (Stein 1999, AMDIS) and is credited as correct.

**Scores:** Basic: 25/40 | Specialized: 37/60 | Total: 62/100
**Assertions:**
- [FAIL] "MS-DIAL 5-alpha excludes GC-MS" holds for the installed, current console — contradicted; `gcms` exists and its help prints real options.
- [PASS] Skill correctly explains why GC-EI deconvolution differs fundamentally from LC peak-picking.
- [FAIL] The Common Errors fix (switch to MS-DIAL 4) is the researcher's best available path — misleading given a working `gcms` mode already exists.
- [PASS] Skill correctly recommends retention-index over raw RT for GC-EI cross-run alignment.

---

### Input 4 — Variant B (parse existing export in Python)
**Prompt:** "I already have an MS-DIAL AlignResult.txt export. Parse it into pandas, split metadata from sample columns, and map annotation tags to MSI confidence levels."

**Executed: true** (`run/input4_python_import.py`, independently-generated synthetic export).

```
Parsed 30 rows x 14 cols. meta_cols found: 8 | sample_cols found: 6
PASS: row/col counts and sample-column identity match synthetic ground truth (30 features, 6 samples).

msi_level
NaN    19
3.0    11
Name: count, dtype: int64

Fill% >= 70 kept 12 / 30 features
PASS: every row kept by keep_fill truly has Fill% >= 70 -> True
```
No feature was ever assigned MSI Level 2, despite the synthetic ground truth containing several
Metabolite/Lipid + MS/MS features. Root-caused with an independent 3-line repro:
```python
>>> df = pd.read_csv(io.StringIO("Alignment ID\tMS/MS assigned\n1\tTRUE\n2\tFALSE\n3\tTRUE\n"), sep="\t")
>>> df.dtypes
MS/MS assigned    bool
>>> df['MS/MS assigned'] == 'TRUE'
0    False
1    False
2    False
```
`pandas.read_csv` silently casts the export's literal `TRUE`/`FALSE` text to native `bool`, so
SKILL.md's only documented idiom for this check (`== 'TRUE'`, written for R's character column)
silently returns all-False when carried into the Python path the Skill also documents — with no
error or warning. The Fill% numeric filter is unaffected and remains correct.

**Scores:** Basic: 29/40 | Specialized: 41/60 | Total: 70/100
**Assertions:**
- [PASS] Python import correctly separates metadata from sample columns — 30/30 rows, 6/6 sample cols, exact match.
- [FAIL] The Skill's MS/MS-support check correctly flags MSI Level 2 features when applied via the Python path — silently broken by pandas' auto-bool-cast; confirmed 0/11 named+MS/MS features tagged Level 2.
- [PASS] Fill% >= 70 filter in Python keeps only truly-qualifying features.
- [PASS] Output does not fabricate identification beyond what the data supports.

---

### Input 5 — Stress (full pipeline)
**Prompt:** "I have a lipidomics LC-MS/MS DIA dataset that needs QC-based filtering and downstream stats. Should I use MS-DIAL or XCMS, build the right console command, import into R, apply Fill%/MS-MS/QC-CV filtering, and hand off to normalization-qc — walk through the whole pipeline."

**Executed: true** (reuses `run/input1_import_filter.R` for the R portion; console command checked against the same verified help output as Input 1).

The MS-DIAL vs. XCMS comparison table and "Decision Tree by Scenario" table give a specific,
defensible answer (DIA + lipid annotation -> MS-DIAL) rather than a generic "it depends."
Scope discipline is correct: SKILL.md explicitly hands QC-CV/D-ratio/blank-filtering and
MNAR-aware imputation to `normalization-qc` with a sourced (Broadhurst 2018) threshold table,
rather than reimplementing them inline or inventing numbers. The console command repeats the
same `MsdialConsoleApp lcmsdda`-does-not-exist defect found in Input 1.

**Scores:** Basic: 31/40 | Specialized: 49/60 | Total: 80/100
**Assertions:**
- [PASS] Clear, defensible MS-DIAL vs. XCMS decision framework.
- [FAIL] Full-pipeline console command runs against the installed console — same defect as Input 1.
- [PASS] Skill defers QC-CV/D-ratio/imputation to normalization-qc rather than reimplementing.
- [PASS] R import + Fill% filter portion runs correctly end-to-end (reuses Input 1's verified logic).
- [PASS] Skill warns that a single-pipeline marker list is a candidate, not a validated result (Li 2018).

---

## Files produced by this audit

- `data/` — reserved for synthetic export fixtures (generated inline by the run scripts; no persistent file needed beyond tempdir during execution)
- `run/input1_import_filter.R` — Input 1 R import + honest-filter test (executed via `rs.sh`)
- `run/input4_python_import.py` — Input 4 Python import + MSI-mapping test, including the pandas bool-cast repro (executed via the candidate venv `python.exe`)
- `eval_report_bio-metabolomics-msdial-preprocessing_result.json`
- `eval_viewer_bio-metabolomics-msdial-preprocessing.md` (this file)
