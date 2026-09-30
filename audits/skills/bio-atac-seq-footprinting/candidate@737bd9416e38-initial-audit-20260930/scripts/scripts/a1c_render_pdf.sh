#!/bin/bash
# Render the Skill script's own CTCF aggregate PDF (A1 and A3) to PNG for visual inspection.
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
python - <<'PY'
import fitz, os
W=os.environ["W"]; A=os.environ["A"]
for tag,p in (("a1",f"{W}/a1/out/validation/ctcf_aggregate.pdf"),("a3_nfr",f"{W}/a3/out/validation/ctcf_aggregate.pdf")):
    d=fitz.open(p); print(tag, "pages", len(d)); d[0].get_pixmap(dpi=110).save(f"{A}/out/{tag}_ctcf_aggregate_page1.png")
PY
