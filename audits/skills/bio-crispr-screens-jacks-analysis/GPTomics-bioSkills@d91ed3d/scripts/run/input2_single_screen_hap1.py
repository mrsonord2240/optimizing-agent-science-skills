"""
Input 2 (Variant A / essential-gene benchmark) -- single-screen JACKS run on the real
HAP1 TKOv3 data, exactly the scenario SKILL.md itself labels "not the right tool" for
JACKS (single screen, no prior efficacy -- "MAGeCK or BAGEL2 work as well"). Runs it
anyway to (a) confirm JACKS still produces a sane, checkable result even off its
advantaged use case, and (b) benchmark essential-gene recovery against CEGv2/NEGv1 per
the audit brief, comparable to the MAGeCK/BAGEL2/drugZ concordance already recorded in
public-data/README.md for the same underlying screen.
"""
import time
from jacks.jacks_io import runJACKS

D = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\data"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out2\hap1_single"

t0 = time.time()
runJACKS(
    countfile=f"{D}/hap1_counts.txt",
    replicatefile=f"{D}/hap1_repmap.txt",
    guidemappingfile=f"{D}/hap1_guidemap.txt",
    rep_hdr='Replicate',
    sample_hdr='Sample',
    common_ctrl_sample='T0',
    sgrna_hdr='sgRNA',
    gene_hdr='Gene',
    outprefix=OUT,
    apply_w_hp=False,
)
print(f"done in {time.time()-t0:.1f}s")
