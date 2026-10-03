"""Independent re-audit assertions for bio-ortholog-inference (live Compara, OrthoDB, OMA, KEGG, PANTHER; local HTTP stub for retry logic)."""
import http.server
import sys
import threading
import time

import requests

sys.dont_write_bytecode = True
CAND = 'F:/OpenScience/wt/dbaccess-ortholog-inference/skills/bio-ortholog-inference'
sys.path.insert(0, CAND + '/scripts')
import ortholog_clients as oc  # noqa: E402


def check(label, fn, expect=None):
    t0 = time.time()
    try:
        r = fn()
        ok = True if expect is None else bool(expect(r))
        print(f'[{"PASS" if ok else "FAIL"}] {label}: {str(r)[:220]}  ({time.time()-t0:.1f}s)', flush=True)
    except Exception as e:
        print(f'[EXC ] {label}: {type(e).__name__}: {str(e)[:260]}  ({time.time()-t0:.1f}s)', flush=True)
    time.sleep(0.5)


# ---- local stub server: retry logic (OI-02) ----
class H(http.server.BaseHTTPRequestHandler):
    hits = {}

    def log_message(self, *a):
        pass

    def do_GET(self):
        n = H.hits[self.path] = H.hits.get(self.path, 0) + 1
        if self.path.startswith('/flaky503'):
            code = 503 if n < 3 else 200
        elif self.path.startswith('/always500'):
            code = 500
        elif self.path.startswith('/rate'):
            code = 429 if n < 2 else 200
        elif self.path.startswith('/gone'):
            code = 404
        else:
            code = 200
        self.send_response(code)
        if code == 429:
            self.send_header('Retry-After', '1')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"ok": true}')


srv = http.server.HTTPServer(('127.0.0.1', 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{srv.server_port}'
REAL_SLEEP = time.sleep
oc.time.sleep = lambda s: None   # keep stub tests quick (global time.sleep, restored below)
check('OI-02 retry 503,503 then 200', lambda: (oc.get_with_retry(base + '/flaky503').status_code, H.hits['/flaky503']),
      lambda r: r == (200, 3))
check('OI-02 429 with Retry-After then 200', lambda: (oc.get_with_retry(base + '/rate').status_code, H.hits['/rate']),
      lambda r: r == (200, 2))
check('OI-02 persistent 500 raises RequestException after max_retries', lambda: oc.get_with_retry(base + '/always500'), lambda r: False)
print('       always500 hits:', H.hits.get('/always500'), flush=True)
check('OI-02 404 raises HTTPError; allow_404 returns', lambda: oc.get_with_retry(base + '/gone', allow_404=True).status_code, lambda r: r == 404)
try:
    oc.get_with_retry(base + '/gone')
    print('[FAIL] 404 without allow_404 did not raise', flush=True)
except requests.HTTPError as e:
    print('[PASS] 404 without allow_404 raises HTTPError:', str(e)[:80], flush=True)
srv.shutdown()
check('OI-02 unreachable host raises RequestException', lambda: oc.get_with_retry('http://127.0.0.1:9/x', max_retries=2), lambda r: False)

oc.time.sleep = REAL_SLEEP

# ---- Compara ----
check('Compara resolve TP53', lambda: oc.resolve_symbol('human', 'TP53'), lambda r: r == 'ENSG00000141510')
check('OI-03 TP53 human->mouse row schema', lambda: oc.compara_orthologs('human', 'TP53', 'mouse'),
      lambda r: len(r) == 1 and r[0]['target_id'] == 'ENSMUSG00000059552' and r[0]['type'] == 'ortholog_one2one'
      and r[0]['taxonomy_level'] and r[0]['confidence'] is None and 70 < r[0]['target_pid'] < 90)
check('compara_one2one Trp53 mouse->human', lambda: oc.compara_one2one('Trp53', source='mouse', target='human'),
      lambda r: r is None or r['target_id'] == 'ENSG00000141510')
check('MARCH1 -> HTTP 400', lambda: oc.resolve_symbol('human', 'MARCH1'), lambda r: False)
check('MARCHF1 resolves', lambda: oc.resolve_symbol('human', 'MARCHF1'), lambda r: r == 'ENSG00000145416')
check('batch_compara 2 genes zebrafish', lambda: oc.batch_compara(['TP53', 'ATM'], source='human', target='zebrafish')[['symbol', 'target_id', 'type', 'taxonomy_level']].to_dict('records'),
      lambda r: len(r) >= 2)
# Doc claim in SKILL.md: /homology/id/<ensembl_gene_id> (no species)
check('SKILL.md route /homology/id/<gene id> without species', lambda: requests.get(oc.ENSEMBL + '/homology/id/ENSG00000141510', params={'type': 'orthologues', 'target_species': 'mouse'},
      headers=oc.HEADERS, timeout=45).status_code, lambda r: r == 200)
check('route /homology/id/human/<gene id>', lambda: requests.get(oc.ENSEMBL + '/homology/id/human/ENSG00000141510', params={'type': 'orthologues', 'target_species': 'mouse'},
      headers=oc.HEADERS, timeout=45).status_code, lambda r: r == 200)

# ---- OrthoDB ----
P53 = '4289813at2759'
check('OI-04 search tumor protein p53 contains exact-name group', lambda: [g for g in oc.orthodb_search('tumor protein p53') if g['name'].lower() == 'tumor protein p53'],
      lambda r: any(g['id'] == P53 for g in r))
check('OI-04 search TP53 first hit is not the p53 group (documented trap)', lambda: oc.orthodb_search('TP53')[:3], lambda r: r and r[0]['id'] != P53)
check('OI-01 p53 group mouse members', lambda: oc.orthodb_orthologs(P53, 10090), lambda r: 'Trp53' in r)
check('OI-01 p53 group human members', lambda: oc.orthodb_orthologs(P53, 9606), lambda r: 'TP53' in r)
check('OI-04 group_has_gene TP53 in p53 group', lambda: oc.orthodb_group_has_gene(P53, 'tp53', 9606), lambda r: r is True)
check('OI-04 group_has_gene rejects BRCA1 in p53 group', lambda: oc.orthodb_group_has_gene(P53, 'BRCA1', 9606), lambda r: r is False)
check('OI-04 TIGAR-ranked group rejected for TP53', lambda: [oc.orthodb_group_has_gene(g['id'], 'TP53', 9606) for g in oc.orthodb_search('TP53')[:2]],
      lambda r: not any(r))
check('OI-01 null data -> [] (p53 group at a species with no member)', lambda: oc.orthodb_orthologs(P53, 4932), lambda r: isinstance(r, list))
check('orthodb_groups returns ids', lambda: oc.orthodb_groups('BRCA1')[:3], lambda r: len(r) > 0)
check('OI-06 /tab?id= returns TSV', lambda: oc.get_with_retry(oc.ORTHODB + '/tab', params={'id': P53}).text[:120], lambda r: '\t' in r)
check('OI-06 /tab?query= is 404', lambda: requests.get(oc.ORTHODB + '/tab', params={'query': P53}, timeout=45).status_code, lambda r: r == 404)
check('OrthoDB /group', lambda: oc.get_with_retry(oc.ORTHODB + '/group', params={'id': P53}).json().get('data', {}), lambda r: r)

# ---- OMA ----
check('OMA TP53 1:1', lambda: [(o.get('canonicalid'), o['species']['code'], o['species']['taxon_id']) for o in oc.oma_orthologs('P04637', rel_type='1:1')][:5],
      lambda r: any(c == 'MOUSE' for _, c, _ in r))
check('OMA BRCA1 P38398 -> [] (documented as no call)', lambda: oc.oma_orthologs('P38398', rel_type='1:1'), lambda r: r == [])
check('OMA hog for P04637', lambda: oc.oma_hog_for_protein('P04637'), lambda r: r)

# ---- KEGG ----
check('KEGG hsa:7157 -> K04451', lambda: oc.ko_for_gene('hsa', '7157'), lambda r: r == ['K04451'])
check('KEGG genes_for_ko', lambda: len(oc.genes_for_ko('K04451')), lambda r: r > 100)
check('KEGG ko_info', lambda: oc.ko_info('K04451')[:60], lambda r: 'K04451' in r)

# ---- PANTHER (documented route, no client) ----
check('OI-07 PANTHER matchortho P04637 -> mouse', lambda: requests.get('https://pantherdb.org/services/oai/pantherdb/ortholog/matchortho',
      params={'geneInputList': 'P04637', 'organism': 9606, 'targetOrganism': 10090, 'orthologType': 'LDO'}, timeout=45).text[:400],
      lambda r: 'P02340' in r or 'Tp53' in r)
check('HomoloGene retired (efetch db=homologene)', lambda: requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi', params={'db': 'homologene', 'id': '460'}, timeout=45).text[:150],
      lambda r: True)
