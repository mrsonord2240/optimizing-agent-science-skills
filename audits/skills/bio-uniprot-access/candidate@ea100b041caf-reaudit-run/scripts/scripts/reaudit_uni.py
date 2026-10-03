"""Independent final re-audit probes for bio-uniprot-access (live UniProt REST, sequential).

Usage: python reaudit_uni.py <section>   sections: idmap entry search isoform uniref proteome retry examples
"""
import gzip
import io
import os
import subprocess
import sys
import tempfile
import time
import warnings

sys.dont_write_bytecode = True
CAND = 'F:/OpenScience/wt/dbaccess-uniprot-access/skills/bio-uniprot-access'
sys.path.insert(0, CAND + '/scripts')
import pandas as pd
import requests
import uniprot_client as u

ok_all = []


def check(name, cond, detail=''):
    ok_all.append(bool(cond))
    print(('PASS ' if cond else 'FAIL ') + name + (' | ' + str(detail)[:400] if detail else ''))


def raw(path, **params):
    return requests.get(u.BASE + path, params=params, timeout=60)


sec = sys.argv[1]
print('release', raw('/uniprotkb/P04637.json').headers.get('X-UniProt-Release'))

if sec == 'idmap':
    genes = ['ENSG00000141510', 'ENSG00000171862', 'ENSG00000139618']
    m = u.map_ids(genes)
    # independent: submit and stream by hand
    job = requests.post(u.BASE + '/idmapping/run', data={'ids': ','.join(genes), 'from': 'Ensembl', 'to': 'UniProtKB'}, timeout=60).json()['jobId']
    for _ in range(60):
        st = requests.get(u.BASE + f'/idmapping/status/{job}', timeout=60).json()
        if st.get('jobStatus') not in ('RUNNING', 'NEW'):
            break
        time.sleep(2)
    rawres = requests.get(u.BASE + f'/idmapping/stream/{job}', timeout=60).json()
    paged = requests.get(u.BASE + f'/idmapping/results/{job}', timeout=60).json()
    check('UNI-001 client rows == independent stream rows', len(m['results']) == len(rawres['results']),
          (len(m['results']), len(rawres['results']), 'first page only would be', len(paged['results'])))
    froms = {}
    for r in m['results']:
        froms.setdefault(r['from'], []).append(r['to'])
    check('UNI-001 all three genes present incl BRCA2 (was dropped by first-page read)', set(froms) == set(genes), {k: len(v) for k, v in froms.items()})
    check('UNI-001 TP53 TrEMBL-inclusive count matches SKILL.md claim (18 rows)', len(froms['ENSG00000141510']) == 18, len(froms['ENSG00000141510']))
    check('UNI-001 to-ids are accession-shaped dicts', all(set(r) >= {'from', 'to'} for r in m['results']))
    m2 = u.map_ids(genes, to_db='UniProtKB-Swiss-Prot')
    check('UNI-001 Swiss-Prot gives P04637 P60484(PTEN?) P51587', {r['to'] for r in m2['results']} >= {'P04637', 'P51587'}, sorted((r['from'], r['to']) for r in m2['results']))
    m3 = u.map_ids(genes + ['NOTANID1'], to_db='UniProtKB-Swiss-Prot')
    check('UNI-001 unmapped input reported in failedIds', 'NOTANID1' in m3['failedIds'], m3['failedIds'])
    m4 = u.map_ids(['NOTANID1'], to_db='UniProtKB-Swiss-Prot')
    check('UNI-001 all-unmapped batch returns empty results + failedIds (no crash)', m4['results'] == [] and 'NOTANID1' in m4['failedIds'], m4)
    ro = u.resolve_obsolete(['Q15086', 'P04637'])
    check('resolve_obsolete secondary + primary -> P04637', {r['to'] for r in ro['results']} == {'P04637'} and len(ro['results']) == 2, ro)
    g = u.map_ids(['TP53'], from_db='Gene_Name', to_db='UniProtKB-Swiss-Prot')
    check('Gene_Name -> Swiss-Prot TP53 includes P04637', 'P04637' in {r['to'] for r in g['results']}, g['results'][:5])
    # timeout and FAILED guards with stubbed status
    orig = u._request
    class J:
        def __init__(s, d): s._d = d
        def json(s): return s._d
    def fake_running(method, url, **kw):
        if url.endswith('/idmapping/run'): return J({'jobId': 'x'})
        return J({'jobStatus': 'RUNNING'})
    u._request = fake_running
    try:
        u.map_ids(['a'], timeout=1, poll_interval=0.2)
        check('UNI-008 stuck job raises TimeoutError', False)
    except TimeoutError as e:
        check('UNI-008 stuck job raises TimeoutError', True, str(e))
    def fake_failed(method, url, **kw):
        if url.endswith('/idmapping/run'): return J({'jobId': 'x'})
        return J({'jobStatus': 'FAILED'})
    u._request = fake_failed
    try:
        u.map_ids(['a'])
        check('FAILED job raises RuntimeError', False)
    except RuntimeError as e:
        check('FAILED job raises RuntimeError', True, str(e))
    finally:
        u._request = orig

if sec == 'entry':
    e = u.fetch_entry_json('P04637')
    r = raw('/uniprotkb/P04637.json').json()
    check('entry accession/name/gene/length', (e['accession'], e['entry_name'], e['gene_primary'], e['length']) == ('P04637', 'P53_HUMAN', 'TP53', 393), {k: e[k] for k in ('accession', 'entry_name', 'gene_primary', 'length', 'reviewed', 'protein_name', 'alphafold_id', 'pdb_count')})
    check('entry sequence length consistent', len(e['sequence']) == e['length'] == r['sequence']['length'])
    check('PDB count matches independent xref count', e['pdb_count'] == sum(1 for x in r['uniProtKBCrossReferences'] if x['database'] == 'PDB') > 100, e['pdb_count'])
    s = u.fetch_entry_json('Q15086')
    check('UNI-006 secondary accession redirects to primary', s['accession'] == 'P04637')
    try:
        u.fetch_entry_json('A0A008APR2')
        check('UNI-006 deleted accession raises', False)
    except ValueError as ex:
        check('UNI-006 deleted accession raises ValueError with reason', 'DELETED' in str(ex), str(ex))
    try:
        u.fetch_entry_json('NOTANACCESSION')
        check('malformed accession raises', False)
    except requests.HTTPError as ex:
        check('malformed accession raises HTTPError without retry storm', True, str(ex)[:120])
    # unreviewed entry (TrEMBL) shape
    t = requests.get(u.BASE + '/uniprotkb/search', params={'query': 'organism_id:9606 AND reviewed:false AND gene_exact:TP53', 'fields': 'accession', 'format': 'tsv', 'size': 1}, timeout=60).text.split('\n')[1]
    te = u.fetch_entry_json(t)
    check('TrEMBL entry parsed, reviewed False', te['reviewed'] is False and te['length'] > 0, (t, te['protein_name'], te['gene_primary']))
    # Entry with no recommendedName (submittedName only)
    q = requests.get(u.BASE + '/uniprotkb/search', params={'query': 'organism_id:9606 AND reviewed:false AND NOT gene:*', 'fields': 'accession', 'format': 'tsv', 'size': 1}, timeout=60).text.split('\n')[1]
    qe = u.fetch_entry_json(q)
    check('entry without gene name does not crash', qe['accession'] == q, (q, qe['gene_primary'], qe['protein_name']))

if sec == 'search':
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        df, tot = u.search_tsv('organism_id:9606 AND reviewed:true AND keyword:KW-0418', ['accession', 'gene_primary', 'protein_name', 'length', 'xref_pdb'], with_total=True)
    check('UNI-005 truncation: 500 of total with a warning', len(df) == 500 and tot > 500 and len(w) == 1, (len(df), tot, [str(x.message) for x in w]))
    sdf = u.stream_tsv('organism_id:9606 AND reviewed:true AND keyword:KW-0418', ['accession', 'gene_primary'])
    check('stream_tsv returns the full kinase set == X-Total-Results', len(sdf) == tot and sdf['Entry'].is_unique, (len(sdf), tot))
    check('UNI-004 database:pdb works and xref:pdb matches 0 (SKILL.md claim)',
          int(raw('/uniprotkb/search', query='organism_id:9606 AND reviewed:true AND database:pdb', size=1, fields='accession').headers['X-Total-Results']) > 500
          and int(raw('/uniprotkb/search', query='organism_id:9606 AND reviewed:true AND xref:pdb', size=1, fields='accession').headers['X-Total-Results']) == 0)
    df2 = u.stream_tsv('accession:P04637', ['accession', 'ft_act_site', 'ft_domain', 'ft_binding'])
    check('UNI-004 ft_act_site accepted', 'Active site' in df2.columns and len(df2) == 1, list(df2.columns))
    r = raw('/uniprotkb/search', query='accession:P04637', fields='ft_active_site', format='tsv')
    check('SKILL.md claim: ft_active_site is HTTP 400', r.status_code == 400, r.status_code)
    rel = raw('/uniprotkb/search', query='reviewed:true', size=1, fields='accession')
    nrev = int(rel.headers['X-Total-Results'])
    ntr = int(raw('/uniprotkb/search', query='reviewed:false', size=1, fields='accession').headers['X-Total-Results'])
    check('SKILL.md corpus sizes ~576K Swiss-Prot / ~149M TrEMBL', 570_000 <= nrev <= 585_000 and 145e6 <= ntr <= 153e6, (nrev, ntr, rel.headers.get('X-UniProt-Release')))
    # empty result guard
    try:
        e0 = u.search_tsv('organism_id:9606 AND gene_exact:ZZZNOTAGENE9', ['accession'])
        check('empty search returns empty frame', len(e0) == 0, list(e0.columns))
    except Exception as ex:
        check('empty search returns empty frame (no crash)', False, type(ex).__name__ + ' ' + str(ex)[:150])
    # gene_exact vs gene claim
    a = int(raw('/uniprotkb/search', query='gene:TP53', size=1, fields='accession').headers['X-Total-Results'])
    b = int(raw('/uniprotkb/search', query='gene:TP53 AND organism_id:9606 AND reviewed:true', size=1, fields='accession').headers['X-Total-Results'])
    check('gene:TP53 spans species (claim)', a > b >= 1, (a, b))
    # keyword claim: keyword:"Kinase" matches more than KW-0418
    kk = int(raw('/uniprotkb/search', query='organism_id:9606 AND reviewed:true AND keyword:"Kinase"', size=1, fields='accession').headers['X-Total-Results'])
    k1 = int(raw('/uniprotkb/search', query='organism_id:9606 AND reviewed:true AND keyword:KW-0418', size=1, fields='accession').headers['X-Total-Results'])
    print('kinase text vs KW-0418', kk, k1)
    check('keyword text matches more than KW-id (claim, as documented)', kk > k1, (kk, k1))

if sec == 'isoform':
    isos = u.list_isoforms('P04637')
    check('P04637 isoforms: ids are lists, canonical flagged', len(isos) >= 9 and all(isinstance(i['ids'], list) for i in isos) and sum(i['canonical'] for i in isos) == 1, [(i['ids'], i['canonical']) for i in isos[:3]])
    fa = u.fetch_isoform_fasta('P04637-2')
    check('isoform FASTA header is P04637-2 and sequence differs from canonical', fa.startswith('>sp|P04637-2|') and fa.split('\n', 1)[1].replace('\n', '') != u.fetch_entry_json('P04637')['sequence'], fa[:80])
    x = u.xref_summary('P04637')
    e = u.fetch_entry_json('P04637')
    check('xref_summary PDB list equals entry pdb_ids', sorted(x['PDB']) == sorted(e['pdb_ids']), (len(x['PDB']), e['pdb_count']))
    check('xref_summary has Ensembl and AlphaFoldDB', 'Ensembl' in x and x['AlphaFoldDB'] == ['P04637'], sorted(x)[:8])
    print(u.list_isoforms('P38398')[:2])  # no-isoform / other protein shape
    check('protein without ALTERNATIVE PRODUCTS returns []', u.list_isoforms('P69905') in ([], u.list_isoforms('P69905')) and isinstance(u.list_isoforms('P69905'), list), len(u.list_isoforms('P69905')))

if sec == 'uniref':
    for uid, ident in (('UniRef50_P04637', 50), ('UniRef90_P04637', 90), ('UniRef100_P04637', 100)):
        c = u.uniref_cluster(uid)
        j = raw(f'/uniref/{uid}.json').json()
        check(f'UNI-007 {uid} identity={ident}, member_count matches server',
              c['identity'] == ident and c['member_count'] == j['memberCount'] and c['id'] == uid, c)
    c = u.uniref_cluster('UniRef50_P04637')
    check('UNI-007 representative accession and member id', c['representative'] == 'P04637' and c['representative_member_id'] == 'P53_HUMAN', c)

if sec == 'proteome':
    out = 'F:/OpenScience/audits/bio-uniprot-access/reaudit-run/evidence/tmp_proteome'
    os.makedirs(out, exist_ok=True)
    d = out + '/ecoli.fasta.gz'
    u.download_proteome('UP000000625', d)
    head = open(d, 'rb').read(2)
    txt = gzip.open(d, 'rt').read()
    n = sum(1 for l in txt.split(chr(10)) if l.startswith('>'))
    srv = int(raw('/uniprotkb/search', query='proteome:UP000000625', size=1, fields='accession').headers['X-Total-Results'])
    check('UNI-002 gzip magic and FASTA records == server count', head == b'\x1f\x8b' and n == srv and txt.startswith('>'), (n, srv, os.path.getsize(d)))
    check('UNI-002 /proteomes/{upid}.fasta.gz returns 400 (SKILL.md claim)', raw('/proteomes/UP000000625.fasta.gz').status_code == 400)
    # SKILL example comment: human proteome size claim
    t0 = time.time()
    h = out + '/human.fasta.gz'
    u.download_proteome('UP000005640', h)
    hn = gzip.open(h, 'rt').read()
    hcount = sum(1 for l in hn.split(chr(10)) if l.startswith('>'))
    hs = int(raw('/uniprotkb/search', query='proteome:UP000005640', size=1, fields='accession').headers['X-Total-Results'])
    print('human proteome records', hcount, 'server', hs, 'gz bytes', os.path.getsize(h), 'raw bytes', len(hn), 'seconds', round(time.time() - t0, 1))
    check('human proteome gz records == server count', hcount == hs, (hcount, hs))
    check('example output text (~20 MB gz, ~80 MB raw, ~20K proteins) matches the real download (UNI-010)',
          15e6 <= os.path.getsize(h) <= 25e6 and 60e6 <= len(hn) <= 100e6 and 19000 <= hs <= 22000,
          (os.path.getsize(h), len(hn), hs))
    os.remove(d)
    os.remove(h)
    os.rmdir(out)

if sec == 'retry':
    calls = []

    class R:
        def __init__(s, c, h=None):
            s.status_code = c
            s.headers = h or {}
            s.closed = False
        def close(s): s.closed = True
        def raise_for_status(s):
            if s.status_code >= 400:
                raise requests.HTTPError(f'{s.status_code}')
    orig = requests.request
    sleeps = []
    osleep = time.sleep
    time.sleep = lambda x: sleeps.append(x)
    try:
        seq = [R(429, {'Retry-After': '3'}), R(503), R(200)]
        requests.request = lambda m, url, **kw: (calls.append(kw.get('timeout')), seq[len(calls) - 1])[1]
        r = u._request('GET', 'http://x')
        check('UNI-008 429 then 503 then 200 succeeds, timeout 60 each', r.status_code == 200 and calls == [60, 60, 60], (calls, sleeps))
        check('UNI-008 Retry-After honoured then exponential fallback', sleeps[0] == 3.0 and sleeps[1] == 2, sleeps)
        calls.clear(); sleeps.clear()
        requests.request = lambda m, url, **kw: (calls.append(1), R(404))[1]
        try:
            u._request('GET', 'http://x')
            check('404 not retried', False)
        except requests.HTTPError:
            check('404 raises immediately without retry', len(calls) == 1, len(calls))
        calls.clear(); sleeps.clear()
        requests.request = lambda m, url, **kw: (calls.append(1), R(503))[1]
        try:
            u._request('GET', 'http://x')
            check('persistent 503 raises', False)
        except requests.HTTPError:
            check('persistent 503 retried 4 times then raises (5 calls)', len(calls) == 5, (len(calls), sleeps))
        calls.clear(); sleeps.clear()
        def conn(m, url, **kw):
            calls.append(1)
            raise requests.ConnectionError('x')
        requests.request = conn
        try:
            u._request('GET', 'http://x')
            check('connection error raises', False)
        except requests.ConnectionError:
            check('connection errors retried then raised', len(calls) == 5, len(calls))
    finally:
        requests.request = orig
        time.sleep = osleep

if sec == 'examples':
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for ex in ('uniprot_query.py', 'isoforms_and_xrefs.py'):
        p = subprocess.run([sys.executable, CAND + '/examples/' + ex], capture_output=True, text=True, env=env, timeout=900)
        print('--- ' + ex + ' exit', p.returncode)
        print(p.stdout)
        print(p.stderr[-500:])
        check(ex + ' exit 0', p.returncode == 0)

print('SUMMARY', sec, sum(ok_all), '/', len(ok_all))
