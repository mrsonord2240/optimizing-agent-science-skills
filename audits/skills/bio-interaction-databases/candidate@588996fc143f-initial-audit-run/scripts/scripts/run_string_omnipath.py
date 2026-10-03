"""STRING + OmniPath + SIGNOR probes for bio-interaction-databases (live services). Sequential, small."""
import os
import sys
import time

sys.dont_write_bytecode = True
CAND = r'F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases'
sys.path.insert(0, os.path.join(CAND, 'scripts'))
import pandas as pd
import requests
import interaction_clients as ic

pd.set_option('display.width', 250)
pd.set_option('display.max_columns', 40)


def step(name, fn, sleep=1.5):
    print(f'--- {name}')
    try:
        print(fn())
    except Exception as e:  # noqa
        print(f'EXC {type(e).__name__}: {str(e)[:250]}')
    time.sleep(sleep)


GENES = ['TP53', 'BRCA1', 'MDM2', 'ATM', 'CHEK2', 'CDK2', 'RB1', 'CDKN1A', 'BAX', 'BCL2']

step('STRING version endpoint', lambda: requests.get('https://string-db.org/api/json/version', timeout=60).json())


def resolve():
    df = ic.string_resolve_ids(GENES)
    return list(df.columns), len(df), df[['queryIndex', 'preferredName', 'stringId']].head(4).to_dict('records')
step('string_resolve_ids columns + rows', resolve)


def multi_id_encoding():
    # the client joins identifiers with the literal text %0d; requests percent-encodes the percent sign
    p = {'identifiers': '%0d'.join(['TP53', 'MDM2', 'ATM']), 'species': 9606, 'caller_identity': ic.CALLER}
    prep = requests.Request('GET', f'{ic.STRING}/tsv/get_string_ids', params=p).prepare()
    r = requests.get(f'{ic.STRING}/tsv/get_string_ids', params=p, timeout=60)
    df = pd.read_csv(__import__('io').StringIO(r.text), sep='\t')
    return prep.url.split('?')[1][:80], len(df), list(df.preferredName)
step('multi-identifier encoding as sent by the client', multi_id_encoding)


def net(thr=700):
    df = ic.string_network(GENES, threshold=thr)
    return df
df700 = None


def s_net():
    global df700
    df700 = ic.string_network(GENES, threshold=700)
    return list(df700.columns), len(df700), df700[['preferredName_A', 'preferredName_B', 'score', 'escore', 'dscore', 'tscore']].head(5).to_string(index=False)
step('string_network threshold 700', s_net)


def tiers():
    out = {}
    for t in (400, 700, 900):
        out[t] = len(ic.string_network(GENES, threshold=t))
        time.sleep(1.5)
    return out
step('confidence tiers edge counts (400/700/900)', tiers)


def physical_vs_escore():
    phys = requests.get(f'{ic.STRING}/tsv/network', params={'identifiers': '\r'.join(GENES), 'species': 9606, 'required_score': 700,
                                                           'network_type': 'physical', 'caller_identity': ic.CALLER}, timeout=60)
    pdf = pd.read_csv(__import__('io').StringIO(phys.text), sep='\t')
    key = lambda d: {tuple(sorted(x)) for x in zip(d.preferredName_A, d.preferredName_B)}
    esc = df700[df700.escore > 0.4]
    s_phys, s_esc = key(pdf), key(esc)
    return {'physical_network_edges@700': len(s_phys), 'escore>0.4 edges@700 (guide physical proxy)': len(s_esc),
            'in escore not in physical network': sorted(s_esc - s_phys), 'in physical network not escore>0.4': sorted(s_phys - s_esc)}
step('SKILL.md physical proxy (escore>0.4) vs STRING network_type=physical', physical_vs_escore)


def omni_license():
    out = {}
    for lic in ('academic', 'commercial'):
        d = ic.omnipath_interactions(['TP53'], types='post_translational', license=lic)
        out[lic] = (len(d), list(d.columns)[:6])
        time.sleep(1)
    return out
step('omnipath TP53 academic vs commercial', omni_license)


def omni_license2():
    out = {}
    for lic in ('academic', 'commercial'):
        r = requests.get(f'{ic.OMNI}/interactions', params={'partners': 'TP53', 'genesymbols': 1, 'license': lic, 'fields': 'sources'}, timeout=90)
        d = pd.read_csv(__import__('io').StringIO(r.text), sep='\t')
        out[lic] = len(d)
        time.sleep(1)
    out['raw url tail'] = r.url.split('?')[1]
    return out
step('omnipath raw license parameter (all default dataset)', omni_license2)


def omni_edge():
    d = ic.omnipath_interactions(['TP53', 'MDM2'])
    row = d[(d.source_genesymbol == 'MDM2') & (d.target_genesymbol == 'TP53')].iloc[0]
    return {c: row[c] for c in ('source_genesymbol', 'target_genesymbol', 'is_directed', 'is_stimulation', 'is_inhibition', 'n_resources')}
step('omnipath MDM2->TP53 edge fields', omni_edge)


def signor_client():
    d = ic.signor_for_gene('TP53')
    return len(d), list(d.columns)
step('signor_for_gene(TP53) via the client', signor_client)


def signor_raw():
    out = {}
    r = requests.get(ic.SIGNOR, params={'organism': 'human', 'entity': 'TP53'}, timeout=90)
    out['organism=human&entity=TP53'] = (r.status_code, r.text[:80])
    time.sleep(1)
    r = requests.get(ic.SIGNOR, params={'organism': '9606', 'id': 'P04637'}, timeout=90)
    lines = r.text.strip().split('\n')
    out['organism=9606&id=P04637'] = (r.status_code, len(lines), len(lines[0].split('\t')))
    rows = [l.split('\t') for l in lines]
    out['first row cols 0-11'] = rows[0][:12]
    out['tf cols'] = [(i, c) for i, c in enumerate(rows[0]) if c and 'PMID' in c.upper() or (c.isdigit() and len(c) >= 6)][:4]
    out['all rows involve P04637'] = all('P04637' in l for l in lines)
    return out
step('SIGNOR raw behaviours', signor_raw)

step('SIGNOR first row after client-style parse (header skipped)', lambda: 'client drops line 0 as header; the raw response has no header, so one real record is lost per query')
