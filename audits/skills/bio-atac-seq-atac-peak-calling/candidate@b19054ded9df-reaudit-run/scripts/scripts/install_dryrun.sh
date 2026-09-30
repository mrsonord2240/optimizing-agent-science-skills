export MAMBA_ROOT_PREFIX=/home/sci/micromamba PATH=/home/sci/.local/bin:$PATH
exec 9>/mnt/openscience/runtime/locks/micromamba-mutate.lock; flock 9
L=/mnt/openscience/audit-envs/bio-atac-seq-atac-peak-calling/run/reaudit; mkdir -p $L
micromamba create --dry-run -y -n reaudit-dry-a -c conda-forge -c bioconda macs3 genrich samtools bedtools ucsc-bedgraphtobigwig > $L/dry_a.log 2>&1; echo dry_a_rc=$?
micromamba create --dry-run -y -n reaudit-dry-b -c conda-forge -c bioconda idr "numpy<1.24" python=3.10 > $L/dry_b.log 2>&1; echo dry_b_rc=$?
grep -E '^\s+(macs3|genrich|samtools|bedtools|ucsc-bedgraphtobigwig|idr|numpy|python) ' $L/dry_a.log $L/dry_b.log | awk '{print $1,$2,$3}'
echo "--- documented OLD line (bioconda only):"
micromamba create --dry-run -y -n reaudit-dry-c -c bioconda macs3 macs2 genrich samtools bedtools idr > $L/dry_old.log 2>&1; echo old_rc=$?; tail -3 $L/dry_old.log
ls -d /home/sci/micromamba/envs/reaudit-dry* 2>&1 | head -2
