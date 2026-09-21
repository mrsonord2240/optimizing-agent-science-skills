# Input 7 support: does the Skill's central warning hold? inter-community distances in spring layouts change with seed; and is anything in the Skill offered for hive / FA2 / datashader
import networkx as nx, numpy as np, itertools, pathlib, re
G=nx.read_graphml('data/synth_ppi.graphml'); blk=nx.get_node_attributes(G,'block')
def cent(pos): return {b:np.mean([pos[n] for n in G if blk[n]==b],axis=0) for b in range(4)}
rows=[]
for seed in [1,2,3,4,5]:
    c=cent(nx.spring_layout(G,seed=seed)); d={(a,b):np.linalg.norm(c[a]-c[b]) for a,b in itertools.combinations(range(4),2)}
    order=sorted(d,key=d.get); rows.append(order[0]); print('seed',seed,'closest pair of blocks',order[0],'dist %.2f'%d[order[0]],'farthest',order[-1])
print('closest block pair varies across seeds:',len(set(rows))>1, '(planted truth: all 4 blocks are symmetric, same p_out)')
t=pathlib.Path('run/skill/data-visualization/network-visualization/SKILL.md').read_text(encoding='utf-8')
py=[b for b in re.findall(r'```python\n(.*?)```',t,re.S)]
for kw in ['forceatlas','fa2','HiveNetX','pyveplot','datashader','adjustText','geom_conn_bundle','bipartite_layout','graphviz_layout']:
    code=[i+1 for i,b in enumerate(py) if kw.lower() in b.lower() and not all(l.strip().startswith('#') for l in b.strip().splitlines() if kw.lower() in l.lower())]
    print(f'{kw:18s} mentioned in prose {t.lower().count(kw.lower())}x | in an executable (non-comment) python block:',code)
