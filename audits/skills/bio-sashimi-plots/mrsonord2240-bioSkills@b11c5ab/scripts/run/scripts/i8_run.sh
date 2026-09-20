source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
export PATH=$RUN/bin:$PATH
micromamba run -n as-core python $RUN/scripts/i8_sparse.py 2>&1 | grep -av -E "^Warning|hts_idx|label.size|annotate|linewidth|deprecated|^ *$|Fontconfig"
