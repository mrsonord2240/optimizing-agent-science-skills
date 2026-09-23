#!/bin/bash
# Fresh Phase-2 exercise of the documented HH-suite command against a reproducible toy profile DB.
set -euo pipefail
base=/mnt/openscience/audits/bio-alignment-pairwise/run/work_hhsearch_retry
mkdir -p "$base/msa" "$base/hhm"
cd "$base"
python3 - <<'PY'
from pathlib import Path
raw = Path('/mnt/openscience/audit-envs/alignment/public-data/msa/globins_uniprot.fasta').read_text().strip().split('>')[1:]
records = []
for part in raw:
    lines = part.splitlines()
    records.append((lines[0].split()[0], ''.join(lines[1:]).upper()))
assert len(records) == 8, len(records)
for ident, sequence in records:
    key = ident.split('|')[1] if '|' in ident else ident
    Path('msa', key + '.a3m').write_text('>' + key + '\n' + sequence + '\n')
assert Path('msa/P69905.a3m').exists()
PY
for x in msa/*.a3m; do hhmake -i "$x" -o "hhm/$(basename "${x%.a3m}").hhm" -v 0; done
ffindex_build -s toydb_a3m.ffdata toydb_a3m.ffindex msa
ffindex_build -s toydb_hhm.ffdata toydb_hhm.ffindex hhm
cstranslate -f -I a3m -i toydb_a3m -o toydb_cs219
hhsearch -i msa/P69905.a3m -d toydb -o query.hhr -v 0
grep -E '^\s*[0-9]+\s+' query.hhr | head -8
python3 - <<'PY'
import re
s = open('query.hhr').read()
rows = [line for line in s.splitlines() if re.match(r'^\s*\d+\s+', line)]
assert len(rows) >= 8, len(rows)
self_row = next(line for line in rows if 'P69905' in line)
assert '100.0' in self_row, self_row
print('PASS hhsearch documented command generated 8+ ranked hits and a 100.0-probability HBA self-hit')
PY
