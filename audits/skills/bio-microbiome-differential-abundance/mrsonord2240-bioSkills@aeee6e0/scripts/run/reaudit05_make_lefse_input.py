"""Build a LEfSe-formatted input file from the fixture's ASV counts + metadata,
following SKILL.md's documented format exactly: row 1 = "class" + each sample's
group label; remaining rows = feature + counts (features in rows, samples in
columns).
"""
import csv

base = "F:/OpenScience/audits/bio-microbiome-differential-abundance/data/asvtable"

with open(f"{base}/metadata.tsv", encoding="utf-8") as f:
    r = csv.DictReader(f, delimiter="\t")
    group_of = {row["SampleID"]: row["Group"] for row in r}

with open(f"{base}/asv_counts.tsv", encoding="utf-8") as f:
    rows = list(csv.reader(f, delimiter="\t"))

header = rows[0]
samples = header[1:]
classes = [group_of[s] for s in samples]

out_path = "F:/OpenScience/audits/bio-microbiome-differential-abundance/run/lefse_input.txt"
with open(out_path, "w", encoding="utf-8", newline="\n") as out:
    out.write("class\t" + "\t".join(classes) + "\n")
    for row in rows[1:]:
        out.write("\t".join(row) + "\n")

print(f"Wrote {out_path}: {len(rows)-1} features x {len(samples)} samples, classes={set(classes)}")
