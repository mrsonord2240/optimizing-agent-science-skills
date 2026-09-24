# bio-proteomics-dia-analysis fixes (2026-09-15)

Branch `fix/proteomics` (worktree `F:\OpenScience\external\bioSkills-wt-proteomics`). DIA-NN, msconvert and easypqp are not installed on this machine; command changes were checked against the documentation and source the auditor saved in `audits/bio-proteomics-dia-analysis/runs/docs/` (DIA-NN README 1.9.2, 2.0, master 2.6.1; pwiz `SpectrumListFactory.cpp`; easypqp 0.1.59 wheel). The Python filter ran on the audit `report.parquet`; the example ran against a stub `diann`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| easypqp library snippet fails as written | P1 | `easypqp convert --pepxml interact-run1.pep.xml --spectra run1.mzXML --psms run1.psmpkl --peaks run1.peakpkl`, then `easypqp library --psmtsv --peptidetsv ... *.psmpkl *.peakpkl`; note that FDR flags are ignored with both tsvs; section retitled "Building an Empirical Library ..."; Common Errors row | help/source: easypqp 0.1.59 `main.py` options (`--spectra` = mzXML or MGF) and `library.py` checks | not executed |
| Staggered-window guidance overstated and incomplete | P1 | Chimerism bullet, decision-tree row, failure mode, Common Errors and usage guide: DIA-NN supports overlapping windows natively, demux optional (few % in DIA-NN #438); msconvert with `peakPicking vendor msLevel=1-` first, then `demultiplex optimization=overlap_only massError=10ppm`; DIA-NN reads .raw on native Linux | docs: DIA-NN README (technology support, raw formats); `usage_demux` and the peak-picking-first warning in `SpectrumListFactory.cpp` | |
| Mass-accuracy advice contradicts DIA-NN docs | P1 | Route text: auto = first run reused, `--individual-mass-acc`; fixed values timsTOF 15/15, Astral 10/4, TripleTOF 20/20; both commands, default line, thresholds row, example and usage guide use fixed values | docs: README "LC-MS-specific parameters"; smoke run passed `--mass-acc 15 --mass-acc-ms1 15` | |
| Large-cohort route diverges from DIA-NN guidance | P1 | Decision-tree row: empirical library from 20-100 runs, search all runs MBR off with fixed accuracies; cohort-FDR fix and thresholds state `Lib.*` replaces `Global.*` under MBR on 1.9.x | docs: README speed optimisation and MBR note (master), 1.9.2 MBR q-value filters | |
| Report filter omits Global.Q.Value | P2 | Added `Global.Q.Value <= 0.01`; comment now names levels and context plus the 1.9.x MBR `Lib.*` rule; thresholds row | ran: 887 x 8, 0 -inf, 0 LOWCONF | column present in the audit parquet |
| Library-based route lacks FASTA and caveat | P2 | `--lib spectral_library.parquet --fasta ...`; `--reannotate` and DIA-NN-generated-library advice in text; decision-tree row | docs: README spectral library section, `--reannotate` | |
| Version drift in output and default claims | P2 | `--out-lib` `.parquet`; output listing; `--qvalue` threshold row says DIA-NN default is 0.05; description, header bullets and insight 3 say library-free = predicted-library route in DIA-NN | docs: README (empirical libraries .parquet, recommended filters, `--qvalue`) | |
| Example script fragile and missing promised filter | P2 | Array `--f "$f"` args, checks for `diann`, FASTA and mzML (nullglob), fixed mass accuracy, `.parquet` library, header no longer promises filtering code; filter notes include Global.Q.Value | ran: `bash -n` OK; stub `diann` run exit 0 with "run A.mzML" as one argument; empty folder exits 1 | filter code stays in SKILL.md rather than duplicated in the script |

Left unfixed: none.

## Final-pass correction (2026-09-24)

Exact source commit: `0e23cf7a1fc896bc332d5729ee93ae2b8d5dc291` on isolated branch `fix/bio-proteomics-dia-final`.

| finding from re-audit | priority | final correction | exact-commit evidence |
|---|---|---|---|
| DIA-NN 2.x rejects the headline one-command predicted-library route | P1 | Made the route explicitly two-stage: generate `<template>.predicted.speclib` from FASTA with no raw files, then search raw files with `--lib` and without FASTA digest/prediction. Kept the executable command only in `examples/diann_analysis.sh`. | Fresh stub verifies Stage 1 has no `--f`, Stage 2 has two `--f` values and no `--fasta-search`/`--predictor`; retained real 2.6.1 report/log re-filtered with the committed block. |
| Matrix/report row-count explanation is inverted on DIA-NN 2.6.1 | P1 | Removed the fixed “matrix lower” claim; directs users to `report.log.txt`, version and actual filters. | Public 2.6.1 archived output: matrix 4440 vs globally filtered report 4375. |
| EasyPQP TSV caveat is not actionable | P2 | Named `FragmentCharge`, `FragmentType`, `FragmentSeriesNumber`; recommends DIA-NN-format export or validated conversion. | Installed EasyPQP 0.1.59 help rerun; original public library-based report re-filtered to 771x3. |
| Output listing, duplicate command, no self-test data | P2 | Added 2.6.1 output files and `report.log.txt`; removed duplicate full command; shipped a tiny synthetic Parquet fixture and its deterministic generator. | Fixture run yields 2x2, excludes global-only low-confidence group, and changes zero to NaN before log2. |

Final exact-commit audit: `F:\OpenScience\audits\bio-proteomics-dia-analysis\eval_report_bio-proteomics-dia-analysis_result.json` (92/100, Production Ready; `auditor_independent: false`).
