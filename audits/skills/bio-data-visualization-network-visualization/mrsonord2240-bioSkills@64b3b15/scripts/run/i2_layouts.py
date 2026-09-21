# Input 2: SKILL.md "Layout Algorithms" block: verbatim standalone, then per-line with the missing names supplied
import networkx as nx, numpy as np, pathlib, traceback, json
G = nx.read_graphml('data/synth_ppi.graphml')
src = pathlib.Path('run/blocks/b01_python.py').read_text(encoding='utf-8')
print('--- verbatim, only G defined')
try: exec(compile(src,'b01','exec'),{'G':G}); print('ran')
except Exception as e: print(type(e).__name__, e)
print('--- verbatim with G, np, hub_nodes, periphery_nodes, top_nodes supplied (top_nodes on G is NOT bipartite)')
deg=dict(G.degree()); hubs=[n for n in G if deg[n]>=30]; per=[n for n in G if n not in hubs]
ns={'G':G,'np':np,'hub_nodes':hubs,'periphery_nodes':per,'top_nodes':hubs}
lines=src.split('\n')
# run each statement separately
for stmt in [l for l in lines if l.startswith('pos =')]:
    try:
        exec('import networkx as nx\n'+stmt,ns); pos=ns['pos']
        ok = len(pos)==len(G) and all(np.isfinite(np.asarray(v)).all() for v in pos.values())
        print(f'OK   {stmt[:80]:80s} n={len(pos)} finite={ok}')
    except Exception as e:
        print(f'FAIL {stmt[:80]:80s} {type(e).__name__}: {str(e)[:100]}')
# reproducibility of every layout
import itertools
def rep(fn,**k):
    a=fn(G,**k);b=fn(G,**k); return all(np.allclose(a[n],b[n]) for n in G)
print('reproducible spring seed:',rep(nx.spring_layout,seed=42,k=1/np.sqrt(len(G)),iterations=100))
print('reproducible kamada_kawai (no seed):',rep(nx.kamada_kawai_layout))
print('reproducible spectral (no seed):',rep(nx.spectral_layout))
# bipartite properly
B=nx.bipartite.random_graph(10,15,0.3,seed=1); top=[n for n,d in B.nodes(data=True) if d['bipartite']==0]
pb=nx.bipartite_layout(B,top); print('bipartite ok',len(pb)==25, 'top x all equal', len({round(pb[n][0],6) for n in top})==1)
# networkx built-in forceatlas2 (SKILL says use fa2_modified / Gephi)
fa=nx.forceatlas2_layout(G,seed=42); fb=nx.forceatlas2_layout(G,seed=42)
print('nx.forceatlas2_layout n',len(fa),'reproducible',all(np.allclose(fa[n],fb[n]) for n in G))
# shell layout with hubs at centre: check radius
ps=nx.shell_layout(G,nlist=[hubs,per]); r={n:np.hypot(*ps[n]) for n in G}
print('shell: hub radius',round(np.mean([r[h] for h in hubs]),3),'periphery radius',round(np.mean([r[p] for p in per]),3))
