#!/bin/bash
# side check for in05: the Skill quotes 5689 records; the verbatim block gave 5688 once. Is umi_tools dedup output run-to-run stable?
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W/in05
for i in 1 2 3 4 5 6; do
  umi_tools dedup --stdin=u.cs.bam --stdout=r$i.bam --paired --extract-umi-method=tag --umi-tag=RX --method=directional >/dev/null 2>&1
  echo "run $i: $(samtools view -c r$i.bam) records"
done
for i in 1 2 3; do
  umi_tools dedup --stdin=u.cs.bam --stdout=s$i.bam --paired --extract-umi-method=tag --umi-tag=RX --method=directional --random-seed=1 >/dev/null 2>&1
  echo "seeded run $i: $(samtools view -c s$i.bam) records"
done
