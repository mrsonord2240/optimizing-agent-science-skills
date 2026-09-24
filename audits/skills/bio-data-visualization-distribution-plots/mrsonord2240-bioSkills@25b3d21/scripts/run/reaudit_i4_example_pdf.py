# Exact-commit re-audit input 4: standalone source example and PDF font inspection.
# Run with: py.sh reaudit_i4_example_pdf.py <directory-containing-raincloud.pdf>
import pathlib
import sys

directory = pathlib.Path(sys.argv[1]).resolve()
pdf = directory / "raincloud.pdf"
assert pdf.is_file(), pdf
data = pdf.read_bytes()
assert len(data) > 2000, len(data)
assert b"/Type3" not in data
assert b"/FontFile" in data or b"/CIDFontType2" in data
print(f"PASS i4: standalone raincloud.pdf={len(data)} bytes; embedded-font marker present; Type3 absent")
