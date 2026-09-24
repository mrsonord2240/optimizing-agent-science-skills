#!/bin/bash
# Input 6 (Stress, NEW): PacBio-HiFi-like full-length 16S amplicons (SYNTHETIC; see s6_make_hifi.py). The fixer did not test HiFi.
# minimap2 -ax map-hifi -> Skill workflow block (verbatim) + 4 flag sets + shipped example + iVar; residual by shipped checker AND independent count.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run; D=$R/data; W=$R/out/i6; rm -rf $W; mkdir -p $W; cd $W
python $R/s6_make_hifi.py
minimap2 -ax map-hifi --secondary=no -t 4 $D/hifi_ref.fa $D/hifi_reads.fq 2> mm2.err | samtools sort -o aln.bam -; samtools index aln.bam
echo "aligned: $(samtools view -c -F 4 aln.bam) mapped of $(samtools view -c aln.bam); supplementary $(samtools view -c -f 2048 aln.bam)"
samtools view aln.bam | awk '{n++; s+=length($10)} END{print "mean read length", s/n}'
echo "aligned CIGAR: reads with leading/trailing S (aligner soft clips) $(samtools view aln.bam | awk '$6 ~ /^[0-9]+S|S$/' | wc -l)"
cp aln.bam input.bam; cp aln.bam.bai input.bam.bai; cp $D/hifi_primers.bed primers.bed; cp $D/hifi_ref.fa reference.fa; samtools faidx reference.fa
cp -r $R/skill/examples examples
echo "== Skill workflow block VERBATIM (steps 0-4)"
python $R/s1_extract_blocks.py $R/skill/SKILL.md $W/blocks > /dev/null
bash blocks/basic_ampliconclip_workflow_1.sh > wf.out 2> wf.err; echo "workflow rc=$?"; grep -v '^COMMAND' wf.out | cut -c1-160; grep -v '^+' wf.err | head -5
echo "== modes (shipped checker + independent count)"
run() { tag=$1; shift; echo "-- $tag: samtools ampliconclip $*"; samtools ampliconclip "$@" -b primers.bed input.bam -o m_$tag.bam 2>&1 | grep -E 'TOTAL CLIPPED|NOT CLIPPED|WRITTEN' | tr '\n' ' '; echo
  samtools sort -o ms_$tag.bam m_$tag.bam; python examples/check_primer_residual.py ms_$tag.bam primers.bed --three-prime; echo "   checker rc=$?"; }
run default; run strand --strand; run both --both-ends; run both_strand --both-ends --strand
python - <<'PY'
import pysam
prim = [l.rstrip("\n").split("\t") for l in open("primers.bed")]
P = [(p[0], int(p[1]), int(p[2]), p[5]) for p in prim]
for tag in ["default", "strand", "both", "both_strand"]:
    n = res5 = res3 = 0
    for r in pysam.AlignmentFile(f"m_{tag}.bam").fetch(until_eof=True):
        n += 1; c, s0, e0 = r.reference_name, r.reference_start, r.reference_end
        five = s0 if not r.is_reverse else e0 - 1; three = e0 - 1 if not r.is_reverse else s0
        res5 += any(pc == c and ps <= five < pe and st == ("-" if r.is_reverse else "+") for pc, ps, pe, st in P)
        res3 += any(pc == c and ps <= three < pe and st == ("+" if r.is_reverse else "-") for pc, ps, pe, st in P)
    print(f"  independent {tag:12s} n={n} 5' residual={res5} 3' residual={res3} ({100*res3/n:.1f}%)")
PY
echo "== shipped example, default CLIP_OPTS, on HiFi"
bash examples/ampliconclip_workflow.sh input.bam primers.bed reference.fa ex_default_final.bam > ex.out 2>&1; echo "example rc=$?"; grep -E 'TOTAL|NOT CLIPPED|records mapped|primer|ERROR' ex.out | cut -c1-160
echo "== planted-truth exact-boundary check"
python $R/s6_check.py
echo "== iVar (Skill block flags -q 0 -m 1) on HiFi"
ivar trim -i input.bam -b primers.bed -p ivar_h -q 0 -m 1 2>&1 | grep -aE 'Trimmed|Found'
samtools sort -o ivar_hs.bam ivar_h.bam; python examples/check_primer_residual.py ivar_hs.bam primers.bed --three-prime; echo "   rc=$?"
echo "== hard clip on HiFi via Quick Reference"
samtools ampliconclip --both-ends --strand --hard-clip -b primers.bed input.bam -o hard.bam 2>/dev/null; samtools view hard.bam | awk '$6 ~ /H/' | wc -l
