#!/bin/bash
# Side checks (part of input 8's evidence): gaps the fixer's text may have left.
#  11a fgbio --strategy=paired on a SINGLE-UMI RX tag (the Skill's ctDNA row says paired -> duplex without saying RX must be 'a-b')
#  11b shipped example and SKILL.md pipeline on a BAM WITHOUT @RG / RG tags (--use-read-groups)
#  11c -d 2500 on non-Illumina read names: how many warnings, and are optical duplicates then silently absent?
#  11d flags named in the Skill exist in samtools 1.24 markdup --help (--read-coords, --barcode-tag, --use-read-groups, -c, -f, -T, -l)
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in11; mkdir in11; cd in11
strip() { sed 's/\x1b\[[0-9;]*m//g'; }
echo "### 11a single-UMI RX with --strategy=paired"
python $RUN/20_make_planted_umi.py raw.bam >/dev/null
samtools view -h raw.bam | awk 'BEGIN{OFS="\t"} /^@/ {print; next} {for(i=12;i<=NF;i++) if($i ~ /^RX:Z:/){split($i,a,"[:-]"); $i="RX:Z:" a[3]} print}' | samtools view -b -o single.bam -
echo "  example RX after rewrite: $(samtools view single.bam | head -1 | grep -o 'RX:Z:[A-Z-]*')"
samtools sort -n -o qn.bam single.bam; samtools fixmate -m qn.bam mated.bam
fgbio GroupReadsByUmi -i mated.bam -o g.bam --strategy=paired --edits=1 --raw-tag=RX 2>&1 | strip | grep -iE 'exception|error|fatal|paired' | head -3; echo "  exit=${PIPESTATUS[0]}"
echo "### 11b BAM without @RG or RG tags"
python - <<'PY'
import pysam
src = pysam.AlignmentFile("/mnt/openscience/audits/bio-duplicate-handling/run/data/planted_dups.bam"); h = src.header.to_dict(); h.pop("RG", None)
print("planted_dups.bam @RG lines in source:", len(src.header.to_dict().get("RG", [])))
o = pysam.AlignmentFile("norg.bam", "wb", header=pysam.AlignmentHeader.from_dict(h))
for r in src:
    r.set_tag("RG", None); o.write(r)
o.close()
PY
mkdir p; cp norg.bam p/input.bam; ( cd p; blk "### Pipeline Version (Optimized)" 1 > p.sh; bash p.sh 2>/dev/null; echo "  SKILL.md pipeline on RG-less BAM: exit=$? flagged $(flagged marked.bam) (truth 100)" )
ASSAY=wgs bash $SK/examples/markdup_pipeline.sh norg.bam ex.bam >/dev/null 2>&1; echo "  shipped example on RG-less BAM: exit=$? flagged $(flagged ex.bam)"
echo "### 11c -d 2500 on non-Illumina names (real human test BAM: names testN:n; 5644 records)"
samtools sort -n -o hn.bam $D/test.paired_end.sorted.bam; samtools fixmate -m hn.bam hf.bam; samtools sort -o hc.bam hf.bam
samtools markdup -d 2500 hc.bam hd.bam 2> hd.err; echo "  stderr lines: $(wc -l < hd.err) 'cannot decipher' lines: $(grep -c 'cannot decipher' hd.err); dt tags emitted: $(samtools view hd.bam | grep -c 'dt:Z')  (records 5644, flagged $(flagged hd.bam))"
python - <<'PY'
import re
lines = [l for l in open("hd.err") if "cannot decipher" in l]
print("  distinct read names warned about:", len({re.search(r'read name (\S+)', l).group(1) for l in lines}))
PY
samtools markdup -d 2500 hc.bam hd2.bam 2>/dev/null; samtools markdup hc.bam hd0.bam; echo "  flagged with -d 2500: $(flagged hd2.bam), without: $(flagged hd0.bam) (same = no optical detection happened; only stderr noise)"
echo "### 11d flags named in the Skill exist in samtools 1.24"
samtools markdup 2>&1 | grep -E -- '--read-coords|--barcode-tag|--use-read-groups|^ *-c,|^ *-f,|^ *-T,|^ *-l,|^ *-d,|^ *-S,|^ *-r,|^ *-s,|^ *-t,' | cut -c1-140
grep -o 'read-coords' $SK/SKILL.md | head -1 | sed 's/^/  Skill mentions: /'
