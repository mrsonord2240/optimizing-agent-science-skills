import os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'F:/OpenScience/wt/dbaccess-interaction-databases/skills/bio-interaction-databases/scripts')
import interaction_clients as ic
for line in open('F:/OpenScience/audit-envs/database-access/private/biogrid.env', encoding='utf-8'):
    if line.startswith('BIOGRID_ACCESS_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"\'')
import networkx as nx
g = ic.aggregate_networks(['TP53', 'MDM2'], biogrid_key=KEY)
for a, b, d in g.edges(data=True):
    print(a, b, sorted(d['sources']), d['string_score'])
print('selfloops', list(nx.selfloop_edges(g)))
print(ic.summary(g))
g2 = ic.aggregate_networks(['TP53', 'MDM2', 'ATM'])
print('nokey selfloops', list(nx.selfloop_edges(g2)), ic.summary(g2))
