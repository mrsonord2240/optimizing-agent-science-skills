# Re-audit: does the pipeline surface a missing bedtools/bedGraphToBigWig (chrombpnet shells out to them; SKILL env table omits them)?
source /mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac/scripts/env.sh
E=/home/sci/micromamba/envs/dlatac-tf/bin; P=$ME/public-cache/pseudo; W=$ME/run/reaudit/nobt; rm -rf $W; mkdir -p $W
which bedtools bedGraphToBigWig samtools 2>&1 | head -3; echo "(system PATH above; env has: $(ls $E | grep -E '^(bedtools|bedGraphToBigWig|samtools)$' | tr '\n' ' '))"
# chrombpnet CLI by absolute path, PATH lacking the env bin (as a pip-only install would have)
PATH=/usr/bin:/bin $E/chrombpnet prep splits -c $P/pseudo.chrom.sizes -tcr chrP1 -vcr chrP2 -op $W/split >/dev/null 2>&1; echo "splits exit=$?"
PATH=/usr/bin:/bin $E/chrombpnet prep nonpeaks -g $P/pseudo.fa -c $P/pseudo.chrom.sizes -p $P/pseudo.narrowPeak -fl $W/split.json -o $W/np 2>&1 | tail -4 | cut -c1-200; echo "nonpeaks exit=${PIPESTATUS[0]}"; ls $W
