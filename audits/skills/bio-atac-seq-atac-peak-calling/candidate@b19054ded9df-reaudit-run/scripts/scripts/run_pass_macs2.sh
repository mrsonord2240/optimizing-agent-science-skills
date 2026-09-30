source /mnt/openscience/audits/bio-atac-seq-atac-peak-calling/reaudit-run/scripts/env.sh
O=$R/pass_macs2; rm -rf $O; echo LD_PRELOAD=$LD_PRELOAD
( time MACS=macs2 bash $S $E1 $E2 2.806e9 $BL $O ) > $R/pass_macs2.log 2>&1; echo RC=$? >> $R/pass_macs2.log
