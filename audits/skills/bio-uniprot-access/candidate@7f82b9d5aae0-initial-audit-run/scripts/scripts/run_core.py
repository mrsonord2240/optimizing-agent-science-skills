"""Core workflow probes for bio-uniprot-access (live UniProt REST, release 2026_03). Sequential, small queries."""
import os
import sys
import time

sys.dont_write_bytecode = True
CAND = r'F:\OpenScience\wt\dbaccess-uniprot-access\skills\bio-uniprot-access'
sys.path.insert(0, os.path.join(CAND, 'scripts'))
import requests
import uniprot_client as uc

B = uc.BASE


def step(name, fn):
    print(f'--- {name}')
    try:
        print(fn())
    except Exception as e:  # noqa
        print(f'EXC {type(e).__name__}: {str(e)[:250]}')
    time.sleep(0.4)


def total(query):
    r = requests.get(f'{B}/uniprotkb/search', params={'query': query, 'size': 1, 'fields': 'accession'}, timeout=60)
    return int(r.headers.get('X-Total-Results', -1)), r.headers.get('X-UniProt-Release')


step('release + Swiss-Prot / TrEMBL totals', lambda: {'reviewed': total('reviewed:true'), 'unreviewed': total('reviewed:false')})


def entry():
    e = uc.fetch_entry_json('P04637')
    return {k: (v if k not in ('sequence', 'pdb_ids') else (v[:12] if k == 'sequence' else v[:5])) for k, v in e.items()}
step('fetch_entry_json P04637', entry)


def entry_tr():
    # an unreviewed (TrEMBL) entry: protein_name path uses recommendedName only
    r = requests.get(f'{B}/uniprotkb/search', params={'query': 'organism_id:9606 AND reviewed:false AND existence:1', 'size': 1, 'fields': 'accession'}, timeout=60,
                     headers={'Accept': 'application/json'})
    acc = r.json()['results'][0]['primaryAccession']
    e = uc.fetch_entry_json(acc)
    j = requests.get(f'{B}/uniprotkb/{acc}.json', timeout=60).json()
    return {'acc': acc, 'reviewed': e['reviewed'], 'protein_name': e['protein_name'], 'has_submissionNames': 'submissionNames' in j.get('proteinDescription', {}),
            'gene_primary': e['gene_primary']}
step('fetch_entry_json on an unreviewed entry', entry_tr)


def secondary():
    e = uc.fetch_entry_json('Q15086')   # secondary accession of P04637
    return e['accession'], e['gene_primary']
step('fetch_entry_json on a secondary accession (Q15086)', secondary)


def inactive():
    r = requests.get(f'{B}/uniprotkb/search', params={'query': 'active:false', 'size': 1, 'fields': 'accession'}, timeout=60)
    return r.status_code, r.text[:200]
step('is there a way to list inactive entries', inactive)


def kinases():
    q = 'organism_id:9606 AND reviewed:true AND keyword:"Kinase"'
    df = uc.search_tsv(q, ['accession', 'gene_primary', 'protein_name', 'length', 'xref_pdb'], size=500)
    t = total(q)
    kw = total('organism_id:9606 AND reviewed:true AND keyword:KW-0418')
    return {'search_tsv rows': len(df), 'server total for the same query': t, 'KW-0418 total': kw, 'columns': list(df.columns), 'head': df.head(2).to_dict('records')}
step('search_tsv kinases (documented quickstart + shipped example)', kinases)


def stream():
    df = uc.stream_tsv('organism_id:9606 AND reviewed:true', ['accession', 'gene_primary', 'length'])
    return {'rows': len(df), 'server total': total('organism_id:9606 AND reviewed:true'), 'P04637 present': 'P04637' in set(df['Entry']), 'dup accessions': int(df['Entry'].duplicated().sum())}
step('stream_tsv human Swiss-Prot', stream)


def mapping():
    ids = ['ENSG00000141510', 'ENSG00000171862', 'ENSG00000139618']
    m = uc.map_ids(ids)
    frm = [r['from'] for r in m.get('results', [])]
    from collections import Counter
    c = Counter(frm)
    # independent route: the stream endpoint returns the full result set
    sub = requests.post(f'{B}/idmapping/run', data={'ids': ','.join(ids), 'from': 'Ensembl', 'to': 'UniProtKB'}, timeout=60).json()['jobId']
    for _ in range(40):
        st = requests.get(f'{B}/idmapping/status/{sub}', timeout=60, allow_redirects=False)
        if st.status_code in (200, 303) and st.json().get('jobStatus', 'FINISHED') != 'RUNNING':
            break
        time.sleep(2)
    s = requests.get(f'{B}/idmapping/stream/{sub}', timeout=120).json()
    sc = Counter(r['from'] for r in s['results'])
    res = requests.get(f'{B}/idmapping/results/{sub}', timeout=60)
    return {'client rows': len(m['results']), 'client per-id counts': dict(c), 'client failedIds': m.get('failedIds'),
            'stream rows': len(s['results']), 'stream per-id counts': dict(sc), 'X-Total-Results (results endpoint)': res.headers.get('X-Total-Results'),
            'Link header present (next page)': 'next' in (res.headers.get('Link') or ''),
            'ids with zero rows in client output': [i for i in ids if i not in c]}
step('map_ids Ensembl gene -> UniProtKB (shipped example input) vs idmapping/stream', mapping)


def obsolete():
    m = uc.resolve_obsolete(['Q15086', 'P04637'])
    return [(r['from'], r['to'] if isinstance(r['to'], str) else r['to'].get('primaryAccession')) for r in m.get('results', [])], m.get('failedIds')
step('resolve_obsolete (secondary accession Q15086 and current P04637)', obsolete)


def bad_map():
    try:
        uc.map_ids(['P04637'], from_db='NotADatabase', to_db='UniProtKB')
        return 'no error'
    except Exception as e:  # noqa
        return f'{type(e).__name__}: {str(e)[:160]}'
step('map_ids invalid from_db', bad_map)


def isoforms():
    isos = uc.list_isoforms('P04637')
    out = {'n': len(isos), 'canonical': [i['ids'] for i in isos if i['canonical']], 'ids': [i['ids'] for i in isos], 'ids type': type(isos[0]['ids']).__name__}
    lens = {}
    for i in isos:
        for iid in i['ids']:
            fa = uc.fetch_isoform_fasta(iid)
            lens[iid] = len(''.join(fa.split('\n')[1:]))
            time.sleep(0.15)
    out['fasta lengths'] = lens
    return out
step('list_isoforms + fetch_isoform_fasta for every P04637 isoform', isoforms)


def xrefs():
    x = uc.xref_summary('P04637')
    df = uc.search_tsv('accession:P04637', ['xref_pdb'])
    pdb_tsv = len([t for t in str(df.iloc[0, 0]).split(';') if t])
    return {'n_dbs': len(x), 'PDB': len(x.get('PDB', [])), 'Ensembl': len(x.get('Ensembl', [])), 'xref_pdb TSV count': pdb_tsv}
step('xref_summary vs xref_pdb field', xrefs)


def uniref():
    c = uc.uniref_cluster('UniRef50_P04637')
    j = requests.get(f'{B}/uniref/UniRef50_P04637.json', timeout=60).json()
    return {'client': c, 'identity field in JSON': j.get('identity'), 'entryType': j.get('entryType'),
            'representative accessions': j['representativeMember'].get('accessions'), 'memberIdType': j['representativeMember'].get('memberIdType')}
step('uniref_cluster', uniref)


def proteome():
    r = requests.get(f'{B}/proteomes/UP000000625.fasta.gz', stream=True, timeout=60)
    status, body = r.status_code, r.text[:150] if r.status_code != 200 else ''
    r.close()
    try:
        uc.download_proteome('UP000000625', os.devnull)
        client = 'no error'
    except Exception as e:  # noqa
        client = f'{type(e).__name__}: {str(e)[:120]}'
    time.sleep(0.4)
    s = requests.get(f'{B}/uniprotkb/stream', params={'query': 'proteome:UP000000625', 'format': 'fasta', 'compressed': 'true'}, stream=True, timeout=120)
    head = next(s.iter_content(64))
    s.close()
    return {'documented route status': status, 'documented body': body, 'client': client, 'stream route status': s.status_code, 'stream gzip magic': head[:2].hex()}
step('download_proteome documented route versus the stream route', proteome)
