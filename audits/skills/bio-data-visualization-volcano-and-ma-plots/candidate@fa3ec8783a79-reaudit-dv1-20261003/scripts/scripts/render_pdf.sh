#!/bin/bash
# Rasterise every PDF in $1 to PNG (150 dpi) for visual inspection; poppler pdftoppm in WSL dv-cli.
cd "$1"; for f in *.pdf; do micromamba run -n dv-cli pdftoppm -png -r 150 -singlefile "$f" "${f%.pdf}_pdf"; done; ls *_pdf.png
