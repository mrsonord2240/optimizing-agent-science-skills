"""INPUT 4 (Variant B, regression + real data). MAF coordinates.
 (a) SYNTHETIC 200-nt genome + hand-built MAF (seeded): SKILL's fixed helper + ground-truth loop run VERBATIM; negative control = old `== '-'` test.
 (b) REAL UCSC MAF (Biopython Tests/MAF/ucsc_mm9_chr10.maf, 48 blocks, 190 minus-strand rows) with ground truth = genomic sequence fetched from the
     public UCSC REST API (api.genome.ucsc.edu/getData/sequence): for every checked row, revcomp(genome[start:start+size]) must equal the ungapped row."""
import random, io, os, json, time, urllib.request
from Bio import AlignIO, Align
from Bio.Seq import Seq
from common import *
os.chdir(DATA)
random.seed(7)
chr1 = ''.join(random.choice('ACGT') for _ in range(200)); chr2 = ''.join(random.choice('ACGT') for _ in range(150))     # SYNTHETIC
ref1 = chr1[20:40]; qry1 = chr2[10:31]; r1 = ref1[:8] + '-' + ref1[8:]
plus_start, size = 60, 24
qry2 = str(Seq(chr2[plus_start:plus_start+size]).reverse_complement()); maf_start = 150 - plus_start - size
ref2 = chr1[100:124]
lines = ['##maf version=1 scoring=synthetic', '', 'a score=100', f's hg.chr1 20 {len(ref1)} + 200 {r1}', f's mm.chr2 10 {len(qry1)} + 150 {qry1}', '',
         'a score=90', f's hg.chr1 100 {len(ref2)} + 200 {ref2}', f's mm.chr2 {maf_start} {size} - 150 {qry2}', '']
open('synthetic.maf', 'w').write('\n'.join(lines))
contigs = {'chr1': chr1, 'chr2': chr2}

print('=== (a) synthetic: SKILL block verbatim')
code = block('MAF Block Coordinate').replace("'blocks.maf'", "'synthetic.maf'")
ns = {'AlignIO': AlignIO, 'Seq': Seq, 'contigs': contigs}
exec(code, ns); ok(True, 'SKILL helper + ground-truth loop ran on every row of synthetic MAF with no AssertionError')
blocks = list(AlignIO.parse('synthetic.maf', 'maf')); minus = blocks[1][1]
res = ns['maf_to_plus_strand_coords'](minus.annotations)
ok(res == plus_start, f'fixed helper on minus row -> {res}; ground truth {plus_start}; strand annotation {minus.annotations["strand"]!r}')
ok(all(isinstance(r.annotations['strand'], int) for b in blocks for r in b), 'strand annotation is int (SKILL now says so)')
old = lambda a: a['srcSize'] - a['start'] - a['size'] if a['strand'] == '-' else a['start']
ok(old(minus.annotations) != plus_start, f'negative control: old `== "-"` helper returns {old(minus.annotations)} (wrong) -> the ground-truth loop would fire')
code_old = code.replace("== -1:\n        return", "== '-':\n        return", 1)
try: exec(code_old, {'AlignIO': AlignIO, 'Seq': Seq, 'contigs': contigs}); ok(False, 'ground-truth loop did NOT catch the old helper')
except AssertionError: ok(True, 'ground-truth loop raises AssertionError with the old (buggy) helper: the verification step is effective')
# Bio.Align MAF
al = list(Align.parse('synthetic.maf', 'maf')); ok(len(al) == 2, 'Align.parse maf -> 2 blocks'); 
buf = io.StringIO(); Align.write(al, buf, 'maf'); ok('s hg.chr1' in buf.getvalue() and 's mm.chr2' in buf.getvalue(), 'Align.write maf writes s-lines (table says R/W)')

print('=== (b) REAL UCSC MAF with UCSC-API ground truth')
blocks = list(AlignIO.parse('ucsc_mm9_chr10.maf', 'maf')); print('blocks', len(blocks))
rows = [(bi, r) for bi, b in enumerate(blocks) for r in b]
nminus = sum(1 for _, r in rows if r.annotations['strand'] == -1); print('rows', len(rows), 'minus-strand rows', nminus)
ok(all({'start','size','strand','srcSize'} <= set(r.annotations) for _, r in rows), 'every real row carries start,size,strand,srcSize')
ok(set(r.annotations['strand'] for _, r in rows) == {1, -1}, 'real strand values are ints {1,-1}')
cache_f = DATA/'ucsc_seq_cache.json'; cache = json.load(open(cache_f)) if cache_f.exists() else {}
def fetch(genome, chrom, s, e):
    k = f'{genome}|{chrom}|{s}|{e}'
    if k in cache: return cache[k]
    u = f'https://api.genome.ucsc.edu/getData/sequence?genome={genome};chrom={chrom};start={s};end={e}'
    try: d = json.load(urllib.request.urlopen(u, timeout=60))['dna']
    except Exception as ex: d = None
    cache[k] = d; time.sleep(0.4); return d
helper = ns['maf_to_plus_strand_coords']
checked = {'plus': [0, 0], 'minus': [0, 0], 'old_minus': [0, 0]}
# every genome except very old assemblies unavailable in the API is skipped and counted
skipped = 0; done_minus = 0
for bi, r in rows:
    a = r.annotations; genome, chrom = r.id.split('.', 1)
    strand_key = 'minus' if a['strand'] == -1 else 'plus'
    if strand_key == 'plus' and checked['plus'][0] >= 12: continue
    if strand_key == 'minus' and done_minus >= 40: continue
    st = helper(a); seq = fetch(genome, chrom, st, st + a['size'])
    if seq is None: skipped += 1; continue
    frag = Seq(seq.upper()); frag = frag.reverse_complement() if a['strand'] == -1 else frag
    good = str(frag) == str(r.seq).replace('-', '').upper()
    checked[strand_key][0] += 1; checked[strand_key][1] += good
    if strand_key == 'minus':
        done_minus += 1
        so = old(a); s2 = fetch(genome, chrom, so, so + a['size']); 
        if s2 is not None:
            f2 = Seq(s2.upper()).reverse_complement(); checked['old_minus'][0] += 1; checked['old_minus'][1] += str(f2) == str(r.seq).replace('-', '').upper()
json.dump(cache, open(cache_f, 'w'))
print('checked (n, matches):', checked, '| rows skipped (assembly not in API):', skipped)
ok(checked['minus'][0] >= 20 and checked['minus'][1] == checked['minus'][0], f"fixed helper: {checked['minus'][1]}/{checked['minus'][0]} REAL minus-strand rows equal revcomp(genome[start:start+size])")
ok(checked['plus'][0] >= 5 and checked['plus'][1] == checked['plus'][0], f"plus-strand rows: {checked['plus'][1]}/{checked['plus'][0]} equal genome[start:start+size]")
ok(checked['old_minus'][0] >= 20 and checked['old_minus'][1] == 0, f"negative control (old helper, unconverted start): {checked['old_minus'][1]}/{checked['old_minus'][0]} match -> the old bug misplaced every minus row")
a = Align.parse('ucsc_mm9_chr10.maf', 'maf'); n = sum(1 for _ in a); ok(n == 48, f'Align.parse real MAF -> {n} alignments (48 blocks)')
summary()
