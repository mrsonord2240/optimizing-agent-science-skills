"""Probe the lighter Compara calls used by examples/compara_homology.py (mouse-target and paralogs) plus TP53; reports each call or its clean error."""
import sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, 'F:/OpenScience/wt/dbaccess-ensembl-rest/skills/bio-ensembl-rest/scripts')
import ensembl_client as c
for label, fn in [
    ('BRCA1->mouse', lambda: c.orthologs_by_symbol('human', 'BRCA1', target='mouse')),
    ('BRCA1 paralogs', lambda: c.paralogs_by_symbol('human', 'BRCA1')),
    ('TP53->mouse', lambda: c.orthologs_by_symbol('human', 'TP53', target='mouse')),
]:
    for attempt in (1, 2):
        t0 = time.time()
        try:
            r = fn()
            print(label, 'OK', len(r), [(h['type'], h['target']['id'], h.get('confidence'), h['target'].get('perc_id')) for h in r[:2]], f'{time.time()-t0:.1f}s')
            break
        except Exception as e:
            print(label, f'attempt{attempt}', type(e).__name__, str(e)[:150], f'{time.time()-t0:.1f}s')
            time.sleep(20)
