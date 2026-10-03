#!/bin/bash
cd "$1"; for f in *.pdf; do echo "== $f"; micromamba run -n dv-cli pdffonts "$f"; done
