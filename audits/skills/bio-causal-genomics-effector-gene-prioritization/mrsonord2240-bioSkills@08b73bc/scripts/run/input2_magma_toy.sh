#!/usr/bin/env bash
set -euo pipefail

# Phase-2 regression: execute the shipped MAGMA pipeline on the shipped PCSK9 fixture
# from an audit-owned copy of the pinned source.
AUDIT=/f/OpenScience/audits/bio-causal-genomics-effector-gene-prioritization
SKILL="$AUDIT/run/skill_copy"
OUT="$AUDIT/run/outputs/input2_magma_toy"
MAGMA=/f/OpenScience/audit-envs/mendelian-randomization-analyst/tools/magma/magma.exe
REF=F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/magma/g1000_eur/g1000_eur

rm -rf "$OUT"
mkdir -p "$OUT"
cp "$SKILL/examples/toy_gwas_sumstats.tsv" "$OUT/gwas.pval.tsv"
cp "$SKILL/examples/toy_gene_loc.txt" "$OUT/NCBI37.3.gene.loc"
cp "$SKILL/examples/toy_snp_loc.txt" "$OUT/gwas.snploc"
printf 'SET_PC\tPCSK9\nSET_DECOY\tDECOY_UPSTREAM\tDECOY_DOWNSTREAM\n' > "$OUT/msigdb_v7.5_C2.gmt"

cd "$OUT"
# MAGMA 1.10's Windows parser resolves a bfile prefix relative to its working
# directory even when Git Bash passes an absolute path. Use audit-owned links.
ln -sf "$REF.bed" g1000_eur.bed
ln -sf "$REF.bim" g1000_eur.bim
ln -sf "$REF.fam" g1000_eur.fam
PATH="$(dirname "$MAGMA"):$PATH" \
  GWAS_PVAL=gwas.pval.tsv GENE_LOC=NCBI37.3.gene.loc SNP_LOC=gwas.snploc \
  REF_BFILE=g1000_eur GENESET_GMT=msigdb_v7.5_C2.gmt OUT_PREFIX=magma_run \
  bash "$SKILL/examples/magma_genebased.sh" | tee input2_magma_toy.log

test -s magma_run_gene.genes.out
test -s magma_run_top50.tsv
awk 'NR==2 { if ($1 != "PCSK9") { print "FAIL: PCSK9 not top gene" > "/dev/stderr"; exit 1 } }' magma_run_top50.tsv
grep -F 'Skipping Step 3' input2_magma_toy.log
echo 'ASSERTIONS PASS: output files exist; PCSK9 ranks first; <200 guard skipped gene-set analysis.'
