#!/bin/bash
# (1) --junc-bed does not block novel junctions: chains of the novel-isoform reads (G057N skip, G058N +30-nt 5'ss) in the example's HiFi and ONT alignments.
# (2) Decision-tree row "De novo discovery: IsoQuant with --genedb omitted" on the planted HiFi alignment; models compared with truth chains.
R=/mnt/openscience/audits/bio-long-read-splicing/run; D=$R/data/plant; export PYTHONDONTWRITEBYTECODE=1
for P in hifi ont; do echo "== $P alignment made by the shipped example (--junc-bed annotation, annotation lacks G057N/G058N)"
  asenv as-lr python $R/pertx_check.py $R/out/ex_$P/out/ctrl1_aligned.bam $D/truth_chains.tsv | grep -A2 -E "^G05[78]N"; done
O=$R/out/iq_denovo; rm -rf $O; mkdir -p $O; cd $O
cp $D/chrQ.fa reference.fa
isoquant --reference reference.fa --bam $R/out/ex_hifi/out/ctrl1_aligned.bam --data_type pacbio_ccs --output iq_dn --threads 8 --prefix dn > dn.log 2>&1; echo "de novo IsoQuant rc=$?"
asenv as-lr python - <<PY
import re, collections
truth = {}
for ln in list(open("$D/truth_chains.tsv"))[1:]:
    f = ln.rstrip("\n").split("\t"); truth[f[0]] = tuple(tuple(map(int, j.split("-"))) for j in f[4].split(";"))
ex = collections.defaultdict(list)
for ln in open("iq_dn/dn/dn.transcript_models.gtf"):
    f = ln.rstrip("\n").split("\t")
    if len(f) > 8 and f[2] == "exon": ex[re.search(r'transcript_id "([^"]+)"', f[8]).group(1)].append((int(f[3]) - 1, int(f[4])))
ch = {t: tuple((sorted(e)[i][1], sorted(e)[i + 1][0]) for i in range(len(e) - 1)) for t, e in ex.items()}
found = {k for k, v in truth.items() if v in set(ch.values())}
print("de novo models: %d ; truth isoforms whose exact chain is among the models: %d/%d ; novel G057N found: %s ; G058N found: %s ; microexon G055A/G056A found: %s/%s" % (
    len(ch), len(found), len(truth), "G057N" in found, "G058N" in found, "G055A" in found, "G056A" in found))
PY
