# Re-audit 2026-09-15, Input 3 (Edge, regression). Shipped examples/protein_groups.py functions (fork 575ab94,
# read-only; copied source exec'd up to the demo section) on the TPM1 IP-MS map, in 3 input orders.
import io, contextlib, itertools
import pandas as pd

SRC = r'F:/OpenScience/external/mrsonord2240__bioSkills/proteomics/protein-inference/examples/protein_groups.py'
src = open(SRC, encoding='utf-8').read()
defs = src.split('selected, nodes, dropped = apply_parsimony(SAMPLE_MAP)')[0]
ns = {}
exec(compile(defs, 'protein_groups.py', 'exec'), ns)

MAP = {
    'LVIIESDLERAEER': ['P09493', 'P09493-2'],
    'IQLVEEELDRAQER': ['P09493', 'P09493-2', 'Q5VU61'],
    'KLVIIEGDLER':    ['P09493', 'P09493-2', 'Q5VU61'],
    'SIDDLEDELYAQK':  ['P09493', 'P09493-2'],
    'MEIQEIQLK':      ['P09493', 'P09493-2'],
    'ELDNALNDITSL':   ['P67936'],
    'AEFAERSVTK':     ['P67936'],
    'HIAEDADRK':      ['P07951'],
    'KLEETLTAR':      ['DECOY_P09493', 'DECOY_P09493-2'],
    'RTEELQAK':       ['DECOY_Q9Y2B0'],
}
def run(label, m):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        sel, nodes, dropped = ns['apply_parsimony'](m)
        groups = ns['build_groups'](sel, nodes, m)
        picked = ns['picked_group_fdr'](groups, 'DECOY_')
    rep = pd.DataFrame(picked).sort_values(['score', 'leading_protein'], ascending=[False, True])
    print(f'--- {label} ---'); print(buf.getvalue().strip())
    print('dropped (subsumable):', dropped)
    print(rep[['leading_protein', 'accessions', 'n_peptides', 'n_unique_peptides', 'is_decoy', 'qvalue']].to_string(index=False))
    return tuple(rep.leading_protein), tuple(map(tuple, rep.accessions))

outs = []
outs.append(run('canonical first', MAP))
outs.append(run('isoform first', {k: sorted(v, key=lambda a: a != 'P09493-2') for k, v in MAP.items()}))
rev = dict(reversed(list(MAP.items())))
outs.append(run('peptide order reversed + members reversed', {k: v[::-1] for k, v in rev.items()}))
print('identical groups/leads across orders:', len(set(outs)) == 1)
