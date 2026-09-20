#!/bin/bash
# NEW INPUT (variant): own planted-truth BAM with a read-less contig, a 100 bp contig, spike, supplementary, QC-fail, dup, secondary, unmapped. Depth recipes, denominators, mosdepth note, BED recipes, pysam, batch loop.
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; N=$R/data/new; cd $R/work; rm -rf own; mkdir own; cd own
B=$N/own_ctg.bam
python - <<'PY'
import json
t=json.load(open('/mnt/openscience/audits/bio-bam-statistics/run/data/new/own_ctg.truth.json'))
print('TRUTH total_len %d (contigs with reads %d) sum_depth %d | mean over ALL %.6f | mean over contigs-with-reads %.6f | >=10x %.4f%% >=20x %.4f%% | max %d covered %d' % (t['total_len'],t['len_contigs_with_reads'],t['sum_depth'],t['mean_all'],t['mean_reads_contigs_only'],t['ge10_all_pct'],t['ge20_all_pct'],t['max'],t['covered']))
print('TRUTH flagstat', t['flagstat'])
PY
echo "=== flagstat -O tsv (first rows)"; samtools flagstat -O tsv $B | head -8 | cut -f1-3
echo "=== block 017 verbatim (depth -aa)"; sed "s#input.bam#$B#" $R/blocks/017_bash.sh | bash
echo "=== same with -a (Skill: -a omits contigs with no reads) -> expect mean over contigs-with-reads"; sed "s#input.bam#$B#; s#depth -aa#depth -a#" $R/blocks/017_bash.sh | bash
echo "=== raw depth mean (Skill warning): $(samtools depth $B | awk '{s+=$3;n++} END{print s/n}')"
echo "rows depth / -a / -aa:"; for o in "" "-a" "-aa"; do samtools depth $o $B | wc -l; done
echo "=== samtools coverage (all contigs)"; samtools coverage $B | cut -f1-7
echo "=== mosdepth default summary (Skill: total covers only contigs that have reads, 20100 of 25100 bp)"; mosdepth -t 2 md $B; cat md.mosdepth.summary.txt
awk -F'\t' '$1=="total"{printf "mosdepth total: %d bp, mean %s ; contigs-with-reads truth %.2f\n", $2,$4, 120200/20100}' md.mosdepth.summary.txt
echo "=== block 021 (depth -aa -b) with a BED touching the read-less contig ctgB, ctgC and ctgA (truth rows: 1000+500+100+50+300 = 1950)"
printf 'ctgA\t0\t1000\tA1\nctgB\t100\t600\tB1\nctgC\t0\t100\tC1\nctgA\t3000\t3050\tSUP\nctgB\t4700\t5000\tB2\n' > r.bed
sed "s#regions.bed#r.bed#; s#input.bam#$B#" $R/blocks/021_bash.sh | bash | awk '{c[$1]++} END{for(k in c) print k, c[k]}' | sort
echo "-a form:"; samtools depth -a -b r.bed $B | awk '{c[$1]++} END{for(k in c) print k, c[k]}' | sort
echo "=== block 025 coverage-from-BED loop"; sed "s#regions.bed#r.bed#; s#input.bam#$B#" $R/blocks/025_bash.sh | bash | cut -f1-7
echo "=== mosdepth --by same BED"; mosdepth --by r.bed --no-per-base mb $B; cat mb.regions.bed.gz | zcat
echo "=== pysam region_depth_stats (block 029) vs truth arrays and samtools depth -a, BAM and CRAM+reference"; python $R/n2_region_truth.py
echo "=== block 005 batch loop on this BAM and the CRAM"; mkdir bt; cp $B bt/own_ctg.bam; cd bt; bash <(cat $R/blocks/005_bash.sh); cat summary.tsv; cd ..
