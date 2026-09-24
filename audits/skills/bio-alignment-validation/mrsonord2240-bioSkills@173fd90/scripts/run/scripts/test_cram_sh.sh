#!/bin/bash
# Follow-up: what does validate_alignment.sh print for the real CRAM when the reference cannot be resolved?
RUN=/mnt/openscience/audits/bio-alignment-validation/run
CR=/mnt/openscience/audit-envs/alignment-files/public-data/human/test.paired_end.sorted.cram
export REF_PATH=/nonexistent_ref_dir
bash $RUN/skill/examples/validate_alignment.sh $CR > /tmp/cram_sh.out 2> /tmp/cram_sh.err; echo "rc=$?"
grep -v -E '^[0-9]+ \+' /tmp/cram_sh.out | head -40
echo "--- stderr:"; cut -c1-160 /tmp/cram_sh.err
echo "--- independent: samtools view -F 2308 CRAM | head:"; samtools view -F 2308 $CR 2>&1 | head -2 | cut -c1-120
echo "--- py:"; python $RUN/skill/examples/validate_alignment.py $CR 2>&1 | head -12 | cut -c1-200; echo "py rc=${PIPESTATUS[0]}"
