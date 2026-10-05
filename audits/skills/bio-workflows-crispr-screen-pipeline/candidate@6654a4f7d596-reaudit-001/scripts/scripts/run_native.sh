#!/bin/bash
# Re-audit native run: route commands as shipped in the candidate, clean dirs.
# Shared venv + tools; WSL (cn) and chronos run separately.
SK=/f/OpenScience/wt/recut-crispr-pipeline/skills/bio-workflows-crispr-screen-pipeline
ENV=/f/OpenScience/audit-envs/crispr-screen-analyst
DATA=$ENV/public-data/derived/crispr-pipeline
W=/f/OpenScience/fix-evidence/recut-crispr-pipeline/reaudit-001/work
export PATH=$ENV/Scripts:$ENV/bin:$PATH
PY=$ENV/Scripts/python.exe
BAGEL=$ENV/tools/dl/bagel/BAGEL.py
DRUGZ=$ENV/tools/dl/drugz/drugz.py
JACKS=$ENV/tools/dl/JACKS/jacks/run_JACKS.py
mkdir -p $W

# count
rm -rf $W/count; mkdir -p $W/count; cp $DATA/count/* $W/count/
cd $W/count
echo "### count"
mageck count --list-seq library.csv --sample-label Plasmid,Day18_r1,Day18_r2,Day18_r3 \
  --fastq Plasmid.fastq.gz Day18_r1.fastq.gz Day18_r2.fastq.gz Day18_r3.fastq.gz \
  --norm-method median --output-prefix experiment --trim-5 5 > log 2>&1
echo "EXIT[count]=$?"

# qc: HAP1 (real), qc-pass (simulated), no plasmid=
rm -rf $W/qc; mkdir -p $W/qc
cp $DATA/rra-qcpass/hap1.count.txt $W/qc/qcpass.count.txt; cp $DATA/qc/hap1.count.txt $W/qc/hap1.count.txt
cd $W/qc
echo "### qc real HAP1 plasmid=HAP1_T0"; $PY $SK/scripts/qc.py hap1.count.txt qc_real.tsv plasmid=HAP1_T0; echo "EXIT[qc_real]=$?"
echo "### qc simulated qcpass plasmid=HAP1_T0"; $PY $SK/scripts/qc.py qcpass.count.txt qc_pass.tsv plasmid=HAP1_T0; echo "EXIT[qc_pass]=$?"
echo "### qc no plasmid="; $PY $SK/scripts/qc.py hap1.count.txt qc_noplasmid.tsv; echo "EXIT[qc_noplasmid]=$?"
echo "### qc bad plasmid name"; $PY $SK/scripts/qc.py hap1.count.txt qc_bad.tsv plasmid=Plasmid; echo "EXIT[qc_bad]=$?"
echo "### qc normalized table"; $PY $SK/scripts/qc.py $W/count/experiment.count_normalized.txt qc_norm.tsv plasmid=Plasmid; echo "EXIT[qc_norm]=$?"
echo "### qc on count-route output"; $PY $SK/scripts/qc.py $W/count/experiment.count.txt qc_count.tsv plasmid=Plasmid min_depth=1; echo "EXIT[qc_count]=$?"

# rra on qc-pass table (canonical) and real HAP1
rm -rf $W/rra; mkdir -p $W/rra; cp $DATA/rra-qcpass/hap1.count.txt $W/rra/experiment.count.txt; cp $DATA/rra/hap1.count.txt $W/rra/hap1.count.txt
cd $W/rra
echo "### rra qcpass"; $PY $SK/scripts/rra.py experiment.count.txt essentiality_rra treatment=HAP1_T18A,HAP1_T18B,HAP1_T18C control=HAP1_T0; echo "EXIT[rra_qcpass]=$?"
echo "### rra real HAP1"; $PY $SK/scripts/rra.py hap1.count.txt hap1_rra treatment=HAP1_T18A,HAP1_T18B,HAP1_T18C control=HAP1_T0; echo "EXIT[rra_hap1]=$?"
echo "### rra missing control (guard)"; $PY $SK/scripts/rra.py hap1.count.txt guard treatment=HAP1_T18A; echo "EXIT[rra_guard]=$?"
echo "### rra control in treatment (guard)"; $PY $SK/scripts/rra.py hap1.count.txt guard2 treatment=HAP1_T0,HAP1_T18A control=HAP1_T0; echo "EXIT[rra_guard2]=$?"

# bagel2 on real HAP1
rm -rf $W/bagel2; mkdir -p $W/bagel2; cp $DATA/bagel2/* $W/bagel2/; cd $W/bagel2
echo "### bagel2"
$PY $BAGEL fc -i hap1.count.txt -o experiment -c HAP1_T0 --min-reads 30 > fc.log 2>&1; echo "EXIT[fc]=$?"
$PY $BAGEL bf -i experiment.foldchange -o bayes_factor.txt -e CEGv2.txt -n NEGv1.txt -c HAP1_T18A,HAP1_T18B,HAP1_T18C --seed 42 > bf.log 2>&1; echo "EXIT[bf]=$?"
$PY $BAGEL bf -i experiment.foldchange -o bayes_factor2.txt -e CEGv2.txt -n NEGv1.txt -c HAP1_T18A,HAP1_T18B,HAP1_T18C --seed 42 > bf2.log 2>&1; echo "EXIT[bf2]=$?"
$PY $BAGEL pr -i bayes_factor.txt -o pr_curve.txt -e CEGv2.txt -n NEGv1.txt > pr.log 2>&1; echo "EXIT[pr]=$?"

# mle
rm -rf $W/mle; mkdir -p $W/mle; cp $DATA/mle/* $W/mle/; cd $W/mle
echo "### mle"
mageck mle --count-table leukemia.count.txt --design-matrix designmat.txt --output-prefix timecourse_mle --norm-method median --permutation-round 10 > mle.log 2>&1
echo "EXIT[mle]=$?"

# drugz (data has one drug column: unpaired variant)
rm -rf $W/drugz; mkdir -p $W/drugz; cp $DATA/drugz/screen.count.txt $W/drugz/; cd $W/drugz
head -1 screen.count.txt
echo "### drugz"
$PY $DRUGZ -i screen.count.txt -o drugz_output.txt -c Veh_r1,Veh_r2 -x Drug_r1 -p 5 -unpaired > drugz.log 2>&1
echo "EXIT[drugz]=$?"

# jacks
rm -rf $W/jacks; mkdir -p $W/jacks; cp $DATA/jacks/* $W/jacks/; cd $W/jacks
echo "### jacks"
$PY $JACKS panel.count.txt replicatemap.txt guidemap.txt \
    --rep_hdr Replicate --sample_hdr Sample --ctrl_sample_hdr Control \
    --sgrna_hdr sgRNA --gene_hdr Gene --outprefix jacks_out --apply_w_hp > jacks.log 2>&1
echo "EXIT[jacks]=$?"

# consensus (from this run's own outputs)
rm -rf $W/consensus; mkdir -p $W/consensus; cd $W/consensus
echo "### consensus"
$PY $SK/scripts/consensus.py tier_consensus.csv mageck=$W/rra/hap1_rra.gene_summary.txt bagel=$W/bagel2/bayes_factor.txt drugz=$W/drugz/drugz_output.txt; echo "EXIT[consensus3]=$?"
$PY $SK/scripts/consensus.py tier2.csv mageck=$W/rra/hap1_rra.gene_summary.txt bagel=$W/bagel2/bayes_factor.txt; echo "EXIT[consensus2]=$?"
$PY $SK/scripts/consensus.py one.csv mageck=$W/rra/hap1_rra.gene_summary.txt; echo "EXIT[consensus1]=$?"
echo DONE
