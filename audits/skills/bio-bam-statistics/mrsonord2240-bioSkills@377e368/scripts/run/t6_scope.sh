#!/bin/bash
# INPUT 6 (Scope boundary, regression of pre-fix input 6): mate-pair insert size, soft-clip recipe on 1.24, Picard HsMetrics, contamination hand-offs, CRAM notes, unverified-claim labelling.
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; cd $R/work; D=$R/data; E=$R/data/edge
echo "=== A. mate-pair (RF) library, proper flag SET and UNSET: what stats reports (Skill: IS reported, outward counts dominate) and what the pysam tools do"
for b in rf rf_noproper; do echo "--- $b"; samtools stats $D/$b.bam | grep -E '^SN\s+(insert size average|inward|outward|pairs with other)'; samtools stats $D/$b.bam | grep -c '^IS'; python $R/skill/examples/qc_report.py $D/$b.bam | tail -6; done
echo "=== B. soft-clip recipe (block 033) vs cigartuples truth, gawk and mawk"
python $R/t6_softclip.py $AFDATA/human/test.paired_end.sorted.bam $AFDATA/human/test.rna.paired_end.sorted.bam $AFDATA/1000g/HG00349.chr20_1400000-1500000.bam $AFDATA/sarscov2/sars-cov-2_v5.3.2.nanopore.bam $D/synth.bam $E/supp_sec_heavy.bam $E/unmapped_only.bam $E/all_qcfail.bam $D/empty.bam $E/ubam_no_sq.bam
echo "=== C. Picard CollectHsMetrics + BedToIntervalList (block 034), human BAM, target = chr22:1952-4617"
printf 'chr22\t1951\t4617\ttarget1\n' > targets.bed
picard BedToIntervalList I=targets.bed O=targets.interval_list SD=$AFDATA/human/genome.dict 2>&1 | grep -E 'Wrote|ERROR|Exception' | head -3
head -c 0 /dev/null; grep -v '^@' targets.interval_list
picard CollectHsMetrics I=$AFDATA/human/test.paired_end.sorted.bam O=hs_metrics.txt R=$AFDATA/human/genome.fasta BAIT_INTERVALS=targets.interval_list TARGET_INTERVALS=targets.interval_list 2>&1 | grep -E 'ERROR|Exception' | head -3
python - <<'PY'
rows=[l.rstrip('\n').split('\t') for l in open('hs_metrics.txt') if l.strip() and not l.startswith('#')]
h,v=rows[0],rows[1]; d=dict(zip(h,v))
for k in ('PCT_OFF_BAIT','PCT_SELECTED_BASES','FOLD_80_BASE_PENALTY','MEAN_TARGET_COVERAGE','AT_DROPOUT','GC_DROPOUT','TOTAL_READS'): print(k, d.get(k,'MISSING'))
PY
echo "independent: samtools depth -s (mates once) mean over target = $(samtools depth -a -s -r chr22:1952-4617 $AFDATA/human/test.paired_end.sorted.bam | awk '{s+=$3;n++} END{print s/n}'); depth (mates twice) = $(samtools depth -a -r chr22:1952-4617 $AFDATA/human/test.paired_end.sorted.bam | awk '{s+=$3;n++} END{print s/n}')"
echo "=== D. contamination / identity hand-offs (block 035): verifybamid2 and somalier flags vs --help, and a real run on the 40 kb slice"
verifybamid2 --help 2>&1 | grep -E -- '--(SVDPrefix|Reference|BamFile|Output)\b' | head -4
verifybamid2 --SVDPrefix $AFDATA/resources/1000g.phase3.10k.b38.vcf.gz.dat --Reference $AFDATA/human/genome.fasta --BamFile $AFDATA/human/test.paired_end.sorted.bam --Output vb_slice 2>&1 | tail -4; ls vb_slice* 2>&1 | head
echo "-- SVDPrefix WITHOUT .dat (Skill says it must include it)"; verifybamid2 --SVDPrefix $AFDATA/resources/1000g.phase3.10k.b38.vcf.gz --Reference $AFDATA/human/genome.fasta --BamFile $AFDATA/human/test.paired_end.sorted.bam --Output vb_nodat 2>&1 | tail -2
mkdir -p ext; somalier extract -s $AFDATA/resources/somalier.sites.hg38.vcf.gz -f $AFDATA/human/genome.fasta -d ext/ $AFDATA/human/test.paired_end.sorted.bam 2>&1 | tail -4; ls ext | head
somalier relate 2>&1 | head -3
somalier contamination 2>&1 | head -4
echo "=== E. CRAM notes: stats needs --reference (not -r), mosdepth needs -f and .crai"
CR=$AFDATA/human/test.paired_end.sorted.cram; cp $CR c.cram
samtools stats -r $AFDATA/human/genome.fasta c.cram 2>&1 | head -2
samtools stats --reference $AFDATA/human/genome.fasta c.cram | grep -E '^SN\s+(raw total|error rate)'
mosdepth -t 2 -f $AFDATA/human/genome.fasta cm c.cram 2>&1 | tail -1; samtools index c.cram; mosdepth -t 2 -f $AFDATA/human/genome.fasta cm2 c.cram && tail -1 cm2.mosdepth.summary.txt
echo "=== F. labelling of unverified numbers in SKILL.md"
grep -n -iE 'literature|commonly|not thresholds|rule of thumb|checked|not run end to end|not benchmarked' $R/skill/SKILL.md | cut -c1-230
echo "=== G. grep for the removed claims"; grep -n -iE '3-10x|10x faster|faster than' $R/skill/SKILL.md $R/skill/usage-guide.md | cut -c1-200
