# Input 7c (NEW data): fastq_screen per SKILL.md rRNA section: literal command and the three setup claims.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run
mkdir -p $R/work/in7/fq; cd $R/work/in7/fq
asenv as-core python $R/70_in7_make_fq.py .
asenv as-core minimap2 -d rrna_ref.mmi rrna_ref.fa 2>&1 | tail -1
asenv as-core fastq_screen --help 2>&1 | grep -i -A1 'aligner' | head -6
# config: only the DATABASE line (prefix of the minimap2 index)
printf 'THREADS\t4\nDATABASE\trRNA\t%s/rrna_ref\n' "$PWD" > fastq_screen.conf
echo "=== 1. literal SKILL.md command (minimap2), gz FASTA next to the .mmi"
cp sample_R1.fq sample_R1.fq.tmp; asenv as-core fastq_screen --aligner minimap2 --conf fastq_screen.conf --threads 8 --force sample_R1.fq > run1.log 2>&1; echo rc=$?
cat sample_R1_screen.txt
echo "=== 2. .fa.gz missing (claim: rc 0, 100% unmapped, only an Aligner warning)"
mkdir -p nogz; cp rrna_ref.mmi nogz/; cp rrna_ref.fa nogz/; printf 'THREADS\t4\nDATABASE\trRNA\t%s/nogz/rrna_ref\n' "$PWD" > nogz.conf
asenv as-core fastq_screen --aligner minimap2 --conf nogz.conf --threads 8 --outdir nogz_out --force sample_R1.fq > run2.log 2>&1; echo rc=$?; grep -i 'warn' run2.log | head -2; sed -n 1,4p nogz_out/sample_R1_screen.txt
echo "=== 3. default aligner (bowtie2 absent): literal command without --aligner (claim rc 255)"
asenv as-core fastq_screen --conf fastq_screen.conf --threads 8 --outdir def_out --force sample_R1.fq > run3.log 2>&1; echo rc=$?; tail -2 run3.log
echo "=== independent truth: minimap2 hits on the rRNA ref straight from minimap2"
asenv as-core minimap2 -x sr -a rrna_ref.fa sample_R1.fq 2>/dev/null | samtools view -c -F 0x904 -q 1 - | awk '{printf "minimap2 mapped reads: %d of 4000 = %.1f%%\n",$1,100*$1/4000}'
