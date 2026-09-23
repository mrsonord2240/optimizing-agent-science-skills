#!/usr/bin/env bash
set -euo pipefail
Rscript -e 'cat("R=", as.character(getRversion()), "\n", sep=""); for (p in c("dplyr", "lme4", "lmerTest", "designit")) cat(p, "=", as.character(packageVersion(p)), "\n", sep="")'
