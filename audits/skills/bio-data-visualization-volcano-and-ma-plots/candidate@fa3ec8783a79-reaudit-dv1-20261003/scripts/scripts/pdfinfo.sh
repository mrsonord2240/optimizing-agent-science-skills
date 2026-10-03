#!/bin/bash
# Page size (pts and mm) via poppler pdfinfo in WSL dv-cli. Usage: pdfinfo.sh <dir>
cd "$1"; for f in *.pdf; do echo "== $f"; micromamba run -n dv-cli pdfinfo "$f" 2>/dev/null | grep -E "Page size"; done
