#!/usr/bin/env bash
# Re-audit (2026-09-19) independent verification of the FUSION.post_process.R single-SNP
# crash + fix. Uses a FRESH fixture (different SNPs/seed than both the original auditor's
# and the fixer's own fixtures) built by reaudit_input2_build_fusion_data.R, and two
# separate clones of fusion_twas: one left unpatched (to reproduce the crash), one with
# the fixer's documented two-line drop=FALSE patch applied (to confirm the fix).
set -x

R_WRAP="/f/OpenScience/audit-envs/mendelian-randomization-analyst/r.sh"
DATA="<scratchpad>/twas-reaudit/data/fusion"   # see reaudit_input2_build_fusion_data.R for exact path

# --- Step 1: build the fixture (real 957x14389 chr1-only plink2R panel as LD ref) ---
"$R_WRAP" reaudit_input2_build_fusion_data.R

# --- Step 2: FUSION.assoc_test.R (unaffected by the fix; ground-truth sanity check) ---
cd fusion_unpatched
"$R_WRAP" FUSION.assoc_test.R \
  --sumstats "$DATA/gwas.sumstats" --weights "$DATA/weights.pos" \
  --weights_dir "$DATA/wgt/" --ref_ld_chr "$DATA/ld/EUR." --chr 1 \
  --out "$DATA/twas_chr1.dat"
# Result: TWAS.Z = 7.200 (true), -0.485 (null), -1.557 (multi) -- exact match to planted values

# --- Step 3: reproduce the crash on UNPATCHED fusion_twas ---
"$R_WRAP" FUSION.post_process.R \
  --input "$DATA/twas_chr1.dat" --sumstats "$DATA/gwas.sumstats" \
  --ref_ld_chr "$DATA/ld/EUR." --chr 1 --out "$DATA/twas_joint_unpatched2" \
  --locus_win 100000
# Result: "Error in wgt.matrix[qc$flip, ] : incorrect number of dimensions" -- reproduced

# --- Step 4: confirm the fix on a PATCHED fusion_twas clone ---
# Patch applied to a separate clone: both occurrences of
#   wgt.matrix = wgt.matrix[m.keep,]          -> wgt.matrix = wgt.matrix[m.keep,,drop=FALSE]
#   cur.genos = genos$bed[,m[m.keep]]         -> cur.genos = genos$bed[,m[m.keep],drop=FALSE]
# at lines ~168/170 and ~251/254, exactly as documented in the fix log and SKILL.md.
cd ../fusion_patched
"$R_WRAP" FUSION.post_process.R \
  --input "$DATA/twas_chr1.dat" --sumstats "$DATA/gwas.sumstats" \
  --ref_ld_chr "$DATA/ld/EUR." --chr 1 --out "$DATA/twas_joint_patched2" \
  --locus_win 100000 --report
# Result: completes cleanly. twas_joint_patched2.joint_included.dat: GENE_TRUE JOINT.P=6e-13 (retained)
#         twas_joint_patched2.joint_dropped.dat: GENE_NULL COND.P=0.63, GENE_MULTI COND.P=0.12 (dropped)
