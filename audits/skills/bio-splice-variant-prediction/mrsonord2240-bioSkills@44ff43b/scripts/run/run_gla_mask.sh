#!/bin/bash
# Show the -m True masking effect on the GLA c.639+919G>A pseudoexon variant: DB with ALL transcripts (the Skill's create_db recipe keeps everything) vs DB without the NMD transcript that annotates the pseudoexon.
export PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1
AS=/mnt/openscience/audit-envs/alternative-splicing
PY=/home/sci/micromamba/envs/as-pangolin/bin
G=$AS/public-data/rnasplice/reference/genes_chrX.gtf
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
awk -F'\t' '$1=="X" && $4>=100640000 && $5<=100670000' $G > data/gla_locus_all.gtf
awk -F'\t' '$2!="nonsense_mediated_decay" && $2!="retained_intron"' data/gla_locus_all.gtf > data/gla_locus_noNMD.gtf
echo "all: $(wc -l < data/gla_locus_all.gtf) lines; no NMD/retained-intron: $(wc -l < data/gla_locus_noNMD.gtf)"
cat > data/gla_var.vcf <<'V'
##fileformat=VCFv4.2
##contig=<ID=X,length=155270560>
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
X	100654735	GLA_c.639+919G>A	C	T	.	.	.
V
$PY/python - <<'P'
import gffutils
for n in ('all', 'noNMD'):
    # Pangolin needs gene features: build them (the chrX GTF has none) via gffutils inference, as the tooling agent's DB did
    gffutils.create_db('data/gla_locus_%s.gtf' % n, 'data/gla_%s.db' % n, force=True, disable_infer_transcripts=True)
    print('built', n)
P
for n in all noNMD; do for m in True False; do
  $PY/pangolin data/gla_var.vcf $AS/public-data/derived/X.fa data/gla_$n.db out/pang_gla_${n}_m$m -d 50 -m $m 2>&1 | grep -a "WARN\|Trace\|Error" | cut -c1-200
  echo "== db=$n mask=$m: $(grep -v '^#' out/pang_gla_${n}_m$m.vcf | cut -f8 | cut -c1-200)"
done; done
