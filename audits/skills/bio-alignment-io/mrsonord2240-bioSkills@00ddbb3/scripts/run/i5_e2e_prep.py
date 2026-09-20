"""INPUT 5 (NEW, Stress / end-to-end). REAL RefSeq HBB CDS x6 and REAL UniProt globins x8, MAFFT-aligned (i5_mafft.sh), REAL ids kept.
A researcher's workflow through the Skill: aligned FASTA -> Clustal file -> shipped convert_formats.py (from a COPY) -> NEXUS / PHYLIP-relaxed for MrBayes, IQ-TREE, RAxML-NG;
then PHYLIP-sequential for codeml. Writes the files the tool script i5_tools.sh consumes; assertions on file content only here (tools judged in i5_check.py)."""
import os, re, shutil, subprocess, sys
from Bio import AlignIO
from common import *
d = DATA/'e2e'; os.chdir(d)
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
def conv(name, fmt_in='fasta'):
    """user has an aligned FASTA; the shipped example reads Clustal, so write Clustal first (as the README-style route says), then run the example from a copy"""
    a = AlignIO.read(f'{name}_aln.fa', fmt_in); AlignIO.write(a, f'{name}.aln', 'clustal')
    w = d/f'ex_{name}'; shutil.rmtree(w, ignore_errors=True); shutil.copytree(SKILL/'examples', w); shutil.copy(f'{name}.aln', w/f'{name}.aln')
    r = subprocess.run([sys.executable, 'convert_formats.py', f'{name}.aln'], cwd=w, capture_output=True, text=True, env=env, encoding='utf-8')
    print(r.stdout.strip()); print('STDERR:', r.stderr.strip()[-200:]) if r.stderr.strip() else None
    return a, w, r
for name, dt in [('hbb6', 'dna'), ('globins8', 'protein')]:
    print(f'=== {name}')
    a, w, r = conv(name)
    ok(r.returncode == 0 and f'Molecule type: {"DNA" if dt=="dna" else "protein"}' in r.stdout and f'datatype={dt}' in r.stdout, f'{name}: convert_formats.py infers {dt} and checks the NEXUS datatype line')
    print('ids:', [x.id for x in a][:3], 'shape', len(a), a.get_alignment_length())
    for fn, fmt in [('output.fasta','fasta'),('output.phy','phylip-relaxed'),('output.nex','nexus')]:
        b = AlignIO.read(w/fn, fmt)
        ok([x.id for x in b] == [x.id for x in a] and [str(x.seq).upper() for x in b] == [str(x.seq).upper() for x in a], f'{name}: {fn} ({fmt}) re-reads identical ids + residues ({len(b)}x{b.get_alignment_length()})')
    nx = (w/'output.nex').read_text()
    print('NEXUS matrix first row:', [l for l in nx.splitlines() if l.strip()][ -len(a)-2 ][:60])
    print('quote chars in example NEXUS:', nx.count("'"))
    shutil.copy(w/'output.nex', f'{name}_example.nex'); shutil.copy(w/'output.phy', f'{name}_relaxed.phy')
    # SKILL MrBayes recipe (verbatim, second python block under the NEXUS heading) applied to the alignment, then NEXUS with molecule_type
    a2 = AlignIO.read(f'{name}_aln.fa', 'fasta'); ns = {'alignment': a2}; exec(block('NEXUS Output Needs', 1), ns)
    for r_ in a2: r_.annotations['molecule_type'] = 'DNA' if dt == 'dna' else 'protein'
    print('ids after recipe:', [x.id for x in a2][:3])
    ok(all(re.fullmatch(r'[A-Za-z0-9_]+', x.id) for x in a2) and len({x.id for x in a2}) == len(a2), f'{name}: recipe ids are [A-Za-z0-9_]+ and unique')
    AlignIO.write(a2, f'{name}_recipe.nex', 'nexus')
    AlignIO.write(a2, f'{name}_recipe.phy', 'phylip-relaxed')
    for r_ in a2: r_.id = r_.id[:10]
    if name == 'hbb6':
        print('10-char prefixes of the recipe ids:', [r_.id for r_ in a2])
# PAML route: SKILL says shorten ids to <= 10 unique chars first
a = AlignIO.read('hbb6_aln.fa', 'fasta')
try: AlignIO.write(a, 'codeml_real_ids.phy', 'phylip-sequential'); ok(False, 'real NCBI ids did not collide in phylip-sequential')
except ValueError as e: ok('Repeated name' in str(e), f'phylip-sequential with real NCBI ids raises, as the SKILL warns: {str(e)[:70]}')
short = {}
for r_ in a: r_.id = re.sub(r'^lcl\|([NX])M_0*(\d+)\.\d+$', r'\1\2', r_.id); r_.name = r_.id; r_.description = ''
print('short ids', [r_.id for r_ in a], [len(r_.id) for r_ in a])
ok(len({r_.id for r_ in a}) == 6 and all(len(r_.id) <= 10 for r_ in a), 'accession-only ids are <= 10 chars and unique')
tree = '(((N518,X508242),N1164428),(N173917,N1164018),N1144841);'
for tag, fmt in [('seq', 'phylip-sequential'), ('rel', 'phylip-relaxed')]:
    w = d/f'codeml_{tag}'; shutil.rmtree(w, ignore_errors=True); w.mkdir()
    AlignIO.write(a, w/'aln.phy', fmt); (w/'tree.nwk').write_text(tree + '\n')
    (w/'codeml.ctl').write_text('seqfile = aln.phy\ntreefile = tree.nwk\noutfile = mlc\nnoisy = 0\nverbose = 0\nrunmode = 0\nseqtype = 1\nCodonFreq = 2\nmodel = 0\nNSsites = 0\nicode = 0\nfix_kappa = 0\nkappa = 2\nfix_omega = 0\nomega = 0.4\ncleandata = 0\n', encoding='utf-8')
    print(tag, open(w/'aln.phy').read()[:90].replace('\n', ' | '))
L = a.get_alignment_length(); ok(L % 3 == 0, f'codon alignment length {L} is a multiple of 3')
print('=== Clustal writer 30-char id limit (probe; not a claim of the SKILL)')
from Bio.Align import MultipleSeqAlignment
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import io
long_ids = ['lcl|NM_000518.5_cds_NP_000509.1_1', 'lcl|NM_000518.5_cds_NP_000509.1_2']   # REAL NCBI id style; second is a SYNTHETIC sibling
cl = MultipleSeqAlignment([SeqRecord(Seq('ACGT'), id=i) for i in long_ids]); buf = io.StringIO(); AlignIO.write(cl, buf, 'clustal')
back = AlignIO.read(io.StringIO(buf.getvalue()), 'clustal'); print('ids after clustal round trip:', [x.id for x in back])
ok(all(len(x.id) == 30 for x in back), 'Clustal writer silently truncates ids to 30 characters')
ok(len({x.id for x in back}) == 1, 'and two ids that differ only after char 30 come back as the SAME id (no error; PHYLIP raises here, Clustal does not)')
ok('truncat' not in ' '.join(l for l in (SKILL/'SKILL.md').read_text(encoding='utf-8').splitlines() if 'Clustal' in l), 'SKILL.md lines mentioning Clustal say nothing about id truncation (documentation gap)')
summary()
