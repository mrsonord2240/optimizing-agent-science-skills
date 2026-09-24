#!/bin/bash
# INPUT 3 (edge, regression): REAL chrX 2v2 (GBR ERR188383,ERR188428 vs YRI ERR188454,ERR204916; 2x75 nt paired-end, unstranded, Ensembl GRCh37; nf-core/rnasplice test data).
# Truth unknown for real data: assertions are internal consistency, the Skill's own quoted numbers, cross-tool concordance, permuted-label control.
# Sections: A rMATS (shipped example from a clean copy + permuted), B leafcutter (Skill flags -m 10, -i 2 -g 2 -c 10), C Shiba (Skill config), D SUPPA2 (Skill loop, both modes).
source /mnt/openscience/audits/bio-differential-splicing/run/common.sh
export LEAFCUTTER=$LC
W=$R/out/in3; rm -rf $W; mkdir -p $W; cd $W
S1=ERR188383; S2=ERR188428; S3=ERR188454; S4=ERR204916
declare -A G1=( [real]="$S1 $S2" [perm]="$S1 $S3" ); declare -A G2=( [real]="$S3 $S4" [perm]="$S2 $S4" )
echo "############ A. rMATS-turbo"
for cmp in real perm; do
  mkdir -p rmats_$cmp; cd rmats_$cmp
  l1=""; for s in ${G1[$cmp]}; do l1="$l1,$D/bam/$s.Aligned.out.bam"; done; echo "${l1#,}" > condition1_bams.txt
  l2=""; for s in ${G2[$cmp]}; do l2="$l2,$D/bam/$s.Aligned.out.bam"; done; echo "${l2#,}" > condition2_bams.txt
  cp $GTFX annotation.gtf; cp $SK/examples/diff_splicing_rmats.sh run.sh
  echo "--- $cmp: shipped example run.sh from a clean copy (auto-detect -t / --readLength)"
  PATH=$R/bin:$PATH $CORE bash run.sh > run.log 2>&1; echo "rc=$?"; grep -a 'Detected from\|rMATS analysis complete\|ERROR' run.log | cut -c1-220
  for e in SE A3SS A5SS MXE RI; do echo "$e rows $(($(wc -l < rmats_output/$e.MATS.JC.txt)-1))"; done
  cd ..
done
echo "--- SKILL.md block flags on the real reads with the WRONG stranding (fr-firststrand, data are unstranded): Skill says SE events drop 226 -> 121"
mkdir -p rmats_fs/tmp rmats_fs/out
$CORE rmats.py --b1 rmats_real/condition1_bams.txt --b2 rmats_real/condition2_bams.txt --gtf $GTFX -t paired --readLength 75 --variable-read-length --libType fr-firststrand --nthread 8 --od rmats_fs/out --tmp rmats_fs/tmp --novelSS --cstat 0.05 > rmats_fs.log 2>&1; echo "rc=$? SE rows $(($(wc -l < rmats_fs/out/SE.MATS.JC.txt)-1))"
echo "--- same with fr-unstranded + --novelSS (the block's flags, libType matched)"
mkdir -p rmats_un/tmp rmats_un/out
$CORE rmats.py --b1 rmats_real/condition1_bams.txt --b2 rmats_real/condition2_bams.txt --gtf $GTFX -t paired --readLength 75 --variable-read-length --libType fr-unstranded --nthread 8 --od rmats_un/out --tmp rmats_un/tmp --novelSS --cstat 0.05 > rmats_un.log 2>&1; echo "rc=$? SE rows $(($(wc -l < rmats_un/out/SE.MATS.JC.txt)-1))"
echo "--- --readLength 150 without --variable-read-length on 75 nt reads (Skill: 0 events)"
mkdir -p rmats_150/tmp rmats_150/out
$CORE rmats.py --b1 rmats_real/condition1_bams.txt --b2 rmats_real/condition2_bams.txt --gtf $GTFX -t paired --readLength 150 --libType fr-unstranded --nthread 8 --od rmats_150/out --tmp rmats_150/tmp > rmats_150.log 2>&1; echo "rc=$? SE rows $(($(wc -l < rmats_150/out/SE.MATS.JC.txt)-1))"
echo "--- --readLength 150 WITH --variable-read-length (Skill: rows appear)"
mkdir -p rmats_150v/tmp rmats_150v/out
$CORE rmats.py --b1 rmats_real/condition1_bams.txt --b2 rmats_real/condition2_bams.txt --gtf $GTFX -t paired --readLength 150 --variable-read-length --libType fr-unstranded --nthread 8 --od rmats_150v/out --tmp rmats_150v/tmp > rmats_150v.log 2>&1; echo "rc=$? SE rows $(($(wc -l < rmats_150v/out/SE.MATS.JC.txt)-1))"

echo "############ B. leafcutter (XS-tagged BAMs)"
mkdir -p lc; cd lc
for s in $S1 $S2 $S3 $S4; do PATH=$R/bin:$PATH regtools junctions extract -a 8 -m 50 -s XS $XB/$s.xs.bam -o $s.junc > /dev/null 2>&1; done
ls *.junc > juncfiles.txt
for m in 50 10; do
  PATH=$R/bin:$PATH python $LC/clustering/leafcutter_cluster_regtools.py -j juncfiles.txt -o lc$m -m $m -l 500000 > cl$m.log 2>&1
  echo "clustering -m $m rc=$? intron rows: $(zcat lc${m}_perind_numers.counts.gz | tail -n +2 | wc -l)   (Skill: -m 50 gives 0 clusters on ~100k-read chrX subsets)"
done
echo "--- STAR BAMs WITHOUT XS (the upstream BAMs) with -s XS: Skill says strand '?' and every junction dropped"
mkdir -p noxs; for s in $S1 $S2 $S3 $S4; do PATH=$R/bin:$PATH regtools junctions extract -a 8 -m 50 -s XS $D/bam/$s.Aligned.out.bam -o noxs/$s.junc > /dev/null 2>&1; done
awk '!/^track/{print $6}' noxs/$S1.junc | sort | uniq -c | tr '\n' ' '; echo
gzip -c $GTFX > annotation.gtf.gz
$RL Rscript $LC/scripts/gtf_to_exons.R annotation.gtf.gz exons.txt.gz > exons.log 2>&1; echo "gtf_to_exons rc=$? rows $(zcat exons.txt.gz | wc -l)"
printf "$S1\tGBR\n$S2\tGBR\n$S3\tYRI\n$S4\tYRI\n" > groups_real.txt
printf "$S1\tP1\n$S3\tP1\n$S2\tP2\n$S4\tP2\n" > groups_perm.txt
echo "--- default flags on 2v2"
$RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -o ds_default lc10_perind_numers.counts.gz groups_real.txt > ds_default.log 2>&1; echo "rc=$?"; grep -a 'less than min_samples_per_intron' ds_default.log | cut -c1-120
for cmp in real perm; do
  $RL Rscript $LC/scripts/leafcutter_ds.R --num_threads 4 -i 2 -g 2 -c 10 --exon_file exons.txt.gz -o ds_$cmp lc10_perind_numers.counts.gz groups_$cmp.txt > ds_$cmp.log 2>&1
  echo "leafcutter $cmp (-i 2 -g 2 -c 10) rc=$? tested $(ntested ds_${cmp}_cluster_significance.txt) ; p.adjust<0.05: $(nsig ds_${cmp}_cluster_significance.txt)"
done
cd ..

echo "############ C. Shiba 0.8.2 (config keys exactly as SKILL.md)"
for cmp in real perm; do
  mkdir -p shiba_$cmp; ( cd shiba_$cmp
  { printf 'sample\tbam\tgroup\ttechnology\n'
    for s in ${G1[$cmp]}; do printf '%s\t%s/%s.xs.bam\tRef\tshort\n' $s $XB $s; done
    for s in ${G2[$cmp]}; do printf '%s\t%s/%s.xs.bam\tAlt\tshort\n' $s $XB $s; done; } > exp.tsv
  cat > config.yaml <<CFG
workdir: $W/shiba_$cmp/shiba_out
gtf: $GTFX
experiment_table: $W/shiba_$cmp/exp.tsv
unannotated: False
minimum_anchor_length: 6
minimum_intron_length: 50
maximum_intron_length: 500000
strand: XS
only_psi: False
only_psi_group: False
fdr: 0.05
delta_psi: 0.1
reference_group: Ref
alternative_group: Alt
minimum_reads: 10
individual_psi: True
ttest: False
excel: False
CFG
  $SH shiba.py -p 8 --mame config.yaml > shiba.log 2>&1; echo "shiba $cmp rc=$?"; ls shiba_out/results/splicing 2>/dev/null | tr '\n' ' '; echo )
done

echo "############ D. SUPPA2 2.4 (as-suppa, statsmodels 0.14.6): SKILL.md loop, then the classical-mode variant"
mkdir -p suppa; cd suppa
$CORE python - <<PY
import pandas as pd
cols = {s: pd.read_csv("$D/salmon/%s/quant.sf" % s, sep="\t", index_col=0)["TPM"] for s in ("$S1", "$S2", "$S3", "$S4")}
t = pd.DataFrame(cols)
def w(name, sub):
    with open(name, "w") as o:   # header = sample names only (Skill: no Name/transcript label)
        o.write("\t".join(sub) + "\n")
        for tid, row in t[sub].iterrows(): o.write(tid + "\t" + "\t".join("%.4f" % v for v in row) + "\n")
w("gbr_tpm.tsv", ["$S1", "$S2"]); w("yri_tpm.tsv", ["$S3", "$S4"]); w("p1_tpm.tsv", ["$S1", "$S3"]); w("p2_tpm.tsv", ["$S2", "$S4"])
print("TPM table", t.shape)
PY
$CORE python $R/extract_blocks.py get 5 /tmp/blk5.sh
for pair in "gbr yri real" "p1 p2 perm"; do set -- $pair
  mkdir -p $3; cd $3; cp $GTFX annotation.gtf
  sed -e "s/ctrl_tpm.tsv/${1}_tpm.tsv/g" -e "s/trt_tpm.tsv/${2}_tpm.tsv/g" -e "s/ctrl_/${1}_/g" -e "s/trt_/${2}_/g" -e 's#suppa.py#micromamba run -n as-suppa suppa.py#g' /tmp/blk5.sh > blk5.sh
  cp ../${1}_tpm.tsv ../${2}_tpm.tsv .
  bash blk5.sh > blk5.log 2>&1; echo "SKILL.md SUPPA2 loop ($3: $1 vs $2, empirical -gc) rc=$?"; ls diff_*.dpsi | tr '\n' ' '; echo
  for ev in SE A5 A3 MX RI; do
    $SU suppa.py diffSplice -m classical -gc -i events_${ev}_strict.ioe -p ${1}_${ev}.psi ${2}_${ev}.psi -e ${1}_tpm.tsv ${2}_tpm.tsv -o diffc_${ev} > diffc_${ev}.log 2>&1
  done
  cd ..
done
cd ..
echo "############ analysis"
$CORE python $R/in3_analyze.py $W $GTFX
