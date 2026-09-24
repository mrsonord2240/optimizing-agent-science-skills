#!/bin/bash
# Input 1 (Canonical): real ARTIC v5.3.2 nanopore BAM + BED + MN908947.3. Runs the Skill's "Basic ampliconclip Workflow" bash
# block (steps 0-4) VERBATIM from SKILL.md, on the real data copied under the block's own file names, then checks by oracle.
set -u
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
R=/mnt/openscience/audits/bio-alignment-amplicon-clipping/run
W=$R/out/i1; rm -rf $W; mkdir -p $W; cd $W
SC=$AFDATA/sarscov2
cp $SC/sars-cov-2_v5.3.2.nanopore.bam input.bam; cp $SC/v5.3.2.primer.bed primers.bed; cp $SC/MN908947.3.fasta reference.fa
cp -r $R/skill/examples examples
python $R/s1_extract_blocks.py $R/skill/SKILL.md $W/blocks
echo "== running blocks/basic_ampliconclip_workflow_1.sh verbatim"
bash -x blocks/basic_ampliconclip_workflow_1.sh > wf.out 2> wf.err; echo "workflow rc=$?"
echo "--- stdout:"; cat wf.out | cut -c1-200
echo "--- stderr tail (non-trace):"; grep -v '^+' wf.err | head -20 | cut -c1-200
