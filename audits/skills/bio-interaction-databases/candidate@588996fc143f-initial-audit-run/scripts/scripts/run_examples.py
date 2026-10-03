"""Run both shipped examples (cwd = run evidence dir so the CSV lands outside the candidate), then inspect edge attributes."""
import os
import runpy
import sys
import time
import traceback

sys.dont_write_bytecode = True
CAND = r'F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases'
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'evidence'))

print('=== examples/string_network.py ===')
try:
    runpy.run_path(os.path.join(CAND, 'examples', 'string_network.py'), run_name='__main__')
    print('EXIT 0')
except Exception:
    print('EXIT 1')
    traceback.print_exc(limit=1)
time.sleep(2)

print('\n=== examples/interaction_query.py ===')
ns = None
try:
    ns = runpy.run_path(os.path.join(CAND, 'examples', 'interaction_query.py'), run_name='__main__')
    print('EXIT 0')
except Exception:
    print('EXIT 1')
    traceback.print_exc(limit=1)

if ns:
    g = ns['g']
    print('\n=== edge attribute audit on the example graph ===')
    by_src = {}
    for a, b, d in g.edges(data=True):
        for s in d['sources']:
            by_src.setdefault(s, set()).add(round(d['max_score'], 4))
    for s, v in sorted(by_src.items()):
        print(f'  {s}: distinct max_score values {sorted(v)[:6]}')
    e = g['MDM2']['CHEK2']
    print('  MDM2->CHEK2 attrs:', {k: (sorted(v) if isinstance(v, set) else v) for k, v in e.items()})
    print('  STRING TSV score for MDM2-CHEK2 was 0.994 (0-1 scale)')
