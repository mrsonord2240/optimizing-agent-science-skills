#!/bin/bash
for v in gg4 gg35; do cd /mnt/openscience/audits/bio-data-visualization-ggplot2-fundamentals/reaudit-dv2-20261003/out/regress_$v || continue
for f in pub_default.pdf pub_183.pdf; do echo "== $v/$f"; micromamba run -n dv-cli pdffonts "$f"; micromamba run -n dv-cli pdfinfo "$f" | grep "Page size"; done; done
