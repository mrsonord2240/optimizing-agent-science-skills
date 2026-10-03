"""BioGRID + aggregate_networks probes. The access key is read at run time from the private env file and is
never printed, stored in a URL, or written to disk; every printed string passes through redact()."""
import io
import os
import sys
import time
from collections import Counter

sys.dont_write_bytecode = True
CAND = r'F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases'
sys.path.insert(0, os.path.join(CAND, 'scripts'))
import requests
import interaction_clients as ic

ENV = r'F:\OpenScience\audit-envs\database-access\private\biogrid.env'
KEY = next(l.split('=', 1)[1].strip().strip('"\'') for l in open(ENV, encoding='utf-8') if l.startswith('BIOGRID_ACCESS_KEY='))


def redact(s):
    import re
    return re.sub(r"accesskey=[^&\s']*", 'accesskey=<REDACTED>', str(s).replace(KEY, '<REDACTED>'))


def step(name, fn):
    print(f'--- {name}')
    try:
        print(redact(fn()))
    except Exception as e:  # noqa
        print(redact(f'EXC {type(e).__name__}: {str(e)[:250]}'))
    time.sleep(1.0)


def raw(params):
    p = {'accesskey': KEY, 'format': 'json', 'searchNames': True, 'taxId': 9606, **params}
    return requests.get(ic.BIOGRID, params=p, timeout=120)


def count():
    r = raw({'geneList': 'TP53', 'format': 'count', 'includeInteractors': True, 'max': 10000})
    r2 = raw({'geneList': 'TP53', 'format': 'count', 'includeInteractors': False, 'max': 10000})
    return {'count includeInteractors=True': r.text.strip()[:30], 'count includeInteractors=False': r2.text.strip()[:30]}
step('TP53 total BioGRID rows (count endpoint)', count)


def rows():
    r = raw({'geneList': 'TP53', 'includeInteractors': True, 'max': 10000})
    j = r.json()
    vals = list(j.values())
    inv = sum(1 for v in vals if 'TP53' in (v['OFFICIAL_SYMBOL_A'], v['OFFICIAL_SYMBOL_B']))
    thr = Counter(v['THROUGHPUT'] for v in vals)
    return {'rows returned (max=10000)': len(vals), 'rows involving TP53': inv, 'throughput': dict(thr),
            'organisms A': dict(Counter(v['ORGANISM_A'] for v in vals).most_common(3)),
            'evidence types': dict(Counter(v['EXPERIMENTAL_SYSTEM_TYPE'] for v in vals))}
step('TP53 rows via the client request shape', rows)


def rows_no_interactors():
    r = raw({'geneList': 'TP53', 'includeInteractors': False, 'max': 10000})
    vals = list(r.json().values())
    lt_phys = [v for v in vals if v['THROUGHPUT'] == 'Low Throughput' and v['EXPERIMENTAL_SYSTEM_TYPE'] == 'physical']
    in_set = [v for v in lt_phys if v['EXPERIMENTAL_SYSTEM'] in ic.PHYSICAL_LT_SYSTEMS]
    return {'rows': len(vals), 'LT physical rows (EXPERIMENTAL_SYSTEM_TYPE=physical)': len(lt_phys),
            'of which in PHYSICAL_LT_SYSTEMS': len(in_set),
            'LT physical systems excluded by the set': dict(Counter(v['EXPERIMENTAL_SYSTEM'] for v in lt_phys if v['EXPERIMENTAL_SYSTEM'] not in ic.PHYSICAL_LT_SYSTEMS)),
            'in-set systems that are not physical type': dict(Counter(v['EXPERIMENTAL_SYSTEM'] for v in vals if v['THROUGHPUT'] == 'Low Throughput' and v['EXPERIMENTAL_SYSTEM'] in ic.PHYSICAL_LT_SYSTEMS and v['EXPERIMENTAL_SYSTEM_TYPE'] != 'physical'))}
step('TP53 LT physical filter versus BioGRID EXPERIMENTAL_SYSTEM_TYPE', rows_no_interactors)


def client_df():
    df = ic.biogrid_lt_physical('TP53', KEY)
    pairs = {tuple(sorted(x)) for x in zip(df.gene_a, df.gene_b)}
    inv = int(((df.gene_a == 'TP53') | (df.gene_b == 'TP53')).sum())
    return {'rows': len(df), 'unique gene pairs': len(pairs), 'rows involving TP53': inv, 'rows not involving TP53': len(df) - inv}
step('biogrid_lt_physical TP53 shape (client)', client_df)


def bad_key():
    fake = 'x' * 32
    r = requests.get(ic.BIOGRID, params={'accesskey': fake, 'format': 'json', 'geneList': 'TP53', 'taxId': 9606}, timeout=60)
    body = r.text[:120]
    try:
        ic.biogrid_lt_physical('TP53', fake)
        return 'no error', r.status_code, body
    except Exception as e:  # noqa
        return f'client raised {type(e).__name__}: {str(e)[:100]}', r.status_code, body
step('invalid key behaviour (fake key, not the real one)', bad_key)


def agg():
    genes = ['TP53', 'MDM2']
    g = ic.aggregate_networks(genes, biogrid_key=KEY)
    by_src = {}
    for a, b, d in g.edges(data=True):
        for s in d['sources']:
            tot, inside = by_src.get(s, (0, 0))
            by_src[s] = (tot + 1, inside + (a in genes and b in genes))
    multi = ic.multi_source_edges(g)
    return {'summary': ic.summary(g), 'edges per source (total, both endpoints in query list)': by_src,
            'multi_source_edges': [(a, b, sorted(d['sources'])) for a, b, d in multi][:5]}
step('aggregate_networks TP53+MDM2 with BioGRID', agg)
