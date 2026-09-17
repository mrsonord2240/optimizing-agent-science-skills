#!/bin/bash
# All console-level verification for this re-audit, run against the real,
# already-installed MSDIALCUI.exe 5.5.260820
# (F:\OpenScience\audit-envs\untargeted-metabolomics-analyst\tools\msdial-console\MSDIALCUI.exe).
# Working directory during the actual runs was a scratchpad dir containing:
#   in/LFQ_Astral_DDA_5min_250pg_Condition_A_REP1.mzML   (real LC-MS DDA data,
#   in/LFQ_Astral_DDA_5min_250pg_Condition_B_REP1.mzML    borrowed from the
#     mass-spec-proteomics-analyst candidate's public-work fixtures)
#   lcms_param.txt        -- this audit's own Key: Value param file (below)
#   filelist.csv           -- this audit's own CSV file-list (below)
# Re-run here with relative paths for the record; requires the two mzML files
# to be present under ./in/ and MSDIALCUI.exe on PATH or referenced by full path.

MSDIAL="F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/tools/msdial-console/MSDIALCUI.exe"

echo "=== Test A: bare console banner (no args) -- confirms real subcommand list ==="
"$MSDIAL"
# Result (this audit, 2026-09-16): Commands: gcms, lcms, lcimms, dims, imms, msn,
# eic, rtcorrection, imagegen. No 'lcmsdda'/'lcmsdia' token. Matches SKILL.md's
# fixed "Run MS-DIAL Headless" section exactly.

echo "=== Test B: lcms --help -- confirms real flags ==="
"$MSDIAL" lcms --help
# Result: -i/-o/-m (all REQUIRED), -p, -t/-target, -?/-h/--help. Matches
# SKILL.md's documented "MSDIALCUI.exe lcms -i <in> -o <out> -m <param.txt>" call.

echo "=== Test C: gcms --help -- confirms GC-MS is real and working in this build ==="
"$MSDIAL" gcms --help
# Result: -i/-o/-m/-p. Real, working subcommand -- confirms SKILL.md's fixed
# "GC-MS is real and working here" claim (superseding the pre-fix "5-alpha
# excludes GC-MS" defect).

echo "=== Test D: full real lcms run, single DDA file, this audit's own Key: Value param file ==="
mkdir -p out
"$MSDIAL" lcms -i ./in -o ./out -m ./lcms_param.txt
# Result: completed, wrote out/AlignResult-<timestamp>.mdalign (5,942,577 bytes,
# 11605 real features, 1 sample column). Confirms the documented AlignResult-
# <timestamp>.mdalign naming (not "AlignResult.txt"), the 4-header-row layout,
# Fill % as a 0-1 fraction, and MS/MS assigned as title-case True/False text --
# see ../data/AlignResult-real-singlesample.mdalign and
# input1_real_import_filter.R for the downstream verification.

echo "=== Test E: same run via the documented CSV -i file-list mechanism, 2 files ==="
mkdir -p out_csv
"$MSDIAL" lcms -i ./filelist.csv -o ./out_csv -m ./lcms_param.txt
# filelist.csv sets acquisition_type=DDA for both rows (no real DIA/ABF data was
# available to force true DIA behavior -- same limitation the fixer recorded).
# Result: completed, wrote out_csv/AlignResult-<timestamp>.mdalign (16442 real
# features, 2 sample columns named CondA/CondB -- taken from the CSV's
# file_name column, not the raw .mzML filenames). This goes beyond what the fix
# log verified ("CSV -i accepted with no parse error"): this is a full,
# completed 2-sample alignment run through the documented CSV mechanism.
# See ../data/AlignResult-real-multisample.mdalign and
# input5_real_multisample_filter.R / input4_real_python_import.py.

echo "=== Test F: Key: Value param actually changes behavior (sanity check before the negative test) ==="
mkdir -p out_highthresh
sed 's/Minimum peak height: 1000/Minimum peak height: 500000/' lcms_param.txt > lcms_param_highthresh.txt
"$MSDIAL" lcms -i ./in -o ./out_highthresh -m ./lcms_param_highthresh.txt
# Result: 13 features (vs 11605 at the default threshold) -- confirms the
# Key: Value param file is genuinely being read and applied, not ignored.

echo "=== Test G (NEW, not in the fix log): Key=Value (old MS-DIAL 4-style syntax) is *silently* ignored, not rejected ==="
mkdir -p out_wrongsyntax_highthresh
sed 's/Minimum peak height: 500000/Minimum peak height=500000/' lcms_param_highthresh.txt > lcms_param_highthresh_wrongsyntax.txt
"$MSDIAL" lcms -i ./in -o ./out_wrongsyntax_highthresh -m ./lcms_param_highthresh_wrongsyntax.txt
# Result: 11605 features -- IDENTICAL to the default/unmodified run, not the 13
# features the correctly-syntaxed Key: Value version produces. The console
# printed no warning or error about the unrecognized "Minimum peak
# height=500000" line; it silently fell back to the built-in default and
# completed with exit code 0. SKILL.md's Common Errors table documents that
# Key=Value causes filter/threshold problems generically, but does not warn
# that the console gives ZERO error signal when it happens -- a researcher who
# reuses an old MS-DIAL 4-style Key=Value param file gets a fully "successful"
# run with silently-wrong parameters. Flagged as a new P2 recommendation.
