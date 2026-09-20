"""INPUT 1 (Canonical, regression of round 1 + round-2 targets). Run every shipped example from a CLEAN COPY of examples/ (never the worktree), as shipped,
then on REAL Pfam PF00042 (73x141) as Clustal. Round-2 targets: convert_formats.py alphabet inference / override / datatype assert, read_alignment.py cwd + label.
Assert on output-file content, not exit codes."""
import subprocess, sys, os, shutil, re
from Bio import AlignIO
from common import *
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
def run(args, cwd):
    r = subprocess.run([sys.executable] + args, cwd=cwd, capture_output=True, text=True, env=env, encoding='utf-8')
    print(f'--- {" ".join(args)} exit={r.returncode}\n{r.stdout.strip()}\n{("STDERR: "+r.stderr.strip()[-300:]) if r.stderr.strip() else ""}')
    return r
def fresh(name):
    d = HERE/'scratch'/name; shutil.rmtree(d, ignore_errors=True); shutil.copytree(SKILL/'examples', d); return d
def dtype(p): return [l.strip() for l in (p).read_text().splitlines() if 'datatype' in l.lower()]

print('=== A. shipped sample, no arguments')
d = fresh('ex_sample')
r = run(['read_alignment.py'], d)
ok('21 columns' in r.stdout and 'Number of sequences: 4' in r.stdout and 'seq1' in r.stdout, 'read_alignment.py prints 21 columns / 4 sequences / seq1')
ok('bp' not in r.stdout and 'columns' in r.stdout.split('Sequence IDs')[1], 'read_alignment.py per-sequence label is "columns" (not "bp")')
r = run(['convert_formats.py'], d)
ok('Molecule type: DNA' in r.stdout and 'Checked: output.nex says datatype=dna' in r.stdout, 'convert_formats.py infers DNA for the shipped nucleotide sample and prints the datatype check')
src = AlignIO.read(d/'sample_alignment.aln', 'clustal'); ids = [x.id for x in src]; seqs = [str(x.seq) for x in src]
for fn, fmt in [('output.fasta','fasta'),('output.phy','phylip-relaxed'),('output.nex','nexus')]:
    try:
        a = AlignIO.read(d/fn, fmt)
        ok([x.id for x in a]==ids and [str(x.seq).upper() for x in a]==[s.upper() for s in seqs], f'{fn} ({fmt}) re-reads 4x21 with ids+residues identical to source; size={(d/fn).stat().st_size}')
    except Exception as e: ok(False, f'{fn} ({fmt}) re-read failed: {type(e).__name__}: {e}')
ok(dtype(d/'output.nex') and 'datatype=dna' in dtype(d/'output.nex')[0].lower(), f'NEXUS datatype line: {dtype(d/"output.nex")}')
r = run(['slice_alignment.py'], d)
t = AlignIO.read(d/'trimmed_subset.fasta', 'fasta')
ok((len(t), t.get_alignment_length()) == (4, 10) and [str(x.seq) for x in t] == [s[5:15] for s in seqs], f'slice_alignment.py -> trimmed_subset.fasta {len(t)}x{t.get_alignment_length()} equals source cols 5:15')
r = run(['batch_convert.py'], d)
c = sorted((d/'converted').glob('*.fasta')); ok([x.name for x in c] == ['sample_alignment.fasta'], f'batch_convert.py converted {[x.name for x in c]}')
b = AlignIO.read(c[0], 'fasta'); ok([str(x.seq) for x in b] == seqs, 'batch output residues identical to source')

print('=== B. real Pfam PF00042 (73 x 141) as Clustal')
d = fresh('ex_pfam')
ref = AlignIO.read(PFAM, 'stockholm'); ok((len(ref), ref.get_alignment_length()) == (73, 141), 'real Pfam seed reads 73x141 via AlignIO stockholm')
AlignIO.write(ref, d/'pfam.aln', 'clustal')
rids = [x.id for x in ref]; rseqs = [str(x.seq).upper().replace('.', '-') for x in ref]
for label, args in [('DEFAULT (no override)', ['convert_formats.py', 'pfam.aln']), ('override protein', ['convert_formats.py', 'pfam.aln', 'protein']), ('override Protein (case)', ['convert_formats.py', 'pfam.aln', 'Protein'])]:
    r = run(args, d)
    ok('Molecule type: protein' in r.stdout and 'datatype=protein' in r.stdout, f'{label}: molecule type protein, datatype=protein checked')
    for fn, fmt in [('output.fasta','fasta'),('output.phy','phylip-relaxed'),('output.nex','nexus')]:
        a = AlignIO.read(d/fn, fmt)
        ok([x.id for x in a]==rids and [str(x.seq).upper().replace('.','-') for x in a]==rseqs, f'{label}: {fn} ({fmt}) re-read {len(a)}x{a.get_alignment_length()} ids+residues identical')
    ok('datatype=protein' in dtype(d/'output.nex')[0].lower(), f'{label}: NEXUS line {dtype(d/"output.nex")}')
r = run(['slice_alignment.py', 'pfam.aln'], d)
t = AlignIO.read(d/'trimmed_subset.fasta', 'fasta')
ok((len(t), t.get_alignment_length()) == (5, 10) and all(str(t[i].seq) == rseqs[i][5:15] for i in range(5)), 'real Pfam slice = source rows 0-4 cols 5:15')
(d/'alns').mkdir(); shutil.copy(d/'pfam.aln', d/'alns'/'a.aln'); shutil.copy(d/'pfam.aln', d/'alns'/'b.aln')
r = run(['batch_convert.py', 'alns'], d)
ok(sorted(x.name for x in (d/'converted').glob('*.fasta')) == ['a.fasta','b.fasta'], 'batch on 2 real files -> a.fasta, b.fasta')

print('=== C. adversarial use of the examples (override behaviour)')
d = fresh('ex_bad')
(d/'empty_dir').mkdir()
r = run(['batch_convert.py', 'empty_dir'], d); ok(r.returncode != 0 and 'No *.aln' in (r.stdout+r.stderr), f'batch_convert on empty dir exits non-zero with a message (exit {r.returncode})')
AlignIO.write(AlignIO.read(d/'sample_alignment.aln','clustal')[:, :10], d/'ten.aln', 'clustal')
r = run(['slice_alignment.py', 'ten.aln'], d); ok(r.returncode != 0 and 'outside' in (r.stdout+r.stderr), f'slice on a 10-col alignment refuses (exit {r.returncode})'); ok(not (d/'trimmed_subset.fasta').exists(), 'no 0-column trimmed_subset.fasta written on refusal')
r = run(['convert_formats.py', 'nope.aln'], d); ok(r.returncode != 0, 'convert_formats on missing file fails (exit %d)' % r.returncode)
for arg, expect_fail in [('foo', True), ('protein', True), ('Protein', True), ('dna', False), ('DNA', False), ('RNA', True), ('rna', True)]:
    for f in ['output.fasta','output.phy','output.nex']:
        if (d/f).exists(): (d/f).unlink()
    r = run(['convert_formats.py', 'sample_alignment.aln', arg], d)
    nex = d/'output.nex'
    wrote = nex.exists() and nex.stat().st_size > 0
    if expect_fail: ok(r.returncode != 0 and not wrote, f'DNA sample with override "{arg}" fails loudly with no usable NEXUS: exit {r.returncode}, usable output.nex={wrote} (exists={nex.exists()}, size={nex.stat().st_size if nex.exists() else None}); last stderr line: {(r.stderr.strip().splitlines() or [""])[-1][:90]}')
    else: ok(r.returncode == 0, f'DNA sample with override "{arg}" accepted: exit {r.returncode}; NEXUS {dtype(nex)[:1]}')
print('note: RNA/rna override on a T-containing alignment is NOT caught by the example guard (nucleotide vs nucleotide); Biopython NEXUS writer raises after fasta/phy were already written')
d2 = fresh('ex_bad2'); AlignIO.write(ref, d2/'pfam.aln', 'clustal')
r = run(['convert_formats.py', 'pfam.aln', 'DNA'], d2); ok(r.returncode != 0 and not (d2/'output.nex').exists(), f'protein alignment with override DNA exits non-zero, no NEXUS: exit {r.returncode}')

print('=== C2. RNA alignment (SYNTHETIC: shipped sample with T->U) inference and override')
d3 = fresh('ex_rna'); txt = (d3/'sample_alignment.aln').read_text()
head, body = txt.split(chr(10), 1); (d3/'rna.aln').write_text(head + chr(10) + body.replace('T', 'U'))
rr = AlignIO.read(d3/'rna.aln', 'clustal'); print('RNA sample residues:', [str(x.seq) for x in rr][:2])
r = run(['convert_formats.py', 'rna.aln'], d3)
ok('Molecule type: RNA' in r.stdout and 'datatype=rna' in dtype(d3/'output.nex')[0].lower(), f'RNA alignment inferred as RNA, NEXUS {dtype(d3/"output.nex")}')
a = AlignIO.read(d3/'output.nex', 'nexus'); ok([str(x.seq).upper() for x in a] == [str(x.seq).upper() for x in rr], 'RNA NEXUS re-reads identical residues')
for f in ['output.fasta','output.phy','output.nex']: (d3/f).unlink()
r = run(['convert_formats.py', 'rna.aln', 'DNA'], d3)
nex = d3/'output.nex'; ok(r.returncode != 0 and not (nex.exists() and nex.stat().st_size > 0), f'RNA alignment with override DNA fails loudly, no usable NEXUS: exit {r.returncode}')

print('=== D. read_alignment.py from another cwd (round-2 target)')
other = HERE/'scratch'/'elsewhere'; shutil.rmtree(other, ignore_errors=True); other.mkdir()
r = subprocess.run([sys.executable, str(HERE/'scratch'/'ex_sample'/'read_alignment.py')], cwd=other, capture_output=True, text=True, env=env, encoding='utf-8')
print(r.stdout[:200], r.stderr[-200:])
ok(r.returncode == 0 and 'Number of sequences: 4' in r.stdout, 'read_alignment.py runs from an unrelated cwd (4 sequences)')
for f in ['slice_alignment.py', 'batch_convert.py', 'convert_formats.py']:
    r = subprocess.run([sys.executable, str(HERE/'scratch'/'ex_sample'/f)], cwd=other, capture_output=True, text=True, env=env, encoding='utf-8')
    ok(r.returncode == 0, f'{f} with no args from an unrelated cwd finds the shipped sample: exit {r.returncode}')
print('__pycache__ under scratch:', list((HERE/'scratch').rglob('__pycache__')))
summary()
