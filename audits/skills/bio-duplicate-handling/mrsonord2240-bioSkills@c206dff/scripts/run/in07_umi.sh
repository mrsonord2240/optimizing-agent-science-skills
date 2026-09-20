#!/bin/bash
# Input 7 (adversarial/ambiguous): "dedup my UMI-tagged BAM" -> SKILL.md 'UMI-Aware Deduplication' commands checked against tool help + run on the
# real nf-core UMI BAM (test.paired_end.umi_unsorted.bam; RX dash-joined duplex-style UMIs, unsorted, no @HD).
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in07; mkdir in07; cd in07
U=$D/test.paired_end.umi_unsorted.bam
echo "records: $(samtools view -c $U); with RX: $(samtools view $U | grep -c 'RX:Z'); sample RX: $(samtools view $U | head -1 | grep -o 'RX:Z:[A-Z-]*')"
echo "### 7a. flags in the SKILL.md umi_tools example exist in 1.1.6 help"
for f in --extract-umi-method --umi-tag --cell-tag --per-cell --method --paired --stdin --stdout; do umi_tools dedup --help 2>&1 | grep -q -- "$f" && echo "  ok $f" || echo "  MISSING $f"; done
umi_tools dedup --help 2>&1 | grep -A4 -- '--method=' | head -8
echo "### 7b. umi_tools dedup verbatim-style on the UNSORTED BAM (Skill never says sort+index first)"
umi_tools dedup --stdin=$U --stdout=d0.bam --extract-umi-method=tag --umi-tag=RX --method=directional 2>&1 | tail -3; echo "  exit=${PIPESTATUS[0]}"
echo "### 7c. sort+index, then umi_tools dedup WITHOUT --paired, and WITH --paired"
samtools sort -o u.cs.bam $U; samtools index u.cs.bam
umi_tools dedup --stdin=u.cs.bam --stdout=d1.bam --extract-umi-method=tag --umi-tag=RX --method=directional >/dev/null 2>d1.log; echo "  no --paired exit=$? records: $(samtools view -c d1.bam)"; tail -2 d1.log
umi_tools dedup --stdin=u.cs.bam --stdout=d2.bam --paired --extract-umi-method=tag --umi-tag=RX --method=directional >/dev/null 2>d2.log; echo "  --paired   exit=$? records: $(samtools view -c d2.bam)  (input $(samtools view -c u.cs.bam); TOOLS.md smoke: 15788 -> 5689)"
umi_tools dedup --stdin=u.cs.bam --stdout=d3.bam --paired --extract-umi-method=tag --umi-tag=RX --method=unique >/dev/null 2>&1; echo "  --method=unique records: $(samtools view -c d3.bam) (SKILL.md: unique treats 1-base UMI errors as distinct molecules -> should keep MORE)"
echo "### 7d. SKILL.md scRNA form (--cell-tag=CB --per-cell) on a BAM with no CB/UB tags: does it fail loudly?"
umi_tools dedup --stdin=u.cs.bam --stdout=d4.bam --paired --extract-umi-method=tag --umi-tag=RX --cell-tag=CB --per-cell --method=directional >/dev/null 2>d4.log; echo "  exit=$?"; tail -2 d4.log
echo "### 7e. samtools markdup --barcode-tag RX (SKILL.md: exact-match UMI, added 1.16)"
samtools sort -n -o u.ns.bam $U; samtools fixmate -m u.ns.bam u.fm.bam; samtools sort -o u.fmcs.bam u.fm.bam
samtools markdup u.fmcs.bam m0.bam; echo "  without barcode: flagged $(samtools view -c -f 1024 m0.bam)"
samtools markdup --barcode-tag RX u.fmcs.bam m1.bam; echo "  --barcode-tag RX: flagged $(samtools view -c -f 1024 m1.bam)  (unique-molecule reads left: $(samtools view -c -F 1024 m1.bam))"
samtools markdup --barcode-tag RX -r u.fmcs.bam m2.bam; echo "  -r: records $(samtools view -c m2.bam)"
echo "### 7f. fgbio flags in the SKILL.md commands vs 4.1.1 help"
for t in AnnotateBamWithUmis GroupReadsByUmi CallMolecularConsensusReads CallDuplexConsensusReads SetMateInformation; do echo "  -- $t"; fgbio $t --help 2>&1 | grep -E '^ *(-i|-o|-f|-s|-e|-M|--input|--output|--fastq|--strategy|--edits|--min-reads|--raw-tag|--umi-tag)' | head -12; done
