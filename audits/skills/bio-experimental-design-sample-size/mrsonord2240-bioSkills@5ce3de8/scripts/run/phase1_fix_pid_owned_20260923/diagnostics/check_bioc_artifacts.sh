#!/usr/bin/env bash
set -euo pipefail
for url in \
  'https://bioconductor.org/packages/3.20/bioc/src/contrib/ssizeRNA_1.3.3.tar.gz' \
  'https://bioconductor.org/packages/3.20/bioc/src/contrib/PROPER_1.38.0.tar.gz' \
  'https://cran.r-project.org/src/contrib/pwr_1.3-0.tar.gz'; do
  echo "### ${url}"
  curl --fail --location --head --max-time 30 --silent --show-error "${url}" | sed -n '1p'
done
