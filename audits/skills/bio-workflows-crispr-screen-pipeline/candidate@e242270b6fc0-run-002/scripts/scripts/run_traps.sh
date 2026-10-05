SK=/f/OpenScience/wt/recut-crispr-pipeline/skills/bio-workflows-crispr-screen-pipeline
R=$(cd .. && pwd)
python $SK/scripts/qc.py $R/cn/screen_cleanr_corrected_counts.txt qc.tsv plasmid=CTRL_ERS717283.plasmid; echo "T1 qc-on-corrected exit $?"
python $SK/scripts/qc.py F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/derived/crispr-pipeline/qc/hap1.count.txt qc.tsv; echo "T2 qc-no-plasmid exit $?"
python $SK/scripts/rra.py F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/derived/crispr-pipeline/rra/hap1.count.txt x treatment=HAP1_T18A; echo "T3 rra-no-control exit $?"
python $SK/scripts/rra.py $R/cn/screen_cleanr_corrected_counts.txt x treatment=A375_C902R1_P1D14,A375_C902R2_P1D14,A375_C902R3_P1D14 control=CTRL_ERS717283.plasmid > rra_cn.log 2>&1; echo "T4 rra-on-corrected exit $?"; tail -3 rra_cn.log
python $SK/scripts/consensus.py out.csv mageck=$R/rra/essentiality_rra.gene_summary.txt; echo "T5 consensus-one exit $?"
