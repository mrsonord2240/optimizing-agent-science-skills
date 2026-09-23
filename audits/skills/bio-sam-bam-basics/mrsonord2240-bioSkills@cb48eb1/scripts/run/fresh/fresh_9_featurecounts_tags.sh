#!/usr/bin/env bash
# Fresh Phase-2 Input 9: independently exercise the documented NH:i featureCounts behavior.
set -euo pipefail

ROOT=/mnt/openscience/audits/bio-sam-bam-basics/run
CASE="$ROOT/data/fresh9"
mkdir -p "$CASE"

cat > "$CASE/in.sam" <<'EOF'
@HD	VN:1.6	SO:coordinate
@SQ	SN:chrA	LN:200
@SQ	SN:chrB	LN:200
u1	0	chrA	11	60	20M	*	0	0	AAAAAAAAAAAAAAAAAAAA	FFFFFFFFFFFFFFFFFFFF	NH:i:1	HI:i:1
m1	0	chrA	51	3	20M	*	0	0	CCCCCCCCCCCCCCCCCCCC	FFFFFFFFFFFFFFFFFFFF	NH:i:2	HI:i:1
m1	0	chrB	51	3	20M	*	0	0	CCCCCCCCCCCCCCCCCCCC	FFFFFFFFFFFFFFFFFFFF	NH:i:2	HI:i:2
EOF
cat > "$CASE/genes.gtf" <<'EOF'
chrA	test	exon	1	200	.	+	.	gene_id "geneA";
chrB	test	exon	1	200	.	+	.	gene_id "geneB";
EOF

samtools view -b -o "$CASE/in.bam" "$CASE/in.sam"
samtools sort -o "$CASE/sorted.bam" "$CASE/in.bam"
samtools index "$CASE/sorted.bam"
micromamba run -n af-subread featureCounts -a "$CASE/genes.gtf" -o "$CASE/default.txt" "$CASE/sorted.bam" >/dev/null
micromamba run -n af-subread featureCounts -M -a "$CASE/genes.gtf" -o "$CASE/multi.txt" "$CASE/sorted.bam" >/dev/null
micromamba run -n af-subread featureCounts -M --fraction -a "$CASE/genes.gtf" -o "$CASE/fraction.txt" "$CASE/sorted.bam" >/dev/null

python - <<'PY'
from pathlib import Path
root = Path('/mnt/openscience/audits/bio-sam-bam-basics/run/data/fresh9')

def counts(name):
    rows = {}
    for line in (root / name).read_text().splitlines():
        if line and not line.startswith(('#', 'Geneid')):
            fields = line.split('\t')
            rows[fields[0]] = float(fields[-1])
    return rows

def summary(name):
    rows = {}
    for line in (root / name).read_text().splitlines():
        if line.startswith('Unassigned_MultiMapping'):
            rows['multimapping'] = int(line.split('\t')[-1])
    return rows

d, m, f = counts('default.txt'), counts('multi.txt'), counts('fraction.txt')
s = summary('default.txt.summary')
assert (d['geneA'], d['geneB']) == (1.0, 0.0), d
assert s['multimapping'] == 2, s
assert (m['geneA'], m['geneB']) == (2.0, 1.0), m
assert (f['geneA'], f['geneB']) == (1.5, 0.5), f
print('PASS default=', d, 'summary=', s, 'multi=', m, 'fraction=', f)
PY
