#!/usr/bin/env bash
# Final-pass verification: examples/susiex_multiancestry.sh's SuSiEx CLI pattern, run for real.
set -euo pipefail
MM=/home/sci/.local/bin/micromamba
cd /mnt/openscience/audits/bio-causal-genomics-fine-mapping/run/final-pass-20260923/susiex_cli_run3
mkdir -p susiex_run
cd susiex_run

# --- Two independent "populations" sharing the same 300-SNP panel layout ---
$MM run -n cg-finemap plink --dummy 1500 300 0 0 12 --out eur_panel
$MM run -n cg-finemap plink --dummy 800  300 0 0 12 --out afr_panel

# SuSiEx filters the PLINK .bim by the summary-statistic genomic coordinates.
# Keep the synthetic reference panels on the same 30 Mb coordinate system as the
# generated summary statistics; only the fixture coordinates change, not alleles.
for POP in eur afr; do
  awk 'BEGIN {OFS="\t"} {$4=$4+30000000; print}' "${POP}_panel.bim" > "${POP}_panel.bim.shifted"
  mv "${POP}_panel.bim.shifted" "${POP}_panel.bim"
done

for POP in eur afr; do
  $MM run -n cg-finemap plink --bfile ${POP}_panel --recode A --out ${POP}_raw
done

python3 - <<'PYEOF'
import random

for pop, seed in [('eur', 1), ('afr', 2)]:
    random.seed(seed)
    with open(f'{pop}_raw.raw') as f:
        header = f.readline().split()
        rows = [line.split() for line in f]
    causal_idx = 149
    causal_col = 6 + causal_idx
    geno = [0.0 if r[causal_col] == 'NA' else float(r[causal_col]) for r in rows]
    beta_true = 0.6
    with open(f'{pop}.phe', 'w') as f:
        for r, g in zip(rows, geno):
            y = beta_true * g + random.gauss(0, 1)
            f.write(f"{r[0]} {r[1]} {y:.6f}\n")
    print(pop, 'phenotype written, n=', len(rows))
PYEOF

for POP in eur afr; do
  $MM run -n cg-finemap plink --bfile ${POP}_panel --pheno ${POP}.phe --linear --allow-no-sex --out ${POP}_gwas
  $MM run -n cg-finemap plink --bfile ${POP}_panel --freq --out ${POP}_freq
done

python3 - <<'PYEOF'
for pop in ('eur', 'afr'):
    bim = {}
    with open(f'{pop}_panel.bim') as f:
        order = []
        for line in f:
            chrom, snp, cm, pos, a1, a2 = line.split()
            bim[snp] = (chrom, pos, a1, a2)
            order.append(snp)
    assoc = {}
    with open(f'{pop}_gwas.assoc.linear') as f:
        hdr = f.readline().split()
        for line in f:
            rec = dict(zip(hdr, line.split()))
            if rec.get('TEST') == 'ADD':
                assoc[rec['SNP']] = rec
    # Columns: CHR SNP BP A1 A2 BETA SE P  (col numbers 1..8)
    with open(f'{pop}_sumstats.txt', 'w') as out:
        out.write('CHR\tSNP\tBP\tA1\tA2\tBETA\tSE\tP\n')
        for snp in order:
            chrom, pos, a1, a2 = bim[snp]
            rec = assoc.get(snp)
            if rec is None or rec['BETA'] == 'NA':
                beta, se, p = '0', '1', '1'
            else:
                beta = rec['BETA']
                stat = float(rec['STAT'])
                se = str(abs(float(beta) / stat)) if stat != 0 else '1'
                p = rec['P']
            out.write(f"{chrom}\t{snp}\t{int(pos)}\t{a1}\t{a2}\t{beta}\t{se}\t{p}\n")
    print(pop, 'sumstats written')
PYEOF

PLINK_BIN=$($MM run -n cg-finemap which plink)
echo "plink binary: $PLINK_BIN"

mkdir -p susiex_out

set +e
$MM run -n cg-finemap SuSiEx \
    --sst_file=eur_sumstats.txt,afr_sumstats.txt \
    --n_gwas=1500,800 \
    --ref_file=eur_panel,afr_panel \
    --ld_file=eur_ld,afr_ld \
    --chr=1 \
    --bp=30000000,30000300 \
    --chr_col=1,1 \
    --snp_col=2,2 \
    --bp_col=3,3 \
    --a1_col=4,4 \
    --a2_col=5,5 \
    --eff_col=6,6 \
    --se_col=7,7 \
    --pval_col=8,8 \
    --plink="$PLINK_BIN" \
    --out_dir=susiex_out \
    --out_name=locus1 \
    --level=0.95 \
    --threads=4
RC=$?
echo "SuSiEx exit code: $RC"
set -e

echo "=== output dir ==="
ls -la susiex_out/ 2>&1 || true
if [ -f susiex_out/locus1.cs ]; then
  echo "=== locus1.cs ==="
  cat susiex_out/locus1.cs
fi
