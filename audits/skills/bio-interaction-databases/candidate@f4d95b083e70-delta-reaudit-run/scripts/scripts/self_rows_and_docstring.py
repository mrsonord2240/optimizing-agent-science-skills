import ast, hashlib, json, os, sys
sys.dont_write_bytecode = True
T = 'F:/OpenScience/wt/dbaccess-interaction-databases/skills/bio-interaction-databases'
OLD = 'F:/OpenScience/audits/bio-interaction-databases/reaudit-run-2/source-identity.json'
c = {f['path']: f['sha256'] for f in json.load(open(OLD, encoding='utf-8'))['files']}
for p, h in c.items():
    print(p, 'SAME' if hashlib.sha256(open(T + '/' + p, 'rb').read()).hexdigest() == h else 'CHANGED')
# reconstruct certified py by reverting the two docstring lines
cur = open(T + '/scripts/interaction_clients.py', encoding='utf-8', newline='').read()
new1 = "Self-interactions (homodimers: a gene with itself, reported by\n    BioGRID) are dropped so density stays in [0, 1]; get them from biogrid_lt_physical. For directed/signed resources keep a DiGraph"
old1 = "Self-interactions (a gene with itself, reported by\n    BioGRID) are dropped so density stays in [0, 1]. For directed/signed resources keep a DiGraph"
assert new1 in cur
rev = cur.replace(new1, old1)
print('py reverted == certified sha:', hashlib.sha256(rev.encode('utf-8')).hexdigest() == c['scripts/interaction_clients.py'])
a, b = ast.parse(cur), ast.parse(rev)
diffs = [(x.name, ast.get_docstring(x) != ast.get_docstring(y)) for x, y in zip(ast.walk(a), ast.walk(b)) if isinstance(x, ast.FunctionDef)]
print('functions whose docstring differs:', [n for n, d in diffs if d])
strip = lambda t: [setattr(n, 'body', n.body[1:]) if isinstance(n, ast.FunctionDef) and n.name == 'aggregate_networks' else None for n in ast.walk(t)]
strip(a); strip(b)
print('ASTs equal with aggregate_networks docstring removed:', ast.dump(a) == ast.dump(b))
# live: do gene_a == gene_b rows remain in biogrid_lt_physical output?
for line in open('F:/OpenScience/audit-envs/database-access/private/biogrid.env', encoding='utf-8'):
    if line.startswith('BIOGRID_ACCESS_KEY='):
        key = line.split('=', 1)[1].strip().strip('"').strip("'")
sys.path.insert(0, T + '/scripts')
import interaction_clients as ic
for g in ('TP53', 'MDM2'):
    df = ic.biogrid_lt_physical(g, key)
    s = df[df.gene_a == df.gene_b]
    print(g, 'rows', len(df), 'self rows', len(s), sorted(set(s.gene_a)), sorted(set(s.system)))
# aggregate: a gene whose only evidence is a self-interaction is not a node
homodimer_only = df if False else None
G = ic.aggregate_networks(['TP53', 'MDM2'], biogrid_key=key)
print('aggregate nodes', sorted(G.nodes), 'self loops', list(__import__('networkx').selfloop_edges(G)))
