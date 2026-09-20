"""Input 1c: shipped 4-seq DNA sample as alignment.aln (in a scratch copy) -> convert_formats.py (clustal->fasta/phylip/nexus) and slice_alignment.py."""
import subprocess, sys, pathlib, os, shutil
here = pathlib.Path(__file__).parent
d = here/'scratch_sample'; shutil.rmtree(d, ignore_errors=True); shutil.copytree(here/'skill'/'examples', d)
shutil.copy(d/'sample_alignment.aln', d/'alignment.aln')
env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
for s in ['convert_formats.py','slice_alignment.py']:
    r = subprocess.run([sys.executable, s], cwd=d, capture_output=True, text=True, env=env, encoding='utf-8')
    print(f'=== {s} exit={r.returncode}\n{r.stdout.strip()}\n{r.stderr.strip()[-200:]}')
print('output.nex exists:', (d/'output.nex').exists(), 'size', (d/'output.nex').stat().st_size if (d/'output.nex').exists() else None)
