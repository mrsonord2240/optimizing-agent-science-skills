"""Final-pass regression of archived BioMart inputs against the current branch.

Usage (from this run directory):
  F:/OpenScience/audit-envs/database-access/Scripts/python.exe finalpass_rerun_archived_inputs.py

This replaces the archived fenced-block harnesses because the shared helper now
lives in the Skill's scripts/ directory. It retains their Input 1-7 scenarios,
then adds two fresh scenarios: real large-list batching and error classification.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from types import SimpleNamespace

SKILL = Path(r"F:/OpenScience/worktrees/bio-biomart-queries-finalpass/database-access/biomart-queries")
sys.path.insert(0, str(SKILL / "scripts"))

import pandas as pd
from pybiomart import Server
from biomart_query import BioMartInputError, BioMartOutageError, BioMartResponseError, query_raw


def run_live(label, operation):
    """Retry only transient server-side failures; assertions still fail fast."""
    last_error = None
    for attempt in range(1, 4):
        try:
            value = operation()
            print(f"{label}: PASS on attempt {attempt}")
            return value
        except (BioMartOutageError, OSError) as exc:
            last_error = exc
            print(f"{label}: transient {type(exc).__name__} on attempt {attempt}: {exc}")
            if attempt < 3:
                time.sleep(attempt)
    raise last_error


print("Input 1 — canonical bulk ID mapping")
# www.ensembl.org was serving its documented HTML outage page during this pass
# (recorded by finalpass_check_hosts.py). Release-110's archive is live and is
# also the Skill's documented reproducibility target, so it is a valid live
# BioMart endpoint for testing the current helper and schemas.
server = Server(host="jul2023.archive.ensembl.org")
dataset = server["ENSEMBL_MART_ENSEMBL"]["hsapiens_gene_ensembl"]
bulk = run_live("Input 1", lambda: query_raw(
    dataset,
    ["ensembl_gene_id", "external_gene_name", "hgnc_id", "refseq_mrna", "uniprotswissprot"],
    {"ensembl_gene_id": ["ENSG00000139618", "ENSG00000141510", "ENSG00000171862", "ENSG00000146648", "ENSG00000136997"]},
))
assert {"TP53", "BRCA2", "PTEN", "EGFR", "MYC"}.issubset(set(bulk["Gene name"].dropna()))
print(f"Input 1 rows={len(bulk)}")

print("Input 2 — chr17 coordinate table and gene_biotype")
coordinates = run_live("Input 2", lambda: query_raw(
    dataset,
    ["ensembl_gene_id", "external_gene_name", "chromosome_name", "start_position", "end_position", "strand", "gene_biotype"],
    {"chromosome_name": "17", "biotype": "protein_coding"},
))
assert len(coordinates) > 100
assert "Gene type" in coordinates.columns
print(f"Input 2 rows={len(coordinates)}")

print("Input 3 — discovery claims")
assert "ensembl_gene_id" not in dataset.filters
assert "gene_biotype" in dataset.attributes and "biotype" in dataset.filters
print("Input 3: PASS (pybiomart nested ID-list gap and gene_biotype schema confirmed)")

print("Input 4 — chr17 ortholog table")
orthologs = run_live("Input 4", lambda: query_raw(
    dataset,
    ["ensembl_gene_id", "external_gene_name", "mmusculus_homolog_ensembl_gene", "mmusculus_homolog_orthology_type", "drerio_homolog_ensembl_gene", "drerio_homolog_orthology_type"],
    {"chromosome_name": "17"},
))
mouse_type = next(column for column in orthologs.columns if "Mouse" in column and "type" in column)
zebrafish_type = next(column for column in orthologs.columns if "Zebrafish" in column and "type" in column)
assert ((orthologs[mouse_type] == "ortholog_one2one") & (orthologs[zebrafish_type] == "ortholog_one2one")).any()
print(f"Input 4 rows={len(orthologs)}")

print("Input 5 — GO annotation plus renamed-symbol boundary")
go = run_live("Input 5", lambda: query_raw(
    dataset,
    ["ensembl_gene_id", "external_gene_name", "go_id", "name_1006", "namespace_1003"],
    {"external_gene_name": ["TP53", "BRCA1", "MYC", "EGFR", "MARCH1"]},
))
assert len(go) > 0 and "TP53" in set(go["Gene name"].dropna())
assert "MARCH1" not in set(go["Gene name"].dropna())
print(f"Input 5 rows={len(go)}")

print("Input 6 — Ensembl Genomes scope boundary")
skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
assert "not** a drop-in `Server(host=...)` swap" in skill_text
assert "Server(host='http://plants.ensembl.org')" not in skill_text
print("Input 6: PASS (unsupported one-line Plants claim removed and caveated)")

print("Input 7 — archived offline escaping/outage/empty-list cases")
class FakeDataset:
    name = "hsapiens_gene_ensembl"
    def __init__(self, body):
        self.body = body
    def get(self, **_kwargs):
        return SimpleNamespace(text=self.body)

escaped = query_raw(FakeDataset("Gene stable ID\nENSG00000141510\n"), ["ensembl_gene_id"], {"external_gene_name": ["A&B<C>"]})
assert len(escaped) == 1
try:
    query_raw(FakeDataset("<html>Service unavailable</html>"), ["ensembl_gene_id"], {"ensembl_gene_id": ["ENSG00000141510"]})
except BioMartOutageError:
    pass
else:
    raise AssertionError("HTML outage response was not classified distinctly")
try:
    query_raw(FakeDataset("Gene stable ID\n"), ["ensembl_gene_id"], {"ensembl_gene_id": []})
except BioMartInputError:
    pass
else:
    raise AssertionError("empty list was not rejected before a request")
print("Input 7: PASS (escaping, outage classification, and local empty-list rejection)")

print("Input 8 — fresh: deterministic 1,001-ID batching")
class CountingDataset(FakeDataset):
    def __init__(self):
        super().__init__("Gene stable ID\nENSG00000141510\n")
        self.queries = []
    def get(self, **kwargs):
        self.queries.append(kwargs["query"])
        return super().get(**kwargs)

counter = CountingDataset()
batched = query_raw(counter, ["ensembl_gene_id"], {"ensembl_gene_id": [f"ENSG{i:011d}" for i in range(1001)]})
assert len(counter.queries) == 3 and len(batched) == 3
print("Input 8: PASS (1,001 IDs made 3 bounded requests)")

print("Input 9 — fresh: live 1,001-ID batching")
source_ids = coordinates["Gene stable ID"].dropna().astype(str).drop_duplicates().tolist()
if len(source_ids) < 501:
    raise AssertionError("chr17 coordinate query did not yield enough IDs for scale test")
large = run_live("Input 9", lambda: query_raw(
    dataset,
    ["ensembl_gene_id", "external_gene_name"],
    {"ensembl_gene_id": (source_ids * 2)[:1001]},
))
assert len(large) > 0 and "Gene stable ID" in large.columns
print(f"Input 9 rows={len(large)}; 1,001 supplied IDs were batched at 500")

print("ALL CURRENT-SOURCE ARCHIVED INPUTS (1-7) AND FRESH INPUTS (8-9) PASSED")
