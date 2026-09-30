source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh
export R_USER_CACHE_DIR=$MD/cache/Rcache
S=$1; shift; export SIGNAC_LIB=${SIGNAC_LIB:-}
cd $MD/work; /usr/bin/time -v micromamba run -n $ENVN Rscript $MD/evidence/scripts/$S > $MD/logs/${S%.R}.log 2> $MD/logs/${S%.R}.err; echo exit $?
tail -60 $MD/logs/${S%.R}.log; grep -E "Elapsed|Maximum res" $MD/logs/${S%.R}.err; grep -i -m5 "^Error" -A3 $MD/logs/${S%.R}.err
