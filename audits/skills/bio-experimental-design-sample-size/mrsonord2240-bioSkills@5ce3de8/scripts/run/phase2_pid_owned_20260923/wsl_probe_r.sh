#!/usr/bin/env bash
set -euo pipefail
Rscript -e 'cat(R.version.string, "\n"); for (p in c("ssizeRNA","PROPER","DESeq2","pwr")) cat(p, requireNamespace(p, quietly=TRUE), "\n")'
