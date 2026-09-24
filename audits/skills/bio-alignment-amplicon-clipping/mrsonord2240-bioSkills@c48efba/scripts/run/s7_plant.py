"""Plant ONE residual 5' primer in a real clipped ARTIC BAM: pick the first forward read whose CIGAR starts nS mM, move its start back 3 bases
and turn 3 soft-clipped bases into aligned bases ((n)S (m)M -> (n-3)S (m+3)M at start-3), i.e. exactly what a leftover primer would look like.
cwd = out/i7 ; reads cl_s.bam, writes planted.bam. WSL env python."""
import pysam, os
V5 = os.environ["AFDATA"] + "/sarscov2/v5.3.2.primer.bed"
plus = [(int(l.split("\t")[1]), int(l.split("\t")[2])) for l in open(V5) if l.split("\t")[5] == "+"]
done = False
with pysam.AlignmentFile("cl_s.bam") as f, pysam.AlignmentFile("planted.bam", "wb", template=f) as o:
    for r in f.fetch(until_eof=True):
        c = r.cigartuples
        if not done and not r.is_reverse and c and c[0][0] == 4 and c[0][1] > 3 and c[1][0] == 0:
            r.reference_start = r.reference_start - 3
            r.cigartuples = [(4, c[0][1] - 3), (0, c[1][1] + 3)] + c[2:]
            hit = [(a, b) for a, b in plus if a <= r.reference_start < b]
            done = True; print("planted: read", r.query_name[:12], "start moved to", r.reference_start, "inside + primer(s)", hit)
        o.write(r)
