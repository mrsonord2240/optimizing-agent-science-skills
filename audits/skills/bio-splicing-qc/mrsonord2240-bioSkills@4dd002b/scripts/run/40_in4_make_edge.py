"""NEW input data (auditor-made, SYNTHETIC): a BAM of hand-specified CIGARs / flags with a hand-written truth table
for junction_stats(). Not from the Skill's test. Usage: python 40_in4_make_edge.py <out dir>"""
import sys, json, pysam
out = sys.argv[1]
hdr = pysam.AlignmentHeader.from_dict({'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': 'chrT', 'LN': 100000}, {'SN': 'chrU', 'LN': 100000}]})
recs = []
def mk(name, ref, pos, cigar, flag=0, mapq=255, nh=1, mate=None, tag_nh=True):
    r = pysam.AlignedSegment(hdr); r.query_name = name; r.reference_id = ref; r.reference_start = pos; r.flag = flag; r.mapping_quality = mapq
    r.cigarstring = cigar
    q = sum(int(n) for n, op in __import__('re').findall(r'(\d+)([MIS=X])', cigar))
    r.query_sequence = 'A' * q; r.query_qualities = pysam.qualitystring_to_array('I' * q)
    if tag_nh: r.set_tag('NH', nh)
    if mate is not None: r.next_reference_id = ref; r.next_reference_start = mate
    recs.append(r)
def many(prefix, n, *a, **k):
    for i in range(n): mk(f'{prefix}{i}', *a, **k)
# truth: key (contig, intron_start0, intron_end) -> (reads with min_overhang 8, reads_all, min_overhang seen)
truth = {}
many('del', 4, 0, 1000, '10M2D20M500N30M');          truth[('chrT', 1032, 1532)] = (4, 4, 30)     # D consumes reference: start = 1000+10+2+20
many('sc', 5, 0, 2000, '5S45M300N50M');              truth[('chrT', 2045, 2345)] = (5, 5, 45)     # soft clip is not overhang
many('ins', 3, 0, 3000, '20M1I30M400N50M');          truth[('chrT', 3050, 3450)] = (3, 3, 50)     # I does not consume reference
many('hc', 2, 0, 4000, '50M300N30M5H');              truth[('chrT', 4050, 4350)] = (2, 2, 30)
many('two', 6, 0, 5000, '30M500N30M400N40M');        truth[('chrT', 5030, 5530)] = (6, 6, 30); truth[('chrT', 5560, 5960)] = (6, 6, 30)
many('noNH', 4, 0, 7000, '50M600N50M', mapq=255, tag_nh=False)          # unique by MAPQ, no NH tag
many('noNHlow', 4, 0, 7000, '50M600N50M', mapq=3, tag_nh=False)         # multi-mapper by MAPQ: skipped
truth[('chrT', 7050, 7650)] = (4, 4, 50)
many('nh1mq0', 2, 0, 7000, '50M600N50M', mapq=0, nh=1)                  # NH=1 wins over MAPQ 0 (STAR-style): counted
truth[('chrT', 7050, 7650)] = (6, 6, 50)
many('nh2', 5, 0, 7000, '50M600N50M', nh=2)                               # skipped
many('rev', 3, 0, 7000, '50M600N50M', flag=16)                            # reverse strand: counted (junction key has no strand)
truth[('chrT', 7050, 7650)] = (9, 9, 50)
many('sec', 4, 0, 7000, '50M600N50M', flag=256); many('sup', 4, 0, 7000, '50M600N50M', flag=2048)   # skipped
# pairs
for i in range(5):     # both mates cross the same junction: one fragment, overhangs 50 and 20
    mk(f'pA{i}', 0, 8000, '50M800N50M', flag=1|2|64|32, mate=8030); mk(f'pA{i}', 0, 8030, '20M800N80M', flag=1|2|128|16, mate=8000)
truth[('chrT', 8050, 8850)] = (5, 5, 20)
for i in range(4):     # only mate 1 spans the junction, mate 2 unspliced
    mk(f'pB{i}', 0, 9000, '50M700N50M', flag=1|2|64|32, mate=9800); mk(f'pB{i}', 0, 9800, '100M', flag=1|2|128|16, mate=9000)
truth[('chrT', 9050, 9750)] = (4, 4, 50)
for i in range(3):     # mates cross two different junctions: one fragment on each
    mk(f'pC{i}', 0, 10000, '50M700N50M', flag=1|2|64|32, mate=11000); mk(f'pC{i}', 0, 11000, '50M700N50M', flag=1|2|128|16, mate=10000)
truth[('chrT', 10050, 10750)] = (3, 3, 50); truth[('chrT', 11050, 11750)] = (3, 3, 50)
many('tiny', 7, 0, 12000, '3M500N97M')                                    # overhang 3: counted only with min_overhang <= 3
truth[('chrT', 12003, 12503)] = (0, 7, 3)
many('u', 5, 1, 1000, '50M300N50M')                                       # other contig, same coordinates as no other read
truth[('chrU', 1050, 1350)] = (5, 5, 50)
recs.sort(key=lambda r: (r.reference_id, r.reference_start))
with pysam.AlignmentFile(f'{out}/edge.bam', 'wb', header=hdr) as o:
    for r in recs: o.write(r)
pysam.index(f'{out}/edge.bam')
json.dump({f'{k[0]}:{k[1]}-{k[2]}': list(v) for k, v in truth.items()}, open(f'{out}/edge_truth.json', 'w'), indent=1)
print('records', len(recs), 'truth junctions', len(truth))
