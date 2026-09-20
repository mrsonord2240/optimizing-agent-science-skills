#!/bin/bash
# SKILL claims: microexons (3-27 nt) are detected because reads span them; --junc-bed helps poorly-annotated sites. Test on SYNTHETIC 10-nt microexon (planted truth).
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-long-read-splicing/run
asenv as-core python $R/make_micro.py
D=$R/data/synth_micro; O=$R/out/micro; rm -rf $O; mkdir -p $O; cd $O
LR="micromamba run -n as-lr"
cat > count_micro.py <<'PY'
import sys, pysam
bam=sys.argv[1]; lab=sys.argv[2]
# microexon exons: 1801-1810 -> junctions (1300,1800) and (1810,2400) (0-based half-open intron coords)
J1=(1300,1800); J2=(1810,2400); JS=(1300,2400)
c={"inc_total":0,"inc_with_micro":0,"inc_skipped_form":0,"inc_other":0,"skip_total":0,"skip_ok":0,"skip_with_micro":0}
for r in pysam.AlignmentFile(bam):
    if r.is_unmapped or r.is_secondary or r.is_supplementary: continue
    pos=r.reference_start; jn=[]
    for op,ln in r.cigartuples:
        if op==3: jn.append((pos,pos+ln)); pos+=ln
        elif op in (0,2,7,8): pos+=ln
    inc="_Minc_" in r.query_name
    has=(J1 in jn and J2 in jn); skp=(JS in jn)
    if inc:
        c["inc_total"]+=1
        if has: c["inc_with_micro"]+=1
        elif skp: c["inc_skipped_form"]+=1
        else: c["inc_other"]+=1
    else:
        c["skip_total"]+=1
        if skp: c["skip_ok"]+=1
        elif has: c["skip_with_micro"]+=1
print("%-52s microexon-including reads: %3d/%3d kept the 10-nt exon (%.0f%%), %3d aligned as exon-skipping, %3d other | skip reads correct %d/%d"%(lab,c["inc_with_micro"],c["inc_total"],100*c["inc_with_micro"]/max(c["inc_total"],1),c["inc_skipped_form"],c["inc_other"],c["skip_ok"],c["skip_total"]))
PY
G=$D/chrM.fa
al() { n=$1; fq=$2; shift 2; $LR minimap2 -ax "$@" -t 4 $G $fq 2>/dev/null | $LR samtools sort -o $n.bam - 2>/dev/null; $LR samtools index $n.bam; $LR python count_micro.py $n.bam "$n :: minimap2 -ax $*"; }
al hifi_hq   $D/hifi.fastq splice:hq -uf --secondary=no
al hifi_hq_junc $D/hifi.fastq splice:hq -uf --secondary=no --junc-bed $D/ref.bed12
al ont_k14   $D/ont.fastq splice -uf -k14 --secondary=no
al ont_k14_junc $D/ont.fastq splice -uf -k14 --secondary=no --junc-bed $D/ref.bed12
al ont_k14_juncbonus $D/ont.fastq splice -uf -k14 --secondary=no --junc-bed $D/ref.bed12 --junc-bonus 20
# IsoQuant (annotation-guided, on the same reads) : does it call/quantify the microexon isoform?
$LR isoquant --reference $G --genedb $D/ref.gtf --bam ont_k14.bam --data_type nanopore --stranded forward --output iq_ont --prefix m --threads 4 > iq.log 2>&1; echo "isoquant(ont_k14.bam) rc=$?"
cat iq_ont/m/m.transcript_counts.tsv 2>/dev/null | grep -v "^#"
$LR isoquant --reference $G --genedb $D/ref.gtf --bam hifi_hq.bam --data_type pacbio_ccs --stranded forward --output iq_hifi --prefix m --threads 4 > iq2.log 2>&1; echo "isoquant(hifi_hq.bam) rc=$?"
cat iq_hifi/m/m.transcript_counts.tsv 2>/dev/null | grep -v "^#"
# minimap2 -N claim and the 'too many anchors' error string
$LR minimap2 2>&1 | grep -E "^\s+-N|--secondary" | head -3
$LR bash -c 'strings $(which minimap2) 2>/dev/null | grep -i -c "too many anchors"'
