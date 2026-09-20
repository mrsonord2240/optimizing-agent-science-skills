"""Input 11 probe (informational): (a) secondary alignments with SEQ '*' + `--ff 0` (the option the Skill's own table recommends to keep every mapped read),
(b) shipped-means-present: do the Skill's Related Skills paths exist in the fork worktree?"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from snippets import load_functions
import pysam
f = load_functions("SKILL.md")
ref = ">sq1\n" + "ACGTTGCAAC" * 10 + "\n"
open(f"{DATA}/ss.fa", "w").write(ref)
seq = "ACGTTGCAAC" * 3
rows = [["p1", 0, "sq1", 1, 60, "30M", "*", 0, 0, seq, "I" * 30], ["p2", 0, "sq1", 1, 60, "30M", "*", 0, 0, seq, "I" * 30],
        ["sec", 256, "sq1", 1, 0, "30M", "*", 0, 0, "*", "*"]]
with open(f"{DATA}/ss.sam", "w", newline="\n") as fh:
    fh.write("@HD\tVN:1.6\tSO:coordinate\n@SQ\tSN:sq1\tLN:100\n")
    for r in rows:
        fh.write("\t".join(map(str, r)) + "\n")
sh(f"cd {DATA} && samtools faidx ss.fa && samtools view -b -o ss.bam ss.sam && rm ss.sam && samtools index ss.bam", check=True)
rc, out, err = sh(f"samtools mpileup -B --ff 0 -f {DATA}/ss.fa -r sq1:5-5 {DATA}/ss.bam")
print("samtools --ff 0 with a SEQ='*' secondary alignment: rc", rc, "row:", out.strip(), "| stderr", err.strip()[:100])
for name, call in [("allele_counts(flag_filter=0)", lambda: f["allele_counts"](f"{DATA}/ss.bam", "sq1", 4, flag_filter=0)),
                   ("pileup_text(flag_filter=0)", lambda: list(f["pileup_text"](f"{DATA}/ss.bam", f"{DATA}/ss.fa", "sq1", 4, 5, flag_filter=0)))]:
    try:
        print(name, "->", call())
    except Exception as e:
        print(name, "-> raised", type(e).__name__, e)
# Related Skills paths
import re
txt = open(SKILL + "/SKILL.md", encoding="utf-8").read().split("## Related Skills")[1]
W = "/mnt/openscience/wt/af-pileup"
for m in re.finditer(r"^- ([\w./-]+) - ", txt, flags=re.M):
    slug = m.group(1)
    cand = [W + "/alignment-files/" + slug, W + "/" + slug]
    print(f"Related skill {slug}: exists =", any(os.path.isdir(c) for c in cand))
