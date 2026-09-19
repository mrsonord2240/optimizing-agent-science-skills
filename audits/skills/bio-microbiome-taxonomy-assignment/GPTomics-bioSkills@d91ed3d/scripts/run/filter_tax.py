import sys
ids_path, tax_path, out_path = sys.argv[1:4]
with open(ids_path, encoding="utf-8") as f:
    ids = set(line.strip() for line in f if line.strip())
with open(tax_path, encoding="utf-8") as f, open(out_path, "w", encoding="utf-8") as out:
    header = next(f)
    out.write(header)
    n = 0
    for line in f:
        fid = line.split("\t", 1)[0]
        if fid in ids:
            out.write(line)
            n += 1
print(f"wrote {n} rows", file=sys.stderr)
