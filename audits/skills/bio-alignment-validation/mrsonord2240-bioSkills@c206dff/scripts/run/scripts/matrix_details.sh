#!/bin/bash
# Look at raw outputs behind surprising matrix cells
D=/mnt/openscience/audits/bio-alignment-validation/run/data
P=/mnt/openscience/audit-envs/alignment-files/public-data
S=/mnt/openscience/audits/bio-alignment-validation/run/skill/examples
echo "##### bitflip_mid: quickcheck / decode / picard"
samtools quickcheck -v $D/bitflip_mid.bam; echo "quickcheck rc=$?"
samtools view -c $D/bitflip_mid.bam 2>&1 | tail -2; echo "decode rc=${PIPESTATUS[0]}"
picard ValidateSamFile I=$D/bitflip_mid.bam MODE=SUMMARY 2>&1 | grep -E 'Exception|ERROR|htsjdk' | head -3
echo "##### drop_block_mid: quickcheck / decode / count"
samtools quickcheck -v $D/drop_block_mid.bam; echo "quickcheck rc=$?"
samtools view -c $D/drop_block_mid.bam; echo "decode rc=$?  (valid file had 5644)"
echo "##### lowmap_placed: picard"
picard ValidateSamFile I=$D/lowmap_placed.bam MODE=SUMMARY R=$P/human/genome.fasta 2>&1 | grep -v '^INFO' | grep -E 'Exception|ERROR|htsjdk|Caused' | head -3
echo "##### python validator on unindexed BAM (planted mate_pos_mismatch)"
python $S/validate_alignment.py $D/mate_pos_mismatch.bam 2>&1 | tail -3
echo "##### python validator on cigar_seq_mismatch"
python $S/validate_alignment.py $D/cigar_seq_mismatch.bam 2>&1 | tail -3
echo "##### quickcheck verbose forms"
samtools quickcheck -v $D/no_eof.bam; echo rc=$?
samtools quickcheck -vv $D/no_eof.bam; echo rc=$?
samtools quickcheck $D/no_eof.bam; echo "silent-form rc=$?"
echo "##### quickcheck -v *.bam > bad_bams.fofn (skill snippet)"
cd $D; samtools quickcheck -v ctl_valid.bam no_eof.bam trunc_tail.bam bitflip_mid.bam orphans.bam > /tmp/bad_bams.fofn 2>/tmp/qc_err.txt; echo "rc=$?"; echo "stdout fofn:"; cat /tmp/bad_bams.fofn; echo "stderr:"; cat /tmp/qc_err.txt
