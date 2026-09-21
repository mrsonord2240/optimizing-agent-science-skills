# Input 4: PyVis route. shipped interactive_network.py from a copy, SKILL PyVis block verbatim (as-is, then repaired), parse HTML and compare to graph
import os, re, json, pathlib, io, contextlib, numpy as np, networkx as nx
ROOT=pathlib.Path('F:/OpenScience/audits/bio-data-visualization-network-visualization'); os.chdir(ROOT/'out/ex_pyvis')
def parse(html):
    t=pathlib.Path(html).read_text(encoding='utf-8')
    nodes=json.loads(re.search(r'nodes = new vis\.DataSet\((\[.*?\])\);',t,re.S).group(1))
    edges=json.loads(re.search(r'edges = new vis\.DataSet\((\[.*?\])\);',t,re.S).group(1))
    return t,nodes,edges
src=(ROOT/'run/skill/data-visualization/network-visualization/examples/interactive_network.py').read_text(encoding='utf-8')
ns={'__name__':'__main__'}; buf=io.StringIO()
with contextlib.redirect_stdout(buf): exec(compile(src,'interactive_network.py','exec'),ns)
print(buf.getvalue().strip().splitlines()[-8:])
G=ns['G']
for f in ['network_basic.html','network_styled.html']:
    t,n,e=parse(f); print(f,'bytes',len(t),'nodes',len(n),'edges',len(e),'graph',G.number_of_nodes(),G.number_of_edges(),'| offline lib inline:', 'cdn.jsdelivr' in t or 'unpkg' in t or 'cdnjs' in t)
t,n,e=parse('network_styled.html')
deg=dict(G.degree()); comms=list(nx.algorithms.community.greedy_modularity_communities(G)); n2c={x:i for i,c in enumerate(comms) for x in c}
palette=['#E64B35','#4DBBD5','#00A087','#3C5488','#F39B7F','#8491B4','#91D1C2','#DC0000']
print('styled: size==10+5*deg',all(d['size']==10+5*deg[d['id']] for d in n),' colour==palette[community]',all(d['color']==palette[n2c[d['id']]%8] for d in n))
print('G edge attrs after example ran (pyvis from_nx mutation check):',dict(list(G.edges(data=True))[0][2]), '| any edge still has weight:',any('weight' in d for _,_,d in G.edges(data=True)))
print('styled edge widths distinct values:',sorted({d['width'] for d in e})[:5],'(intended 3*weight in [1.2,3.0])')
G0=ns['G']
print('styled: edge set equals graph edges',{frozenset((d['from'],d['to'])) for d in e}=={frozenset(x) for x in G.edges()})
# SKILL block 6 verbatim (needs G, degrees, palette, node_to_community)
from pyvis.network import Network
b6=(ROOT/'run/blocks/b06_python.py').read_text(encoding='utf-8')
print('--- SKILL PyVis block verbatim with G, degrees, node_to_community defined but NOT palette')
ns2={'G':G,'degrees':deg,'node_to_community':n2c}
try: exec(compile(b6,'b06','exec'),ns2); print('ran')
except Exception as ex: print(type(ex).__name__,ex)
print('--- with palette defined too')
ns3=dict(ns2,palette=palette)
try: exec(compile(b6,'b06','exec'),ns3); print('ran'); t,n,e=parse('network.html'); print('block html nodes',len(n),'edges',len(e),'size ok',all(d['size']==10+5*deg[d['id']] for d in n),'color ok',all(d['color']==palette[n2c[d['id']]] for d in n),'title has degree',all(f"Degree: {deg[d['id']]}" in d['title'] for d in n))
except Exception as ex: print(type(ex).__name__,ex)
# directed graph in pyvis: SKILL says nothing; from_nx on DiGraph
D=nx.read_graphml(str(ROOT/'data/synth_grn.graphml')); print('GRN is directed',D.is_directed(), D.number_of_nodes(),D.number_of_edges())
net=Network(height='700px',width='100%'); net.from_nx(D); net.save_graph('grn_default.html'); t,n,e=parse('grn_default.html'); print('default from_nx on DiGraph: arrows in edges?', any('arrows' in d for d in e), '| directed option in html:', 'arrows' in t and '"to"' in t)
net=Network(height='700px',width='100%',directed=True); net.from_nx(D); net.save_graph('grn_directed.html'); t,n,e=parse('grn_directed.html'); print('Network(directed=True): edges',len(e),'arrows to:',sum(1 for d in e if d.get('arrows')=='to'),'/',len(e))
# large graph claim: 2000 nodes html size
Gb=nx.barabasi_albert_graph(2000,2,seed=1); net=Network(); net.from_nx(Gb); net.save_graph('big2000.html'); print('2000-node html bytes',os.path.getsize('big2000.html'))
