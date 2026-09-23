#!/bin/bash
# Audit-local, non-mutating alternate launcher: same supported R 4.4.3 library as
# crispr-screen-analyst/r.sh, but uses Rterm.exe rather than Rscript.exe so the
# auditor's owned process is not an Rscript PID.
export RTOOLS44_HOME="C:/rtools44"
export PATH="/f/OpenScience/runtime/envs/.r/Library/bin:/f/OpenScience/runtime/envs/.r/Library/mingw-w64/bin:/c/rtools44/usr/bin:/c/rtools44/x86_64-w64-mingw32.static.posix/bin:$PATH"
export PKG_CONFIG_PATH="/c/rtools44/x86_64-w64-mingw32.static.posix/lib/pkgconfig"
export R_MAKEVARS_USER="F:/OpenScience/audit-envs/crispr-screen-analyst/tools/r-staging/Makevars.win"
export R_LIBS_USER="F:/OpenScience/audit-envs/crispr-screen-analyst/R-lib"
exec /f/OpenScience/runtime/envs/.r/lib/R/bin/x64/Rterm.exe --vanilla --slave -f "$1" --args "${@:2}"
