"""
Exercise the Skill's own examples/blast_wrapper.py (copied into run/skill_examples, never imported
from F:\\OpenScience\\external\\...) against our synthetic data, using the real functions
(make_blast_db, run_blast, parse_tabular, top_by_bitscore_per_query, filter_hits) rather than its
__main__ block (which references placeholder filenames that don't exist).
"""
import os
import sys
import shutil

BIN_DIR = r"F:\OpenScience\audit-envs\database-access\tools\blast\ncbi-blast-2.17.0+\bin"
DATA = r"F:\OpenScience\audits\bio-local-blast\data"
WORK = r"F:\OpenScience\audits\bio-local-blast\run\work\wrapper_test"
os.makedirs(WORK, exist_ok=True)
os.chdir(WORK)

# Put the BLAST+ bin dir on PATH so shutil.which() in the wrapper finds the tools
# (the wrapper's require()/require_tool() checks shutil.which, and the wrapper calls
# the bare program name via subprocess, so PATH must contain the .exe dir).
os.environ["PATH"] = BIN_DIR + os.pathsep + os.environ["PATH"]

sys.path.insert(0, r"F:\OpenScience\audits\bio-local-blast\run\skill_examples")
import blast_wrapper as bw  # noqa: E402

print("--- shutil.which sanity ---")
print("makeblastdb:", shutil.which("makeblastdb"))
print("blastp:", shutil.which("blastp"))

print("\n--- make_blast_db (protein, v5, parse_seqids) ---")
bw.make_blast_db(os.path.join(DATA, "ref_proteins.fasta"), "ref_db", dbtype="prot")
print("DB built: ref_db.*", [f for f in os.listdir(WORK) if f.startswith("ref_db")])

print("\n--- run_blast (blastp, dc-megablast N/A for protein so task=None) ---")
bw.run_blast(os.path.join(DATA, "query_proteins.fasta"), "ref_db", "results.tsv",
             program="blastp", evalue=1e-10, threads=8)
print("results.tsv exists:", os.path.exists("results.tsv"), "size:", os.path.getsize("results.tsv"))

print("\n--- parse_tabular ---")
rows = bw.parse_tabular("results.tsv")
print(f"Total HSPs: {len(rows)}")
print(f"Unique queries with any hit: {len(set(r['qseqid'] for r in rows))}")
for r in rows:
    print(" ", r["qseqid"], "->", r["sseqid"], "pident=", r["pident"], "qcovs=", r["qcovs"],
          "evalue=", r["evalue"], "bitscore=", r["bitscore"])

print("\n--- filter_hits (min_pident=70, min_qcovs=80, max_evalue=1e-5) ---")
good = bw.filter_hits(rows, min_pident=70.0, min_qcovs=80.0, max_evalue=1e-5)
print(f"After identity>=70 + qcovs>=80 + E<=1e-5: {len(good)}")
for r in good:
    print(" ", r["qseqid"], "->", r["sseqid"])

print("\n--- top_by_bitscore_per_query ---")
top = bw.top_by_bitscore_per_query(rows, n=1)
for q, t in top.items():
    h = t[0]
    print(f"  {q} -> {h['sseqid']}  bits={h['bitscore']:.1f}  qcovs={h['qcovs']:.0f}%  E={h['evalue']:.1e}")

print("\n--- require() on a nonexistent tool (error path) ---")
try:
    bw.require("definitely_not_a_real_tool_xyz")
    print("UNEXPECTED: no exception raised")
except RuntimeError as e:
    print("Correctly raised RuntimeError:", e)
