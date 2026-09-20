#!/bin/bash
# Input 5 (stress): shipped examples/markdup_pipeline.sh run from a COPY; usage-guide pipelines; failure exit codes.
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in05; mkdir in05; cd in05
cp -r $SK skill; chmod +x skill/examples/markdup_pipeline.sh
bash -n skill/examples/markdup_pipeline.sh && echo "bash -n: syntax OK"
echo "### 5a. example on planted_dups.bam (truth 100)"
mkdir a; cd a
../skill/examples/markdup_pipeline.sh $D/planted_dups.bam out.bam 2 2>&1 | tail -22; echo "exit=${PIPESTATUS[0]}"
echo "[check] dup flagged: $(samtools view -c -f 1024 out.bam) ; index exists: $(ls out.bam.bai 2>&1)"; ls
cd ..
echo "### 5b. example on real human BAM (truth 1656)"
mkdir b; cd b
../skill/examples/markdup_pipeline.sh $D/test.paired_end.sorted.bam out.bam >/dev/null 2>&1; echo "exit=$?"
echo "[check] dup flagged: $(samtools view -c -f 1024 out.bam)"; cd ..
echo "### 5c. example with a MISSING input file"
mkdir c; cd c
../skill/examples/markdup_pipeline.sh nonexistent.bam out.bam 2>&1 | tail -8; echo "script exit=${PIPESTATUS[0]}"; echo "output left behind: $(ls -la out.bam 2>&1)"; cd ..
echo "### 5d. example with a CORRUPT (truncated) input"
mkdir d; cd d; head -c 3000 $D/planted_dups.bam > trunc.bam
../skill/examples/markdup_pipeline.sh trunc.bam out.bam 2>&1 | tail -8; echo "script exit=${PIPESTATUS[0]}"; echo "output: $(ls -la out.bam 2>&1) dup=$(samtools view -c -f 1024 out.bam 2>&1)"; cd ..
echo "### 5e. example with an UNWRITABLE output dir (markdup itself fails)"
mkdir e; cd e
../skill/examples/markdup_pipeline.sh $D/planted_dups.bam /nonexistent_dir/out.bam 2>&1 | tail -6; echo "script exit=${PIPESTATUS[0]}"; cd ..
echo "### 5f. example with only one argument (usage path)"
skill/examples/markdup_pipeline.sh one.bam; echo "exit=$?"
echo "### 5g. usage-guide 'Pipeline (No Intermediate Files)' verbatim"
mkdir g; cd g; cp $D/planted_dups.bam input.bam
samtools sort -n -@ 4 input.bam | \
    samtools fixmate -m -@ 4 - - | \
    samtools sort -@ 4 - | \
    samtools markdup -@ 4 - marked.bam
echo "exit codes ${PIPESTATUS[*]}"; samtools index marked.bam; echo "[check] dup flagged: $(samtools view -c -f 1024 marked.bam) (truth 100)"
echo "### 5h. usage-guide step-by-step + duplicate-rate one-liner + flagstat grep"
samtools sort -n -@ 4 -o namesort.bam input.bam
samtools fixmate -m -@ 4 namesort.bam fixmate.bam
samtools sort -@ 4 -o coordsort.bam fixmate.bam
samtools markdup -@ 4 coordsort.bam marked2.bam
samtools index marked2.bam
samtools flagstat marked2.bam | grep duplicates
total=$(samtools view -c -F 256 marked2.bam)
dups=$(samtools view -c -f 1024 -F 256 marked2.bam)
echo "Duplicate rate: $(echo "scale=2; $dups * 100 / $total" | bc)%"
echo "### 5i. usage-guide '-d 100' / '-d 2500' / -s / -f variants exist and run (syntax check)"
samtools markdup -d 100 coordsort.bam v1.bam 2>&1 | grep -c warning | sed 's/^/  -d 100 warnings (non-Illumina names): /'
samtools markdup -s coordsort.bam v3.bam 2> stats.txt; grep -c DUPLICATE stats.txt | sed 's/^/  -s stats lines: /'
samtools markdup -f stats2.txt coordsort.bam v4.bam; grep 'DUPLICATE TOTAL' stats2.txt
echo "### 5j. usage-guide troubleshooting 'High Memory Usage: markdup -@ 8 reduces memory' - measure max RSS on 1000G slice (-@0 vs -@8)"
cp $D/HG00349.chr20_1400000-1500000.bam kg.bam; samtools sort -n -o k1.bam kg.bam; samtools fixmate -m k1.bam k2.bam; samtools sort -o k3.bam k2.bam
for t in 0 8; do /usr/bin/time -f "  -@ $t: maxRSS=%M KB wall=%es" samtools markdup -@ $t k3.bam kt$t.bam 2>&1 | tail -1; done
