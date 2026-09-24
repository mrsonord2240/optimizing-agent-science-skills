# Fix log: bio-metabolomics-msdial-preprocessing (2026-09-16)

Commit: `a1d795a` on `fix/r2-metab-b` (worktree `F:\OpenScience\wt\metab-b`).

Real MS-DIAL console installed at
`F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\tools\msdial-console\MSDIALCUI.exe`
(5.5.260820). Ran it end to end (not just `--help`) on a real DDA mzML file
(`F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\public-work\mzml\dda\LFQ_Astral_DDA_5min_250pg_Condition_A_REP1.mzML`,
copied to scratchpad), producing a genuine `AlignResult-*.mdalign` export, then
ran the corrected R and Python import/filter code (from SKILL.md, verbatim)
against that real output and checked the numbers by hand (96 features, 1
sample column detected, 94/96 real MS/MS-assigned, intensity range
5056-134010) -- not just exit codes.

| Finding | Priority | Change | Verified | Notes |
| --- | --- | --- | --- | --- |
| `MsdialConsoleApp lcmsdda`/`lcmsdia` do not exist | P1 | Renamed to real binary `MSDIALCUI.exe`, real subcommand `lcms` (one token for DDA+DIA); `MsdialConsoleApp` naming noted as retired pre-5.x console | ran (`MSDIALCUI.exe`, `lcms --help`, and a full real `lcms` run producing real output) | |
| SKILL.md never says how DDA vs DIA is actually chosen in the real console | P1 (same finding, Input 2) | Documented the real mechanism: per-file `acquisition_type` column in a CSV passed to `-i` | docs (official MS-DIAL 5 console tutorial, systemsomicslab.github.io/msdial5tutorial) + ran (CSV `-i` accepted with no parse error by the real console) | Could not empirically force true DIA/SWATH behavior (no DIA/ABF data available); mechanism is sourced from the current MSDIALCUI-specific tutorial, not the old console docs |
| "MS-DIAL 5-alpha excludes GC-MS" / GC-EI needs MS-DIAL 4 | P1 | Removed; `gcms` documented as real and working in the installed 5.5.260820 | ran (`gcms --help` prints real `-i/-o/-m` option list; `MsdialGcMsApi.dll` ships in the release) | |
| Silent MSI-level bug porting the R filter idiom to Python (pandas auto-bool-cast) | P1 | Added explicit `.astype(str).str.strip().str.lower() == 'true'` guard for the Python path | ran (on synthetic data reproducing the cast) | Also covers the newly-found True/False case issue below |
| No "When NOT to use" section | P2 | Added, pointing to the four already-cross-referenced sibling Skills | n/a (structural) | |
| Parameter file uses `Key=Value` | not in report, found while fixing P1-1 | Corrected to real `Key: Value` (colon) syntax | ran (accepted by the real console with no parse error) + docs (official MS-DIAL 5 method-file reference, Jiung-Wen/msdial `lcms_param`) | |
| Real console writes `AlignResult-<timestamp>.mdalign`, not `AlignResult.txt` | not in report, found while fixing P1-1 | Import code now globs for `AlignResult-*.mdalign` | ran (real console run) | |
| Real "Fill %" column is a 0-1 fraction, not 0-100 | not in report, found while fixing P1-1 | All `>= 70` thresholds (R, Python, thresholds table, failure modes, Common Errors) changed to `>= 0.70` | ran (real console output: `Fill % = 1.00` for a fully-detected feature) | |
| Real "MS/MS assigned" value is `True`/`False` (title case), not `TRUE`/`FALSE` | not in report, found while fixing P1-1 | R/Python filters compare case-insensitively | ran (real console output; old exact-case check gave 0/96 matches, fixed check gave 94/96) | |
| "Everything after the last known metadata column is a sample column" breaks on real output (extra annotation/QC columns intervene) | not in report, found while fixing P1-1 | Replaced with an anchor on the header block's `Class` label cell (R and Python) | ran (both against a real 36-column MS-DIAL export and against an updated synthetic fixture reproducing the same layout) | This was silently pulling text columns (dot-product scores, spectra text) into what should be a numeric intensity matrix |
| Shipped example script used the old (wrong) Fill%/case/column conventions | not in report | Rewrote `examples/process_msdial_output.R` to emit and detect the real conventions above | ran (Rscript `parse()` + full execution) | |

All findings from the report and from AUDIT.md's top line for this Skill are
fixed. Nothing left unfixed.

## Final pass — 2026-09-24

Exact source commit: `e857587ffaea6bb9bb8c00787b3f562d5bb6f6a5` on
`agent/finalpass-bio-metabolomics-msdial-preprocessing-20260924`.

| Finding | Priority | Change | Verification |
| --- | --- | --- | --- |
| Targeted MRM/SRM/PRM requests had no explicit boundary | P2 | Added a decision-tree route, a `When NOT to Use` boundary, Related Skills entry, and usage-guide prompt pointing fixed target panels to `metabolomics/targeted-analysis`; stated that console `-t`/`--target` does not supply calibration, co-eluting internal standards, or validation. | Exact-source contract checks passed across SKILL.md, usage-guide.md, and the sibling targeted-analysis Skill. |
| `Key=Value` or a misspelled method key can exit 0 while silently using defaults | P1 | Added an explicit warning and a pre-batch acceptance protocol: change one safe known key on representative data, verify the expected feature-count response, and retain both method files and counts. Added the same recovery to Common Errors and usage guide. | Exact-source contract checks passed; the preserved real-export Python regression also passed: 16,437 features, `CondA`/`CondB` matrix, and 6,887 dtype-safe MS/MS-supported features. |
| DIA CSV behavior was described more conclusively than local evidence supported | P2 | Kept the official-tutorial CSV guidance but explicitly marked true DIA/ABF MS2Dec behavior as not locally exercised; users must retain inputs/methods and inspect representative deconvolved spectra before interpretation. | Exact-source contract checks passed in both SKILL.md and usage guide. |

Final audit: 10 scenario areas (7 archived areas rechecked, 3 fresh); 23/23
assertions passed. A fresh MS-DIAL-console or R run was not claimed because neither
runtime is installed in the final-pass worker.
