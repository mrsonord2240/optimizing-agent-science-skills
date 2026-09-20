"""INPUT 8 (NEW, Data Analysis / edge-stress): the round-2 alphabet inference in examples/convert_formats.py (>= 90% ACGTUN = nucleotide; U without T = RNA; else protein).
Every case is a Clustal file (the example's input format) run through the SHIPPED script from a COPY of examples/ with no override; the output is the 'Molecule type:' line,
the NEXUS 'datatype=' line and whether the NEXUS re-reads. REAL data: MAFFT-aligned RefSeq HBB CDS (lower case), Rfam RF00005 tRNA (RNA), Pfam PF00042, UniProt globins.
SYNTHETIC (labelled): IUPAC / N / X substitutions into the real HBB alignment, mixed T+U, all-gap, tiny and ACGTN-only 'protein' alignments.
Truth label = what the residues really are; the assertion is that the script's label equals the truth (FAIL = mislabel or unhelpful failure)."""
import os, re, random, shutil, subprocess, sys
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from common import *
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
w = HERE/'scratch'/'infer'; shutil.rmtree(w, ignore_errors=True); shutil.copytree(SKILL/'examples', w)
E2E = DATA/'e2e'
hbb = AlignIO.read(E2E/'hbb6_aln.fa', 'fasta')          # real, lower case, 6 x 444
rfam = AlignIO.read(DATA/'rfam_RF00005.sto', 'stockholm')
pfam = AlignIO.read(str(PFAM), 'stockholm')
glob = AlignIO.read(E2E/'globins8_aln.fa', 'fasta')
random.seed(11)
def subst(aln, frac, alphabet, seed=11):
    rnd = random.Random(seed); out = []
    for r in aln:
        s = list(str(r.seq))
        idx = [i for i, c in enumerate(s) if c not in '-.']
        for i in rnd.sample(idx, int(frac * len(idx))): s[i] = rnd.choice(alphabet)
        out.append(SeqRecord(Seq(''.join(s)), id=r.id))
    return MultipleSeqAlignment(out)
def mk(ids_seqs): return MultipleSeqAlignment([SeqRecord(Seq(s), id=i) for i, s in ids_seqs])
def frac_nuc(aln):
    res = re.sub(r'[-.?*]', '', ''.join(str(r.seq) for r in aln).upper()); return sum(res.count(c) for c in 'ACGTUN') / max(len(res), 1)
rna_lc = MultipleSeqAlignment([SeqRecord(Seq(str(r.seq).lower().replace('t', 'u')), id=r.id) for r in hbb])   # SYNTHETIC: real HBB, lower-case, T->U
gappy = MultipleSeqAlignment([SeqRecord(Seq(''.join(c if (i % 10 == 0 or c == '-') else '-' for i, c in enumerate(str(r.seq)))), id=r.id) for r in hbb])   # 90% gaps
mixed = MultipleSeqAlignment([SeqRecord(Seq(str(r.seq).lower().replace('t', 'u') if k else str(r.seq)), id=r.id) for k, r in enumerate(hbb)])   # 1 DNA row + 5 RNA rows
pstop = MultipleSeqAlignment([SeqRecord(Seq(str(r.seq).replace('.', '-') + '*'), id=r.id) for r in glob])
cases = [
 # name, alignment, truth, note
 ('real_HBB_CDS_lowercase',      hbb,                          'DNA',     'REAL MAFFT output, lower case'),
 ('real_Rfam_tRNA_954',          rfam,                         'RNA',     'REAL Rfam RF00005 seed'),
 ('real_Pfam_PF00042',           pfam,                         'protein', 'REAL Pfam seed'),
 ('real_UniProt_globins',        glob,                         'protein', 'REAL UniProt, MAFFT'),
 ('HBB_5pct_IUPAC',              subst(hbb, .05, 'RYKMSW'),    'DNA',     'SYNTHETIC 5% ambiguity codes'),
 ('HBB_12pct_IUPAC',             subst(hbb, .12, 'RYKMSW'),    'DNA',     'SYNTHETIC 12% ambiguity codes (degenerate-primer / low-quality data)'),
 ('HBB_12pct_N',                 subst(hbb, .12, 'N'),         'DNA',     'SYNTHETIC 12% N'),
 ('HBB_12pct_X_mask',            subst(hbb, .12, 'X'),         'DNA',     'SYNTHETIC 12% X mask'),
 ('HBB_lowercase_RNA',           rna_lc,                       'RNA',     'SYNTHETIC: real HBB T->U, lower case'),
 ('HBB_90pct_gaps',              gappy,                        'DNA',     'SYNTHETIC: real HBB, 90% of residues replaced by gaps'),
 ('mixed_1DNA_5RNA_rows',        mixed,                        'ambiguous','SYNTHETIC: one row with T, five with U'),
 ('all_gap',                     mk([('a', '-----'), ('b', '-----')]), 'n/a', 'SYNTHETIC: no residues'),
 ('tiny_DNA_3x4',                mk([('a', 'ACGT'), ('b', 'ACGA'), ('c', 'ACGT')]), 'DNA', 'SYNTHETIC tiny'),
 ('protein_only_ACGTN_letters',  mk([('a', 'GATTACA'), ('b', 'GATTAGA'), ('c', 'GATNACA')]), 'protein', 'SYNTHETIC peptide made only of A,C,G,T,N letters: inherently ambiguous'),
 ('glob_with_terminal_stop',     pstop,                        'protein', 'SYNTHETIC: real globin MAFFT + terminal "*"'),
]
def dt(p): return ([l.strip() for l in p.read_text().splitlines() if 'datatype' in l.lower()] or [None])[0]
rows = []
for name, aln, truth, note in cases:
    for f in ['output.fasta', 'output.phy', 'output.nex']:
        if (w/f).exists(): (w/f).unlink()
    AlignIO.write(aln, w/f'{name}.aln', 'clustal')
    r = subprocess.run([sys.executable, 'convert_formats.py', f'{name}.aln'], cwd=w, capture_output=True, text=True, env=env, encoding='utf-8')
    mt = (re.search(r'Molecule type: (\S+)', r.stdout) or [None, None])[1]
    nex = w/'output.nex'; d = dt(nex) if nex.exists() and nex.stat().st_size else None
    err = (r.stderr.strip().splitlines() or [''])[-1][:90]
    rereads = None
    if d:
        try: b = AlignIO.read(nex, 'nexus'); rereads = (len(b), b.get_alignment_length()) == (len(aln), aln.get_alignment_length())
        except Exception as e: rereads = f'ERR {type(e).__name__}'
    rows.append((name, truth, mt, d, r.returncode, err, rereads, round(frac_nuc(aln), 3) if name != 'all_gap' else None))
    print(f'{name:28s} nuc-fraction={rows[-1][7]} truth={truth:9s} label={mt} NEXUS={d} exit={r.returncode} reread={rereads} {err if r.returncode else ""}')
R = {r[0]: r for r in rows}
expect = lambda n, lab: R[n][2] == lab and (R[n][3] or '').startswith(f'format datatype={lab.lower()}') and R[n][6] is True
ok(expect('real_HBB_CDS_lowercase', 'DNA'), 'real HBB CDS (lower case, MAFFT) -> DNA, datatype=dna, NEXUS re-reads')
ok(expect('real_Rfam_tRNA_954', 'RNA'), 'real Rfam tRNA seed (954 x 118) -> RNA, datatype=rna, NEXUS re-reads 954x118')
ok(expect('real_Pfam_PF00042', 'protein'), 'real Pfam -> protein')
ok(expect('real_UniProt_globins', 'protein'), 'real UniProt globins -> protein')
ok(expect('HBB_5pct_IUPAC', 'DNA'), 'DNA with 5% IUPAC ambiguity codes -> DNA')
ok(expect('HBB_12pct_IUPAC', 'DNA'), f"DNA with 12% IUPAC ambiguity codes labelled correctly (label={R['HBB_12pct_IUPAC'][2]}, NEXUS {R['HBB_12pct_IUPAC'][3]}) [ACGTUN counts only 4 of 11 IUPAC nucleotide letters, so >10% R/Y/K/M/S/W flips to protein silently]")
ok(expect('HBB_12pct_N', 'DNA'), 'DNA with 12% N -> DNA')
ok(expect('HBB_12pct_X_mask', 'DNA'), f"DNA with 12% X mask labelled correctly (label={R['HBB_12pct_X_mask'][2]})")
ok(expect('HBB_lowercase_RNA', 'RNA'), 'lower-case RNA -> RNA')
ok(expect('HBB_90pct_gaps', 'DNA'), '90%-gap DNA -> DNA (gaps ignored)')
ok(R['all_gap'][4] != 0 and 'No residues' in R['all_gap'][5], f"all-gap alignment exits with 'No residues in the alignment': {R['all_gap'][5]}")
ok(expect('tiny_DNA_3x4', 'DNA'), 'tiny DNA 3x4 -> DNA')
ok(expect('glob_with_terminal_stop', 'protein'), 'protein with terminal "*" -> protein')
m = R['mixed_1DNA_5RNA_rows']; print('mixed T/U case:', m[2:7])
ok(m[4] != 0 or (m[2] == 'DNA' and m[3] and m[6] is True), f'mixed T+U alignment: loud failure or a consistent file (label={m[2]}, exit={m[4]}, {m[5]}); silent RNA-in-DNA mislabel would be a defect')
p = R['protein_only_ACGTN_letters']; print('ACGTN-only peptide: label', p[2], '(inherent ambiguity: not asserted)')
summary()
