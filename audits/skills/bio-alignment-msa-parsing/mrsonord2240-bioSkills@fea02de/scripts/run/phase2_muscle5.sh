#!/usr/bin/env bash
set -euo pipefail
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
run=/mnt/openscience/audits/bio-alignment-msa-parsing/run
work="$run/data/muscle5"
mkdir -p "$work"
cd "$work"
muscle -align /mnt/openscience/audit-envs/alignment/public-data/msa/globins_uniprot.fasta -stratified -output ens.efa
muscle -maxcc ens.efa -output maxcc.afa 2> maxcc.stderr
muscle -addconfseq ens.efa -output ens_cc.efa
replicate=$(sed -n 's/.*best \([^ ]*\).*/\1/p' maxcc.stderr | tail -n 1)
test -n "$replicate"
python "$run/skill/examples/muscle5_column_confidence.py" ens_cc.efa "$replicate" 0.9 masked.fa | tee parser.txt
python - "$replicate" <<'PY'
from Bio import SeqIO
import sys
rows = list(SeqIO.parse('masked.fa', 'fasta'))
assert len(rows) == 8 and len({len(r.seq) for r in rows}) == 1 and len(rows[0]) > 0
print(f'MUSCLE5 PASS: replicate {sys.argv[1]}, 8 rows x {len(rows[0])} masked columns')
PY
