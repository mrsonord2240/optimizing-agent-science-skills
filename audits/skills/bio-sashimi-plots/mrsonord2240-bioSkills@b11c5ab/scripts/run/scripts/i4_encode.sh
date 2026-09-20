# Input 4: real ENCODE 12-BAM, 3 groups (Endothelial/Epithelial/Mesenchymal), ggsashimi per the Skill's flags in the ggplot2 3.4.4 env, plus strand options
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
export PATH=$RUN/bin:$PATH
S=$AS/public-data/sashimi
W=$RUN/out/i4; rm -rf $W; mkdir -p $W; cd $W
# absolute BAM paths (ggsashimi resolves relative ones against the TSV directory)
awk -F'\t' -v s=$S 'BEGIN{OFS="\t"}{print $1, s"/"$2, $3}' $S/input_bams.tsv > groups.tsv
printf '#1b9e77\n#d95f02\n#7570b3\n' > palette.txt
micromamba run -n as-core samtools flagstat $S/bams/ENCFF088HTJ.chr10_27035000_27050000.bam | head -8
R=chr10:27040584-27048100
for F in svg png; do
  ggsashimi.py -b groups.tsv -c $R -o ex -M 1 --alpha 0.25 --height 3 --width 10 --shrink --fix-y-scale --ann-height 4 -g $S/annotation.gtf --base-size 14 -O 3 -C 3 -P palette.txt -A mean_j -F $F > ex_$F.log 2>&1; echo "[$F] rc=$? $(stat -c %s ex.$F)"
done
micromamba run -n as-core python $RUN/scripts/jtruth.py $R groups.tsv --M 1 --agg mean_j --svg ex.svg | tail -12
echo "--- per-sample (no overlay) labels for the 4 Endothelial samples, -M 1"
grep Endothelial groups.tsv > endo.tsv
ggsashimi.py -b endo.tsv -c $R -o endo -M 1 --shrink -g $S/annotation.gtf -F svg > endo.log 2>&1; echo "rc=$?"
micromamba run -n as-core python $RUN/scripts/jtruth.py $R endo.tsv --M 1 --agg none --svg endo.svg | tail -3
echo "--- strand routing"
for ST in SENSE ANTISENSE; do
  ggsashimi.py -b endo.tsv -c $R -o st_$ST -M 1 -s $ST -F svg -g $S/annotation.gtf > st_$ST.log 2>&1; echo "-s $ST rc=$? files: $(ls st_$ST* 2>/dev/null | grep -v log | tr '\n' ' ')"
done
micromamba run -n as-core python - <<'PY'
import pysam, collections
S='/mnt/openscience/audit-envs/alternative-splicing/public-data/sashimi/bams/'
c={'+':0,'-':0}
for l in open('endo.tsv'):
    b=l.split('\t')[1]
    with pysam.AlignmentFile(b) as f:
        for r in f.fetch('chr10',27040583,27048100):
            if any(op==3 for op,_ in (r.cigartuples or [])): c['-' if r.is_reverse else '+']+=1
print('spliced reads by read strand (SENSE routing): +',c['+'],' -',c['-'])
PY
for ST in SENSE ANTISENSE; do for s in + -; do echo "st_${ST}_$s: $(micromamba run -n as-core python $RUN/scripts/svg_labels.py st_${ST}_$s.svg 2>/dev/null | grep -aE '^[0-9]+$' | tr '\n' ' ')"; done; done
