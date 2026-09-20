#!/bin/bash
# Picard's raw SUMMARY text for the new fixtures where matrix_new.py parsed no ERROR lines
D=/mnt/openscience/audits/bio-alignment-validation/run/data/new
for f in n_mate_other_chrom n_qual_out_of_range; do
  echo "=== $f (no R)"; picard ValidateSamFile I=$D/$f.bam MODE=SUMMARY 2>&1 | grep -v -E 'INFO|^$' | head -12 | cut -c1-200
done
echo "=== n_md_wrong with R"; picard ValidateSamFile I=$D/n_md_wrong.bam MODE=SUMMARY R=/mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta 2>&1 | grep -v INFO | head -5
echo "=== samtools calmd (independent check that the MD edit is really wrong)"
samtools calmd $D/n_md_wrong.bam /mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta 2>/dev/null | samtools view - | cut -f1,12- | tr '\t' ' ' | grep -o 'MD:Z:[0-9A-Z^]*' | head -0
python - <<'PY'
import pysam
D="/mnt/openscience/audits/bio-alignment-validation/run/data/new/"
ref="/mnt/openscience/audit-envs/alignment-files/public-data/human/genome.fasta"
import subprocess
recomp={}
out=subprocess.run(["samtools","calmd",D+"n_md_wrong.bam",ref],capture_output=True,text=True).stdout
for l in out.splitlines():
    if l.startswith("@"): continue
    f=l.split("\t"); md=[x for x in f[11:] if x.startswith("MD:Z:")]
    recomp[(f[0],int(f[1]))]=md[0] if md else None
bad=0;tot=0
with pysam.AlignmentFile(D+"n_md_wrong.bam") as b:
    for r in b.fetch(until_eof=True):
        if r.is_unmapped or not r.has_tag("MD"): continue
        tot+=1
        if recomp.get((r.query_name,r.flag))!="MD:Z:"+r.get_tag("MD"): bad+=1
print("reads whose stored MD differs from samtools calmd recomputation:",bad,"of",tot)
PY
grep -n "NM/MD\|NM tag\|MD" /mnt/openscience/audits/bio-alignment-validation/run/skill/SKILL.md | head
grep -n "NM/MD\|NM/MD" /mnt/openscience/audits/_pre-fix-20260920/bio-alignment-validation/run/skill/SKILL.md | head -3
