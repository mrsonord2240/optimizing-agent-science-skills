#!/usr/bin/env bash
set -euo pipefail
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
run=/mnt/openscience/audits/bio-alignment-msa-parsing/run
data="$run/data"
mkdir -p "$data"
hmmbuild --amino "$data/pfam.hmm" /mnt/openscience/audit-envs/alignment/public-data/msa/PF00042_seed.sto > "$data/hmmbuild_phase2.txt"
hmmalign --outformat a2m -o "$data/hmmalign_globins8.a2m" "$data/pfam.hmm" /mnt/openscience/audit-envs/alignment/public-data/msa/globins_uniprot.fasta
python - "$data/hmmalign_globins8.a2m" <<'PY'
from Bio import SeqIO
import sys
rows = list(SeqIO.parse(sys.argv[1], 'fasta'))
lengths = sorted({len(r.seq) for r in rows})
matches = {len(''.join(c for c in str(r.seq) if c.isupper() or c == '-')) for r in rows}
assert len(rows) == 8 and len(lengths) > 1 and matches == {117}, (len(rows), lengths, matches)
print(f'HMMER A2M PASS: {len(rows)} rows; lengths {lengths}; match lengths {sorted(matches)}')
PY
