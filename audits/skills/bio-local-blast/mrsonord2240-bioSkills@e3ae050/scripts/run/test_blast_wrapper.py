"""Exercise the bundled examples/blast_wrapper.py (copied, never imported from the fix worktree
or external/ clone) against real BLAST+ output. Re-run of the pre-fix regression check."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "skill_examples"))
os.environ["PATH"] = (
    r"F:\OpenScience\audit-envs\database-access\tools\blast\ncbi-blast-2.17.0+\bin"
    + os.pathsep
    + os.environ["PATH"]
)

import blast_wrapper as bw

work = os.path.join(os.path.dirname(__file__), "work", "wrapper_test")
os.makedirs(work, exist_ok=True)
os.chdir(work)

import shutil

shutil.copy(r"F:\OpenScience\audits\bio-local-blast\data\ref_proteins.fasta", ".")
shutil.copy(r"F:\OpenScience\audits\bio-local-blast\data\query_proteins.fasta", ".")

print("=== make_blast_db ===")
bw.make_blast_db("ref_proteins.fasta", "ref_db", dbtype="prot")
print("DB files:", [f for f in os.listdir(".") if f.startswith("ref_db")])

print("=== run_blast (blastp) ===")
bw.run_blast("query_proteins.fasta", "ref_db", "results.tsv", program="blastp")
print("results.tsv size:", os.path.getsize("results.tsv"))

print("=== parse_tabular ===")
rows = bw.parse_tabular("results.tsv")
print(f"{len(rows)} HSPs, {len(set(r['qseqid'] for r in rows))} unique queries")

print("=== top_by_bitscore_per_query ===")
top = bw.top_by_bitscore_per_query(rows, n=1)
for q, recs in top.items():
    print(q, "->", recs[0]["sseqid"], recs[0]["bitscore"])

print("=== require() on a fake tool ===")
try:
    bw.require("definitely_not_a_real_tool_xyz")
    print("FAIL: did not raise")
except RuntimeError as e:
    print("OK, raised RuntimeError:", e)

print("\nALL WRAPPER CHECKS COMPLETED")
