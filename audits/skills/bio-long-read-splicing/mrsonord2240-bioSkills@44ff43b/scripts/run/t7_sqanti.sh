#!/bin/bash
# Input 4/7: SQANTI3 recipes from SKILL.md + example script on a SYNTHETIC isoform GTF with KNOWN categories (query_truth.tsv).
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-long-read-splicing/run
D=$R/data/synth
O=$R/out/sqanti; rm -rf $O; mkdir -p $O; cd $O
SQ="micromamba run -n as-sqanti"
echo "##### A. SKILL command (verbatim structure; CAGE/polyA files omitted because hg38 refTSS / motif list are not for a synthetic genome) with --output <prefix>"
$SQ sqanti3_qc.py --isoforms $D/query_isoforms.gtf --refGTF $D/ref.gtf --refFasta $D/chrS1.fa --output sqanti3_qc --aligner_choice minimap2 --cpus 4 --report skip > qcA.log 2>&1
echo "rc=$?"; tail -4 qcA.log | cut -c1-200; ls
echo "##### A2. SKILL verbatim WITH the old --skipORF (flag flagged by the tooling pass)"
$SQ sqanti3_qc.py --isoforms $D/query_isoforms.gtf --refGTF $D/ref.gtf --refFasta $D/chrS1.fa --output sqanti3_skiporf --aligner_choice minimap2 --cpus 4 --skipORF --report skip > qcA2.log 2>&1
echo "rc=$?"; tail -3 qcA2.log | cut -c1-200
echo "##### A3. SKILL full command incl. --CAGE_peak and --polyA_motif_list with files that do not exist (error handling)"
$SQ sqanti3_qc.py --isoforms $D/query_isoforms.gtf --refGTF $D/ref.gtf --refFasta $D/chrS1.fa --output sqanti3_nocage --aligner_choice minimap2 --CAGE_peak refTSS_v3.3_human_coordinate.hg38.bed --polyA_motif_list mouse_and_human.polyA_motif.txt --cpus 4 --report skip > qcA3.log 2>&1
echo "rc=$?"; tail -3 qcA3.log | cut -c1-250
echo "##### B. classification vs planted expected categories"
CLS=$(ls sqanti3_results/*_classification.txt | head -1); echo "classification file: $CLS"
asenv as-core python - <<'PY'
import csv,glob
D="/mnt/openscience/audits/bio-long-read-splicing/run/data/synth/query_truth.tsv"
exp={r["isoform"]:r["expected_category"] for r in csv.DictReader(open(D),delimiter="\t")}
f=sorted(glob.glob("sqanti3_results/sqanti3_qc_classification.txt"))[0]
rows=list(csv.DictReader(open(f),delimiter="\t"))
print("columns:", list(rows[0].keys())[:12], "...", len(rows[0]), "cols")
ok=0
for r in rows:
    e=exp[r["isoform"]]; got=r["structural_category"]; sub=r.get("subcategory","")
    m = (e==got) or (e=="genic" and got.startswith("genic"))
    ok+=m
    print("%-18s expected=%-24s got=%-24s sub=%-22s assoc_gene=%-4s canonical=%s RTS=%s FSM_class=%s %s"%(r["isoform"],e,got,sub,r["associated_gene"],r.get("all_canonical"),r.get("RTS_stage"),r.get("FSM_class",""),"OK" if m else "MISMATCH"))
print("category matches: %d/%d"%(ok,len(rows)))
PY
echo "##### C. sqanti3_filter.py rules (SKILL: --sqanti_class --filter_isoforms --filter_gtf --output)"
# isoform fasta for filter: extract from genome with gffread (SKILL passes 'isoforms.fa' without saying how to make it)
asenv as-core gffread -g $D/chrS1.fa -w query_isoforms.fa $D/query_isoforms.gtf
$SQ sqanti3_filter.py rules --sqanti_class sqanti3_results/sqanti3_qc_classification.txt --filter_isoforms query_isoforms.fa --filter_gtf $D/query_isoforms.gtf --output sqanti3_filtered > fltC.log 2>&1
echo "rc=$?"; tail -4 fltC.log | cut -c1-250; ls sqanti3_results | grep -i -E "filter|Rules" ; ls
echo "##### C2. same with --skip_report -d and inspect filter result"
$SQ sqanti3_filter.py rules --sqanti_class sqanti3_results/sqanti3_qc_classification.txt --filter_gtf $D/query_isoforms.gtf --output flt2 -d filt2 --skip_report > fltC2.log 2>&1
echo "rc=$?"; ls filt2 2>/dev/null; true
python3 - <<'PY'
import csv,glob
for f in glob.glob("filt2/*RulesFilter_result_classification.txt"):
    rows=list(csv.DictReader(open(f),delimiter="\t"))
    print(f, list(rows[0].keys())[-4:])
    for r in rows: print("  %-18s %-24s filter_result=%s"%(r["isoform"],r["structural_category"],r.get("filter_result")))
PY
echo "##### D. example-pipeline path convention: --output <dir>/sqanti3 with a slash and later classification at <dir>/sqanti3/<SAMPLE>_classification.txt"
mkdir -p exdir
$SQ sqanti3_qc.py --isoforms $D/query_isoforms.gtf --refGTF $D/ref.gtf --refFasta $D/chrS1.fa --output exdir/sqanti3 --aligner_choice minimap2 --cpus 4 --report skip > qcD.log 2>&1
echo "rc=$?"; tail -3 qcD.log | cut -c1-250; find . -name "*sqanti3_classification*" | head; ls exdir
echo "example expects: exdir/sqanti3/sample_classification.txt -> $([ -f exdir/sqanti3/sample_classification.txt ] && echo present || echo ABSENT)"
