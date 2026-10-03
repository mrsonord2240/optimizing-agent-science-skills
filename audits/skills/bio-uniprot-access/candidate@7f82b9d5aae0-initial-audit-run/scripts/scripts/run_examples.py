"""Run both shipped UniProt examples via runpy; capture exit state."""
import os, runpy, sys, time, traceback
sys.dont_write_bytecode = True
CAND = r'F:\OpenScience\wt\dbaccess-uniprot-access\skills\bio-uniprot-access'
for name in ('uniprot_query', 'isoforms_and_xrefs'):
    print(f'=== examples/{name}.py ===')
    try:
        runpy.run_path(os.path.join(CAND, 'examples', f'{name}.py'), run_name='__main__')
        print('EXIT 0')
    except Exception:
        print('EXIT 1')
        traceback.print_exc(limit=1)
    time.sleep(1)
