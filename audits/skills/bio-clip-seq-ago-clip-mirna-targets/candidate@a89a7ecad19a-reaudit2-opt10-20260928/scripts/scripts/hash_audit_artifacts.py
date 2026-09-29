#!/usr/bin/env python3
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
destination = root / "evidence" / "audit-artifacts.sha256"
files = sorted((p for p in root.rglob("*") if p.is_file() and p != destination), key=lambda p: p.relative_to(root).as_posix())
lines = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root).as_posix()}" for p in files]
destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"hashed {len(files)} files; inventory={destination}")
