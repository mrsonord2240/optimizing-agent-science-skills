"""Input 6: NMD 50-55 nt / last-exon check for the two stop_gained calls on the SYNTHETIC gene SYNG1
(exon CDS spans from data/genes.gff3). Uses the rule stated in SKILL.md (Abou Tayoun 2018)."""
cds_exons = [(1011, 1100), (1201, 1300), (1401, 1480)]   # CDS pieces, + strand
def cds_pos(g):
    off = 0
    for s, e in cds_exons:
        if s <= g <= e:
            return off + (g - s) + 1
        off += e - s + 1
    return None
last_junction = sum(e - s + 1 for s, e in cds_exons[:-1])      # CDS position of the last exon-exon junction
for g, label in [(1231, 'chr1:1231 C>T stop_gained (p.Q41*)'), (1466, 'chr1:1466 C>T stop_gained, last exon')]:
    c = cds_pos(g)
    exon = next(i for i, (s, e) in enumerate(cds_exons, 1) if s <= g <= e)
    dist = last_junction - c
    verdict = 'predicted NMD (PTC >50-55 nt upstream of last junction)' if dist > 55 else 'predicted to ESCAPE NMD'
    print(f'{label}: CDS c.{c}, exon {exon}/{len(cds_exons)}, {dist} nt upstream of last junction -> {verdict}')
