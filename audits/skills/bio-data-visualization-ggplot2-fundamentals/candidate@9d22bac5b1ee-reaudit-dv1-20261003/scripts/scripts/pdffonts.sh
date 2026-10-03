#!/bin/bash
# pdffonts/pdfinfo over re-audit PDFs (gg4 = ggplot2 4.0.3, gg35 = 3.5.2)
R=/mnt/openscience/audits/bio-data-visualization-ggplot2-fundamentals/reaudit-dv1-20261003/out
for d in gg4 snip4 gg35 snip35; do
  for f in $R/$d/*.pdf; do echo "== $d/$(basename $f)"; micromamba run -n dv-cli pdffonts "$f"; micromamba run -n dv-cli pdfinfo "$f" | grep "Page size"; done
done
