"""Render the run_tobias.sh CTCF aggregate PDFs (runs A and N, cond1 and cond2) to PNG for visual inspection."""
import fitz
W = "/mnt/openscience/audit-envs/bio-atac-seq-footprinting/reaudit-final/rt"
O = "/mnt/openscience/audits/bio-atac-seq-footprinting/reaudit-final-20260930/out"
for run in ("A", "N"):
    for cond in ("cond1", "cond2"):
        doc = fitz.open(f"{W}/{run}/validation/ctcf_{cond}_aggregate.pdf")
        doc[0].get_pixmap(dpi=80).save(f"{O}/r8_{run}_ctcf_{cond}.png"); print(run, cond, doc.page_count, "pages")
