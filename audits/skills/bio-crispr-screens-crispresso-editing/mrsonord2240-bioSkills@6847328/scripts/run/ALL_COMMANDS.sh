#!/bin/bash
# Consolidated command log for all 9 audit inputs, bio-crispr-screens-crispresso-editing
# (fixed Skill, mrsonord2240/bioSkills@6847328).
#
# All commands executed via the Docker image pinellolab/crispresso2:latest (CRISPResso2 2.3.4),
# from F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\crispresso-editing-audit\
# (on Docker Desktop's file-sharing allowlist per TOOLS.md section 6 note #10), using the
# Windows-path -v source / MSYS_NO_PATHCONV=1 invocation documented in TOOLS.md note #11.
#
# AMPLICON (FANCF locus, CRISPResso2's own published test amplicon) and GUIDE are shared
# across inputs 1, 2, 4-1(control leg via input8), 8, 9:
AMPLICON="CGGATGTTCCAATCAGTACGCAGAGAGTCGCCGTCTCCAAGGTGAAAGCGGAAGTAGGGCCTTCGCGCACCTCATGGAATCCCTTCTGCAGCACCTGGATCGCTTTTCCGAGCTTCTGGCGGTCTCAAGCACTACCTACGTCAGCACCTGGGACCCCGCCACCGTGCGCCGGGCCTTGCAGTGGGCGCGCTACCTGCGCCACATCCATCGGCGCTTTGGTCGG"
GUIDE="GGAATCCCTTCTGCAGCACC"
HEK3_AMPLICON="GGAAACGCCCATGCAATTAGTCTATTTCTGCTGCAAGTAAGCATGCATTTGTAGGCTTGATGCTTTTTTTCTGCTTCTCCAGCCCTGGCCTGGGTCAATCCTTGGGGCCCAGACTGAGCACGTGATGGCAGAGGAAAGGAAGCCCTGCTTCCTCCAGAGGGCGTCGCAGGACAGCTTTTCCTAGACAGGGGCTAGTATGTGCAGCTCCTGCACCGGGATACTGGTTGACAAG"
HEK3_GUIDE="GGCCCAGACTGAGCACGTGA"
DOCKER_BASE='MSYS_NO_PATHCONV=1 docker run --rm -v "F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\crispresso-editing-audit:/DATA" -w /DATA pinellolab/crispresso2:latest'

# --- Input 1 (Canonical): single Cas9 amplicon, with and without --min_average_read_quality 30,
#     to independently reproduce the SKILL.md-documented 26.38%->24.89% shift.
eval $DOCKER_BASE CRISPResso --fastq_r1 FANC.Cas9.fastq --amplicon_seq "\"$AMPLICON\"" --guide_seq "\"$GUIDE\"" \
  --output_folder . --name input1_noqfilter
eval $DOCKER_BASE CRISPResso --fastq_r1 FANC.Cas9.fastq --amplicon_seq "\"$AMPLICON\"" --guide_seq "\"$GUIDE\"" \
  --min_average_read_quality 30 --output_folder . --name input1_canonical
# -> see run/input6_parse_output/test_parse_crispresso.py for the fixed parse_crispresso()
#    regression test against CRISPResso_on_input1_noqfilter.

# --- Input 2 (Variant A): CBE base-editor quantification-window code path.
eval $DOCKER_BASE CRISPResso --fastq_r1 FANC.Cas9.fastq --amplicon_seq "\"$AMPLICON\"" --guide_seq "\"$GUIDE\"" \
  --base_editor_output --conversion_nuc_from C --conversion_nuc_to T \
  --quantification_window_size 10 --quantification_window_center -10 \
  --output_folder . --name input2_cbe

# --- Input 3 (Edge, audit's index; "input4_edge" on disk): total alignment failure --
#     FANC reads against the wrong (HEK3) amplicon+guide.
eval $DOCKER_BASE CRISPResso --fastq_r1 FANC.Cas9.fastq --amplicon_seq "\"$HEK3_AMPLICON\"" --guide_seq "\"$HEK3_GUIDE\"" \
  --output_folder . --name input4_edge_wrongamplicon

# --- Input 4 (Variant B, audit's index; "input3_pooled" on disk): CRISPRessoPooled,
#     default threshold (all-NA regression) then fixed (--min_reads_to_use_region 100).
eval $DOCKER_BASE CRISPRessoPooled --fastq_r1 Both.Cas9.fastq --amplicons_file Cas9.amplicons.txt \
  --output_folder . --name input3_pooled
eval $DOCKER_BASE CRISPRessoPooled --fastq_r1 Both.Cas9.fastq --amplicons_file Cas9.amplicons.txt \
  --min_reads_to_use_region 100 --output_folder . --name input3_pooled_fixed

# --- Input 5 (Stress): CRISPRessoBatch (Untreated vs Cas9) + CRISPRessoCompare.
eval $DOCKER_BASE CRISPRessoBatch --batch_settings FANC.local.batch \
  --batch_output_folder . --name input5_batch
eval $DOCKER_BASE CRISPRessoCompare CRISPRessoBatch_on_input5_batch/CRISPResso_on_Untreated \
  CRISPRessoBatch_on_input5_batch/CRISPResso_on_Cas9 --output_folder . --name input5_compare

# --- Input 6 (Scope Boundary): parse_crispresso() rerun -- see run/input6_parse_output/.
#     CRISPRessoWGS flags checked via --help only (no reference FASTA cached for the
#     small-genome BAM; genuinely time-boxed per TOOLS.md, not a Skill defect).

# --- Input 7 (Adversarial): ABE-vs-CBE default check via --help (no CLI-level warning
#     if --conversion_nuc_from/_to are omitted with --base_editor_output).
eval $DOCKER_BASE CRISPResso --help | grep -A2 "conversion_nuc"

# --- Input 8 (NEW): shipped examples/crispresso_analysis.sh (fixed positional
#     CRISPRessoCompare syntax) run end-to-end -- see input8_shipped_script/.

# --- Input 9 (NEW): real ABE quantification-window code path -- see input9_abe/run_abe.sh.
