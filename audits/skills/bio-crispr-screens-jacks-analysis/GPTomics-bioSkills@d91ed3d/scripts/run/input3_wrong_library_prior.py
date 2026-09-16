"""
Input 3 (Edge) -- SKILL.md's own "Reference Efficacy Prior from Wrong Library" failure
mode: build an efficacy prior from JACKS' Project Score run (Input 1) and pass it via
--reffile to the unrelated HAP1 TKOv3 screen (Input 2). SKILL.md's Failure Modes table
predicts a *soft* failure ("worse gene-effect estimation than no prior"). This checks what
actually happens against the real installed JACKS 0.2.
"""
import pandas as pd
from jacks.jacks_io import runJACKS

D = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\data"
OUT1 = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out1\whp_false_as_skillmd_recommends"
OUT3 = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out3\hap1_wrong_prior"

# Build the reference prior exactly as SKILL.md's own extract_efficacy_prior() function does
df = pd.read_csv(f"{OUT1}_grna_JACKS_results.txt", sep='\t')
prior = df[['sgrna', 'X1', 'X2']]
prior.to_csv(r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out3\projectscore_efficacy_prior.tsv", sep='\t', index=False)
print("Prior built from Project Score run:", len(prior), "sgRNAs")

try:
    runJACKS(
        countfile=f"{D}/hap1_counts.txt",
        replicatefile=f"{D}/hap1_repmap.txt",
        guidemappingfile=f"{D}/hap1_guidemap.txt",
        rep_hdr='Replicate', sample_hdr='Sample', common_ctrl_sample='T0',
        sgrna_hdr='sgRNA', gene_hdr='Gene',
        outprefix=OUT3,
        reffile=r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out3\projectscore_efficacy_prior.tsv",
    )
    print("Run completed (unexpected -- SKILL.md implies this degrades silently, not that it completes)")
except Exception as e:
    print("RAISED:", type(e).__name__, "--", str(e)[:300])
