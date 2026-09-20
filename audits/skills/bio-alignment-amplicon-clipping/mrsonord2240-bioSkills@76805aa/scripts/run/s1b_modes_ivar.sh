#!/bin/bash
# Input 1 cont.: (a) oracle on workflow output, (b) 4 flag sets on the real ARTIC BAM -> reproduces the SKILL "Choosing the Clip Mode"
# table (3-prime residual %) with the shipped checker AND an independent inline pysam count, NOT CLIPPED/--clipped/--fail numbers,
# (c) iVar block from SKILL.md verbatim + its claims.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run
W=$R/out/i1; cd $W
echo "== (a) oracle"; python $R/s1_oracle.py $W
echo "== (b) modes on real ARTIC (input $(samtools view -c input.bam) reads)"
run() { tag=$1; shift; echo "-- $tag: samtools ampliconclip $*"; samtools ampliconclip "$@" -b primers.bed input.bam -o m_$tag.bam 2>&1 | grep -E 'TOTAL CLIPPED|NOT CLIPPED|WRITTEN|FILTERED|FAILED' | tr '\n' ' '; echo
  samtools sort -o ms_$tag.bam m_$tag.bam; python examples/check_primer_residual.py ms_$tag.bam primers.bed; echo "   checker rc=$?"; }
run default; run strand --strand; run both --both-ends; run both_strand --both-ends --strand
echo "-- independent count (no shipped code): 3' end inside an opposite-strand primer"
python $R/s1_indep_residual.py
echo "-- --clipped / --fail / --original / --keep-tag / --primer-counts / --tolerance"
samtools ampliconclip --both-ends --strand --clipped -b primers.bed input.bam -o c_clipped.bam 2>&1 | grep -E 'NOT CLIPPED|FILTERED|WRITTEN' | tr '\n' ' '; echo; echo "   --clipped records: $(samtools view -c c_clipped.bam)"
samtools ampliconclip --strand --clipped -b primers.bed input.bam -o c_clipped_s.bam 2>&1 | grep -E 'NOT CLIPPED|FILTERED|WRITTEN' | tr '\n' ' '; echo; echo "   --strand --clipped records: $(samtools view -c c_clipped_s.bam)"
samtools ampliconclip --both-ends --strand --fail -b primers.bed input.bam -o c_fail.bam 2>&1 | grep -E 'FAILED|WRITTEN' | tr '\n' ' '; echo; echo "   --fail: QCFAIL(0x200) reads: $(samtools view -c -f 512 c_fail.bam) of $(samtools view -c c_fail.bam)"
samtools ampliconclip --both-ends --strand --original -b primers.bed input.bam -o c_orig.bam 2>/dev/null; echo "   --original: reads with OA tag $(samtools view c_orig.bam | grep -c 'OA:Z:')"
samtools ampliconclip --both-ends --strand --keep-tag -b primers.bed input.bam -o c_keep.bam 2>/dev/null; echo "   --keep-tag: reads with NM $(samtools view c_keep.bam | grep -c 'NM:i:'); raw default output NM: $(samtools view m_both_strand.bam | grep -c 'NM:i:'); input NM: $(samtools view input.bam | grep -c 'NM:i:')"
samtools ampliconclip --both-ends --strand --primer-counts pc.bedgraph -b primers.bed input.bam -o /dev/null 2>/dev/null; echo "   --primer-counts: $(wc -l < pc.bedgraph) lines; head: $(head -2 pc.bedgraph | tr '\n' ' ')"
for t in 0 5 20; do echo "   --tolerance $t: $(samtools ampliconclip --both-ends --strand --tolerance $t -b primers.bed input.bam -o /dev/null 2>&1 | grep -E 'NOT CLIPPED|TOTAL CLIPPED' | tr '\n' ' ')"; done
echo "   header of raw output: $(samtools view -H m_both_strand.bam | head -1)"; samtools index m_both_strand.bam 2>&1 | head -1 | cut -c1-120
echo "== (c) iVar block VERBATIM (blocks/sars_cov_2_artic_comparison_1.sh)"
cat blocks/sars_cov_2_artic_comparison_1.sh
bash blocks/sars_cov_2_artic_comparison_1.sh 2>&1 | grep -aE 'Trimmed|Found|Error|rror' | head
echo "   ivar_trimmed.bam records: $(samtools view -c ivar_trimmed.bam)"
samtools sort -o ivar_s.bam ivar_trimmed.bam; samtools index ivar_s.bam
python examples/check_primer_residual.py ivar_s.bam primers.bed --three-prime; echo "   ivar residual rc=$?"
samtools view ivar_s.bam | awk '{print $1"\t"$2"\t"$4"\t"$6}' | sort > ivar.tsv
samtools ampliconclip --both-ends --strand --clipped -b primers.bed input.bam 2>/dev/null | samtools view - | awk '{print $1"\t"$2"\t"$4"\t"$6}' | sort > ac.tsv
echo "   ivar records $(wc -l < ivar.tsv), ampliconclip --both-ends --strand --clipped records $(wc -l < ac.tsv), identical (name,flag,pos,cigar) $(comm -12 ivar.tsv ac.tsv | wc -l)"
echo "-- iVar defaults (no -q/-m):"; ivar trim -i input.bam -b primers.bed -p ivar_def 2>&1 | grep -aE 'Trimmed|Found|Error|quality|Minimum' | head -6; echo "   default records: $(samtools view -c ivar_def.bam)"
echo "-- iVar -e (include reads with no primers), -q 0 -m 1:"; ivar trim -e -i input.bam -b primers.bed -p ivar_e -q 0 -m 1 2>&1 | grep -aE 'Trimmed' ; echo "   -e records: $(samtools view -c ivar_e.bam)"
echo "-- iVar trim option help:"; ivar trim 2>&1 | grep -aE '^ *-(q|m|e|s|b|i|p) ' | head -12
