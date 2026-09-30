# launches all re-audit runs (WSL science); logs to reaudit-run/logs
R=/mnt/openscience/audits/bio-atac-seq-single-cell-atac/reaudit-run; T=/mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/tools
for t in doc relaxed guard; do bash $R/scripts/ra_signac.sh $t > $R/logs/signac_$t.log 2>&1 & done
bash $T/runpy.sh python $R/scripts/ra_snap.py > $R/logs/snap.log 2>&1 &
bash $T/run_named.sh ../../audits/bio-atac-seq-single-cell-atac/reaudit-run/scripts/ra_wnn.R > $R/logs/wnn.log 2>&1 &
bash $R/scripts/ra_amulet.sh > $R/logs/amulet.log 2>&1 &
wait
