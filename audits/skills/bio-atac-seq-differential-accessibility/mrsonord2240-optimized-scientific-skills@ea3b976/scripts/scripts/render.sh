#!/bin/bash
export PATH=/home/sci/.local/bin:/usr/bin:/bin:$PATH MAMBA_ROOT_PREFIX=/home/sci/micromamba
cd /mnt/openscience/audits/bio-atac-seq-differential-accessibility/reaudit-run/work; mkdir -p ../png
for c in default:d edger:e design:des sva:s; do d=${c%%:*}; p=${c##*:}
 for k in annoplot diagnostics; do micromamba run -n pdf-render-poppler pdftoppm -png -r 80 $d/${p}_$k.pdf ../png/${d}_$k; done; done
ls ../png
