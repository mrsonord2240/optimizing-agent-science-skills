from multiprocessing import Pool
from pathlib import Path
from Bio import SeqIO


def process_file(filepath):
    total = 0
    bp = 0
    for record in SeqIO.parse(filepath, "fasta"):
        total += 1
        bp += len(record.seq)
    return {"file": filepath.name, "count": total, "total_bp": bp}


files = list(Path("data").glob("*.fasta"))
with Pool(4) as pool:
    results = pool.map(process_file, files)

print(results)
