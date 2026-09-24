#!/usr/bin/env python3
"""Make a syntactically valid one-row KSEA prior to exercise its coverage guard."""
from pathlib import Path
import csv

source = Path(r"F:/OpenScience/audits/bio-proteomics-ptm-analysis/pass5/ksea/PSP&NetworKIN_Kinase_Substrate_Dataset.csv")
with source.open(newline="", encoding="utf-8") as incoming:
    reader = csv.DictReader(incoming)
    row = next(r for r in reader if "PhosphoSitePlus" in r["Source"])
    columns = reader.fieldnames
with Path("in5_one_row_prior.csv").open("w", newline="", encoding="utf-8") as outgoing:
    writer = csv.DictWriter(outgoing, fieldnames=columns)
    writer.writeheader()
    writer.writerow(row)
print("wrote valid one-row PhosphoSitePlus prior")
