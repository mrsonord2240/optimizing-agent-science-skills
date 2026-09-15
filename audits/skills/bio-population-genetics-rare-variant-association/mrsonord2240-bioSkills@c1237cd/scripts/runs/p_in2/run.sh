#!/bin/bash
# Windows R 4.4.3 (Open Science runtime) with SKAT 2.2.5 in the candidate's private library.
set -uo pipefail
R=/f/OpenScience/runtime/envs/.r
export PATH=$R:$R/Library/mingw-w64/bin:$R/Library/usr/bin:$R/Library/bin:$R/Scripts:$R/lib/R/bin/x64:$PATH
export R_LIBS_USER='F:\OpenScience\audit-envs\variant-annotation-curation-analyst\R-lib'
Rscript.exe skat.R
