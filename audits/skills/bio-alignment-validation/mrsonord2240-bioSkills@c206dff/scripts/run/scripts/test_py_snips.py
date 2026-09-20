"""Run the Python snippets of SKILL.md / usage-guide.md verbatim (extracted to run/snip) and assert on printed values.
Also ast-parse every python block. Run in WSL from run/out/work3."""
import ast, contextlib, io, os, subprocess, sys, statistics
import numpy as np
RUN = "/mnt/openscience/audits/bio-alignment-validation/run"
SN = RUN + "/snip"
W = RUN + "/out/work3"; os.makedirs(W, exist_ok=True); os.chdir(W)
I = RUN + "/data/idx/"
for f in sorted(os.listdir(SN)):
    if f.endswith("_python.txt"):
        src = open(f"{SN}/{f}", encoding="utf-8").read()
        try:
            ast.parse(src); print(f"parse OK  {f}")
        except SyntaxError as e:
            print(f"parse FAIL {f}: {e}")

def run_insert(snip, bam):
    src = open(f"{SN}/{snip}", encoding="utf-8").read().replace("'sample.bam'", repr(bam)).replace("insert_size_dist.pdf", f"{snip}.pdf")
    buf = io.StringIO()
    ns = {}
    with contextlib.redirect_stdout(buf):
        exec(src, ns)
    return buf.getvalue(), ns

# truth by independent method: samtools stats IS table / pysam until_eof on proper-pair read1 leftmost
import pysam
def truth(bam):
    t = []
    with pysam.AlignmentFile(bam) as b:
        for r in b.fetch(until_eof=True):
            if r.is_proper_pair and not r.is_secondary and not r.is_supplementary and r.template_length > 0:
                t.append(r.template_length)
    return t

for snip in ("SKILL_07_python.txt", "usage-guide_07_python.txt"):
    for lab, bam in (("human_PE", I + "real_human_PE.bam"), ("1000g", I + "real_1000g_chr20.bam"), ("RNA", I + "real_human_RNA.bam")):
        out, ns = run_insert(snip, bam)
        t = truth(bam)
        med = float(out.split("Median")[1].split(":")[1].split()[0]) if "Median" in out else None
        print(f"{snip:26s} {lab:9s} printed: {' | '.join(l for l in out.strip().splitlines()[:3])}   truth median={np.median(t):.0f} mean={np.mean(t):.0f} n={len(t)}  ->", "PASS" if med is not None and abs(med - np.median(t)) < 1 else "FAIL")
print("pdf written:", [f for f in os.listdir(W) if f.endswith('.pdf')])
# max_reads=100000 head-of-file default vs a file with >100k reads: not testable with the small corpus (largest BAM 15788 records) -> recorded as not executed
