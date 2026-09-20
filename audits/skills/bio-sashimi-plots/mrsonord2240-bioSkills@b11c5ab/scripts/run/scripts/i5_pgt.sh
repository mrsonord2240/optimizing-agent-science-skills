# Input 5: SKILL.md pyGenomeTracks blocks 08-11 run literally (planted 3v3, then real chrX 2v2 with XS-tagged BAMs), figures viewed, BEDPE scores vs pysam
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
export PATH=$RUN/bin:$PATH
PUB=$AS/public-data
run_set() { # name region gtf ctrl-bams... -- trt-bams...
  name=$1; region=$2; gtf=$3; shift 3
  W=$RUN/out/i5_$name; rm -rf $W; mkdir -p $W; cd $W
  C=(); T=(); cur=C
  for x in "$@"; do if [ "$x" = -- ]; then cur=T; continue; fi; [ $cur = C ] && C+=("$x") || T+=("$x"); done
  # block 08: literal with BAM names replaced by an explicit list
  sed -e "s#ctrl1.bam ctrl2.bam ctrl3.bam#${C[*]}#g;s#trt1.bam trt2.bam trt3.bam#${T[*]}#g" $RUN/blocks/08_*.sh > b08.sh
  bash b08.sh > b08.log 2>&1; echo "[$name b08] rc=$? $(ls ctrl.bedgraph trt.bedgraph | tr '\n' ' ') lines: $(wc -l < ctrl.bedgraph) $(wc -l < trt.bedgraph)"
  sed -e "s#annotation.gtf#$gtf#" $RUN/blocks/09_*.ini > tracks.ini
  bash $RUN/blocks/10_*.sh > b10.log 2>&1; echo "[$name b10] rc=$? bedpe lines: $(wc -l < junctions.bedpe)"; cat junctions.bedpe | head -12
  for F in pdf png; do
    sed -e "s#chr17:43094000-43125000#$region#;s#figure.pdf#figure.$F#" $RUN/blocks/11_*.sh > b11_$F.sh
    bash b11_$F.sh > b11_$F.log 2>&1; echo "[$name b11 $F] rc=$? $(stat -c %s figure.$F 2>/dev/null || echo NOFILE)"; grep -a -i -E "error|Traceback" b11_$F.log | head -3
  done
}
D=$PUB/rnasplice/derived 2>/dev/null
run_set planted chrP:1-1200 $PUB/planted/planted.gtf $PUB/planted/G1_rep1.bam $PUB/planted/G1_rep2.bam $PUB/planted/G1_rep3.bam -- $PUB/planted/G2_rep1.bam $PUB/planted/G2_rep2.bam $PUB/planted/G2_rep3.bam
X=$PUB/derived/xs_bams
run_set real X:69508600-69510300 $PUB/rnasplice/reference/genes_chrX.gtf $X/ERR188383.xs.bam $X/ERR188428.xs.bam -- $X/ERR188454.xs.bam $X/ERR204916.xs.bam
