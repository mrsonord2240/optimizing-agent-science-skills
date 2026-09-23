"""Create a small FOCUS panel from the final-pass FUSION fixture for fresh execution."""
from pathlib import Path
import math
import shutil

audit = Path(r"F:\OpenScience\audits\bio-causal-genomics-transcriptome-wide-association")
fusion = audit / "data" / "fusion"
out = audit / "data" / "focus_final"
if out.exists():
    shutil.rmtree(out)
(out / "1000G_EUR").mkdir(parents=True)
for suffix in ("bed", "bim", "fam"):
    shutil.copyfile(fusion / "ld" / f"EUR.1.{suffix}", out / "1000G_EUR" / f"all.{suffix}")

lookup = {}
with (fusion / "ld" / "EUR.1.bim").open() as handle:
    for line in handle:
        chrom, snp, _cm, pos, a1, a0 = line.split()
        if snp in {"rs637471", "rs2786797"}:
            lookup[snp] = (chrom, int(pos), a1, a0)
if set(lookup) != {"rs637471", "rs2786797"}:
    raise RuntimeError(f"expected fixture SNPs not found: {lookup}")

rows = [("GENE1", "rs637471", 0.18, 1e-6), ("GENE2", "rs2786797", 0.09, 1e-3)]
with (out / "panel.tsv").open("w", newline="") as handle:
    handle.write("gene\tchrom\ttxstart\ttxstop\tsnp\tpos\ta1\ta0\tweight\tcv_r2\tcv_r2_pval\n")
    for gene, snp, r2, pval in rows:
        chrom, pos, a1, a0 = lookup[snp]
        handle.write(f"{gene}\t{chrom}\t{pos-500000}\t{pos+500000}\t{snp}\t{pos}\t{a1}\t{a0}\t1.0\t{r2}\t{pval}\n")

z = {"rs637471": 6.5, "rs2786797": -0.5568952560424805}
with (out / "gwas.sumstats").open("w", newline="") as handle:
    handle.write("CHR SNP BP A1 A2 Z P\n")
    for snp, value in z.items():
        chrom, pos, a1, a0 = lookup[snp]
        p = math.erfc(abs(value) / math.sqrt(2.0))
        handle.write(f"{chrom} {snp} {pos} {a1} {a0} {value} {p:.12g}\n")
print(f"wrote {out}: 2 genes and 2 GWAS SNPs")
