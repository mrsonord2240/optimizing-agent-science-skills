#!/bin/bash
# Side check (not scored as an input): SKILL.md says the collate/-u piped "Pipeline Version (Optimized)" "is ~30% faster than sort -n | fixmate | sort | markdup
# on typical 30x WGS". Time both at 4 threads on a SYNTHETIC 800k-read BAM (30x WGS is ~1e9 reads; this is a scale check only).
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in09; mkdir in09; cd in09
python $RUN/30_make_big.py big.bam 400000
nproc | sed 's/^/cores: /'
t() { local s=$(date +%s.%N); "$@" > /dev/null 2>&1; local e=$(date +%s.%N); echo "$e - $s" | bc; }
opt() { rm -rf tmpdir; mkdir -p tmpdir; samtools collate -O -u big.bam tmpdir/collate | samtools fixmate -m -u - - | samtools sort -u -@ 4 -T tmpdir/sort - | samtools markdup -@ 4 -d 2500 --use-read-groups -f st.txt - m_opt.bam; }
old() { samtools sort -n -@ 4 -o ns.bam big.bam && samtools fixmate -m -@ 4 ns.bam fm.bam && samtools sort -@ 4 -o cs.bam fm.bam && samtools markdup -@ 4 -d 2500 --use-read-groups cs.bam m_old.bam; }
for i in 1 2 3; do echo "rep $i: optimized $(t bash -c "$(declare -f opt); opt")  s | 5-step $(t bash -c "$(declare -f old); old") s"; done
echo "flagged: optimized $(flagged m_opt.bam)  5-step $(flagged m_old.bam)  (equal counts expected)"
