"""Input 1b: canonical workflow on REAL data. Real Pfam PF00042 seed (73 x 141) -> clustal 'alignment.aln' placed next to the
shipped example scripts (in the COPY), then run convert_formats.py, slice_alignment.py, batch_convert.py; assert on the output files."""
import subprocess, sys, pathlib, os, shutil
from Bio import AlignIO
here = pathlib.Path(__file__).parent
ex = here/'skill'/'examples'
src = pathlib.Path(r'F:\OpenScience\audit-envs\alignment\public-data\msa\PF00042_seed.sto')
ref = AlignIO.read(src, 'stockholm')
assert (len(ref), ref.get_alignment_length()) == (73, 141)
AlignIO.write(ref, ex/'alignment.aln', 'clustal')
(ex/'alignments').mkdir(exist_ok=True)
shutil.copy(ex/'alignment.aln', ex/'alignments'/'globin_a.aln'); shutil.copy(ex/'alignment.aln', ex/'alignments'/'globin_b.aln')
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
def run(s):
    r = subprocess.run([sys.executable, s], cwd=ex, capture_output=True, text=True, env=env, encoding='utf-8')
    print(f'=== {s} exit={r.returncode}\n{r.stdout.strip()}\n{r.stderr.strip()[-300:]}'); return r
run('convert_formats.py'); run('slice_alignment.py'); run('batch_convert.py')

# Output assertions (content, not exit code)
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m)
ids = [r.id for r in ref]; seqs = [str(r.seq).upper().replace('.', '-') for r in ref]
for fn, fmt in [('output.fasta','fasta'),('output.phy','phylip-relaxed'),('output.nex','nexus')]:
    try:
        a = AlignIO.read(ex/fn, fmt)
        same = [r.id for r in a]==ids and [str(r.seq).upper().replace('.', '-') for r in a]==seqs
        ok(same and a.get_alignment_length()==141, f'{fn} ({fmt}) re-read: {len(a)}x{a.get_alignment_length()} ids+seqs identical to source = {same}')
    except Exception as e:
        ok(False, f'{fn} ({fmt}) re-read failed: {type(e).__name__}: {e}')
t = AlignIO.read(ex/'trimmed_subset.fasta','fasta')
ok((len(t), t.get_alignment_length())==(5,91), f'trimmed_subset.fasta shape {len(t)}x{t.get_alignment_length()} (expect 5x91: script hard-codes 50:150 but the alignment has 141 cols)')
ok(all(str(t[i].seq)==seqs[i][50:150] for i in range(5)), 'trimmed_subset content == source rows 0-4, cols 50:150')
conv = sorted((ex/'converted').glob('*.fasta'))
ok([c.name for c in conv]==['globin_a.fasta','globin_b.fasta'], f'batch_convert wrote {[c.name for c in conv]}')
