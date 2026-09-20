# mapDamage --rescale check: quality of damage-consistent T (ref C) at read position 1 must drop after rescaling; matching bases mid-read must not.
import pysam
ref = pysam.FastaFile("ref.fa"); g = ref.fetch(ref.references[0]).upper()
def q_at_damage(path):
    qs = []
    for r in pysam.AlignmentFile(path):
        if r.query_sequence[0] == "T" and g[r.reference_start] == "C": qs.append(r.query_qualities[0])
    return len(qs), (sum(qs) / len(qs) if qs else float("nan"))
def q_mid(path):
    qs = [r.query_qualities[30] for r in pysam.AlignmentFile(path) if r.query_sequence[30] == g[r.reference_start + 30]]
    return sum(qs) / len(qs)
def q_5prime_match(path):
    qs = [r.query_qualities[0] for r in pysam.AlignmentFile(path) if r.query_sequence[0] == g[r.reference_start] == "C"]
    return len(qs), sum(qs) / len(qs)
for lab, p in [("input", "marked.bam"), ("rescaled", "mapdamage_out/marked.rescaled.bam")]:
    n, q = q_at_damage(p); n2, q2 = q_5prime_match(p)
    print(f"  {lab:9s}: C->T at 5' pos1: n={n}, mean Q {q:.1f}; unchanged C at pos1: n={n2}, mean Q {q2:.1f}; mid-read matching base mean Q {q_mid(p):.1f}")
