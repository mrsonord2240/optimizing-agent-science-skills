"""Misc doc-claim probes: STRING v11.5 host, IntAct liveness, BioGRID max=10000 cap on a very large gene. Key redacted."""
import os
import sys
import time

sys.dont_write_bytecode = True
import requests

ENV = r'F:\OpenScience\audit-envs\database-access\private\biogrid.env'
KEY = next(l.split('=', 1)[1].strip().strip('"\'') for l in open(ENV, encoding='utf-8') if l.startswith('BIOGRID_ACCESS_KEY='))


def red(s):
    return str(s).replace(KEY, '<REDACTED>')


def step(name, fn):
    print(f'--- {name}')
    try:
        print(red(fn()))
    except Exception as e:  # noqa
        print(red(f'EXC {type(e).__name__}: {str(e)[:200]}'))
    time.sleep(1.5)


def v115():
    r = requests.get('https://version-11-5.string-db.org/api/json/version', timeout=60)
    return r.status_code, r.text[:120]
step('STRING version-11-5 host', v115)


def intact():
    r = requests.get('https://www.ebi.ac.uk/intact/ws/interaction/findInteractions/P04637', params={'pageSize': 3}, timeout=90,
                     headers={'Accept': 'application/json'})
    j = r.json()
    return r.status_code, j.get('totalElements'), [(x.get('idA'), x.get('idB')) for x in j.get('content', [])[:1]]
step('IntAct findInteractions/P04637 (liveness; no client function ships)', intact)


def big():
    out = {}
    for g in ('UBC', 'TP53'):
        r = requests.get('https://webservice.thebiogrid.org/interactions/', params={'accesskey': KEY, 'format': 'count', 'geneList': g,
                                                                                    'searchNames': True, 'taxId': 9606, 'includeInteractors': True}, timeout=120)
        out[g] = r.text.strip()[:20]
        time.sleep(1)
    return out
step('BioGRID total rows for a very large gene vs the client max=10000', big)
