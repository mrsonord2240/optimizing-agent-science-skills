# Synthetic thin-library dataset for bio-crispr-screens-bagel-essentiality audit.
# Purpose: exercise the Skill's documented "Bootstrap CI is wide; BF estimates
# unstable" failure mode (Failure Modes section, 3rd entry) with a real run,
# rather than trusting the prose. Genes are REAL CEGv2/NEGv1 symbols (read from
# the reference files shipped alongside BAGEL2) so the KDE has enough training
# material and the only stressed variable is sgRNAs/gene: 3/gene, below the
# Skill's own 4-6 sgRNA/gene recommendation.
import random
random.seed(7)

with open("CEGv2.txt") as fh:
    all_ess = [line.split("\t")[0] for line in fh.readlines()[1:] if line.strip()]
with open("NEGv1.txt") as fh:
    all_non = [line.split("\t")[0] for line in fh.readlines()[1:] if line.strip()]

essential_genes = all_ess[:100]
nonessential_genes = all_non[:100]

genes = essential_genes + nonessential_genes  # 200 real genes
sgrnas_per_gene = 3
samples = ["T0", "T18A", "T18B", "T18C"]

rows = []
for gene in genes:
    is_ess = gene in essential_genes
    for g in range(sgrnas_per_gene):
        seq = "".join(random.choice("ACGT") for _ in range(20))
        t0 = random.randint(200, 400)
        if is_ess:
            # dropout: strong depletion by T18, with sgRNA-to-sgRNA noise
            factor = max(0.02, random.gauss(0.08, 0.05))
        else:
            factor = max(0.5, random.gauss(1.0, 0.15))
        t18 = [max(0, int(t0 * factor * random.gauss(1.0, 0.1))) for _ in range(3)]
        rows.append([seq, gene, t0] + t18)

with open("HAP1_thin_library_synthetic.txt", "w") as fh:
    fh.write("SEQUENCE\tGENE\t" + "\t".join(samples) + "\n")
    for r in rows:
        fh.write("\t".join(str(x) for x in r) + "\n")

print(f"Wrote {len(rows)} sgRNA rows across {len(genes)} genes "
      f"({sgrnas_per_gene} sgRNAs/gene) -- SYNTHETIC data.")
