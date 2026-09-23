"""Execute every ```python block of the Skill's SKILL.md, in order, in ONE namespace, with no examples/ on the path.

This is the 'code the agent copies from the Skill' path, taken from the file itself (no hand transcription).
Returns (namespace, log). Blocks read alignment.fasta / pfam.sto / alignment.sto from the working dir, which is a
scratch dir holding the REAL Pfam PF00042 seed under those names.
"""
import os, re, sys, shutil, traceback, io, contextlib, warnings
from common import SKILL, DATA, PFAM_STO


def blocks(md_path):
    text = open(md_path, encoding='utf-8').read()
    return re.findall(r'```python\n(.*?)```', text, flags=re.S)


def load(workdir=None):
    workdir = workdir or os.path.join(DATA, 'skillns_work')
    os.makedirs(workdir, exist_ok=True)
    from Bio import AlignIO
    aln = AlignIO.read(PFAM_STO, 'stockholm')
    AlignIO.write(aln, os.path.join(workdir, 'alignment.fasta'), 'fasta')
    shutil.copy(PFAM_STO, os.path.join(workdir, 'pfam.sto'))
    shutil.copy(PFAM_STO, os.path.join(workdir, 'alignment.sto'))
    ns = {'__name__': 'skillns'}
    log = []
    cwd = os.getcwd()
    os.chdir(workdir)
    # make sure examples/ is NOT importable: proves the SKILL.md code is self-contained
    saved_path = list(sys.path)
    sys.path[:] = [p for p in sys.path if os.path.normcase(os.path.abspath(p)).find(os.path.normcase(os.path.join('skill', 'examples'))) < 0]
    try:
        for i, code in enumerate(blocks(os.path.join(SKILL, 'SKILL.md'))):
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf), warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    exec(compile(code, f'SKILL.md block {i}', 'exec'), ns)
                log.append((i, True, code.strip().splitlines()[0][:70], buf.getvalue()[:200]))
            except Exception as e:
                log.append((i, False, code.strip().splitlines()[0][:70], f'{type(e).__name__}: {e}'))
    finally:
        os.chdir(cwd)
        sys.path[:] = saved_path
    return ns, log


if __name__ == '__main__':
    ns, log = load()
    for i, ok, first, out in log:
        print(f"block {i:2d} {'ok ' if ok else 'ERR'} | {first} | {out.strip()[:100]}")
    print(sum(1 for l in log if l[1]), 'of', len(log), 'blocks ran')
