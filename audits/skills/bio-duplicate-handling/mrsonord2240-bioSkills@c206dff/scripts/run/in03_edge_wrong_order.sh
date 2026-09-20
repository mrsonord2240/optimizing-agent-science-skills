#!/bin/bash
# Input 3 (edge): wrong-order pipelines. Truth on planted_dups.bam = 100 dup reads. Records what markdup/fixmate really do
# and compares with the SKILL.md / usage-guide "Common Errors" table and "Critical pitfall" text.
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in03; mkdir in03; cd in03
cp $D/planted_dups.bam in.bam
show() { echo "   -> exit=$1  output_exists=$( [ -s $2 ] && echo yes || echo no)  dup_flagged=$(samtools view -c -f 1024 $2 2>/dev/null || echo NA)"; }
echo "### 3a. markdup on raw coordinate-sorted BAM (no fixmate at all)"
samtools markdup in.bam a.bam; show $? a.bam
echo "### 3b. fixmate WITHOUT -m, then coordinate sort, then markdup"
samtools sort -n -o ns.bam in.bam; samtools fixmate ns.bam fm_nom.bam; samtools sort -o cs_nom.bam fm_nom.bam
samtools markdup cs_nom.bam b.bam; show $? b.bam
echo "### 3c. fixmate -m on COORDINATE-sorted input (skipped the name sort)"
samtools fixmate -m in.bam c.bam; show $? c.bam
echo "### 3d. fixmate -m ok, but skip the coordinate re-sort (markdup on name-sorted)"
samtools fixmate -m ns.bam fm.bam; samtools markdup fm.bam d.bam; show $? d.bam
echo "### 3e. tags lost in a Python round-trip: strip ms,MC from a correct fixmate -m + coordinate-sorted BAM"
samtools sort -o cs.bam fm.bam
python /mnt/openscience/audits/bio-duplicate-handling/run/03_strip_tags.py cs.bam cs_strip.bam ms,MC
samtools markdup cs_strip.bam e.bam; show $? e.bam
echo "   strip only MC:"; python /mnt/openscience/audits/bio-duplicate-handling/run/03_strip_tags.py cs.bam cs_mc.bam MC; samtools markdup cs_mc.bam e2.bam; show $? e2.bam
echo "   strip only ms:"; python /mnt/openscience/audits/bio-duplicate-handling/run/03_strip_tags.py cs.bam cs_ms.bam ms; samtools markdup cs_ms.bam e3.bam; show $? e3.bam
echo "### 3f. correct pipeline control"
samtools markdup cs.bam f.bam; show $? f.bam
echo "### 3g. re-run markdup on already-marked output (idempotency) and -c clearing"
samtools markdup f.bam g.bam; show $? g.bam
samtools markdup -c f.bam g2.bam; show $? g2.bam
echo "### 3h. pre-marked real BAM (1000G HG00349 slice: 101 pre-flagged dups): re-mark without and with -c"
cp $D/HG00349.chr20_1400000-1500000.bam kg.bam
echo "   preflagged: $(samtools view -c -f 1024 kg.bam)"
samtools sort -n -o kg_ns.bam kg.bam; samtools fixmate -m kg_ns.bam kg_fm.bam; samtools sort -o kg_cs.bam kg_fm.bam
samtools markdup kg_cs.bam kg_m.bam; echo "   markdup (no -c): $(samtools view -c -f 1024 kg_m.bam)"
samtools markdup -c kg_cs.bam kg_mc.bam; echo "   markdup -c    : $(samtools view -c -f 1024 kg_mc.bam)"
picard MarkDuplicates I=kg.bam O=kg_pic.bam M=kg_pic.txt >/dev/null 2>&1; echo "   picard        : $(samtools view -c -f 1024 kg_pic.bam)  ($(grep -A1 '^LIBRARY' kg_pic.txt | tail -1 | cut -f1,3,7))"
echo "   supplementary/secondary in slice: $(samtools view -c -f 2304 kg.bam); with -S: $(samtools markdup -S kg_cs.bam kg_S.bam; samtools view -c -f 1024 kg_S.bam)"
