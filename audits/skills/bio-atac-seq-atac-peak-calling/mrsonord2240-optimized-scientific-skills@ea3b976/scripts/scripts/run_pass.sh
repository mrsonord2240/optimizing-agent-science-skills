source /mnt/openscience/audit-envs/bio-atac-seq-atac-peak-calling/tools/../wsl_env.sh
source /mnt/openscience/audits/bio-atac-seq-atac-peak-calling/reaudit-run/scripts/env.sh
O=$R/pass_macs3; rm -rf $O
( time bash $S $E1 $E2 2.806e9 $BL $O $CS ) > $R/pass_macs3.log 2>&1; echo RC=$? >> $R/pass_macs3.log
