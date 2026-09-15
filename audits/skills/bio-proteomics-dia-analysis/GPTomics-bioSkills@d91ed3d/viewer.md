> **Audit record for `bio-proteomics-dia-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/proteomics/dia-analysis) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-11 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-dia-analysis
Generated: 2026-09-11 · Sub-auditor for round-2 candidate `mass-spec-proteomics-analyst` · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:proteomics/dia-analysis` (SKILL.md 236 lines,
usage-guide.md 77 lines, examples/diann_analysis.sh 53 lines). Role in candidate: supporting (DIA identification/quant).
Category: Data Analysis · Mode A · Complexity: Moderate → N = 5 (`evaluate_skill.py` also returns Moderate/5: three task
types — run the search engine, filter the report, choose acquisition-aware conversion — with a decision tree but one tool family).

Environment: venv `F:\OpenScience\audit-envs\mass-spec-proteomics-analyst` (Python 3.12, pandas 3.0.5, numpy 2.5,
pyarrow 25, pyopenms 3.5.0). **DIA-NN, msconvert and a working EasyPQP install are not available.** DIA-NN flags were checked
against the DIA-NN README at tags 1.8.1, 1.9.2, 2.0 and master (2.6.1) (downloaded to `runs/docs/`, table in
`runs/diann_flag_check.txt`); msconvert against the ProteoWizard source (`SpectrumListFactory.cpp`, usage_demux). EasyPQP:
`pip install easypqp` would downgrade the shared venv's numpy 2.5 → 1.26.4 and scipy 1.18 → 1.17.1 and add numba/llvmlite, so I
**did not install it**. I downloaded the easypqp 0.1.59 wheel plus the pure-Python click/colorama/tqdm wheels with `--no-deps`,
extracted them under `runs/easypqp_sandbox/` and ran the CLI from PYTHONPATH with import-time stubs for seaborn/numba. The venv was not
modified. The external clone is still clean (`git status` empty).

**All data are SYNTHETIC.** `data/report.parquet` is the shared DIA-NN 1.9-style report (8 runs, 947 groups, 60 `LOWCONF*`
groups that pass run-level q but have Global.PG.Q.Value 0.04, ~1% PG.MaxLFQ zeros). `data/synthetic_*_8Th.mzML` (pyOpenMS,
staggered vs fixed windows) and a 600-run cohort report (`runs/in5_make_cohort.py`, seeded; 3.05 M rows; the 142 MB parquet
was deleted after the run to keep the folder small and can be rebuilt with the same seed) were made for this audit.

## Step 1 — Skill Veto
| Dim | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | Python block ran as written on 2 reports (3/3 runs exit 0); `bash -n examples/diann_analysis.sh` exit 0; example run with a stub `diann` exit 0 (`runs/smoke_example_stdout.txt`) |
| T2 Contract | PASS | `name`, `description` present; extra `tool_type`, `primary_tool` harmless |
| T3 Determinism | PASS | the filter is deterministic. DIA-NN's automatic mass accuracy depends on run order (docs), which the Skill does not mention (scored in 8.4) |
| T4 Security | PASS | no eval/exec, no network, no credentials |

## Step 2 — Static score: 77/100
| # | Criterion | Score | Note |
|---|---|---|---|
| 1.1 | Completeness | 3 | DIA-NN library-free/library/filter fully covered; OpenSWATH+PyProphet, Spectronaut, EncyclopeDIA appear only as table rows even though the decision tree recommends OpenSWATH for auditable FDR |
| 1.2 | Correctness | 2 | Filter, parquet default, `--matrix-spec-q` 5%, 0→NaN all correct. Wrong or misleading: the `easypqp library` command exits 1 as written; the example comments say `--mass-acc 0` auto-optimises "per file" (it optimises on the first run and reuses that, unless `--individual-mass-acc`); demultiplexing is presented as a MUST for every tool; `--out-lib *.tsv` is stale since 1.9.1; `--qvalue 0.01` is called "DIA-NN default" (the current docs say 5%) |
| 1.3 | Appropriateness | 3 | The route choice and FDR framing fit the task; the chimerism/window essay is heavier than an analyst needs |
| 2.1 | Fault tolerance | 3 | Per-method failure modes are well explained. The example has no check that `diann` or the FASTA exists; with no mzML present it passes a literal `*.mzML` |
| 2.2 | Error reporting | 3 | A Common Errors table gives cause and fix; no structured codes |
| 2.3 | Recoverability | 3 | Re-runs are safe; reusing `.quant` files and fast reanalysis are not mentioned |
| 3.1 | Token cost | 3 | 2,939 words in one file, all loaded; nothing is gated |
| 3.2 | Execution efficiency | 3 | Linear single-command route; `--mass-acc 0` just restates the default |
| 4.1 | Learnability | 3 | Clear. "Library-free directDIA" and the "predicted-library route" are contrasted in Insight 3 but treated as the same thing in the section title "Predicted-Library (directDIA) Route". DIA-NN's own docs say they are the same thing |
| 4.2 | Consistency | 3 | The directDIA naming above. The code comment "Per-run filter … Add Global.PG.Q.Value for the cross-run matrix" sits over code that always applies all three filters |
| 4.3 | Feedback design | 3 | Output files and the filtered matrix are specified; no expected per-run ID sanity check |
| 4.4 | Error prevention | 3 | Strong on parquet vs tsv, zeros, matrix-vs-report counts and cohort FDR. Silent on run-order-dependent automatic mass accuracy, the caveat for third-party libraries, and peak picking before demultiplexing |
| 5.1 | Discoverability | 3 | The description is jargon-dense but names DIA-NN, report.parquet and "identifying and quantifying proteins from DIA"; the usage guide has natural prompts |
| 5.2 | Forgiveness | 3 | An introspect-versions rule and a "verify matrix dotting" hint; input requirements are implicit |
| 6.1 | Credential safety | 4 | none used |
| 6.2 | Input validation | 3 | No column or version checks on the report. The example's unquoted `--f $f` splits a filename with a space into two argv entries (shown with the stub) |
| 6.3 | Data safety | 4 | nothing retained or sent |
| 7.1 | Modularity | 3 | Sections are cleanly separated; single file |
| 7.2 | Modifiability | 3 | Thresholds sit in one table; the command is duplicated across SKILL.md and the example |
| 7.3 | Testability | 2 | No test data. The example says it filters the report but contains only comments about filtering. The DIA-NN steps can't be verified without the binary |
| 8.1 | Trigger precision | 4 | Explicit route-outs to spectral-libraries, quantification and differential-abundance |
| 8.2 | Progressive disclosure | 3 | 236 lines under 500, but no references/ layer |
| 8.3 | Composability | 4 | Related Skills all exist; the hand-off is a log2 matrix |
| 8.4 | Idempotency | 3 | The filter is idempotent; the recommended automatic mass accuracy makes DIA-NN results depend on run order (DIA-NN docs) with no warning |
| 8.5 | Escape hatches | 3 | Routing lines and "confirm current engine"; no explicit stop conditions |

Category totals: Functional 8/12 · Reliability 9/12 · Performance 6/8 · Agent usability 12/16 · Human 6/8 · Security 11/12 ·
Maintainability 8/12 · Agent-specific 17/20 = **77**.

**Gate 8 (shipped-means-present): PASS.** SKILL.md and usage-guide.md point at no `references/` or `scripts/` files.
`examples/diann_analysis.sh` exists (not referenced by SKILL.md). All 7 Related Skills exist in the clone.

## Lead's leads — confirmed / refuted
1. **DIA-NN flags:** CONFIRMED that they exist. 22 of the 23 listed flags appear in the README command-line reference at 1.9.2, 2.0 and master
   (`runs/diann_flag_check.txt`). `--unimod4` is in no README, but DIA-NN 2.0 accepts it (the log in vdemichev/DiaNN#1490 prints
   "Cysteine carbamidomethylation enabled as a fixed modification"). **`--mass-acc 0` = auto: CONFIRMED with a correction.**
   0 is the default and means automatic, but "optimise them automatically for the first run in the experiment and then reuse the
   optimised settings for other runs … results will depend on which run is first in the list. It is preferable to fix these"
   (master README l.93). Per-run optimisation needs `--individual-mass-acc`. So the Skill's "auto-optimize tolerances per file"
   (SKILL.md l.82, example l.15) is wrong, and its "Default when uncertain" advice runs against the docs. `bash -n` on the example: OK.
2. **EasyPQP:** the subcommand names are CONFIRMED (`easypqp --help` lists `convert`, `library`, `insilico-library`…; `convert --format` →
   "No such option '--format'"). **The Skill's `easypqp library` command is REFUTED at runtime:** `Error: No PSMs files present. Need
   to have tag 'psmpkl' in filename.` exit 1. `library` needs positional `*.psmpkl`/`*.peakpkl` files from a prior `easypqp convert`.
   With those added it still fails: `There is a psm.tsv but no peptide.tsv.` With both tsvs given, easypqp prints that it will
   *ignore* `--peptide_fdr_threshold/--protein_fdr_threshold` (library.py l.538-541). The section is also titled "Generating a
   *Predicted* Library" but builds an empirical DDA library.
3. **Python filter on report.parquet:** 0/60 LOWCONF groups survive the Skill's filter; 60/60 survive a run-level-only filter.
   0→NaN works: 229 zero rows (0.99%), 61 zero matrix cells → NaN, 0 −Inf.
4. **Matrix 5% run-specific PG filter / parquet:** CONFIRMED. README: "Additional 5% run-specific protein-level FDR filter is
   applied to the protein matrices, use --matrix-spec-q to adjust it". Parquet since 1.9, and 2.0 documents only the parquet main report.
   Nuance: DIA-NN 1.9/1.9.2 docs say that with MBR you should filter **Lib.Q.Value / Lib.PG.Q.Value instead of Global.***. The
   Skill always enables MBR yet treats Lib.* as optional. This guidance was dropped from 2.0+ docs, so the filter to use depends on the version.
5. **msconvert demultiplex:** filter string CONFIRMED (`optimization=<(none)|overlap_only>` in pwiz usage_demux). But DIA-NN
   docs say "Acquisition schemes with overlapping windows are supported" (Demichev on DiaNN#11: "Yes!"), a community
   benchmark on DiaNN#438 found no-demux cost "just a few % coverage", and DIA-NN requires peak picking (vendor) as the
   *first* msconvert filter. The Skill's "MUST … or every tool sees the wide physical window" overstates the case, and its snippet
   leaves out peak picking.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 35 | 49 | 84 | 4/5 | yes (Python + example with stub diann; DIA-NN not run) | ✅ |
| 2 | Variant A | 37 | 54 | 91 | 4/5 | yes | ✅ |
| 3 | Edge | 31 | 39 | 70 | 2/4 | partly (window detector ran; msconvert not run) | ⚠️ |
| 4 | Variant B | 29 | 35 | 64 | 2/4 | yes (easypqp command ran and failed; DIA-NN not run) | ❌ |
| 5 | Stress | 32 | 45 | 77 | 4/5 | yes (Python on 3.05 M rows; DIA-NN not run) | ✅ |

**Execution Average: 77.2 / 100** · **Assertion Pass Rate: 16/23 (69.6 %)** · Layer 1 avg 32.8 · Layer 2 avg 44.4

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have 8 DIA runs from an Exploris 480 (variable windows, 60-min gradient), 4 control and 4 treated HeLa, already
converted to mzML. Run DIA-NN library-free against UniProt human reviewed and give me a 1%-FDR protein matrix I can take into limma."

**Output (following the Skill):** the DIA-NN predicted-library command from SKILL.md (`runs/in1_diann_cmd.sh`, `bash -n` OK,
**not executed**). Then the Skill's filter block, verbatim except the path (`runs/in1_skill_filter.py`), on the report. The
explanation given: precursor and PG q-values control the level, Global.PG.Q.Value controls the cohort context, the pg_matrix.tsv count
will be lower (5% run-specific filter), and normalisation/testing go to quantification/differential-abundance. The example script
was smoke-run with a stub `diann` that echoes argv: 38 arguments, exit 0.

Printed (`runs/in1_stdout.txt`, trimmed):
```
report rows 23020 | runs 8 | protein groups 947
Skill matrix shape (887, 8)
LOWCONF groups surviving Skill filter: 0
run-level-only matrix shape (947, 8) | LOWCONF surviving run-level-only: 60
README-recommended filter matrix groups 887
zeros in pivoted matrix before replace: 61
-inf in Skill log2 matrix: 0 | NaN cells: 589 (8.3% missing)
max distinct PG.MaxLFQ per (group, run): 1        # aggfunc='first' is safe
per-run protein counts: C1 823 ... T4 814
```
**Scores:** Basic 35 (FC 8: the matrix is right, but following the Skill gives "auto per file" mass accuracy and a stale `.tsv`
`--out-lib`; clarity 9; efficiency 9; scope 9) · Specialized 49 (method 17; code 12: the Python is out-of-the-box and the DIA-NN
command is verified only against docs; QC 8; reproducibility 7: run-order-dependent auto tolerances not disclosed, where DIA-NN docs
say to fix MS1/MS2 accuracy per instrument; security 5) · **84**

**Assertions (4/5):**
- [PASS] Filter names both LEVEL and CONTEXT (Q.Value, PG.Q.Value, Global.PG.Q.Value) — as written in the Skill.
- [PASS] Skill code runs as written and yields a log2 matrix without −Inf — 887×8, 0 −Inf.
- [PASS] Every DIA-NN flag in the command is documented or demonstrably accepted — 22 in README; `--unimod4` via the 2.0 log.
- [FAIL] Mass-accuracy guidance matches DIA-NN docs — the Skill says "per file"; the docs say first run reused, and fixing is preferred.
- [PASS] Scope: stays within search + filtering and routes normalisation/stats out.

### Input 2 — Variant A
**Prompt:** "Our core ran DIA-NN 1.9 on my 8 runs and sent report.parquet and report.pg_matrix.tsv. The matrix has fewer proteins than
I count in the report. Which q-value columns should I filter for a cohort-level protein matrix, and can you build the log2 matrix?"

**Output:** the Skill's filter (same code as Input 1) plus `runs/in2_dropped_groups.py` describing what it removed. The explanation:
the report is designed to be filtered, and the pg_matrix applies 1% global PG plus an extra 5% run-specific PG filter
(`--matrix-spec-q`), so the count difference is expected. Filter Q.Value and PG.Q.Value (level) and Global.PG.Q.Value (context).

Printed (`runs/in2_stdout.txt`):
```
groups passing run-level filters: 947
groups removed by Global.PG.Q.Value <= 0.01: 60 | all LOWCONF*: True
runs in which the removed groups had passed run-level 1% PG FDR: {1: 24, 2: 16, 3: 20}
zero cells converted to NaN before log2: 61 | -inf after log2: 0
groups with >= 3 valid values in both conditions: 803 of 887
groups completely absent in one condition (candidate on/off, not imputable as MAR): 26
```
**Scores:** Basic 37 (FC 9, clarity 9, efficiency 9, scope 10) · Specialized 54 (method 18: no Global.Q.Value precursor
filter, which DIA-NN recommends at 0.01; code 14; QC 9; reproducibility 8; security 5) · **91**

**Assertions (4/5):**
- [PASS] Groups failing Global.PG.Q.Value are removed — 0/60 LOWCONF survive vs 60/60 with a run-level-only filter.
- [PASS] 0 → NaN before log2 — 61 zero cells become NaN, 0 −Inf.
- [PASS] The matrix-vs-report explanation matches DIA-NN docs — 5% run-specific PG filter via `--matrix-spec-q` confirmed.
- [FAIL] The filter includes every report filter DIA-NN recommends — Global.Q.Value ≤ 0.01 is missing (no effect on this synthetic set).
- [PASS] Scope: the matrix goes to quantification/differential-abundance; no normalisation or testing here.

### Input 3 — Edge
**Prompt:** "Our Exploris 480 DIA method uses staggered 2 × 8 Th overlapping windows. We run DIA-NN on a Linux cluster, so I have to
convert the .raw files. What should the conversion and search look like?"

**Output (following the Skill):** "Staggered data MUST be demultiplexed at conversion or the selectivity benefit is silently lost",
with `msconvert run.raw --mzML --filter "demultiplex optimization=overlap_only"` for each run (`runs/in3_convert_cmd.sh`, `bash -n`
OK, **not executed**), then the Input 1 DIA-NN command. As usage-guide step 1 asks, the agent first checks the acquisition scheme. It wrote a
pyOpenMS reader that lists MS2 isolation windows and flags partial overlaps (`runs/in3_staggered_check.py`, **executed**):
```
synthetic_staggered_8Th.mzML: 21 distinct MS2 windows, physical width(s) [8.0] Th, partially-overlapping pairs 20 -> OVERLAPPING windows ...
synthetic_fixed_8Th.mzML: 10 distinct MS2 windows, physical width(s) [8.0] Th, partially-overlapping pairs 0 -> non-overlapping windows
```
Audit check: the filter string is valid (pwiz `optimization=<(none)|overlap_only>`). But the Skill's command leaves out the
`peakPicking vendor` filter, which DIA-NN docs require as the *first* msconvert filter (mzML must be centroided, and Skyline says to
centroid before demultiplexing). The Skill also never says that DIA-NN supports overlapping windows natively, or that current DIA-NN
reads Thermo .raw directly on Windows and on native Linux builds (master README l.127). The user's premise that Linux forces
conversion is out of date, and the Skill does not correct it.

**Scores:** Basic 31 (FC 6: the conversion as written would give profile mzML; clarity 8; efficiency 8; scope 9) ·
Specialized 39 (method 13: right idea, overstated and incomplete; code 9: one valid filter string, command incomplete, not
executed; QC 6; reproducibility 6; security 5) · **70**

**Assertions (2/4):**
- [PASS] The msconvert demultiplex filter string is valid ProteoWizard syntax — matches usage_demux in SpectrumListFactory.cpp.
- [FAIL] The conversion puts vendor peak picking first — missing from the Skill; DIA-NN docs require it.
- [FAIL] The output reflects that DIA-NN handles overlapping windows natively and demux is an optional few-% gain — the Skill says MUST / every tool.
- [PASS] Scope: no redesign of the acquisition method; treats the window scheme as inherited.

### Input 4 — Variant B
**Prompt:** "We ran 12 high-pH DDA fractions and searched them in FragPipe, so I have psm.tsv, peptide.tsv and the interact pep.xml
files. I want an experimental spectral library from that and to search my 8 DIA runs against it in DIA-NN instead of library-free.
Commands and filtering please."

**Output (following the Skill):** the Skill's `easypqp library --psmtsv psm.tsv --rt_reference irt.tsv --peptide_fdr_threshold 0.01
--protein_fdr_threshold 0.01 --out library.tsv`, then the library-based DIA-NN command (`--lib library.tsv`, no `--fasta`,
`runs/in4_cmds.sh`), then the Input 1 filter. The easypqp line **was executed** (sandbox, `runs/in4_easypqp_stdout.txt`):
```
$ easypqp library --psmtsv psm.tsv --rt_reference irt.tsv --peptide_fdr_threshold 0.01 --protein_fdr_threshold 0.01 --out library.tsv
Error: No PSMs files present. Need to have tag 'psmpkl' in filename.     exit=1
$ ... + run1.psmpkl run1.peakpkl
Error: There is a psm.tsv but no peptide.tsv.                             exit=1
```
The working route, which the Skill does not give, is `easypqp convert --pepxml … --spectra …` per run, then `easypqp library --psmtsv
psm.tsv --peptidetsv peptide.tsv *.psmpkl *.peakpkl` (with both tsvs the FDR flags are ignored), or FragPipe's own DIA-NN library.
DIA-NN: the flags are valid. The command drops `--fasta`, so protein annotation relies on the third-party library (`--reannotate` exists
for this), and the Skill never mentions DIA-NN's caution that third-party library "compatibility should be verified".

**Scores:** Basic 29 (FC 5: the central command fails; clarity 7; efficiency 8; scope 9) · Specialized 35 (method 13; code 5:
the Skill's key command errors out; QC 6; reproducibility 6; security 5) · **64**

**Assertions (2/4):**
- [FAIL] The EasyPQP library command runs as written — exit 1, "No PSMs files present".
- [PASS] The library-based DIA-NN flags exist in the documented version — `--lib`, `--reanalyse`, `--matrices`… in 1.9.2/2.0/master.
- [FAIL] The output supplies the FASTA / warns about third-party library compatibility — neither appears in the Skill.
- [PASS] Scope: library QC/building details deferred to spectral-libraries — the Skill routes it, though it also ships the failing snippet.

### Input 5 — Stress
**Prompt:** "600 plasma runs on a timsTOF (diaPASEF), 12 batches of 50. We want MBR, a cohort protein matrix, a per-run ID QC, and
a methods sentence that states exactly which q-value columns and thresholds we used."

**Output (following the Skill):** the decision-tree row "Large cohort → DIA-NN `--reanalyse`, filter on Global.PG.Q.Value" with
`--mass-acc 0` (`runs/in5_diann_cmd.sh`, **not executed**). The Skill's filter block **ran as written** on the SYNTHETIC 600-run report.
Methods sentence: "Precursors were filtered at run-specific Q.Value ≤ 0.01 and protein groups at run-specific PG.Q.Value ≤ 0.01 and
experiment-wide Global.PG.Q.Value ≤ 0.01 (DIA-NN x.y, MBR enabled); PG.MaxLFQ values of 0 were treated as missing."

Printed (`runs/in5_stdout.txt`):
```
rows 3,046,139 | Skill filter+pivot+log2 wall time 1.9 s | matrix (2000, 600)
-inf cells: 0 | missing 17.2%
FALSE groups in Skill matrix: 0
N runs | union groups run-level-only | of which FALSE | FALSE share | union groups Skill filter
     8 |  1966 |  16 |  0.81% | 1950
    50 |  2078 |  91 |  4.38% | 1987
   200 |  2363 | 370 | 15.66% | 1993
   600 |  2892 | 892 | 30.84% | 2000
per-run protein groups: median 1667, MAD 43, min 1541, max 1771; runs flagged: 0
```
(The false-group model is constructed and shows the mechanism, not a statistical proof.) Audit check against the docs: for
large experiments DIA-NN recommends building an empirical library from 20-100 good runs and searching everything with it
(MBR is "just a convenience feature"; its second pass is held in memory). For timsTOF the docs say to fix MS1/MS2 accuracy at 15 ppm
rather than use auto, which is run-order dependent — important across 12 batches. Under DIA-NN 1.9.x MBR the docs say Lib.* q-values
replace Global.*. The Skill's scaling and FDR-context claims hold; its large-cohort route does not match the tool author's guidance.

**Scores:** Basic 32 (FC 7, clarity 8, efficiency 8, scope 9) · Specialized 45 (method 14; code 13: the Python scales,
the DIA-NN route is not executed; QC 7: per-run QC was agent-added since the Skill routes it to proteomics-qc; reproducibility 6: auto mass
accuracy over 600 runs; security 5) · **77**

**Assertions (4/5):**
- [PASS] The Skill filter scales to a 3 M-row report in seconds with no −Inf — 1.9 s.
- [PASS] The global filter stops false groups accumulating across runs — 0 vs 892 false groups at 600 runs.
- [FAIL] The large-cohort route matches DIA-NN docs (empirical library from a subset, fixed mass accuracy) — the Skill says `--reanalyse` on all runs with `--mass-acc 0`.
- [PASS] The methods sentence names column, level, context and DIA-NN version — the Skill's level/context principle made this direct.
- [PASS] Safety: no individual-level diagnostic or clinical claims from the plasma cohort — output is a research matrix only.

## Research Veto
- M1 Scientific integrity: **PASS**. The nine references check out (journal, volume, pages); no invented numbers. All data are labelled SYNTHETIC.
- M2 Practice boundaries: **PASS**. No output diagnoses, prescribes or triages; the plasma cohort is handled as research data.
- M3 Methodological baseline: **PASS**. The FDR level/context guidance is correct (Rosenberger 2017; confirmed by execution). The
  demultiplexing overstatement and the large-cohort route are best-practice deviations, not principled fallacies.
- M4 Code usability: **PASS**. The Python ran as written (Inputs 1, 2, 5); every DIA-NN flag is documented or shown accepted; the msconvert
  filter string is valid. The failing `easypqp library` invocation is a usage error in one snippet, not a syntax or dependency
  failure. Filed as P1.

## Final
Static 77 × 0.4 = **30.8** · Execution 77.2 × 0.6 = **46.3** · 30.8 + 46.3 = 77.1 → **77** → band Limited Release.
Floors for Limited Release: static 77 ≥ 70 ✓ · execution 77.2 ≥ 75 ✓ · L1 32.8 ≥ 28 ✓ · L2 44.4 ≥ 42 ✓ · **assertions 69.6 % < 80 % ✗**
→ down one tier → **⚠️ Beta Only**. Not deployable. No veto override; no safety/scope assertion failures.

## Recommendations
- **[P1] `easypqp library` snippet fails as written** (Input 4). Missing positional `*.psmpkl/*.peakpkl` from `easypqp convert`, and
  `--psmtsv` needs `--peptidetsv`. Fix: show `easypqp convert` per run, then `easypqp library --psmtsv psm.tsv --peptidetsv peptide.tsv
  --out library.tsv *.psmpkl *.peakpkl`, note that the FDR flags are ignored when both tsvs are given, and retitle the section (it builds an empirical library, not a predicted one).
- **[P1] Staggered-window guidance overstated and incomplete** (Input 3). Say that DIA-NN supports overlapping windows natively (and reads .raw on
  Windows and native Linux), that demultiplexing is an optional few-% gain, and give `--filter "peakPicking vendor msLevel=1-" --filter "demultiplex
  optimization=overlap_only massError=10ppm"` with peak picking first.
- **[P1] Mass-accuracy advice contradicts DIA-NN docs** (Inputs 1, 5). `--mass-acc 0` = auto on the first run, reused; per-run needs
  `--individual-mass-acc`; the docs prefer fixed values (timsTOF 15/15, Astral MS1 4 / MS2 10, TripleTOF 20/20). Fix the "per file" wording in
  SKILL.md l.82 and example l.15, and the "Default when uncertain" line.
- **[P1] Large-cohort route diverges from DIA-NN guidance** (Input 5). Recommend an empirical library from 20-100 runs, then search all runs
  with fixed mass accuracy. State which q-value columns apply under MBR by version (1.9.x: Lib.* instead of Global.*; 2.x: Global.*).
- [P2] Add Global.Q.Value ≤ 0.01 to the report filter as DIA-NN recommends; fix the comment that says "per-run filter".
- [P2] Library-based route: add `--fasta` (+ `--reannotate` for third-party libraries) and the DIA-NN compatibility caution.
- [P2] Version drift: `--out-lib *.tsv` (empirical libraries are .parquet since 1.9.1); "`--qvalue 0.01` = DIA-NN default" (the current docs say 5%);
  "library-free directDIA" vs "predicted-library route" are the same thing in DIA-NN.
- [P2] Example script: quote filenames (`args+=(--f "$f")`), check that `diann`/FASTA/mzML exist, and include the filter code the header promises.
