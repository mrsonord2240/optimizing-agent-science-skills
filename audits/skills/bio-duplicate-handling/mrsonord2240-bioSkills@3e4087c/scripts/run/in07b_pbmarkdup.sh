#!/bin/bash
# Input 7b (NEW): the pbmarkdup block, verbatim, on a SYNTHETIC HiFi-style unaligned BAM (mk_hifi.py: 60 reads x 1.2 kb, 12 planted exact duplicates).
# The Skill says the block "writes duplicate flags (0x400) into the BAM; --rmdup drops them, --dup-file keeps them in a separate file".
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in07b; mkdir in07b; cd in07b
python $RUN/mk_hifi.py
blk "### pbmarkdup (PacBio HiFi amplicons, unaligned BAM/FASTQ)" 1 > pb.sh; echo "[extracted pbmarkdup block]"; cat pb.sh
extra bash pb.sh > pb.out 2> pb.err; echo "[pbmarkdup block verbatim] exit=$? out records $(samtools view -c marked.bam 2>&1 | tail -1); flagged (0x400) $(flagged marked.bam 2>&1 | tail -1)  (truth 12 of 60)"; head -c 300 pb.err
echo "  flagged read names are the planted clones? $(samtools view -f 1024 marked.bam | cut -f1 | sed 's#.*/\([0-9]*\)/ccs#\1#' | sort -n | tr '\n' ' ')  (planted clones are ZMW 148..159)"
extra pbmarkdup --rmdup hifi.bam rm.bam 2>/dev/null; echo "[--rmdup] records $(samtools view -c rm.bam) (truth 48)"
extra pbmarkdup --dup-file dups.bam hifi.bam keep.bam 2>/dev/null; echo "[--dup-file] main out records $(samtools view -c keep.bam), dup-file records $(samtools view -c dups.bam), main flagged $(flagged keep.bam)"
extra pbmarkdup hifi.fastq fq_out.fastq 2>fq.err; echo "[FASTQ in/out] exit=$? out reads $(grep -c '^@m84011' fq_out.fastq); text 'dup' in output: $(grep -ci 'dup' fq_out.fastq)"
extra pbmarkdup --rmdup hifi.fastq fq_rm.fastq 2>/dev/null; echo "[FASTQ --rmdup] reads $(grep -c '^@m84011' fq_rm.fastq)"
extra pbmarkdup --version
