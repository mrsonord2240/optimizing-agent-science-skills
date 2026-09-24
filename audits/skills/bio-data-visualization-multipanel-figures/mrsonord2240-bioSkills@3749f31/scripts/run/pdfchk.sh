#!/bin/bash
# usage: pdfchk.sh name.pdf ...  (files under audits/<skill>/out). Prints page size, fonts (poppler pdffonts), word count; writes name.bbox.html (pdftotext -bbox) for bbox.py
P=/mnt/openscience/audits/bio-data-visualization-multipanel-figures/out
for f in "$@"; do
  echo "== $f"
  MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc "cd $P && micromamba run -n dv-cli pdfinfo '$f' | grep -E 'Page size|Pages' ; micromamba run -n dv-cli pdffonts '$f'; micromamba run -n dv-cli pdftotext -bbox '$f' '${f%.pdf}.bbox.html'; echo -n 'words: '; grep -c '<word' '${f%.pdf}.bbox.html'"
done
