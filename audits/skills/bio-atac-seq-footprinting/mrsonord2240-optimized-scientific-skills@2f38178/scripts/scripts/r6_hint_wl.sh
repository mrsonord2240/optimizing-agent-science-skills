#!/bin/bash
# Re-audit: SKILL.md HINT-ATAC and Wellington -A commands (live envs, fingerprints unchanged since the prior fresh-recipe
# re-audit) and candidate scripts/site_concordance.sh against this re-audit's TOBIAS run A (cond1 = GM12878) calls.
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PATH=/home/sci/.local/bin:$PATH PYTHONDONTWRITEBYTECODE=1
Q=bio-atac-seq-footprinting; E=/mnt/openscience/audit-envs/$Q; SKILL=/mnt/openscience/wt/atac-footprinting/skills/$Q
W=$E/reaudit-final/hint; rm -rf $W; mkdir -p $W; cd $W
cp $E/fix-run/hint/pk60.bed $E/fix-run/hint/w.bam $E/fix-run/hint/w.bam.bai .
export RGTDATA=$E/rgtdata
mkdir hint_out
micromamba run -n $Q-rgt rgt-hint footprinting --atac-seq --paired-end --organism=hg38 --output-location hint_out --output-prefix sample w.bam pk60.bed > hint.log 2>&1; echo "hint rc=$?"
wc -l < hint_out/sample.bed; head -2 hint_out/sample.bed
mkdir wellington_out; micromamba run -n $Q-pydnase wellington_footprints.py -A pk60.bed w.bam wellington_out/ > wl.log 2>&1; echo "wellington -A rc=$?"; wc -l wellington_out/*FDR*.bed
export PATH=/home/sci/micromamba/envs/$Q/bin:$PATH
B=$E/reaudit-final/rt/A/bindetect
cat $B/*/beds/*_cond1_bound.bed > all_bound.bed; cat $B/*/beds/*_cond1_unbound.bed > all_unbound.bed
echo "### HINT vs TOBIAS"; bash $SKILL/scripts/site_concordance.sh all_bound.bed all_unbound.bed hint_out/sample.bed pk60.bed; echo "rc=$?"
echo "### Wellington -A vs TOBIAS"; bash $SKILL/scripts/site_concordance.sh all_bound.bed all_unbound.bed wellington_out/*FDR*.bed pk60.bed; echo "rc=$?"
echo "### guard: empty call set"; : > empty.bed; bash $SKILL/scripts/site_concordance.sh all_bound.bed all_unbound.bed empty.bed; echo "rc=$?"
# independent recomputation (python, interval overlap, no bedtools)
python3 - <<'PY'
import glob
def rd(p, R=None):
    s = sorted({tuple(l.split("\t")[:3]) for l in open(p) if l.strip()}); s = [(c, int(a), int(b)) for c, a, b in s]
    return [x for x in s if R is None or any(x[0] == r[0] and x[1] < r[2] and r[1] < x[2] for r in R)]
def ov(A, B): return sum(any(a[0] == b[0] and a[1] < b[2] and b[1] < a[2] for b in B) for a in A)
R = rd("pk60.bed"); bo, un = rd("all_bound.bed", R), rd("all_unbound.bed", R)
for name, p in (("HINT", "hint_out/sample.bed"), ("Wellington -A", glob.glob("wellington_out/*FDR*.bed")[0])):
    o = rd(p, R); print(f"python {name}: bound {ov(bo,o)}/{len(bo)} unbound {ov(un,o)}/{len(un)} reverse {ov(o,bo)}/{len(o)}")
PY
