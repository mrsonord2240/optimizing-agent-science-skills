"""INPUT 1 (Canonical, regression). Run every shipped example from a CLEAN COPY of examples/ (never the worktree), as shipped,
then on REAL Pfam PF00042 (73x141). Assert on output-file content, not exit codes."""
import subprocess, sys, os, shutil
from Bio import AlignIO
from common import *
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
def run(args, cwd):
    r = subprocess.run([sys.executable] + args, cwd=cwd, capture_output=True, text=True, env=env, encoding='utf-8')
    print(f'--- {" ".join(args)} exit={r.returncode}\n{r.stdout.strip()}\n{("STDERR: "+r.stderr.strip()[-300:]) if r.stderr.strip() else ""}')
    return r
def fresh(name):
    d = HERE/'scratch'/name; shutil.rmtree(d, ignore_errors=True); shutil.copytree(SKILL/'examples', d); return d

print('=== A. shipped sample, no arguments')
d = fresh('ex_sample')
r = run(['read_alignment.py'], d)
ok('21 columns' in r.stdout and 'Number of sequences: 4' in r.stdout and 'seq1' in r.stdout, 'read_alignment.py prints 21 columns / 4 sequences / seq1')
r = run(['convert_formats.py'], d)
src = AlignIO.read(d/'sample_alignment.aln', 'clustal'); ids = [x.id for x in src]; seqs = [str(x.seq) for x in src]
for fn, fmt in [('output.fasta','fasta'),('output.phy','phylip-relaxed'),('output.nex','nexus')]:
    try:
        a = AlignIO.read(d/fn, fmt)
        ok([x.id for x in a]==ids and [str(x.seq).upper() for x in a]==[s.upper() for s in seqs], f'{fn} ({fmt}) re-reads 4x21 with ids+residues identical to source; size={(d/fn).stat().st_size}')
    except Exception as e: ok(False, f'{fn} ({fmt}) re-read failed: {type(e).__name__}: {e}')
nex = (d/'output.nex').read_text()
ok('DATATYPE=DNA' in nex.upper() or 'datatype=dna' in nex.lower(), 'NEXUS file declares datatype DNA (molecule_type honoured): ' + [l for l in nex.splitlines() if 'atatype' in l.lower()][0].strip())
r = run(['slice_alignment.py'], d)
t = AlignIO.read(d/'trimmed_subset.fasta', 'fasta')
ok((len(t), t.get_alignment_length()) == (4, 10) and [str(x.seq) for x in t] == [s[5:15] for s in seqs], f'slice_alignment.py -> trimmed_subset.fasta {len(t)}x{t.get_alignment_length()} equals source cols 5:15')
r = run(['batch_convert.py'], d)
c = sorted((d/'converted').glob('*.fasta')); ok([x.name for x in c] == ['sample_alignment.fasta'], f'batch_convert.py converted {[x.name for x in c]}')
b = AlignIO.read(c[0], 'fasta'); ok([str(x.seq) for x in b] == seqs, 'batch output residues identical to source')

print('=== B. real Pfam PF00042 (73 x 141) as Clustal, examples given the file via argv')
d = fresh('ex_pfam')
ref = AlignIO.read(PFAM, 'stockholm'); ok((len(ref), ref.get_alignment_length()) == (73, 141), 'real Pfam seed reads 73x141 via AlignIO stockholm')
AlignIO.write(ref, d/'pfam.aln', 'clustal')
rids = [x.id for x in ref]; rseqs = [str(x.seq).upper().replace('.', '-') for x in ref]
r = run(['convert_formats.py', 'pfam.aln', 'protein'], d)
for fn, fmt in [('output.fasta','fasta'),('output.phy','phylip-relaxed'),('output.nex','nexus')]:
    try:
        a = AlignIO.read(d/fn, fmt)
        ok([x.id for x in a]==rids and [str(x.seq).upper().replace('.','-') for x in a]==rseqs, f'{fn} ({fmt}) re-read {len(a)}x{a.get_alignment_length()} ids+residues identical')
    except Exception as e: ok(False, f'{fn} re-read: {type(e).__name__}: {e}')
r = run(['convert_formats.py', 'pfam.aln'], d)   # default molecule type DNA on protein: does it fail loudly or write a wrong NEXUS?
nex = (d/'output.nex').read_text().lower(); print('default-DNA on protein NEXUS datatype line:', [l.strip() for l in nex.splitlines() if 'datatype' in l])
r = run(['slice_alignment.py', 'pfam.aln'], d)
t = AlignIO.read(d/'trimmed_subset.fasta', 'fasta')
ok((len(t), t.get_alignment_length()) == (5, 10) and all(str(t[i].seq) == rseqs[i][5:15] for i in range(5)), 'real Pfam slice = source rows 0-4 cols 5:15')
(d/'alns').mkdir(); shutil.copy(d/'pfam.aln', d/'alns'/'a.aln'); shutil.copy(d/'pfam.aln', d/'alns'/'b.aln')
r = run(['batch_convert.py', 'alns'], d)
ok(sorted(x.name for x in (d/'converted').glob('*.fasta')) == ['a.fasta','b.fasta'], 'batch on 2 real files -> a.fasta, b.fasta')

print('=== C. adversarial use of the examples')
d = fresh('ex_bad')
(d/'empty_dir').mkdir()
r = run(['batch_convert.py', 'empty_dir'], d); ok(r.returncode != 0 and 'No *.aln' in (r.stdout+r.stderr), f'batch_convert on empty dir exits non-zero with a message (exit {r.returncode})')
short = d/'short.aln'; short.write_text((d/'sample_alignment.aln').read_text())   # 21 cols, slice wants 5:15 => in range; make a 10-col one
AlignIO.write(AlignIO.read(d/'sample_alignment.aln','clustal')[:, :10], d/'ten.aln', 'clustal')
r = run(['slice_alignment.py', 'ten.aln'], d); ok(r.returncode != 0 and 'outside' in (r.stdout+r.stderr), f'slice on a 10-col alignment refuses (exit {r.returncode})'); ok(not (d/'trimmed_subset.fasta').exists(), 'no 0-column trimmed_subset.fasta written on refusal')
r = run(['convert_formats.py', 'nope.aln'], d); ok(r.returncode != 0, 'convert_formats on missing file fails (exit %d)' % r.returncode)
r = run(['convert_formats.py', 'sample_alignment.aln', 'dna'], d); print('lowercase molecule_type "dna" ->', 'exit', r.returncode, (r.stderr.strip().splitlines() or [''])[-1][:160])
r = run(['convert_formats.py', 'sample_alignment.aln', 'Protein'], d); print('"Protein" ->', 'exit', r.returncode, (r.stderr.strip().splitlines() or [''])[-1][:160])
summary()
