"""Tooling smoke for bio-ortholog-inference client + live service status (read-only import)."""
import sys, time, os, subprocess
sys.dont_write_bytecode = True
SK = r'F:\OpenScience\wt\dbaccess-ortholog-inference\skills\bio-ortholog-inference'
sys.path.insert(0, SK + r'\scripts')
import ortholog_clients as oc, requests
_orig = requests.Session.request
def _t(self, *a, **k):
    k.setdefault('timeout', 60)  # harness-only: client itself sets no timeout
    return _orig(self, *a, **k)
requests.Session.request = _t
results = []
def check(name, fn):
    try: ok, d = fn()
    except Exception as e: ok, d = False, f'EXC {type(e).__name__}: {str(e)[:220]}'
    results.append((name, ok, d)); print(('PASS' if ok else 'FAIL'), name, '|', d, flush=True); time.sleep(0.3)

def t_resolve():
    i = oc.resolve_symbol('human', 'TP53'); m = oc.resolve_symbol('mouse', 'Trp53')
    return i == 'ENSG00000141510' and m == 'ENSMUSG00000059552', f"human TP53={i} mouse Trp53={m}"
def t_march1():
    try: old = oc.resolve_symbol('human', 'MARCH1'); o = f'MARCH1 -> {old}'
    except requests.HTTPError as e: o = f'MARCH1 HTTP {e.response.status_code}'
    new = oc.resolve_symbol('human', 'MARCHF1')
    return new.startswith('ENSG'), f"{o}; MARCHF1 -> {new}"
def t_compara():
    o = oc.compara_orthologs('human', 'TP53', 'mouse')
    return len(o) == 1 and o[0]['target_id'] == 'ENSMUSG00000059552' and o[0]['type'] == 'ortholog_one2one', f"{o}"
def t_one2one():
    o = oc.compara_one2one('Trp53', 'mouse', 'human')
    return o and o['target_id'] == 'ENSG00000141510', f"{o}"
def t_batch():
    df = oc.batch_compara(['TP53', 'BRCA1', 'MYC', 'NOT_A_GENE_XYZ'], 'human', 'zebrafish')
    d = df[df.type == 'ortholog_one2one'] if 'type' in df else df
    return 'error' in df and len(d) >= 1, f"rows={len(df)} types={df['type'].value_counts(dropna=False).to_dict() if 'type' in df else None} errors={int(df['error'].notna().sum()) if 'error' in df else 0}; zebrafish tp53={df[(df.symbol=='TP53')].target_id.tolist()}"
def t_orthodb():
    g = oc.orthodb_groups('BRCA1', 9606)
    return len(g) > 0, f"{len(g)} groups, first={g[:3]}"
def t_orthodb_members():
    g = oc.orthodb_groups('TP53', 9606); out = {}
    for og in g[:5]:
        try: m = oc.orthodb_orthologs(og, 10090); out[og] = f"{len(m)} items, non-None={sum(x is not None for x in m)}"
        except Exception as e: out[og] = f"EXC {type(e).__name__}: {e}"
        time.sleep(0.3)
    return True, f"OBSERVED orthodb_orthologs (mouse level) per group: {out}"
def oma_retry(path, tries=4):
    last = None
    for i in range(tries):
        r = requests.get(f'{oc.OMA}{path}', timeout=60); last = r
        if r.status_code != 502: break
        time.sleep(4 * (i + 1))
    return last
def t_oma_orthologs():
    r = oma_retry('/protein/P38398/orthologs/')
    if r.status_code != 200: return True, f"OBSERVED OMA orthologs HTTP {r.status_code} after retries ({r.text[:60]!r})"
    j = r.json(); mouse = [x for x in j if 'MOUSE' in str(x.get('canonicalid'))]
    return True, f"OMA orthologs n={len(j)} mouse={[x.get('omaid') for x in mouse][:3]}"
def t_oma_protein():
    r = oma_retry('/protein/P38398/')
    if r.status_code != 200: return True, f"OBSERVED OMA protein HTTP {r.status_code} after retries"
    return True, f"OMA protein oma_hog_id={r.json().get('oma_hog_id')} omaid={r.json().get('omaid')}"
def t_oma_version():
    r = requests.get('https://omabrowser.org/api/version/', timeout=60)
    return True, f"OBSERVED OMA /version HTTP {r.status_code} {r.text[:100]!r}"
def t_kegg():
    ko = oc.ko_for_gene('hsa', '7157'); mm = oc.ko_for_gene('mmu', '22059')
    return ko == ['K04451'] and mm == ['K04451'], f"hsa:7157 -> {ko}; mmu:22059 (Trp53) -> {mm}"
def t_kegg_members():
    g = oc.genes_for_ko('K04451'); info = oc.ko_info('K04451')
    sp = {x.split(':')[0] for x in g}
    return 'hsa:7157' in g and 'mmu:22059' in g and 'p53' in info.lower(), f"{len(g)} members, {len(sp)} species; info first line={info.splitlines()[0:2]}"
def t_panther():
    r = requests.get('https://pantherdb.org/services/oai/pantherdb/ortholog/matchortho', params={'geneInputList': 'P04637', 'organism': 9606, 'targetOrganism': 10090, 'orthologType': 'LDO'}, timeout=60)
    m = r.json()['search']['mapping']['mapped']
    return m['target_gene_symbol'] == 'Tp53', f"PANTHER (no client function; liveness) P04637 -> {m['target_gene_symbol']} {m['target_gene']} v{r.json()['search']['product']['version']}"
def t_eggnog():
    r = requests.get('https://eggnog6.embl.de/api/', allow_redirects=True, timeout=60)
    return True, f"OBSERVED eggNOG API -> final {r.url} HTTP {r.status_code} (BLOCKED for scripts)"
def t_homologene():
    r = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi', params={'db': 'homologene', 'id': '460', 'retmode': 'text'}, timeout=60)
    return True, f"OBSERVED HomoloGene efetch HTTP {r.status_code} {r.text[:100]!r}"
def run_ex(name, to=300):
    def f():
        p = subprocess.run([sys.executable, '-B', os.path.join(SK, 'examples', name + '.py')], capture_output=True, text=True, timeout=to)
        open(rf'F:\OpenScience\audits\bio-ortholog-inference\examples_out_{name}.txt', 'w', encoding='utf-8').write(p.stdout + p.stderr)
        return p.returncode == 0, f'example {name}.py exit={p.returncode}'
    return f
for n, f in [('Compara resolve_symbol', t_resolve), ('Compara MARCH1->MARCHF1', t_march1), ('compara_orthologs TP53 human->mouse', t_compara),
             ('compara_one2one Trp53', t_one2one), ('batch_compara zebrafish + bad symbol', t_batch),
             ('orthodb_groups BRCA1', t_orthodb), ('orthodb_orthologs mouse level', t_orthodb_members),
             ('OMA /version', t_oma_version), ('OMA orthologs P38398', t_oma_orthologs), ('OMA protein P38398', t_oma_protein),
             ('KEGG ko_for_gene', t_kegg), ('KEGG genes_for_ko/ko_info', t_kegg_members),
             ('PANTHER liveness', t_panther), ('eggNOG API', t_eggnog), ('HomoloGene efetch', t_homologene),
             ('example compara_orthologs.py', run_ex('compara_orthologs')), ('example kegg_orthology.py', run_ex('kegg_orthology')),
             ('example cross_resource.py', run_ex('cross_resource'))]:
    check(n, f)
print(f"\nSUMMARY {sum(1 for _, o, _ in results if o)}/{len(results)} pass")
