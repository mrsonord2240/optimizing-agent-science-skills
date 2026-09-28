import hashlib
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
OUTPUT = RUN / "artifact-hashes.tsv"

rows = ["path\tbytes\tsha256"]
for path in sorted((p for p in RUN.rglob("*") if p.is_file() and p != OUTPUT), key=lambda p: p.relative_to(RUN).as_posix()):
    rel = path.relative_to(RUN).as_posix()
    rows.append(f"{rel}\t{path.stat().st_size}\t{hashlib.sha256(path.read_bytes()).hexdigest()}")
OUTPUT.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(f"hashed={len(rows) - 1}")
