samtools view -F 2308 aligned.bam | awk '{for(i=12;i<=NF;i++) if($i ~ /^ts:A:/){n++; if($i=="ts:A:+") p++}} END{printf "%.3f\n", p/n}'
# ~1.000 -> oriented reads (-uf is safe); ~0.5 -> unoriented (never -uf). Measured: oriented HiFi 1.000, unstranded ONT 0.501, real LRGASP cDNA 0.503
