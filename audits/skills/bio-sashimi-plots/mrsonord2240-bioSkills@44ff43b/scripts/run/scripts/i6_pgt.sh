source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
mkdir -p $RUN/data/pgt; cd $RUN/data/pgt
P=$RUN/data/planted
echo "== regtools junctions extract (planted G1_rep1; XS present)"
regtools junctions extract -a 8 -m 50 -s XS -o g1.bed $P/G1_rep1.bam 2>&1 | tail -2; cat g1.bed
echo "== Skill's awk BEDPE conversion, verbatim"
awk 'BEGIN{OFS="\t"} {split($11,a,","); split($12,b,","); s=$2+a[1]; e=$2+b[2]; print $1, s, s+1, $1, e-1, e, $5}' g1.bed > junctions.bedpe
cat junctions.bedpe
echo "== bedtools genomecov -> bedgraph ; bigwig tools?"
bedtools genomecov -split -ibam $P/G1_rep1.bam -bga > ctrl.bedgraph; wc -l ctrl.bedgraph
which bedGraphToBigWig bamCoverage wigToBigWig 2>&1 | head; micromamba run -n as-viz python -c "import pyBigWig; print('pyBigWig ok')" 2>&1 | tail -1
micromamba run -n as-viz pyGenomeTracks --track_file_types 2>&1 | tr '\r' '\n' | head -3
micromamba run -n as-viz pyGenomeTracks --help 2>&1 | tr '\r' '\n' | grep -a -i "listTracks\|version" | head
micromamba run -n as-viz pyGenomeTracks --version 2>&1 | tail -1
