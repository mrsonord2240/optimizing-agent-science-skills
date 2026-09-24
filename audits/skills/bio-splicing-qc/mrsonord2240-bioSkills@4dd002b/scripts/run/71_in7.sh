# Input 7: rRNA (B12 samtools recipe, fastq_screen), 3' bias / Picard (B10) on planted BAMs (synthetic) + NEW real-data Picard run and NEW fastq_screen data.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; D=$R/data/synthetic; P=$ASDATA/rnasplice
mkdir -p $R/work/in7; cd $R/work/in7
echo "=== A. B12 literal on pe_rrna (truth: 22% of primary mapped fragments)"
mkdir -p rrna; cd rrna; cp $D/pe_rrna.bam sample.bam; cp $D/pe_rrna.bam.bai .; cp $D/synth.rrna.bed rRNA_intervals.bed
asenv as-core bash $R/blocks/B12.sh
echo "old recipe (no -F 0x904) for contrast:"
t=$(samtools view -c sample.bam); r=$(samtools view -c -L rRNA_intervals.bed sample.bam); awk -v r=$r -v t=$t 'BEGIN{printf "  %d / %d = %.1f%%\n", r, t, 100*r/t}'
cd ..
echo "=== B. B10 literal (awk refFlat, Picard, geneBody) on planted libraries"
for lib in pe_dutp pe_fwd pe_bias3 pe_rrna; do
  mkdir -p $lib; cd $lib; cp $D/$lib.bam sample.bam; cp $D/$lib.bam.bai sample.bam.bai; cp $D/synth.bed12 genes.bed12; cp $D/synth.rrna.interval_list rRNA_intervals.interval_list
  sed 's/SECOND_READ_TRANSCRIPTION_STRAND/'"$( [ $lib = pe_fwd ] && echo FIRST_READ_TRANSCRIPTION_STRAND || echo SECOND_READ_TRANSCRIPTION_STRAND)"'/' $R/blocks/B10.sh > b10.sh
  echo "--- $lib"
  # picard lives in af-picard3 (not as-core); RSeQC geneBody in as-core: split the block by tool
  grep -v '^geneBody' b10.sh > b10_picard.sh; grep '^geneBody' b10.sh > b10_gb.sh
  micromamba run -n af-picard3 bash b10_picard.sh > picard.log 2>&1; echo picard rc=$?
  asenv as-core bash b10_gb.sh > gb.log 2>&1; echo geneBody rc=$?
  awk 'BEGIN{FS="\t"} /^## METRICS/{getline; for(i=1;i<=NF;i++)h[i]=$i; getline; for(i=1;i<=NF;i++) if(h[i]~/^(PF_ALIGNED_BASES|PCT_CODING_BASES|PCT_UTR_BASES|PCT_INTRONIC_BASES|PCT_INTERGENIC_BASES|PCT_RIBOSOMAL_BASES|MEDIAN_5PRIME_TO_3PRIME_BIAS|PCT_CORRECT_STRAND_READS)$/) printf "  %s=%s\n", h[i], $i; exit}' sample.rna_metrics.txt
  python3 - <<'PY'
import re
rows = [l.split('\t') for l in open('sample_geneBody.geneBodyCoverage.txt').read().strip().splitlines()]
for r in rows[1:]:
    v = [float(x) for x in r[1:]]
    print('  geneBody 5p(first10)/3p(last10) = %.3f' % (sum(v[:10]) / max(sum(v[-10:]), 1e-9)))
PY
  cd ..
done
