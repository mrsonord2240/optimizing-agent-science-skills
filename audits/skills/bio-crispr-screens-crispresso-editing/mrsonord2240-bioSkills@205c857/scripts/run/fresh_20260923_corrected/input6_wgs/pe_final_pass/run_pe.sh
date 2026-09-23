#!/bin/bash
set -x
MSYS_NO_PATHCONV=1 docker run --rm \
  -v "F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\crispresso-editing-audit\pe_final_pass:/DATA" \
  -w /DATA pinellolab/crispresso2:latest \
  CRISPResso \
    -r1 pe_sample.fastq \
    -a GGAAACGCCCATGCAATTAGTCTATTTCTGCTGCAAGTAAGCATGCATTTGTAGGCTTGATGCTTTTTTTCTGCTTCTCCAGCCCTGGCCTGGGTCAATCCTTGGGGCCCAGACTGAGCACGTGATGGCAGAGGAAAGGAAGCCCTGCTTCCTCCAGAGGGCGTCGCAGGACAGCTTTTCCTAGACAGGGGCTAGTATGTGCAGCTCCTGCACCGGGATACTGGTTGACAAG \
    -g GGCCCAGACTGAGCACGTGA \
    --prime_editing_pegRNA_spacer_seq GGCCCAGACTGAGCACGTGA \
    --prime_editing_pegRNA_extension_seq TCTGCTATCACGTGCTCAGTCTG \
    -n pe_final_pass \
    --debug
echo "DOCKER_EXIT=$?"
