#!/usr/bin/env bash
set -euo pipefail
out='/mnt/openscience/audits/bio-microbiome-amplicon-processing/work/final_pass_20260923/its'
mkdir -p "$out"
curl --fail --silent --show-error 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=KT459474.1&rettype=fasta&retmode=text' > "$out/source.fa"
micromamba run -n itsxpress python - "$out" <<'PY'
from pathlib import Path
import sys
out = Path(sys.argv[1])
seq = ''.join(x.strip() for x in (out/'source.fa').read_text().splitlines() if not x.startswith('>')).upper()
assert len(seq) >= 500, len(seq)
def rc(s): return s.translate(str.maketrans('ACGTN','TGCAN'))[::-1]
r1, r2 = seq[450:700], rc(seq[600:850])
q = 'I' * 250
with (out/'r1.fastq').open('w') as f1, (out/'r2.fastq').open('w') as f2:
    for i in range(200):
        f1.write('@ITS_%d/1\n%s\n+\n%s\n' % (i, r1, q))
        f2.write('@ITS_%d/2\n%s\n+\n%s\n' % (i, r2, q))
PY
micromamba run -n itsxpress itsxpress --fastq "$out/r1.fastq" --fastq2 "$out/r2.fastq" --region ITS2 --taxa Fungi --outfile "$out/trimmed.fastq.gz" --threads 2
micromamba run -n itsxpress python - "$out/trimmed.fastq.gz" <<'PY'
import gzip, sys
with gzip.open(sys.argv[1], 'rt') as f: lines = sum(1 for _ in f)
assert lines == 800, lines
print('ITSXPRESS_PASS merged_trimmed_reads=%d' % (lines//4))
PY
