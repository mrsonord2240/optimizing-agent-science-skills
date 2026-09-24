#!/bin/bash
# t27 printed identical FLAIR numbers with and without SR_JUNCTIONS on real cDNA. Is the junction file used at all? flair correct on the same BED, three ways.
R=/mnt/openscience/audits/bio-long-read-splicing/run; P=/mnt/openscience/audit-envs/alternative-splicing/public-data/longread/flair_test; cd $R/out/ex_realont_sj/out
head -3 $P/input/basic.shortread_junctions.tab; wc -l $P/input/basic.shortread_junctions.tab
for V in "none|" "tab|--junction_tab $P/input/basic.shortread_junctions.tab"; do N=${V%%|*}; A=${V#*|}
  flair correct -q lrgasp.bed -f ../annotation.gtf $A -o chk_$N -t 6 > chk_$N.log 2>&1; echo "$N: rc=$? corrected $(wc -l < chk_${N}_all_corrected.bed) inconsistent $(wc -l < chk_${N}_all_inconsistent.bed)"; done
python3 - <<'PY'
import re, collections
ann = set()
for ln in open("../annotation.gtf"):
    f = ln.split("\t")
    if len(f) > 8 and f[2] == "exon": ann.add((f[0], int(f[3]), int(f[4]), re.search(r'transcript_id "([^"]+)"', f[8]).group(1)))
ex = collections.defaultdict(list)
for c, a, b, t in ann: ex[t].append((c, a, b))
introns = set()
for t, e in ex.items():
    e.sort(key=lambda x: x[1])
    for i in range(len(e) - 1): introns.add((e[i][0], e[i][2] + 1, e[i + 1][1] - 1))
import os
P = "/mnt/openscience/audit-envs/alternative-splicing/public-data/longread/flair_test/input/basic.shortread_junctions.tab"
sj = [tuple(ln.split("\t")[:3]) for ln in open(P) if ln.strip()]
sj = {(c, int(a), int(b)) for c, a, b in sj}
print("short-read junctions %d ; of them annotated introns %d ; not in the annotation %d" % (len(sj), len(sj & introns), len(sj - introns)))
PY
