"""INPUT 7 prep part 2: foreign-file variants for the round-2 claim rows (single punctuation character per file, hand-written like a foreign file because Biopython's
relaxed writer would rewrite them), '*'-equivalence variants, and Biopython's own NEXUS quoting per punctuation character. Real Pfam PF00042 rows; injected characters are SYNTHETIC."""
import os, io
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from common import *
d = DATA/'tools'; os.chdir(d)
lines = open('pf12_relaxed.phy').read().splitlines(); hdr, rows = lines[0], lines[1:]
print('header', hdr, '| first row name', rows[0].split(' ')[0])
def variant(tag, newname):
    r = list(rows); nm, rest = r[0].split(' ', 1); r[0] = f'{newname} {rest}'
    open(f'pf12_name_{tag}.phy', 'w').write(hdr + '\n' + '\n'.join(r) + '\n')
for tag, nm in [('colon', 'GLB:1'), ('comma', 'GLB,1'), ('paren', 'GLB(1)'), ('bracket', 'GLB[1]'), ('pipe', 'GLB|1')]: variant(tag, nm)
print('wrote pf12_name_{colon,comma,paren,bracket,pipe}.phy')
# '*' variants: does RAxML-NG treat protein '*' as undetermined (same likelihood as '-' or 'X' at that position)?
star = AlignIO.read('pf12_star.phy', 'phylip-relaxed'); s = str(star[0].seq); i = s.index('*')
for tag, ch in [('dash', '-'), ('X', 'X')]:
    a = AlignIO.read('pf12_star.phy', 'phylip-relaxed'); a[0].seq = Seq(s[:i] + ch + s[i+1:]); AlignIO.write(a, f'pf12_star_{tag}.phy', 'phylip-relaxed')
print("'*' at column", i, '; row 0 residue before/after:', s[i-2:i+3])
# nucleotide alignment with '*' (SYNTHETIC, 5 taxa x 12 nt)
open('dna_star.phy', 'w').write(' 5 12\nA1  ACGTACGTACGT\nA2  ACGTACGTACGA\nA3  ACGTTCGTACGT\nA4  ACGAACGTTCGT\nA5  ACG*ACGTACGT\n')
# NEXUS quoting rules of Biopython's writer, per punctuation character (SKILL: quotes - + : space...; not / .)
res = {}
for ch in list('-+:;,()[]\'"=*/.|_#@% &!'):
    rec = SeqRecord(Seq('ACGT'), id=f'a{ch}b'); rec.annotations['molecule_type'] = 'DNA'
    rec2 = SeqRecord(Seq('ACGT'), id='cc'); rec2.annotations['molecule_type'] = 'DNA'
    buf = io.StringIO()
    try: AlignIO.write(MultipleSeqAlignment([rec, rec2]), buf, 'nexus')
    except Exception as e: res[ch] = f'ERR {type(e).__name__}'; continue
    row = [l for l in buf.getvalue().splitlines() if l.startswith(("'a", 'a')) and 'ACGT' in l.upper()][0]
    res[ch] = 'quoted' if row.startswith("'") else 'plain'
print('Biopython NEXUS id quoting:', res)
quoted = {c for c, v in res.items() if v == 'quoted'}; plain = {c for c, v in res.items() if v == 'plain'}
print('quoted:', ''.join(sorted(quoted)), '| plain:', ''.join(sorted(plain)))
ok({'-', '+', ':', ',', '(', ')', '[', ']', ' '} <= quoted, "SKILL: Biopython quotes ids with '-', '+', ':', space (and , ( ) [ ]) - confirmed")
ok({'/', '.'} <= plain, "SKILL: '/' and '.' alone are not quoted - confirmed")
print("info: '|' is", res['|'], "(MrBayes rejects an unquoted '|', see input 5)")
summary()
