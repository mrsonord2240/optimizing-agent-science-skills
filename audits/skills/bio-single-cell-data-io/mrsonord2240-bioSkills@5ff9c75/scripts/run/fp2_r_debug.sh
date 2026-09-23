#!/bin/bash
# Diagnostic for the mandated R wrapper; retained as audit evidence.
set -x
export RTOOLS44_HOME="C:/rtools44"
export PATH="/f/OpenScience/runtime/envs/.r:/f/OpenScience/runtime/envs/.r/Library/bin:/f/OpenScience/runtime/envs/.r/Library/mingw-w64/bin:/f/OpenScience/runtime/envs/.r/lib/R/bin/x64:/c/rtools44/usr/bin:/c/rtools44/x86_64-w64-mingw32.static.posix/bin:$PATH"
/f/OpenScience/runtime/envs/.r/lib/R/bin/x64/Rscript.exe --version
echo "R_VERSION_EXIT=$?"
