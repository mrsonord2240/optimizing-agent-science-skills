R=/mnt/openscience/audits/bio-atac-seq-single-cell-atac/reaudit-run; T=/mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/tools
bash $T/runr.sh Rscript $R/scripts/ra_check_signac.R > $R/logs/check_signac.log 2>&1
bash $T/runpy.sh python $R/scripts/ra_peakvi.py > $R/logs/peakvi.log 2>&1 &
bash $T/runr.sh Rscript $R/scripts/ra_archr_guard.R > $R/logs/archr_guard.log 2>&1 &
bash $T/runr.sh Rscript $R/scripts/ra_wnn.R > $R/logs/wnn.log 2>&1 && bash $T/runr.sh Rscript $R/scripts/ra_cellcycle.R > $R/logs/cellcycle.log 2>&1 &
wait
echo ALLDONE > $R/logs/launch2.done
