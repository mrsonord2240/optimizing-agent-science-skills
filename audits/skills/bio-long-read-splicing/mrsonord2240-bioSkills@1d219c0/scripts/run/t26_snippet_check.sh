#!/bin/bash
# SKILL Microexons python check (extracted verbatim as out/blocks/microexons-3-27-nt_2.txt) on my micro2 BAMs, genes M03 (6 nt), M05 (9 nt), M12 (27 nt).
# UP/DOWN = the two introns flanking the microexon (first two introns of the inc chain), SKIP = first intron of the skip chain (truth_chains.tsv, 0-based half-open).
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/micro2; export PYTHONDONTWRITEBYTECODE=1
cp $R/out/blocks/microexons-3-27-nt_2.txt $R/out/check.py
for g in M03 M05 M12; do
  args=$(asenv as-lr python - <<PY
t = {l.split("\t")[0]: l.split("\t")[4] for l in open("$D/truth_chains.tsv")}
i = t["${g}inc"].split(";"); s = t["${g}skip"].split(";")
print(" ".join(x.replace("-", " ") for x in (i[0], i[1], s[0])))
PY
)
  for P in hifi ontunstr; do for bam in plain juncbed bonus16 bonus20; do
    echo "$g $P $bam: $(asenv as-lr python $R/out/check.py $R/out/micro2_$P/$bam.bam $args)   (truth: 150 inclusion, 150 skipping)"
  done; done
done
