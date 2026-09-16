"""
Input 1 (Canonical) -- exercises SKILL.md's "Run JACKS Joint Analysis" section verbatim:
programmatic `from jacks.jacks_io import runJACKS` call, matched per-sample controls,
apply_w_hp=True exactly as SKILL.md's own worked example sets it (SKILL.md's own inline
comment on that same line says "not recommended"). Run on JACKS' real bundled 16-cell-line
Project Score dataset (jacks/example/), not synthetic data.

Also runs a second pass with apply_w_hp=False (the Skill's own stated recommendation,
repeated in usage-guide.md's Tips and in the CLI comment) to check whether the
contradiction in SKILL.md's own example materially changes results.
"""
import time, os
from jacks.jacks_io import runJACKS

JD = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks\example"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out1"
os.makedirs(OUT, exist_ok=True)

counts = os.path.join(JD, "example_count_data.tab")
repmap = os.path.join(JD, "example_repmap_matched_ctrls.tab")
guidemap = counts  # same file has sgRNA + gene columns; SKILL.md's own countfile/guidemap can be the same file

for apply_w_hp, tag in [(True, "whp_true_as_skillmd_literal"), (False, "whp_false_as_skillmd_recommends")]:
    outprefix = os.path.join(OUT, tag)
    t0 = time.time()
    runJACKS(
        countfile=counts,
        replicatefile=repmap,
        guidemappingfile=guidemap,
        rep_hdr='Replicate',
        sample_hdr='Sample',
        ctrl_sample_hdr='Control',
        sgrna_hdr='sgRNA',
        gene_hdr='gene',
        outprefix=outprefix,
        apply_w_hp=apply_w_hp,
    )
    print(f"[{tag}] done in {time.time()-t0:.1f}s")
