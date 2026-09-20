# Helper for input 3: emulate "a re-sort that loses aux tags via Python round-trip" (SKILL.md Critical pitfall).
# usage: strip_tags.py in.bam out.bam TAG[,TAG...]
import sys, pysam
src, dst, tags = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
with pysam.AlignmentFile(src, "rb") as i, pysam.AlignmentFile(dst, "wb", header=i.header) as o:
    n = 0
    for r in i:
        for t in tags:
            if r.has_tag(t):
                r.set_tag(t, None)
        o.write(r); n += 1
print(f"stripped {tags} from {n} records -> {dst}")
