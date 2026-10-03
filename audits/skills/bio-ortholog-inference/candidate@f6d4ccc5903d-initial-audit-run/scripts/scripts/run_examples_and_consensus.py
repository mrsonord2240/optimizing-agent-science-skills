"""Run the three shipped examples unmodified (subprocess, 240 s cap) and a TP53 human->mouse consensus using only shipped client functions."""
import sys, os, subprocess, time, json
sys.dont_write_bytecode=True
SK=r'F:\OpenScience\wt\dbaccess-ortholog-inference\skills\bio-ortholog-inference'
sys.path.insert(0, SK+r'\scripts')
here=os.path.dirname(os.path.abspath(__file__))
res={}
for n in ['compara_orthologs','kegg_orthology','cross_resource']:
    try:
        p=subprocess.run([sys.executable,'-B',os.path.join(SK,'examples',n+'.py')],capture_output=True,text=True,timeout=240)
        open(os.path.join(here,f'example_{n}_output.txt'),'w',encoding='utf-8').write(f'exit={p.returncode}\n'+p.stdout+p.stderr[-1500:])
        res[n]=p.returncode; print(n,'exit',p.returncode); print(p.stdout[-700:]); print(p.stderr[-300:])
    except subprocess.TimeoutExpired: res[n]='timeout'; print(n,'TIMEOUT')
    time.sleep(1)
import ortholog_clients as oc
print('--- TP53 consensus via shipped functions ---')
c=oc.compara_orthologs('human','TP53','mouse'); print('Compara:',[(x['target_id'],x['type'],x['confidence']) for x in c])
try: o=oc.oma_orthologs('P04637'); print('OMA mouse:',[x['canonicalid'] for x in o if x['species']['code']=='MOUSE'], 'keys include taxonId?', 'taxonId' in (o[0] if o else {}))
except Exception as e: print('OMA raised',type(e).__name__,str(e)[:80])
g=oc.orthodb_groups('TP53',9606); print('OrthoDB first 3 groups:',g[:3])
try: print('orthodb_orthologs(first TP53 hit, mouse):',oc.orthodb_orthologs(g[0],10090))
except Exception as e: print('orthodb_orthologs raised',type(e).__name__,e)
try: print('orthodb_orthologs(4289813at2759 [tumor protein p53], mouse):',oc.orthodb_orthologs('4289813at2759',10090))
except Exception as e: print('orthodb_orthologs raised',type(e).__name__,e)
print('KEGG:',oc.ko_for_gene('hsa','7157'), 'unknown gene ->', oc.ko_for_gene('hsa','99999999'))
