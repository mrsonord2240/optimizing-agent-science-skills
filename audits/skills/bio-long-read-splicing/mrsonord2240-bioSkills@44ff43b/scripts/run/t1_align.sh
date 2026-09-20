#!/bin/bash
# Input 1/7 part A: the SKILL's minimap2 recipes on SYNTHETIC reads with planted truth (run in WSL).
# Each recipe copied from SKILL.md "Splice-Aware Alignment"; reference = synthetic chrS1.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-long-read-splicing/run
D=$R/data/synth
O=$R/out/align; mkdir -p $O
G=$D/chrS1.fa
LR="micromamba run -n as-lr"
cat_fq() { cat $D/$1/ctrl1.fastq $D/$1/ctrl2.fastq $D/$1/ctrl3.fastq; }
cat_fq hifi > $O/hifi.fq; cat_fq ontunstr > $O/ontunstr.fq; cat_fq ontstr > $O/ontstr.fq
run() { # name reads preset...
  n=$1; fq=$2; shift 2
  $LR minimap2 -ax "$@" -t 4 $G $fq 2>$O/$n.mm2.log | $LR samtools sort -o $O/$n.bam - 2>/dev/null
  $LR samtools index $O/$n.bam
  $LR python $R/junction_check.py $O/$n.bam $D/read_tx.gtf "$n :: minimap2 -ax $*"
}
# --- SKILL recipes ---
run hifi_splicehq_uf_sec   $O/hifi.fq     splice:hq -uf --secondary=no      # SKILL: HiFi
run ontunstr_splice_k14    $O/ontunstr.fq splice -k14                        # SKILL: ONT direct cDNA (unstranded, omit -uf)
run ontstr_splice_uf_k14   $O/ontstr.fq   splice -uf -k14                    # SKILL: direct RNA (stranded)
# --- contradictory recipe used by Decision Tree / usage-guide 'What the agent will do' / example pipeline: ONT cDNA with -uf
run ontunstr_splice_uf_k14 $O/ontunstr.fq splice -uf -k14
# --- SKILL 'Critical' preset claims: wrong-preset controls
run hifi_splice_k14        $O/hifi.fq     splice -uf --secondary=no          # HiFi with plain splice (SKILL: underuses quality)
run ontunstr_splicehq      $O/ontunstr.fq splice:hq                          # ONT with splice:hq (SKILL: misses true junctions)
run ontstr_splicehq_uf     $O/ontstr.fq   splice:hq -uf
