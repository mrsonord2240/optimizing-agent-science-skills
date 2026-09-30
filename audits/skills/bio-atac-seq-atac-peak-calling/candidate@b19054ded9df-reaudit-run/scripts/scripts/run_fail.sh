source /mnt/openscience/audits/bio-atac-seq-atac-peak-calling/reaudit-run/scripts/env.sh
O=$R/fail_lib; rm -rf $O
( time bash $S $E1 $R/rep2_6pct.bam 2.806e9 $BL $O ) > $R/fail_lib.log 2>&1; echo RC=$? >> $R/fail_lib.log
