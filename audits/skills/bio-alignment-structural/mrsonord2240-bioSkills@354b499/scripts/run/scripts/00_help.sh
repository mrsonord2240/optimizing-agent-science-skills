# Verify every flag the Skill uses against the installed tools' --help. Run via wsl_run.sh
cd /mnt/openscience/audits/bio-alignment-structural/run/work
echo "=== TMalign banner/flags"; TMalign </dev/null 2>&1 | head -60
echo "=== USalign flags"; USalign -h </dev/null 2>&1 | grep -aE "^\s+-(mm|ter|a |L|outfmt|byresi|mol|o |I |TMcut|se|infmt)" | head -40
echo "=== foldseek versions"; foldseek version </dev/null; foldmason version </dev/null
