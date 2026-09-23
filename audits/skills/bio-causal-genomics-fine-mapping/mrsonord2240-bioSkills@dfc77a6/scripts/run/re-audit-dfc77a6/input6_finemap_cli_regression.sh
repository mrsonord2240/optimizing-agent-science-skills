#!/usr/bin/env bash
# Final-pass verification: examples/finemap_pipeline.sh's FINEMAP CLI pattern, run for real.
set -euo pipefail
cd /mnt/openscience/audits/bio-causal-genomics-fine-mapping/run/re-audit-dfc77a6/finemap_cli_run

# --- Step 0: synthetic panel (2000 samples, 300 SNPs, no LD structure by construction) ---
/home/sci/.local/bin/micromamba run -n cg-finemap plink --dummy 2000 300 0 0 12 --out panel

# --- Step 1: plant a causal SNP and simulate a quantitative phenotype ---
/home/sci/.local/bin/micromamba run -n cg-finemap plink --bfile panel --recode A --out panel_raw

python3 - <<'PYEOF'
import random
random.seed(42)

with open('panel_raw.raw') as f:
    header = f.readline().split()
    rows = [line.split() for line in f]

snp_cols = header[6:]  # FID IID PAT MAT SEX PHENOTYPE <snps...>
causal_idx = 149  # SNP150 (0-based 149th data snp)
causal_col = 6 + causal_idx
print('Causal genotype column:', snp_cols[causal_idx])

geno = []
for r in rows:
    v = r[causal_col]
    geno.append(0.0 if v == 'NA' else float(v))

beta_true = 0.6
pheno_lines = []
for r, g in zip(rows, geno):
    y = beta_true * g + random.gauss(0, 1)
    pheno_lines.append(f"{r[0]} {r[1]} {y:.6f}")

with open('panel.phe', 'w') as f:
    f.write('\n'.join(pheno_lines) + '\n')

print('Wrote panel.phe, n=', len(pheno_lines))
PYEOF

# --- Step 2: real GWAS via plink --linear ---
/home/sci/.local/bin/micromamba run -n cg-finemap plink --bfile panel --pheno panel.phe --linear --allow-no-sex --out gwas

# --- Step 3: in-sample LD (exactly the example's own recipe, --r square) ---
/home/sci/.local/bin/micromamba run -n cg-finemap plink --bfile panel --r square spaces --out locus_ld

# --- Step 4: build FINEMAP .z file (rsid chromosome position allele1 allele2 maf beta se) ---
python3 - <<'PYEOF'
import csv

freq = {}
with open('/dev/null'):
    pass

# get MAF via plink --freq output built below in shell; placeholder read after
PYEOF

/home/sci/.local/bin/micromamba run -n cg-finemap plink --bfile panel --freq --out panel_freq

python3 - <<'PYEOF'
bim = {}
with open('panel.bim') as f:
    for line in f:
        chrom, snp, cm, pos, a1, a2 = line.split()
        bim[snp] = (chrom, pos, a1, a2)

freq = {}
with open('panel_freq.frq') as f:
    header = f.readline()
    for line in f:
        parts = line.split()
        chrom, snp, a1, a2, maf, nchrobs = parts
        freq[snp] = float(maf)

assoc = {}
with open('gwas.assoc.linear') as f:
    header = f.readline().split()
    for line in f:
        parts = line.split()
        rec = dict(zip(header, parts))
        if rec.get('TEST') != 'ADD':
            continue
        assoc[rec['SNP']] = rec

with open('panel.bim') as f:
    snp_order = [line.split()[1] for line in f]

with open('locus.z', 'w') as out:
    out.write('rsid chromosome position allele1 allele2 maf beta se\n')
    for snp in snp_order:
        chrom, pos, a1, a2 = bim[snp]
        maf = freq.get(snp, 0.0)
        rec = assoc.get(snp)
        beta = rec['BETA'] if rec and rec['BETA'] != 'NA' else '0'
        se = rec['STAT'] if False else (rec['SE'] if rec and 'SE' in rec and rec['SE'] != 'NA' else '1')
        out.write(f"{snp} {chrom} {int(pos) + 30000000} {a1} {a2} {maf} {beta} {se}\n")

print('Wrote locus.z with', len(snp_order), 'SNPs')
PYEOF

mv locus_ld.ld locus.ld

# --- Step 5: master file (exact format documented in references/finemap-cli.md) ---
cat > master.txt << 'EOF'
z;ld;snp;config;cred;log;n_samples
locus.z;locus.ld;locus.snp;locus.config;locus.cred;locus.log;2000
EOF

# --- Step 6: run FINEMAP exactly as SKILL.md's tighter-search invocation ---
/home/sci/.local/bin/micromamba run -n cg-finemap finemap --sss --in-files master.txt --n-causal-snps 5 --prob-conv-sss-tol 0.001 --n-iter 100000 --n-conv-sss 1000

echo "=== locus.snp top 10 by prob ==="
head -1 locus.snp
sort -k11 -nr locus.snp | head -10

echo "=== locus.cred* (head) ==="
head -20 locus.cred*

CAUSAL_SNP=$(awk 'NR==150{print $2}' panel.bim)
echo "=== Planted causal SNP was: $CAUSAL_SNP ==="
grep -w "$CAUSAL_SNP" locus.snp || true
