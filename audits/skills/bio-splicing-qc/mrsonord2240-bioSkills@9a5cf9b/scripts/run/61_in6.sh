source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; P=$ASDATA/rnasplice
cd $R; mkdir -p work/in6; cd work/in6; cp -r $R/skill/examples .
echo "--- B08 literal (as-maxent)"; asenv as-maxent python $R/blocks/B08.py
echo "--- real chrX MaxEnt via helper"; asenv as-maxent python $R/60_in6_sites.py $R/skill/examples $P/reference/genes_chrX.gtf $ASDATA/derived/X.fa
echo "--- helper CLI sites"; asenv as-maxent python examples/splicing_qc.py sites --donor CAGGTAAGT --donor CAGATAAGT --acceptor TTTTTTTTTTTTTTCCTTAGGAG
