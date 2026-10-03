"""Second raw probe: OrthoDB group semantics (symbol search vs full text), null-data orthologs responses, OMA record/hog endpoints. Timeouts on all calls."""
import sys, json, time, requests
sys.dont_write_bytecode = True
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s,flush=True); out.append(s)
def get(url, **kw):
    try: return requests.get(url, timeout=45, **kw)
    except Exception as e: P('  EXC',type(e).__name__,str(e)[:120]); return None
OD='https://data.orthodb.org/v12'
for sym in ['TP53','BRCA1']:
    r=get(OD+'/search',params={'query':sym,'species':9606}); ids=r.json()['data']
    P(sym,'search n=',len(ids), 'keys', list(r.json()))
    for og in ids[:4]:
        g=get(OD+'/group',params={'id':og}).json()['data']
        P('  ',og,'name=',g.get('name'),'| genes',g.get('genes_count'),'species',g.get('species_count'))
        time.sleep(0.4)
# raw data for null cases
for og in ['4219792at2759','1464927at33208']:
    r=get(OD+'/orthologs',params={'id':og,'species':10090}); P('orthologs',og,r.status_code,r.text[:200])
    r=get(OD+'/orthologs',params={'id':og,'species':9606}); P('orthologs human',og,r.status_code,r.text[:120].replace('\n',' '))
    time.sleep(0.4)
# structure of a populated orthologs response
r=get(OD+'/orthologs',params={'id':'4837993at2759','species':10090}).json()['data']
P('populated: type',type(r).__name__,'n groups',len(r),'group keys',sorted(r[0]) ,'n genes',len(r[0]['genes']))
P('first gene keys', sorted(r[0]['genes'][0]))
P('first gene gene_id',r[0]['genes'][0]['gene_id'],'organism',r[0]['genes'][0].get('organism'))
# find the actual p53 group: search by 'tumor protein p53'
r=get(OD+'/search',params={'query':'cellular tumor antigen p53','species':9606}); ids=r.json()['data'][:5]
for og in ids:
    g=get(OD+'/group',params={'id':og}).json()['data']; P('  p53 text search',og,g.get('name')); time.sleep(0.4)
# OMA
OMA='https://omabrowser.org/api'
for path in ['/protein/P38398/','/protein/HUMAN34016/orthologs/','/protein/P04637/','/protein/P04637/orthologs/','/protein/P04637/orthologs/?rel_type=1:1']:
    for i in range(3):
        r=get(OMA+path)
        if r is not None and r.status_code!=502: break
        time.sleep(5)
    P('OMA',path,None if r is None else (r.status_code,r.text[:260].replace('\n',' ')))
    if r is not None and r.ok and path=='/protein/P04637/':
        hog=r.json().get('oma_hog_id'); P('   oma_hog_id=',repr(hog), 'keys',sorted(r.json()))
        if hog:
            h=get(OMA+f'/hog/{hog}/'); P('   hog',None if h is None else (h.status_code,h.text[:200]))
    time.sleep(1)
open('probe_orthodb_oma_output.txt','w',encoding='utf-8').write('\n'.join(out))
