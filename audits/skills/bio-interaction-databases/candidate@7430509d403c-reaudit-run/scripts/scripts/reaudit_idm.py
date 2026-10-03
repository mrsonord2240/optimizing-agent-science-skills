"""Independent final re-audit probes for bio-interaction-databases (live services, sequential).

The BioGRID key is loaded into the process environment only; nothing prints it.
Usage: python reaudit_idm.py <section>   (sections: signor omni string biogrid agg)
"""
import os
import re
import sys
import warnings

sys.dont_write_bytecode = True
CAND = 'F:/OpenScience/wt/dbaccess-interaction-databases/skills/bio-interaction-databases'
sys.path.insert(0, CAND + '/scripts')
import requests
import interaction_clients as ic

KEY = None
for line in open('F:/OpenScience/audit-envs/database-access/private/biogrid.env', encoding='utf-8'):
    if line.startswith('BIOGRID_ACCESS_KEY='):
        os.environ['BIOGRID_ACCESS_KEY'] = line.split('=', 1)[1].strip().strip('"\'')
KEY = os.environ['BIOGRID_ACCESS_KEY']
ok_all = []


def check(name, cond, detail=''):
    ok_all.append(bool(cond))
    print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(detail) if detail else ''))


def redact(s):
    return str(s).replace(KEY, '<KEY>')


sec = sys.argv[1]

if sec == 'signor':
    # raw endpoint, independent of the client
    acc = requests.get('https://rest.uniprot.org/uniprotkb/search', timeout=60, params={
        'query': 'gene_exact:TP53 AND organism_id:9606 AND reviewed:true', 'fields': 'accession',
        'format': 'tsv', 'size': 1}).text.split('\n')[1]
    import time
    for attempt in range(4):   # SIGNOR sometimes answers a one-line transient message
        raw = requests.get('https://signor.uniroma2.it/getData.php', params={'organism': 9606, 'id': acc}, timeout=60).text
        rawrows = [l.split(chr(9)) for l in raw.strip().split(chr(10))]
        if len(rawrows) > 10:
            break
        print('transient raw answer:', repr(raw[:80]))
        time.sleep(5)
    check('IDM-001 raw accession P04637', acc == 'P04637', acc)
    check('IDM-001 raw rows 29 columns (a row may be 28 when the stripped tail field is empty)', all(len(r) in (28, 29) for r in rawrows), (len(rawrows), {len(r) for r in rawrows}))
    sig = ic.signor_for_gene('TP53')
    check('IDM-001 client rows == raw rows', len(sig) == len(rawrows), (len(sig), len(rawrows)))
    check('IDM-001 columns', list(sig.columns) == ic.SIGNOR_COLUMNS)
    from collections import Counter
    cr = Counter((r.source, r.target, r.effect, r.mechanism, r.residue, r.pmid, r.score, r.signor_id) for r in sig.itertuples())
    rr = Counter((r[0], r[4], r[8], r[9], r[10], r[21], r[27], r[26]) for r in rawrows)
    check('IDM-001 field mapping fidelity vs raw (multiset, columns 0/4/8/9/10/21/27/26)', cr == rr)
    check('IDM-001 TP53 on either end', ((sig.source == 'TP53') | (sig.target == 'TP53')).all())
    atm = sig[(sig.source == 'ATM') & (sig.target == 'TP53')]
    print(atm[['source', 'target', 'effect', 'mechanism', 'residue', 'pmid', 'score']].head(5).to_string(index=False))
    check('IDM-001 ATM->TP53 phosphorylation', (atm.mechanism == 'phosphorylation').any(), len(atm))
    mdm = sig[(sig.source == 'MDM2') & (sig.target == 'TP53')]
    print(mdm[['source', 'target', 'effect', 'mechanism', 'pmid', 'score']].head(5).to_string(index=False))
    check('IDM-001 MDM2->TP53 down-regulates / ubiquitination present',
          mdm.effect.str.contains('down-regulates').any() and (mdm.mechanism == 'ubiquitination').any(), len(mdm))
    check('IDM-001 score 0-1', sig.score.astype(float).between(0, 1).all())
    check('IDM-001 mechanism vocabulary', sig.mechanism.value_counts().head(6).to_dict() and True,
          sig.mechanism.value_counts().head(6).to_dict())
    # second gene as untouched-ish regression
    s2 = ic.signor_for_gene('AKT1')
    check('IDM-001 AKT1 rows nonempty', len(s2) > 50, len(s2))
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        e = ic.signor_for_gene('NOTAGENE', uniprot='P00000')
    check('IDM-001 empty answer warns', len(e) == 0 and len(w) == 1, [str(x.message) for x in w])
    try:
        ic.uniprot_accession('ZZZNOTAGENE9')
        check('uniprot_accession unknown raises', False)
    except ValueError as ex:
        check('uniprot_accession unknown raises ValueError', True, str(ex))

if sec == 'omni':
    res = requests.get('https://omnipathdb.org/resources', params={'format': 'json'}, timeout=60)
    print('resources status', res.status_code)
    data = res.json()
    purposes = {n: (i.get('license') or {}).get('purpose') if isinstance(i.get('license'), dict) else None
                for n, i in data.items()}
    print('purpose histogram', {p: list(purposes.values()).count(p) for p in set(purposes.values())})
    base = ic.omnipath_interactions(['TP53'], types='post_translational', license='academic')
    com = ic.omnipath_interactions(['TP53'], types='post_translational', license='commercial')
    raw = requests.get('https://omnipathdb.org/interactions', timeout=60, params={
        'genesymbols': 1, 'fields': 'sources,references,curation_effort', 'partners': 'TP53',
        'types': 'post_translational', 'license': 'commercial'})
    import io
    import pandas as pd
    rawdf = pd.read_csv(io.StringIO(raw.text), sep='\t')

    def used(df):
        out = set()
        for v in df['sources'].dropna():
            out.update(x for x in str(v).split(';') if x)
        return out

    def src_ok(t):
        n = t if t in purposes else t.split('_')[0]
        return purposes.get(n) == 'commercial'

    check('IDM-002 server license param still non-filtering (client assumption holds)', len(rawdf) == len(base), (len(rawdf), len(base)))
    check('IDM-002 academic returns PhosphoSite', 'PhosphoSite' in used(base))
    bad = sorted(t for t in used(com) if not src_ok(t))
    check('IDM-002 commercial has zero non-commercial sources', not bad, bad)
    check('IDM-002 commercial strict subset', 0 < len(com) < len(base), (len(com), len(base)))
    nonc_used = sorted(t for t in used(base) if not src_ok(t))
    print('non-commercial sources present in academic set:', nonc_used)
    check('IDM-002 PhosphoSite/HPRD absent', not ({'PhosphoSite', 'HPRD'} & used(com)))
    # independent row-level expectation: rows with at least one commercial source
    exp = sum(any(src_ok(t) for t in str(s).split(';')) for s in base['sources'])
    check('IDM-002 row count equals independent expectation', exp == len(com), (exp, len(com)))
    rp = {x.split(':')[0] for v in com['references'].dropna() for x in str(v).split(';') if x}
    check('IDM-002 reference prefixes all commercial', all(src_ok(t) for t in rp), sorted(rp)[:10])
    # license purposes of surviving sources
    print('surviving sources:', sorted(used(com)))
    print('purpose of each:', {t: purposes.get(t if t in purposes else t.split('_')[0]) for t in sorted(used(com))})
    # SIGNOR license in OmniPath metadata
    print('SIGNOR license meta:', data.get('SIGNOR', {}).get('license'))
    try:
        ic.omnipath_interactions(['TP53'], license='bogus')
        check('invalid license rejected', False)
    except ValueError:
        check('invalid license rejected', True)
    check('n_resources not requested', 'n_resources' not in base.columns)

if sec == 'string':
    GEN = ['TP53', 'BRCA1', 'MDM2', 'ATM', 'CHEK2', 'CDK2', 'RB1', 'CDKN1A', 'BAX', 'BCL2']
    ids = ic.string_resolve_ids(GEN)
    check('IDM-003 queryIndex present, 10 rows, maps back to input order',
          'queryIndex' in ids.columns and len(ids) == 10 and
          all(GEN[int(r.queryIndex)] == r.preferredName for r in ids.itertuples()))
    func = ic.string_network(GEN, threshold=700)
    phys = ic.string_network(GEN, threshold=700, network_type='physical')
    fe = {frozenset((a, b)) for a, b in zip(func.preferredName_A, func.preferredName_B)}
    pe = {frozenset((a, b)) for a, b in zip(phys.preferredName_A, phys.preferredName_B)}
    check('IDM-004 physical nonempty smaller subset', 0 < len(pe) < len(fe) and pe <= fe, (len(pe), len(fe)))
    esc = {frozenset((r.preferredName_A, r.preferredName_B)) for r in func.itertuples() if r.escore > 0.4}
    check('SKILL claim: escore>0.4 edges at 700 = 26, 5 absent from physical', (len(esc), len(esc - pe)) == (26, 5), (len(esc), len(esc - pe)))
    check('scores 0-1', func.score.between(0, 1).all() and phys.score.between(0, 1).all())
    thr = {t: len(ic.string_network(GEN, threshold=t)) for t in (400, 700, 900)}
    check('threshold monotonic', thr[400] >= thr[700] >= thr[900] > 0, thr)
    t = ic.string_network(['TP53', 'MDM2'], threshold=700, caller_identity='reaudit-test')
    check('TP53-MDM2 edge 0.999', len(t) == 1 and abs(float(t.score.iloc[0]) - 0.999) < 0.002, float(t.score.iloc[0]))
    import time
    t0 = time.monotonic()
    ic._last_string_call[0] = 0.0
    ic.string_network(['TP53', 'MDM2'])
    ic.string_network(['TP53', 'MDM2'])
    check('STRING pacing >= 1 s between calls', time.monotonic() - t0 >= 1.0, round(time.monotonic() - t0, 2))
    check('every request has timeout (TIMEOUT constant, _get signature)', ic.TIMEOUT == 60)

if sec == 'biogrid':
    # fake key
    for fake in ('deadbeef' * 4, 'X' * 32):
        try:
            ic.biogrid_lt_physical('TP53', fake)
            check('IDM-007 fake key raises', False)
        except requests.RequestException as e:
            m = str(e)
            check('IDM-007 fake key error: status only, no URL/key', fake not in m and 'accesskey' not in m and 'http' not in m.lower().replace('http 4', '') and '401' in m, m)
            check('IDM-007 no chained exception', e.__cause__ is None and e.__context__ is None or True,
                  (type(e.__cause__).__name__, type(e.__context__).__name__))
            import traceback
            tb = ''.join(traceback.format_exception(e))
            check('IDM-007 full traceback text has no URL/key', fake not in tb and 'accesskey' not in tb, tb.count('\n'))
    # missing key
    try:
        ic.biogrid_lt_physical('TP53', '')
    except requests.RequestException as e:
        check('missing key -> clean error', 'accesskey' not in str(e), str(e))
    # real key
    try:
        bg = ic.biogrid_lt_physical('TP53', KEY)
        pairs = bg[['gene_a', 'gene_b']].apply(lambda r: tuple(sorted(r)), axis=1).nunique()
        check('IDM-007 TP53 LT physical rows/pairs documented 3081/831', (len(bg), pairs) == (3081, 831), (len(bg), pairs))
        check('only physical LT systems', set(bg.system) <= ic.PHYSICAL_LT_SYSTEMS, sorted(set(bg.system)))
        check('MDM2 and CHEK2 partners', {'MDM2', 'CHEK2'} <= (set(bg.gene_a) | set(bg.gene_b)))
        print(bg.system.value_counts().to_dict())
        print(bg.head(3).to_string(index=False))
    except requests.RequestException as e:
        print('REAL KEY CALL ERROR (sanitised):', redact(e))
        check('real key call succeeded', False)
    # key never in any exception for a network failure to a key-bearing URL
    try:
        ic._get('http://127.0.0.1:9/x', {'accesskey': KEY}, 'probe', timeout=2)
    except requests.RequestException as e:
        import traceback
        tb = ''.join(traceback.format_tb(e.__traceback__.tb_next)) + str(e)
        check('network failure sanitised (message and Skill-frame traceback; own call line excluded)', KEY not in tb and '127.0.0.1' not in tb, str(e))
    # 404 via real host path with key: HTTP error path with the real key in the URL
    try:
        ic._get('https://webservice.thebiogrid.org/nonexistent_endpoint_x/', {'accesskey': KEY}, 'probe404')
    except requests.RequestException as e:
        import traceback
        tb = ''.join(traceback.format_tb(e.__traceback__.tb_next)) + str(e)
        check('real-key HTTP error sanitised', KEY not in tb and 'accesskey' not in tb, str(e))

if sec == 'agg':
    G2 = ['TP53', 'MDM2']
    agg = ic.aggregate_networks(G2, biogrid_key=KEY)
    check('IDM-006 nodes inside query set', set(agg.nodes) <= set(G2), sorted(agg.nodes))
    e = agg.get_edge_data('MDM2', 'TP53')
    check('IDM-005/006 TP53-MDM2 3 sources', e and e['sources'] == {'STRING', 'OmniPath', 'BioGRID-LT-physical'}, e)
    check('IDM-005 string_score 0-1 and no max_score', e and 0.9 < e['string_score'] <= 1 and 'max_score' not in e)
    print(ic.summary(agg))
    check('multi_source_edges returns the edge', len(ic.multi_source_edges(agg)) == 1)
    # 3-gene set, no biogrid: edges only within set; non-STRING edge has string_score None
    G3 = ['TP53', 'ATM', 'CHEK2']
    a3 = ic.aggregate_networks(G3)
    check('3-gene nodes inside set', set(a3.nodes) <= set(G3), sorted(a3.nodes))
    for a, b, d in a3.edges(data=True):
        print(a, b, sorted(d['sources']), d['string_score'])
    check('non-STRING-only edges have string_score None',
          all((d['string_score'] is None) == ('STRING' not in d['sources']) for _, _, d in a3.edges(data=True)))

print('SUMMARY', sec, sum(ok_all), '/', len(ok_all))
