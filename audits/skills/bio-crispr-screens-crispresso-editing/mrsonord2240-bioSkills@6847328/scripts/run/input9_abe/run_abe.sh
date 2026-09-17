#!/bin/bash
# Input 9 (new, auditor-added): real ABE quantification-window code path.
# Pre-fix and the fixer's own pass only ever exercised the CBE branch
# (--conversion_nuc_from C --conversion_nuc_to T); this input runs the ABE branch
# (--conversion_nuc_from A --conversion_nuc_to G) for the first time against real data,
# exactly mirroring the SKILL.md worked-example CLI pattern for base editors.
MSYS_NO_PATHCONV=1 docker run --rm \
  -v "F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\crispresso-editing-audit:/DATA" \
  -w /DATA pinellolab/crispresso2:latest \
  CRISPResso --fastq_r1 FANC.Cas9.fastq \
    --amplicon_seq "CGGATGTTCCAATCAGTACGCAGAGAGTCGCCGTCTCCAAGGTGAAAGCGGAAGTAGGGCCTTCGCGCACCTCATGGAATCCCTTCTGCAGCACCTGGATCGCTTTTCCGAGCTTCTGGCGGTCTCAAGCACTACCTACGTCAGCACCTGGGACCCCGCCACCGTGCGCCGGGCCTTGCAGTGGGCGCGCTACCTGCGCCACATCCATCGGCGCTTTGGTCGG" \
    --guide_seq "GGAATCCCTTCTGCAGCACC" \
    --base_editor_output \
    --conversion_nuc_from A --conversion_nuc_to G \
    --quantification_window_size 10 --quantification_window_center -10 \
    --output_folder abe_test --name input9_abe
