#!/usr/bin/env python3
"""Build a small, real-identifier PTM-SEA input from the installed PTMsigDB v1.9.1."""
from pathlib import Path
import csv

gmt = Path(r"F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/tools/ssGSEA2.0/db/ptmsigdb/v1.9.1/ptm.sig.db.all.flanking.human.v1.9.1.gmt")
out = Path("ptmsea_sites.tsv")
target = []
other = []
seen = set()
for line in gmt.open(encoding="utf-8"):
    fields = line.rstrip("\n").split("\t")
    phospho = [x.split(";")[0] for x in fields[2:] if x.endswith("-p;u") or x.endswith("-p;d")]
    for site in phospho:
        if site in seen:
            continue
        seen.add(site)
        if fields[0] == "KINASE-PSP_CDK1":
            target.append(site)
        else:
            other.append(site)
if len(target) < 12:
    raise SystemExit("KINASE-PSP_CDK1 did not provide 12 phosphosite identifiers")
with out.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["seq_window", "stat"], delimiter="\t")
    writer.writeheader()
    for i, site in enumerate(target[:20] + other[:500]):
        core = site.removesuffix("-p")
        if len(core) != 15:
            raise SystemExit(f"unexpected PTMsigDB site length: {site}")
        writer.writerow({"seq_window": "AAAAAAAA" + core + "AAAAAAAA", "stat": 2.0 if i < 20 else ((i % 19) - 9) / 10})
print(f"wrote {20 + min(500, len(other))} real PTMsigDB identifiers to {out}; 20 are CDK1-shifted")
