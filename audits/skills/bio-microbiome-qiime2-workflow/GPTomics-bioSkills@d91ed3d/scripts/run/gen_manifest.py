import csv

samples = [f"S{i:02d}" for i in range(1, 11)]
base = "/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/casava_clean"

rows = [["sample-id", "forward-absolute-filepath", "reverse-absolute-filepath"]]
for s in samples:
    rows.append([
        s,
        f"{base}/{s}_S1_L001_R1_001.fastq.gz",
        f"{base}/{s}_S1_L001_R2_001.fastq.gz",
    ])

with open("/mnt/openscience/audits/bio-microbiome-qiime2-workflow/run/ws/manifest.tsv", "w", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerows(rows)

print("wrote manifest with", len(rows) - 1, "samples")
