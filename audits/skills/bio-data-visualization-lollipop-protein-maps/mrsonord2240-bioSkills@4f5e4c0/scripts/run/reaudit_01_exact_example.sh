#!/usr/bin/env bash
# Re-run the exact committed lollipop example in a disposable directory.
# Usage: bash reaudit_01_exact_example.sh
set -euo pipefail

WORKTREE='/f/OpenScience/wt/data-visualization-lollipop-protein-maps'
AUDIT='/f/OpenScience/audits/bio-data-visualization-lollipop-protein-maps'
OUT="$AUDIT/run/reaudit_exact_example"
GUARD='/f/OpenScience/external/mrsonord2240__bioSkills/proteomics/ptm-analysis/scripts/cli_windows_cleanup_guard.Rprofile'

rm -rf "$OUT"
mkdir -p "$OUT"
test "$(git -C "$WORKTREE" rev-parse HEAD)" = 'e526c0d363d7c07ed2c923074217f6689282564b'
cp "$WORKTREE/data-visualization/lollipop-protein-maps/examples/lollipop_phd.R" "$OUT/lollipop_phd.R"

(
  cd "$OUT"
  export R_PROFILE_USER="$GUARD"
  export CLI_WINDOWS_CLEANUP_GUARD_RECEIPT="$OUT/cli_guard_receipt.txt"
  /f/OpenScience/audit-envs/data-visualization/r.sh lollipop_phd.R
) 2>&1 | tee "$OUT/example.log"

for f in TP53_lollipop.pdf TP53_lollipop_subtype.pdf TP53_trackviewer.pdf TP53_lollipop.html; do
  test -s "$OUT/$f"
done
test ! -e "$OUT/Rplots.pdf"
test -s "$OUT/cli_guard_receipt.txt"
grep -Eq 'g3Lollipop|g3viz' "$OUT/TP53_lollipop.html"
for f in "$OUT"/*.pdf; do
  pdftotext "$f" - >/dev/null
done
printf 'OUTPUT_BYTES\n'
wc -c "$OUT"/TP53_lollipop.pdf "$OUT"/TP53_lollipop_subtype.pdf "$OUT"/TP53_trackviewer.pdf "$OUT"/TP53_lollipop.html
printf 'EXACT_EXAMPLE_PASS\n'
