# Input 6b: SKILL.md Jutils block (07) run literally from the Jutils clone (as the Skill says: python3 jutils.py ...). Planted for sashimi/venn; real chrX (197 SE) for the heatmap.
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
P=$AS/public-data/planted; PUB=$AS/public-data
J=$SRC/Jutils
run_set() { name=$1 rmdir=$2 gtf=$3 coord=$4 meta=$5 bamlist=$6
  W=$RUN/out/i6_jutils_$name; rm -rf $W; mkdir -p $W; cd $W
  mkdir -p rmats_output; cp $rmdir/*.MATS.J*.txt rmats_output/
  cp $meta meta.tsv; cp $bamlist bam_list.tsv
  # block 07 literal; jutils.py -> clone path; annotation.gtf / coordinate substituted
  sed -e "s#python3 jutils.py#micromamba run -n as-viz-gg34 python3 $J/jutils.py#g;s#annotation.gtf#$gtf#;s#chr1:1000-2000#$coord#" $RUN/blocks/07_*.sh > b07.sh
  echo "== $name"; bash b07.sh > b07.log 2>&1; echo "block rc=$?"
  tr '\r' '\n' < b07.log | grep -a -i -E "error|Traceback|Skipping|not enough|warn" | head -6
  find . -type f \( -name '*.pdf' -o -name '*.png' -o -name '*results.tsv' \) | sort | xargs ls -l | awk '{print $5,$9}'
}
# planted (1 event): convert, sashimi, venn expected to work; heatmap "Skipping" (needs >=2 events)
printf 'G1_rep1\tG1\nG1_rep2\tG1\nG1_rep3\tG1\nG2_rep1\tG2\nG2_rep2\tG2\nG2_rep3\tG2\n' > $RUN/out/pl_meta.tsv
for i in 1 2 3; do printf "G1_rep$i\t$P/G1_rep$i.bam\tG1\n"; done > $RUN/out/pl_bamlist.tsv
for i in 1 2 3; do printf "G2_rep$i\t$P/G2_rep$i.bam\tG2\n"; done >> $RUN/out/pl_bamlist.tsv
run_set planted $RUN/data/rmats_planted $P/planted.gtf chrP:1-1200 $RUN/out/pl_meta.tsv $RUN/out/pl_bamlist.tsv
# real chrX 2v2 (heatmap needs >=2 events after cutoffs: the SKILL cutoff is --q-value 0.05)
printf 'ERR188383\tGBR\nERR188428\tGBR\nERR188454\tYRI\nERR204916\tYRI\n' > $RUN/out/re_meta.tsv
D=$PUB/rnasplice/bam
printf "ERR188383\t$D/ERR188383.Aligned.out.bam\tGBR\nERR188428\t$D/ERR188428.Aligned.out.bam\tGBR\nERR188454\t$D/ERR188454.Aligned.out.bam\tYRI\nERR204916\t$D/ERR204916.Aligned.out.bam\tYRI\n" > $RUN/out/re_bamlist.tsv
run_set real $RUN/data/rmats_real $PUB/rnasplice/reference/genes_chrX.gtf X:69508604-69510295 $RUN/out/re_meta.tsv $RUN/out/re_bamlist.tsv
