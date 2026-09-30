source /mnt/openscience/audits/bio-atac-seq-atac-qc/reaudit-run/scripts/env.sh; cd $O
j(){ tr -d '\n ' ; echo; }
T(){ echo "## $1"; shift; python $S/encode_tss_enrichment.py "$@" 2>&1 | j; echo "exit=${PIPESTATUS[0]}"; }
T "planted BED6 (truth 21.0; 3 TSS incl minus & chr2)" planted.bw tss_bed6.bed
T "gene intervals (minus TSS=end-1; truth 21.0)" planted.bw gene_bed6.bed
T "absent chrom (expect exit1)" planted.bw absent_chrom.bed
T "empty BED (expect exit1)" planted.bw empty.bed
T "BED3 (expect error)" planted.bw bed3.bed
T "mixed valid+absent+edge (expect used 1)" planted.bw mixed.bed
echo "## real slice, in-slice TSS (deepTools ref 11.391)"; python $S/encode_tss_enrichment.py $QCROOT/work/rep1.bw $QCROOT/work/tss_slice.bed --output real.json | j
