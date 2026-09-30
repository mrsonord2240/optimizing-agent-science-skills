source /mnt/openscience/audit-envs/bio-atac-seq-atac-qc/wsl_env.sh
S=/mnt/openscience/wt/atac-atac-qc/skills/bio-atac-seq-atac-qc/scripts
A=/mnt/openscience/audits/bio-atac-seq-atac-qc/audit-run; O=$A/out; cd $O
F=$ATACDATA/encode/GM12878_rep1_filtered.chr1_1-30000000.bam
T=$ATACDATA/annotation/gencode_v29_protein_coding_tss.chr1.bed
awk '$2>2000 && $2<29000000' $T > tss_slice_audit.bed; wc -l tss_slice_audit.bed
bamCoverage -b $F -o bw_extend.bw -bs 1 -p 8 --normalizeUsing None --extendReads >/dev/null 2>&1
bamCoverage -b $F -o bw_plain.bw -bs 1 -p 8 --normalizeUsing None >/dev/null 2>&1
bamCoverage -b $F -o bw_5p.bw -bs 1 -p 8 --normalizeUsing None --Offset 1 >/dev/null 2>&1
bamCoverage -b $F -o bw_cpm.bw -bs 10 -p 8 --normalizeUsing CPM --extendReads >/dev/null 2>&1
for b in extend plain 5p cpm; do echo "## bw_$b"; python $S/encode_tss_enrichment.py bw_$b.bw tss_slice_audit.bed | tr -d '\n '; echo; done
