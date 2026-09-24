#!/usr/bin/env bash
set -euo pipefail
base=/mnt/openscience/audits/bio-data-visualization-multipanel-figures/run/multipanel_fix_20260923

check_pdf() {
  local file="$1"
  echo "--- $file ---"
  pdfinfo "$file" | grep -E 'Pages:|Page size:'
  pdffonts "$file"
  test "$(pdffonts "$file" | grep -c 'Type 3')" -eq 0
  test "$(pdffonts "$file" | grep -E -c 'TrueType|CID TrueType')" -gt 0
  pdftoppm -png -r 100 -singlefile "$file" "${file%.pdf}" >/dev/null
  test -s "${file%.pdf}.png"
}

for f in "$base"/out_r/*.pdf "$base"/out_py/*.pdf; do
  check_pdf "$f"
done

# 183 x 140 mm = 518.74 x 396.85 pt. Windows cairo quantises its MediaBox to
# whole points; matplotlib retains fractional points. Both begin from the exact
# 183 x 140 mm API constants, and each backend gets its measured tolerance.
for f in "$base"/out_r/Figure1.pdf "$base"/out_py/multipanel_2x2.pdf "$base"/out_py/multipanel_mosaic.pdf; do
  size=$(pdfinfo "$f" | awk -F: '/Page size:/ {print $2}')
  echo "$f ::$size"
  python3 - "$size" <<'PY'
import re, sys
n = [float(x) for x in re.findall(r"[0-9.]+", sys.argv[1])[:2]]
tolerance = 1.0 if all(x.is_integer() for x in n) else 0.1
assert len(n) == 2 and abs(n[0] - 518.74) <= tolerance and abs(n[1] - 396.85) <= tolerance, n
PY
done

echo 'PDF verification PASS'
