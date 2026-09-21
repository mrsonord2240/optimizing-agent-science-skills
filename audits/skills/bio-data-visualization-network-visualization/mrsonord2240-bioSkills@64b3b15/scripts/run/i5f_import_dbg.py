# Input 5f: debug GraphML import: 500 error on data/ path, and node-count inflation
import networkx as nx, py4cytoscape as p4c, os, shutil
A='/mnt/openscience/audits/bio-data-visualization-network-visualization'
os.chdir(A+'/out/cyto5')
def imp(path):
    try:
        r=p4c.import_network_from_file(path); suid=r['networks'][0]
        names=p4c.get_table_columns('node',['name'],network=suid)['name'].tolist()
        print('OK',os.path.basename(path),'suid',suid,'nodes',len(p4c.get_all_nodes(network=suid)),'edges',len(p4c.get_all_edges(network=suid)),'| names not in source:',[n for n in names if not n.startswith('G') and not n.startswith('T')][:6])
        return suid
    except Exception as e: print('FAIL',path[-40:],str(e).split('Error processing')[-1][:90])
imp(A+'/data/synth_ppi.graphml')
shutil.copy(A+'/data/synth_ppi.graphml','/tmp/cyto_home/synth_ppi.graphml'); imp('/tmp/cyto_home/synth_ppi.graphml')
shutil.copy(A+'/data/synth_ppi.graphml',A+'/out/cyto5/copy_ppi.graphml'); imp(A+'/out/cyto5/copy_ppi.graphml')
imp(A+'/data/synth_grn.graphml')
print('N networks',len(p4c.get_network_list()),p4c.get_network_list()[:8])
