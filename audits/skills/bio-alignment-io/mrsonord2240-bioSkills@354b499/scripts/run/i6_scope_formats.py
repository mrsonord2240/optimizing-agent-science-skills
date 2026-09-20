"""Input 6 (Scope boundary): SKILL 'Formats NOT in BioPython' table + coverage map vs Biopython 1.88 Bio.Align. Small SYNTHETIC PSL/chain/A2M/MSF files, parsed for real."""
import pathlib, io
import Bio; from Bio import Align
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m)
here = pathlib.Path(__file__).parent; d = here/'data'
print('Biopython', Bio.__version__, '| Bio.Align.formats =', Align.formats)
# SYNTHETIC PSL: one ungapped 30-base match on + strand (columns: matches mismatches repMatches nCount qNumInsert qBaseInsert tNumInsert tBaseInsert strand qName qSize qStart qEnd tName tSize tStart tEnd blockCount blockSizes qStarts tStarts)
psl = '30\t0\t0\t0\t0\t0\t0\t0\t+\tq1\t50\t5\t35\tchr1\t200\t100\t130\t1\t30,\t5,\t100,\n'
(d/'synthetic.psl').write_text(psl, encoding='utf-8')
try:
    a = list(Align.parse(d/'synthetic.psl', 'psl')); ok(len(a) == 1 and a[0].coordinates.tolist() == [[100, 130], [5, 35]], f'Bio.Align.parse(psl) works: coordinates {a[0].coordinates.tolist()} -> SKILL says PSL is NOT in BioPython')
except Exception as e: ok(False, f'psl parse: {type(e).__name__}: {e}')
# SYNTHETIC UCSC chain
chain = 'chain 1000 chr1 200 + 100 130 q1 50 + 5 35 1\n30\n\n'
(d/'synthetic.chain').write_text(chain, encoding='utf-8')
try:
    a = list(Align.parse(d/'synthetic.chain', 'chain')); ok(len(a) == 1, f'Bio.Align.parse(chain) works: {a[0].coordinates.tolist()} -> SKILL says chain/net NOT in BioPython')
except Exception as e: ok(False, f'chain parse: {type(e).__name__}: {e}')
# A2M: read via Bio.Align (SKILL coverage table says "--")
a2m = d/'globins_hmm.a2m'
try:
    a = Align.read(a2m, 'a2m'); print('Align.read a2m ->', len(a), a.shape)
except Exception as e: print('Align.read(hmmalign a2m) ->', type(e).__name__, str(e)[:100])
padded = '>s1\nACD..EF\n>s2\nA-Dgg-F\n'      # SYNTHETIC padded A2M (dots pad inserts) 
try:
    a = Align.read(io.StringIO(padded), 'a2m'); ok(True, f'Align.read a2m on a padded A2M: shape {a.shape}')
except Exception as e: print('Align.read(padded a2m) ->', type(e).__name__, str(e)[:100])
# MSF in Bio.Align (coverage map says "--")
msf_txt = open(d.parent/'skill'/'examples'/'sample_alignment.aln').read()
try:
    from Bio import AlignIO
    ali = AlignIO.read(d/'pf.clustal', 'clustal'); AlignIO.write(ali[:3], d/'x.msf', 'clustal')
except Exception as e: pass
print('Align modules list has msf:', 'msf' in Align.formats, '| a2m:', 'a2m' in Align.formats, '| psl:', 'psl' in Align.formats, '| chain:', 'chain' in Align.formats)
print('--- GFA / HAL / AXT / GAF (SKILL says out of scope): no reader in Biopython?')
for f in ['gfa', 'hal', 'axt', 'gaf', 'rgfa']: print(f, 'in Bio.Align.formats:', f in Align.formats)
