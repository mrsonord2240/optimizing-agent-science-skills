#!/bin/bash
# Misc SKILL claims: (1) calmd with wrong reference -> message, exit code, MD absent; (2) iVar trim on an unindexed BAM;
# (3) leftover 'BAQ depends on MD' wording in the shipped example; (4) SKILL/usage-guide/example line counts vs pre-fix; (5) __pycache__ hygiene.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run; W=$R/out/i8; rm -rf $W; mkdir -p $W; cd $W
SC=$AFDATA/sarscov2; ART=$SC/sars-cov-2_v5.3.2.nanopore.bam; V5=$SC/v5.3.2.primer.bed
echo "== (1) calmd with a wrong-contig reference"
samtools ampliconclip --both-ends --strand -b $V5 $ART -o c.bam 2>/dev/null
samtools calmd -b c.bam $SC/genome.fasta > wrong.bam 2> wrong.err; echo "calmd rc=$?  stderr first line: $(head -1 wrong.err | cut -c1-120)  records $(samtools view -c wrong.bam)  MD tags $(samtools view wrong.bam | grep -c 'MD:Z:')"
echo "== (2) iVar on an UNINDEXED coordinate-sorted BAM (SKILL says it needs sorted, indexed input)"
cp $ART noidx.bam; rm -f noidx.bam.bai
ivar trim -i noidx.bam -b $V5 -p noidx_out -q 0 -m 1 2>&1 | grep -aiE 'Trimmed|index|rror|Found' | head -4; echo "records out: $(samtools view -c noidx_out.bam 2>/dev/null)"
echo "== (3) leftover BAQ/MD wording"
grep -n -i 'baq' $R/skill/SKILL.md $R/skill/usage-guide.md $R/skill/examples/ampliconclip_workflow.sh | cut -c1-250
echo "== (4) sizes"
wc -l $R/skill/SKILL.md $R/skill/usage-guide.md $R/skill/examples/*
echo "== (5) pycache under skill copies (must be none)"
find $R/skill -name __pycache__ | wc -l
