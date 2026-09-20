#!/bin/bash
# Check the Skill's install line `conda install -c bioconda rmats regtools suppa shiba`: do these package names exist on bioconda, and which versions?
for p in rmats regtools suppa shiba; do
  echo "== $p"; micromamba search -c bioconda -c conda-forge --override-channels "$p" 2>&1 | grep -a -v '^$' | awk 'NR>1' | tail -4 | cut -c1-110
done
echo "== installed in as-core / as-suppa / as-shiba:"
micromamba list -n as-core 2>/dev/null | grep -a -i '^ *\(rmats\|regtools\|suppa\)' | cut -c1-100
micromamba list -n as-suppa 2>/dev/null | grep -a -i '^ *suppa' | cut -c1-100
micromamba list -n as-shiba 2>/dev/null | grep -a -i '^ *shiba' | cut -c1-100
