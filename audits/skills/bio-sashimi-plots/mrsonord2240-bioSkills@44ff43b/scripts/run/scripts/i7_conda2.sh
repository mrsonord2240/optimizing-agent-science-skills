source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
for p in ggsashimi jutils "*ggsashimi*"; do echo "== $p"; micromamba search -c bioconda -c conda-forge --override-channels "$p" 2>&1 | tr '\r' '\n' | tail -4 | cut -c1-160; done
