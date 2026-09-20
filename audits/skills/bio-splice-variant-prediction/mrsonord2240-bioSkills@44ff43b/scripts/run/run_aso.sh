#!/bin/bash
# INPUT 6: the Skill's ASO recipe step 3: "simulate splice-site occlusion impact via SpliceAI on the masked sequence".  Try to do it: replace a 22-nt window with N's.
export PYTHONDONTWRITEBYTECODE=1
AS=/mnt/openscience/audit-envs/alternative-splicing
PY=/home/sci/micromamba/envs/as-spliceai/bin
FA=$AS/public-data/derived/X.fa
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
$PY/python - <<'P'
import pyfaidx
fa = pyfaidx.Fasta('/mnt/openscience/audit-envs/alternative-splicing/public-data/derived/X.fa')
b = lambda p, n=1: fa['X'][p-1:p-1+n].seq.upper()
hdr = '##fileformat=VCFv4.2\n##contig=<ID=X,length=155270560>\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n'
rows = [('N22_all_N_at_donor', 193052, b(193052, 22), 'N' * 22),
        ('N22_anchor_plus_21N_at_donor', 193052, b(193052, 22), b(193052) + 'N' * 21),
        ('N22_anchor_plus_21N_intron_control', 193200, b(193200, 22), b(193200) + 'N' * 21)]
open('data/aso_mask.vcf', 'w', newline='\n').write(hdr + ''.join('\t'.join(['X', str(p), n, r, a, '.', '.', '.']) + '\n' for n, p, r, a in rows))
P
$PY/spliceai -I data/aso_mask.vcf -O out/sai_aso.vcf -R $FA -A grch37 -D 50 -M 0 > out/sai_aso.log 2>&1; echo "spliceai rc=$?"
grep -a "WARNING:root\|Error\|error" out/sai_aso.log | cut -c1-200
grep -v '^##' out/sai_aso.vcf | cut -f2,3,8 | cut -c1-200
