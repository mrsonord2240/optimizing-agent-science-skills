"""Write each fenced block of a SKILL.md to rerun4/blocks/<name>.<ext> verbatim,
so the R and Python runs below source the Skill's own text rather than a copy."""
import os
import sys

sys.path.insert(0, r"F:\OpenScience\audits\bio-proteomics-peptide-identification\rerun4")
from extract import blocks  # noqa: E402

SKILL, OUT, WANT = sys.argv[1], sys.argv[2], sys.argv[3:]
os.makedirs(OUT, exist_ok=True)
names = {
    "Summarize peptides to proteins with MSstats": "msstats.R",
    "Run the real MaxLFQ (not median centering)": "maxlfq.R",
    "Median-center label-free intensities (a normalizer, not a summarizer)": "median_center.py",
    "Extract and impurity-correct reporter ions": "tmt_reporters.R",
    "Bridge multiple TMT plexes with IRS": "irs.py",
    "Check labeling efficiency and Arg->Pro first": "silac_pilot.py",
    "Ratios that keep on/off biology": "silac_ratio.py",
    "AP-MS / Affinity-Enrichment Scoring": "apms.py",
}
for h, lang, body in blocks(SKILL):
    fn = names.get(h)
    if fn is None:
        print(f"  (no filename mapped for: {h})")
        continue
    if WANT and fn not in WANT:
        continue
    p = os.path.join(OUT, fn)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    print(f"  wrote {p}  ({len(body.splitlines())} lines, lang={lang})")
