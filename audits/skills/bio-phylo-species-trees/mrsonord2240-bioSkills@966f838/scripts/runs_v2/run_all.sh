#!/bin/bash
# Re-audit of bio-phylo-species-trees at mrsonord2240/bioSkills@966f838. SYNTHETIC data (data/make_data.py).
# Per-locus gene trees are REUSED from the pre-fix audit (runs/inN/loci.treefile: `iqtree2 -S ... -B 1000 --seed 12345`,
# a command the fix did not change apart from the binary name); every ASTER / concordance step is re-run.
set -u
A=/f/OpenScience/audits/bio-phylo-species-trees; R=$A/runs_v2; OLD=$A/runs
X=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/aster/ASTER-Windows/exe
PY=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts/python.exe
JAR=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/Astral/astral.5.7.8.jar
SK=/f/OpenScience/external/mrsonord2240__bioSkills/phylogenetics/species-trees
TT="$PY $A/data/treetools.py"
export PATH=$X:/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools/bin:$PATH
export PYTHONIOENCODING=utf-8

pipe() { # $1 inN  $2 dataset  $3 outgroup
  mkdir -p $R/$1 && cd $R/$1
  cp $OLD/$1/loci.treefile . ; [ -f $OLD/$1/concat.treefile ] && cp $OLD/$1/concat.treefile .
  $TT contract loci.treefile gene_trees.nwk 10
  wastral -i gene_trees.nwk -o species_wastral.tre 2> species_wastral.log;          echo "wastral exit $?"
  astral -t 4 -i gene_trees.nwk -o species.tre 2> species.log;                      echo "astral -t 4 exit $?"
  astral -u 2 -i gene_trees.nwk -o species_annot.tre 2> species_annot.log;          echo "astral -u 2 exit $?"
  astral --root $3 -i gene_trees.nwk -o species_rooted.tre 2> species_rooted.log;   echo "astral --root exit $?"
  astral --length CULength -i gene_trees.nwk -o species_cu.tre 2> species_cu.log;   echo "astral --length CULength exit $?"
  iqtree2 -t species.tre --gcf gene_trees.nwk --prefix cf_g > cf_g.stdout 2>&1;     echo "Skill gCF call exit $?"
  iqtree2 -te species.tre -s $A/data/$2/concat.fasta --scfl 100 --prefix cf_s > cf_s.stdout 2>&1; echo "Skill sCF call exit $?"
  echo "-- RF vs simulated species tree"; $TT rf $A/data/$2/species_true.nwk species_wastral.tre species.tre species_rooted.tre concat.treefile
  echo "-- -u 2 labels"; $TT splits species_annot.tre
  echo "-- gCF"; grep -v '^#' cf_g.cf.stat; echo "-- sCF"; grep -v '^#' cf_s.cf.stat | cut -f1-8
}

echo "######## IN1 rad canonical"; pipe in1 rad S10
echo "######## IN2 az anomaly zone"; pipe in2 az Sp_O
cd $R/in2 && java -jar $JAR -i gene_trees.nwk -t 10 -o polytomy_t10.tre > polytomy.log 2>&1; echo "java -t 10 exit $?"; cat polytomy_t10.tre
cp $OLD/in2/est_gene_tree_freq.txt . 2>/dev/null; head -4 est_gene_tree_freq.txt
echo "######## IN3 short loci"; pipe in3 short S10
echo "######## IN4 intro: -u 3 freqQuad + binomial on gDF1/gDF2 (Skill's test)"; pipe in4 intro Sp_H
cd $R/in4 && mkdir -p u3 && (cd u3 && astral -u 3 -i ../gene_trees.nwk -o sp_u3.tre 2> u3.log; echo "astral -u 3 exit $?"; ls; head -20 freqQuad.csv 2>/dev/null)
$PY $R/symtest.py cf_g.cf.stat
echo "######## IN5 fam: ASTRAL-Pro with -a (Skill verbatim)"
mkdir -p $R/in5 && cd $R/in5 && cp $OLD/in5/loci.treefile family_trees.nwk && cp $A/data/fam/gene2species.txt .
astral-pro -a gene2species.txt -i family_trees.nwk -o species_pro.tre 2> species_pro.log; echo "astral-pro -a exit $?"; cat species_pro.tre
astral-pro -u 2 -a gene2species.txt -i family_trees.nwk -o species_pro_u2.tre 2> pro_u2.log; echo "exit $?"
$TT rf $A/data/fam/species_true.nwk species_pro.tre; $TT splits species_pro_u2.tre
echo "######## IN6 units on rad: default vs --length CULength vs wastral (S01,S02 true 0.20 CU)"
cd $R/in1 && echo "default:  $(cat species.tre)"; echo "CULength: $(cat species_cu.tre)"; echo "wastral:  $(cat species_wastral.tre)"
echo "######## IN7 -t 4 (Java -t 8 intent) vs -u 2 labels"
cd $R/in1 && echo "-t 4 tree: $(cat species.tre)"; grep -o "q1=[0-9.]*" species_annot.tre | head -3
echo "######## IN8 NEW: measure ILS first on az: rooted CULength + -u 2"
mkdir -p $R/in8 && cd $R/in8 && cp $R/in2/gene_trees.nwk .
astral --root Sp_O --length CULength -u 2 -i gene_trees.nwk -o az_cu_rooted.tre 2> az.log; echo "exit $?"; cat az_cu_rooted.tre
echo "######## IN9 NEW: inconsistent leaf names across gene trees"
mkdir -p $R/in9 && cd $R/in9 && $PY $R/relabel.py
astral -i gene_trees_mixed.nwk -o sp_mixed.tre 2> sp_mixed.log; echo "astral plain exit $?"; cat sp_mixed.tre; grep -i -E "warn|taxa|species" sp_mixed.log | head -5
astral -h 2>&1 | grep -i -E "mapping|-a " | head -3
astral -a name2species.txt -i gene_trees_mixed.nwk -o sp_mapped.tre 2> sp_mapped.log; echo "astral -a exit $?"; cat sp_mapped.tre
$TT rf $A/data/rad/species_true.nwk sp_mapped.tre
wastral -i gene_trees_mixed.nwk -o sp_mixed_w.tre 2> w.log; echo "wastral plain exit $?"; cat sp_mixed_w.tre
echo "######## EXAMPLE astral_pipeline.sh as shipped"
mkdir -p $R/example && cd $R/example && cp -r $OLD/example/loci $OLD/example/concat.fasta $OLD/example/shim . && bash -n $SK/examples/astral_pipeline.sh && echo "bash -n OK"
t0=$(date +%s); PATH=$R/example/shim:$PATH bash $SK/examples/astral_pipeline.sh > example.out 2>&1; echo "example exit $? after $(( $(date +%s) - t0 ))s"
tail -12 example.out; ls species_tree_results | head -30
$TT rf $A/data/rad/species_true.nwk species_tree_results/species_wastral.tre species_tree_results/species_astral.tre
echo ALL DONE
