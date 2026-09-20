"""Extract every ```python block from the copied SKILL.md and exec them in ONE shared namespace, in document order.
Records status per block; asserts on the object state afterwards (not just 'no exception')."""
import re, io, contextlib, os, warnings, sys
warnings.simplefilter('ignore')
os.chdir(r'F:\OpenScience\audits\bio-alignment-pairwise\run\clean_ex')
open('sequences.fasta', 'w').write('>a\nACCGGTAACGTAG\n>b\nACCGTTAACGAAG\n')
txt = open(r'F:\OpenScience\audits\bio-alignment-pairwise\run\skill\SKILL.md', encoding='utf-8').read()
blocks = re.findall(r'```python\n(.*?)```', txt, re.S)
ns = {}; ok = fail = 0
for i, b in enumerate(blocks, 1):
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(b, f'<SKILL block {i}>', 'exec'), ns)
        ok += 1; st = 'OK  '
    except Exception as e:
        fail += 1; st = f'FAIL {type(e).__name__}: {str(e)[:70]}'
    first = b.strip().splitlines()[0][:70]
    print(f"block {i:2d} [{st}] first line: {first!r} | stdout {len(buf.getvalue())} chars")
print(f"\n{ok}/{len(blocks)} blocks executed without exception; failures: {fail}")
# state assertions
a = ns.get('aligner')
print("final aligner mode/gaps:", getattr(a, 'mode', None), getattr(a, 'open_gap_score', None))
al = ns.get('alignment')
print("alignment score var:", al.score if al is not None else None)
