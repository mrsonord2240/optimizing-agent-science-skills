import sys
tsv_path, out_path = sys.argv[1:3]
with open(tsv_path, encoding="utf-8") as f, open(out_path, "w", encoding="utf-8") as out:
    n = 0
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        fid, seq = parts[0], parts[2]
        out.write(f">{fid}\n{seq}\n")
        n += 1
print(f"wrote {n} records", file=sys.stderr)
