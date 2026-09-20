"""Execute the ```python blocks of skill/SKILL.md VERBATIM (no edits), in order, in one namespace.
Blocks whose functions are `...` stubs are skipped (full implementation is in examples/). Each block's stdout /
exception is recorded so we can say which snippets actually ran. The blocks read 'alignment.fasta' from cwd,
so callers chdir into a work dir holding that file."""
import contextlib
import io
import os
import re
import sys
import traceback

SKILL_MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skill', 'SKILL.md')


def extract_blocks():
    text = open(SKILL_MD, encoding='utf-8').read()
    return re.findall(r"```python\n(.*?)```", text, flags=re.S)


def is_stub(block):
    return re.search(r"^\s+\.\.\.\s*$", block, flags=re.M) is not None


def run_all(verbose=True):
    ns = {'__name__': 'skillns'}
    log = []
    for i, b in enumerate(extract_blocks()):
        first = next((l for l in b.splitlines() if l.strip()), '')[:70]
        if is_stub(b):
            log.append((i, first, 'SKIPPED_STUB', ''))
            continue
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(b, f'<SKILL.md block {i}>', 'exec'), ns)
            log.append((i, first, 'OK', buf.getvalue()))
        except Exception as e:  # record, keep going
            log.append((i, first, 'ERROR ' + type(e).__name__ + ': ' + str(e)[:150], buf.getvalue()))
    if verbose:
        for i, first, st, out in log:
            print(f'[block {i:2d}] {st:<40} {first}')
    return ns, log


if __name__ == '__main__':
    ns, log = run_all()
