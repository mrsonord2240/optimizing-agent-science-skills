#!/bin/bash
# usage: pdffonts.sh <dir-with-pdfs> ; run via wsl_run.sh 'bash /mnt/openscience/audits/.../pdffonts.sh <dir>'
cd "$1"; for f in *.pdf; do echo "== $f"; micromamba run -n dv-cli pdffonts "$f"; done
