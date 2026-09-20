source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
# usage-guide: conda install -c bioconda ggsashimi rmats2sashimiplot pygenometracks ; conda install -c bioconda jutils   (search only, nothing installed)
for p in ggsashimi rmats2sashimiplot pygenometracks jutils; do
  n=$(micromamba search -c bioconda -c conda-forge --override-channels $p 2>&1 | grep -ac "^ $p \| $p  *[0-9]"); 
  echo "== $p"; micromamba search -c bioconda -c conda-forge --override-channels "$p" 2>&1 | tr '\r' '\n' | grep -a -i "^ *$p \|No match\|Could not\|error" | head -3
done
