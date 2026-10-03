"""Independent probes for IDM-010 (self-interaction drop) and IDM-011 (SIGNOR unparseable answer)."""
import os, sys, warnings
sys.dont_write_bytecode = True
sys.path.insert(0, 'F:/OpenScience/wt/dbaccess-interaction-databases/skills/bio-interaction-databases/scripts')
import interaction_clients as ic
import networkx as nx
import pandas as pd
res = []
def check(n, c, d=''):
    res.append(bool(c)); print(('PASS ' if c else 'FAIL ') + n + (' | ' + str(d) if d else ''))

# --- IDM-010: mocked sources, no network
str_df = pd.DataFrame({'preferredName_A': ['TP53'], 'preferredName_B': ['MDM2'], 'score': [0.99]})
omni_df = pd.DataFrame({'source_genesymbol': ['TP53', 'ATM'], 'target_genesymbol': ['TP53', 'TP53']})
bio_df = pd.DataFrame({'gene_a': ['MDM2', 'TP53', 'TP53', 'TP53'], 'gene_b': ['MDM2', 'TP53', 'MDM2', 'ATM'],
                       'system': ['Two-hybrid'] * 4, 'pmid': [1, 2, 3, 4]})
ic.string_network = lambda genes, threshold=700, **k: str_df
ic.omnipath_interactions = lambda genes, types=None, license='academic': omni_df
ic.biogrid_lt_physical = lambda gene, key, taxon=9606: bio_df
g = ic.aggregate_networks(['TP53', 'MDM2', 'ATM'], biogrid_key='x')
print(sorted(g.nodes), [(a, b, sorted(d['sources'])) for a, b, d in g.edges(data=True)])
check('no self loops', not list(nx.selfloop_edges(g)))
check('edges = TP53-MDM2, ATM-TP53', {frozenset((a, b)) for a, b in g.edges} == {frozenset(('TP53', 'MDM2')), frozenset(('ATM', 'TP53'))})
e = g.get_edge_data('MDM2', 'TP53')
check('TP53-MDM2 sources STRING+BioGRID, score kept', e['sources'] == {'STRING', 'BioGRID-LT-physical'} and e['string_score'] == 0.99, e)
s = ic.summary(g); print(s)
check('density in [0,1]', 0 <= s['density'] <= 1, s)
check('multi_source_edges: both 2-source edges (probe expectation corrected from 1 to 2: TP53-ATM has OmniPath+BioGRID)', len(ic.multi_source_edges(g)) == 2)
# homodimer-only gene: node absent (information silently not represented)
bio_df2 = pd.DataFrame({'gene_a': ['MDM2'], 'gene_b': ['MDM2'], 'system': ['Two-hybrid'], 'pmid': [1]})
ic.biogrid_lt_physical = lambda gene, key, taxon=9606: bio_df2
ic.omnipath_interactions = lambda genes, types=None, license='academic': omni_df.iloc[0:0]
ic.string_network = lambda genes, threshold=700, **k: str_df.iloc[0:0]
g2 = ic.aggregate_networks(['MDM2', 'TP53'], biogrid_key='x')
print('homodimer-only graph nodes/edges', g2.number_of_nodes(), g2.number_of_edges(), ic.summary(g2))
check('homodimer-only: empty graph, summary does not crash', g2.number_of_nodes() == 0 and ic.summary(g2)['density'] == 0)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    ic.aggregate_networks(['MDM2', 'TP53'], biogrid_key='x')
print('warnings on dropping a self-interaction:', len(w))

# --- IDM-011: mocked SIGNOR
class R:
    def __init__(self, t): self.text = t
ok_row = '\t'.join(['TP53', 'x', 'x', 'x', 'MDM2', 'x', 'x', 'x', 'down-regulates', 'ubiquitination', 'S20', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', '123', 'x', 'x', 'x', 'x', 'SIGNOR-1', '0.5', ''])
cases = {
    'No result found.': 'empty', '': 'empty', '   \n': 'empty',
    'Service temporarily unavailable': 'raise', '<html><body>502</body></html>': 'raise',
    'a\tb\tc': 'raise',
    ok_row: 'rows', 'garbage line\n' + ok_row + '\n': 'rows', ok_row + '\n' + ok_row: 'rows',
}
for txt, want in cases.items():
    ic._get = lambda *a, _t=txt, **k: R(_t)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        try:
            df = ic.signor_for_gene('TP53', uniprot='P04637'); got = 'empty' if len(df) == 0 else 'rows'
            extra = (len(df), len(w), list(df.columns) == ic.SIGNOR_COLUMNS)
        except ValueError as ex:
            got, extra = 'raise', str(ex)[:90]
    check(f'SIGNOR {txt[:30]!r} -> {want}', got == want, (got, extra))
df = ic.signor_for_gene.__wrapped__ if hasattr(ic.signor_for_gene, '__wrapped__') else None
ic._get = lambda *a, _t=ok_row, **k: R(_t)
d = ic.signor_for_gene('TP53', uniprot='P04637').iloc[0].to_dict()
check('field mapping', d == {'source': 'TP53', 'target': 'MDM2', 'effect': 'down-regulates', 'mechanism': 'ubiquitination', 'residue': 'S20', 'pmid': '123', 'score': '0.5', 'signor_id': 'SIGNOR-1'}, d)
# aggregate_networks does not touch SIGNOR
import inspect
check('aggregate_networks never calls signor_for_gene', 'signor' not in inspect.getsource(ic.aggregate_networks).lower())
print('SUMMARY', sum(res), '/', len(res))
