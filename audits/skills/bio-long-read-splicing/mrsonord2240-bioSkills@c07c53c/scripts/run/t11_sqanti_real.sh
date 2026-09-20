#!/bin/bash
# SQANTI3 block VERBATIM (incl. --CAGE_peak/--polyA_motif_list, downloaded from the URLs the SKILL names) on REAL FLAIR isoforms (out/real), and on the
# FLAIR isoforms of my planted 6-sample run (out/hifi6) where the novel categories are known: G057N = novel_in_catalog, G058N = novel_not_in_catalog.
R=/mnt/openscience/audits/bio-long-read-splicing/run; B=$R/out/blocks; export PYTHONDONTWRITEBYTECODE=1
cd $R/out/real; rm -rf sqanti3_qc sqanti3_filtered
cp flair_collapsed.isoforms.gtf isoforms.gtf
gunzip -c $R/out/dl/hg38.cage_peak_phase1and2combined_coord.bed.gz > hg38.cage_peak_phase1and2combined_coord.bed; cp $R/out/dl/human.polyA.list.txt .
echo "########## REAL: SQANTI3 block verbatim on FLAIR isoforms.gtf (34 isoforms expected)"
bash $B/sqanti3-classification_1.sh > sqanti_block.log 2>&1; echo "rc=$?"; grep -a -E "Traceback|ERROR|Error" sqanti_block.log | head -5
echo "isoforms in isoforms.gtf: $(awk '$3=="transcript"' isoforms.gtf | wc -l)"
python3 - <<'PY'
import csv, collections
rows = list(csv.DictReader(open("sqanti3_qc/sqanti3_classification.txt"), delimiter="\t"))
print("classification rows:", len(rows), dict(collections.Counter(r["structural_category"] for r in rows)))
print("within_CAGE_peak filled:", collections.Counter(r["within_CAGE_peak"] for r in rows), " polyA_motif_found:", collections.Counter(r["polyA_motif_found"] for r in rows))
PY
ls sqanti3_filtered | tr '\n' ' '; echo; echo "pass_isoforms: $(wc -l < sqanti3_filtered/sqanti3_filtered_pass_isoforms.txt)  filtered.gtf lines: $(wc -l < sqanti3_filtered/sqanti3_filtered.filtered.gtf)"
echo "########## PLANTED: FLAIR isoforms (hifi6), SQANTI3 block without the optional CAGE/polyA lines"
cd $R/out/hifi6; rm -rf sqanti3_qc sqanti3_filtered; cp flair_collapsed.isoforms.gtf isoforms.gtf
grep -v -E "CAGE_peak|polyA_motif_list" $B/sqanti3-classification_1.sh > sq_block.sh
bash sq_block.sh > sq.log 2>&1; echo "rc=$?"; grep -a -E "Traceback|ERROR" sq.log | head -3
python3 - <<'PY'
import csv, collections, re, os
D = "/mnt/openscience/audits/bio-long-read-splicing/run/data/plant"
truth = {}
for ln in list(open(D + "/truth_chains.tsv"))[1:]:
    f = ln.rstrip("\n").split("\t"); truth[f[0]] = (f[3] == "1")
rows = list(csv.DictReader(open("sqanti3_qc/sqanti3_classification.txt"), delimiter="\t"))
cat = {r["isoform"].split("_")[0]: r["structural_category"] for r in rows}
print("categories:", dict(collections.Counter(cat.values())))
print("annotated truth isoforms classified FSM: %d/%d" % (sum(1 for t, a in truth.items() if a and cat.get(t) == "full-splice_match"), sum(1 for a in truth.values() if a)))
print("novel G057N (skip exon, known junction combination) ->", cat.get("G057N"), " ; novel G058N (novel 5'ss +30 nt) ->", cat.get("G058N"))
PY
echo "pass_isoforms: $(wc -l < sqanti3_filtered/sqanti3_filtered_pass_isoforms.txt)"
