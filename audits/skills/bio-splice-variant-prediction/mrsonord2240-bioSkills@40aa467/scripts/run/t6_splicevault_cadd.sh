#!/bin/bash
# Input 6: SpliceVault example + CADD API block from SKILL.md, run as written (env as-spvp).
export PYTHONDONTWRITEBYTECODE=1
cd /mnt/openscience/audits/bio-splice-variant-prediction/run
mkdir -p out/sv && cd out/sv
curl -sS -O https://ftp.ensembl.org/pub/current_variation/SpliceVault/SpliceVault_data_GRCh38.tsv.gz.tbi; ls -la *.tbi
S=../../skill/examples
echo "== TP53 c.673-2A>G (SKILL.md command)"
micromamba run -n as-spvp python $S/splicevault_lookup.py chr17 7674292 T C --transcript ENST00000269305 --tbi SpliceVault_data_GRCh38.tsv.gz.tbi
echo "== all transcripts for TP53 (no --transcript filter): rows"
micromamba run -n as-spvp python $S/splicevault_lookup.py chr17 7674292 T C --tbi SpliceVault_data_GRCh38.tsv.gz.tbi | grep -c "samples"
echo "== DMD c.9563+1G>A (GRCh38 chrX:31209497 C>T)"
micromamba run -n as-spvp python $S/splicevault_lookup.py chrX 31209497 C T --tbi SpliceVault_data_GRCh38.tsv.gz.tbi | head -12
echo "== deep intronic GLA c.639+919G>A (expect: not catalogued)"
micromamba run -n as-spvp python $S/splicevault_lookup.py chrX 101399747 C T --tbi SpliceVault_data_GRCh38.tsv.gz.tbi
echo "== wrong REF (expect: no entry message)"
micromamba run -n as-spvp python $S/splicevault_lookup.py chr17 7674292 A C --tbi SpliceVault_data_GRCh38.tsv.gz.tbi
echo "== bare contig name '17'"
micromamba run -n as-spvp python $S/splicevault_lookup.py 17 7674292 T C --transcript ENST00000269305 --tbi SpliceVault_data_GRCh38.tsv.gz.tbi | head -2
echo "== CADD API (SKILL.md curl block)"
curl -s "https://cadd.gs.washington.edu/api/v1.0/GRCh38-v1.7/17:7674292_T_C"; echo
curl -s "https://cadd.gs.washington.edu/api/v1.0/GRCh38-v1.7/23:31209497_C_T"; echo
curl -s "https://cadd.gs.washington.edu/api/v1.0/GRCh38-v1.7/X:101399747_C_T"; echo
