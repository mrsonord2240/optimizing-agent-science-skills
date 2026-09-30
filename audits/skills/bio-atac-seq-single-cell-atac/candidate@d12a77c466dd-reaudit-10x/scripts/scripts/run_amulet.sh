# independent re-audit AMULET per the Skill's flag table. usage: run_amulet.sh bam_arc | frag_arc | frag_atac2x
source /mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/tools/env.sh
A=$SCA/public-cache/amulet; P=$ATACDATA/10x-multiome; W=$SCA/work/reaudit10x_amulet_$1; rm -rf $W; mkdir -p $W; cd $W
REP=$A/RestrictionRepeatLists/restrictionlist_repeats_segdups_rmsk_hg38.bed
echo chr1 > chr1.txt
E="micromamba run -n bio-atac-seq-single-cell-atac-amulet"
M=$P/arc-pbmc3k/pbmc_granulocyte_sorted_3k_per_barcode_metrics.csv
case $1 in
bam_arc) ARGS="--forcesorted --bcidx 0 --cellidx 0 --iscellidx 3 $P/arc-pbmc3k/chr1_1-30Mb.possorted.bam $M";;
frag_arc) # exactly the skill text: two-column csv barcode,is__cell_barcode from 'barcode' and 'is_cell'
  python3 - "$M" > $W/arc_singlecell.csv <<'PY'
import csv,sys
r=csv.DictReader(open(sys.argv[1]));print("barcode,is__cell_barcode")
for x in r:print(f"{x['barcode']},{x['is_cell']}")
PY
  ARGS="$P/arc-pbmc3k/pbmc_granulocyte_sorted_3k_atac_fragments.tsv.gz $W/arc_singlecell.csv";;
frag_atac2x) ARGS="$P/atac2x-pbmc10k/chr1_1-30Mb.fragments.tsv.gz $P/atac2x-pbmc10k/10k_pbmc_ATACv2_nextgem_Chromium_Controller_singlecell.csv";;
esac
echo "CMD AMULET.sh $ARGS"
time $E bash $A/AMULET.sh $ARGS $W/chr1.txt $REP $W $A 2>&1 | tail -15
ls -la $W; cat $W/MultipletSummary.txt; wc -l $W/MultipletBarcodes_01.txt $W/MultipletProbabilities.txt
