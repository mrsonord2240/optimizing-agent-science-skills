#!/bin/bash
# Input 5 (stress/adversarial, regression of pre-fix input 7): "paired-end capture BAM with duplex UMIs in RX: dedup with the UMIs, consensus,
# duplex if possible". The fixer's rewritten umi_tools block and fgbio block are extracted VERBATIM and run on the real nf-core UMI BAM
# (unsorted, no @HD, dash-joined RX). Asserts by output: record counts, empty-output guard exit status, MI /A /B suffix counts,
# consensus reads are unmapped, adjacency->duplex still crashes as the comment says, SetMateInformation route equals fixmate route.
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in05; mkdir in05; cd in05
U=$D/test.paired_end.umi_unsorted.bam
strip() { sed 's/\x1b\[[0-9;]*m//g'; }
echo "records $(samtools view -c $U); with RX $(samtools view $U | grep -c 'RX:Z'); with CB $(samtools view $U | grep -c 'CB:Z')"
echo "### 5a umi_tools section text: 'sorted and indexed' + --paired claim numbers"
grep -n "5689\|2805" $SK/SKILL.md | cut -c1-200
echo "### 5b claim replication: unsorted -> error; sorted no --paired -> 2805; --paired -> 5689"
umi_tools dedup --stdin=$U --stdout=d0.bam --extract-umi-method=tag --umi-tag=RX --method=directional 2>&1 | tail -1
samtools sort -o u.cs.bam $U; samtools index u.cs.bam
umi_tools dedup --stdin=u.cs.bam --stdout=d1.bam --extract-umi-method=tag --umi-tag=RX --method=directional >/dev/null 2>&1; echo "  sorted, no --paired: $(samtools view -c d1.bam) records"
umi_tools dedup --stdin=u.cs.bam --stdout=d2.bam --paired --extract-umi-method=tag --umi-tag=RX --method=directional >/dev/null 2>&1; echo "  sorted, --paired:    $(samtools view -c d2.bam) records"
echo "### 5c the umi_tools code block, verbatim, in a dir where cellranger_possorted.bam = the sorted+indexed UMI BAM (NO CB/UB tags) and raw.bam = the unsorted UMI BAM"
mkdir -p ut; cd ut
cp ../u.cs.bam cellranger_possorted.bam; cp ../u.cs.bam.bai cellranger_possorted.bam.bai; cp $U raw.bam
blk "### umi_tools dedup" 1 > ut_block.sh; echo "[block: $(wc -l < ut_block.sh) lines]"
bash ut_block.sh > ut.out 2> ut.err; rc=$?
echo "  block exit (last command) = $rc; tag pre-check output line: $(head -1 ut.out)"
echo "  dedup.bam (overwritten by the bulk step) records: $(samtools view -c dedup.bam); sorted.bam indexed: $(ls sorted.bam.bai)"
echo "  --- guard in isolation, scRNA part only:"
sed -n '1,/^test /p' ut_block.sh | grep -v '^$' > sc_part.sh
rm -f dedup.bam; bash sc_part.sh > sc.out 2> sc.err; echo "  scRNA part exit=$? (must be non-zero: no CB tags -> empty output); dedup.bam records $(samtools view -c dedup.bam); grep-count line: $(head -1 sc.out)"
cd ..
echo "### 5d fgbio block, verbatim, in a dir with raw.bam = the UMI BAM"
mkdir -p fg; cd fg; cp $U raw.bam
blk "### fgbio consensus (bulk UMI / ctDNA, best practice for low-VAF detection)" 1 > fg_block.sh; echo "[block: $(wc -l < fg_block.sh) lines]"
bash -e fg_block.sh > fg.out 2> fg.err; rc=$?; echo "  block exit=$rc"; strip < fg.err | grep -iE 'exception|error' | head -3
for f in mated grouped consensus grouped_duplex duplex; do echo "  $f.bam records: $(samtools view -c $f.bam)"; done
echo "  grouped MI groups: $(samtools view grouped.bam | grep -o 'MI:Z:[0-9/AB]*' | sort -u | wc -l); grouped_duplex records with /A|/B: $(samtools view grouped_duplex.bam | grep -c 'MI:Z:[0-9]*/[AB]') of $(samtools view -c grouped_duplex.bam)"
echo "  consensus.bam: mapped reads (flag!=4 & !=77/141): $(samtools view -F 4 consensus.bam | wc -l); unmapped: $(samtools view -f 4 consensus.bam | wc -l) of $(samtools view -c consensus.bam)  [Skill: 'written unmapped']"
echo "  duplex.bam:    mapped reads: $(samtools view -F 4 duplex.bam | wc -l); unmapped: $(samtools view -f 4 duplex.bam | wc -l) of $(samtools view -c duplex.bam)"
echo "  consensus per-base tags on first read: $(samtools view consensus.bam | head -1 | tr '\t' '\n' | sed -n '12,40p' | cut -c1-6 | tr '\n' ' ')"
echo "### 5e the alternative named in the block: fgbio SetMateInformation on queryname input instead of fixmate -m"
samtools sort -n -o qn.bam raw.bam
fgbio SetMateInformation -i qn.bam -o smi.bam 2>&1 | strip | tail -1
fgbio GroupReadsByUmi -i smi.bam -o g_smi.bam --strategy=adjacency --edits=1 --raw-tag=RX 2>&1 | strip | tail -1
echo "  SetMateInformation route: $(samtools view -c g_smi.bam) records, $(samtools view g_smi.bam | grep -o 'MI:Z:[0-9/AB]*' | sort -u | wc -l) MI groups   | fixmate -m route: $(samtools view -c grouped.bam) records, $(samtools view grouped.bam | grep -o 'MI:Z:[0-9/AB]*' | sort -u | wc -l) MI groups"
echo "### 5f comment claims: duplex on ADJACENCY-grouped reads crashes; GroupReadsByUmi with NO mate info fails with the table's message"
fgbio CallDuplexConsensusReads -i grouped.bam -o dbad.bam --min-reads 1 1 0 2>&1 | strip | grep -m2 -iE 'exception|error'
echo "  (exit ${PIPESTATUS[0]})"
fgbio GroupReadsByUmi -i qn.bam -o nomq.bam --strategy=adjacency --edits=1 --raw-tag=RX 2>&1 | strip | grep -m1 -F 'Mate mapping quality (MQ) tag not present'; echo "  MQ message present: $?  (0 = yes)"
echo "  MQ tag counts after fixmate -m: reads with MQ $(samtools view mated.bam | grep -c 'MQ:i') of $(samtools view -c mated.bam) ; raw $(samtools view raw.bam | grep -c 'MQ:i')"
cd ..
echo "### 5g claims retained from the first audit: --method=unique keeps more; samtools markdup --barcode-tag RX (added 1.16)"
umi_tools dedup --stdin=u.cs.bam --stdout=d3.bam --paired --extract-umi-method=tag --umi-tag=RX --method=unique >/dev/null 2>&1; echo "  --paired unique: $(samtools view -c d3.bam) vs directional $(samtools view -c d2.bam)"
samtools sort -n -o u.ns.bam $U; samtools fixmate -m u.ns.bam u.fm.bam; samtools sort -o u.fmcs.bam u.fm.bam
samtools markdup u.fmcs.bam m0.bam; samtools markdup --barcode-tag RX u.fmcs.bam m1.bam; echo "  markdup flagged without barcode $(flagged m0.bam), with --barcode-tag RX $(flagged m1.bam)"
grep -o 'barcode-tag RX. (UMI[^)]*)' $SK/SKILL.md | head -1
