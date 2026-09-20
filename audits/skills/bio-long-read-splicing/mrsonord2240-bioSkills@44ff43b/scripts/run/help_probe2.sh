#!/bin/bash
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
O=/mnt/openscience/audits/bio-long-read-splicing/run/logs
micromamba run -n as-lr isoquant --full_help > $O/isoquant_full_help.txt 2>&1
for s in organize_gene_info_by_chr simplify_alignment_info organize_alignment_info_by_gene_and_chr detect_splicing_events create_gtf_from_asm_definitions count_reads_for_asms; do
  micromamba run -n as-rmatslong rmats-long ${s}.py --help > $O/rmatslong_${s}_help.txt 2>&1
done
micromamba run -n as-lr minimap2 2>&1 | head -0
micromamba run -n as-lr pip download isoquant --no-deps -d /tmp/pipchk 2>&1 | tail -3 > $O/pip_isoquant.txt
micromamba run -n as-lr pip download flair-brookslab --no-deps -d /tmp/pipchk 2>&1 | tail -3 >> $O/pip_isoquant.txt
cat /home/sci/micromamba/envs/as-sqanti/share/sqanti3-6.0.2-1/src/utilities/filter/filter_default.json > $O/sqanti_filter_default.json
