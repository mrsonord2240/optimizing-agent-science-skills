#!/bin/bash
# SQANTI3 follow-ups: (1) filter behaviour on a planted intra-priming (A-rich downstream of TTS) isoform,
# (2) SQANTI3 on the FLAIR-collapsed isoforms of the SYNTHETIC HiFi data (end-to-end FLAIR -> SQANTI3), categories vs truth,
# (3) SQANTI3 with --fasta input from FLAIR (isoforms.fa) for the mm2 alignment route.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-long-read-splicing/run
D=$R/data/synth
O=$R/out/sqanti2; rm -rf $O; mkdir -p $O; cd $O
SQ="micromamba run -n as-sqanti"
echo "##### 1. planted intra-priming: copy genome, put 20 x A right after the 3' end of GC.1 (10901-10920)"
asenv as-core python - <<'PY'
D="/mnt/openscience/audits/bio-long-read-splicing/run/data/synth"
seq="".join(l.strip() for l in open(D+"/chrS1.fa") if not l.startswith(">"))
seq=seq[:10900]+"A"*20+seq[10920:]
open("chrS1_A.fa","w").write(">chrS1\n"+"\n".join(seq[i:i+60] for i in range(0,len(seq),60))+"\n")
g=open(D+"/query_isoforms.gtf").read().splitlines()
extra=[l.replace("Q01_GA1_exact","Q11_GC1_polyA") for l in g if False]
# Q11 = GC.1 (annotated, FSM) whose genome 3' end is followed by A-rich sequence
gc=[l for l in open(D+"/ref.gtf") if 'transcript_id "GC.1"' in l]
q=[l.replace('gene_id "GC"','gene_id "QC"').replace('transcript_id "GC.1"','transcript_id "Q11_GC1_polyA"') for l in gc]
open("query_A.gtf","w").write("".join(g[i]+"\n" for i in range(len(g)))+"".join(q))
PY
$SQ sqanti3_qc.py --isoforms query_A.gtf --refGTF $D/ref.gtf --refFasta chrS1_A.fa --output qcA --aligner_choice minimap2 --cpus 4 --report skip > qc1.log 2>&1; echo "qc rc=$?"
asenv as-core python - <<'PY'
import csv
rows=list(csv.DictReader(open("sqanti3_results/qcA_classification.txt"),delimiter="\t"))
for r in rows:
    if r["isoform"] in ("Q11_GC1_polyA","Q01_GA1_exact","Q02_GB1_exact"): print(r["isoform"],r["structural_category"],"perc_A_downstream_TTS=",r.get("perc_A_downstream_TTS"),"RTS_stage=",r.get("RTS_stage"),"polyA_motif_found=",r.get("polyA_motif_found"))
PY
$SQ sqanti3_filter.py rules --sqanti_class sqanti3_results/qcA_classification.txt --filter_gtf query_A.gtf --output fltA -d fltA_dir --skip_report > flt1.log 2>&1; echo "filter rc=$?"
echo "pass_isoforms:"; cat fltA_dir/fltA_pass_isoforms.txt 2>/dev/null | head -20
echo "filtering reasons:"; head -20 fltA_dir/fltA_filtering_reasons.txt 2>/dev/null
echo "##### 2. SQANTI3 on FLAIR isoforms (synthetic, junction_bed-corrected run) classification vs truth"
$SQ sqanti3_qc.py --isoforms $R/out/flair/collapsedSR.isoforms.gtf --refGTF $D/ref.gtf --refFasta $D/chrS1.fa --output flairqc --aligner_choice minimap2 --cpus 4 --report skip > qc2.log 2>&1; echo "qc rc=$?"
asenv as-core python - <<'PY'
import csv
for r in csv.DictReader(open("sqanti3_results/flairqc_classification.txt"),delimiter="\t"):
    print("%-22s %-24s %-32s gene=%-4s"%(r["isoform"],r["structural_category"],r["subcategory"],r["associated_gene"]))
PY
echo "##### 3. FASTA input route: --fasta with FLAIR isoforms.fa (aligns with minimap2 inside SQANTI3)"
$SQ sqanti3_qc.py --isoforms $R/out/flair/collapsedSR.isoforms.fa --fasta --refGTF $D/ref.gtf --refFasta $D/chrS1.fa --output flairfa --aligner_choice minimap2 --cpus 4 --report skip > qc3.log 2>&1; echo "qc rc=$?"; tail -2 qc3.log | cut -c1-200
[ -f sqanti3_results/flairfa_classification.txt ] && cut -f1,8,9 sqanti3_results/flairfa_classification.txt
