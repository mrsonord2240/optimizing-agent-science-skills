#!/usr/bin/env bash
set -euo pipefail
curl --fail --location --max-time 60 --silent --show-error 'https://bioconductor.org/packages/3.20/bioc/src/contrib/PACKAGES.gz' | gzip -dc | awk '/^Package: (ssizeRNA|PROPER)$/{show=1} show{print} /^$/{show=0}'
