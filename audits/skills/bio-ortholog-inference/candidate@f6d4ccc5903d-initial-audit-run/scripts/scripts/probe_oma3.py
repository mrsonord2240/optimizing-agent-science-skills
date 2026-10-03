"""Third probe: OMA ortholog behavior with/without rel_type filter; mouse subset via client-style parsing. Timeouts on all calls."""
import sys, time, json, requests
sys.dont_write_bytecode=True
sys.path.insert(0, r'F:\OpenScience\wt\dbaccess-ortholog-inference\skills\bio-ortholog-inference\scripts')
import ortholog_clients as oc
out=[]
def P(*a):
    s=' '.join(str(x) for x in a); print(s,flush=True); out.append(s)
def get(u,**k):
    for i in range(3):
        try: r=requests.get(u,timeout=60,**k)
        except Exception as e: P('EXC',e); return None
        if r.status_code!=502: return r
        time.sleep(5)
    return r
B='https://omabrowser.org/api'
for acc in ['P38398','P04637']:
    for rt in [None,'1:1','1:n','m:1','m:n']:
        r=get(f'{B}/protein/{acc}/orthologs/',params={'rel_type':rt} if rt else None)
        if r.status_code==200:
            j=r.json(); mouse=[x['canonicalid'] for x in j if x['species']['code']=='MOUSE']
            P(acc,rt,'200 n=',len(j),'mouse',mouse, 'item keys', sorted(j[0]) if j else None)
        else: P(acc,rt,r.status_code)
        time.sleep(1)
# exercise the client exactly as the Skill ships it, no timeout patch (urllib default: none) -> use thread-limited call
P('client oma_hog_for_protein(P04637) =', oc.oma_hog_for_protein('P04637'))
m=oc.oma_hog_members('HOG:F0782425.2c.7a'); P('client oma_hog_members type',type(m).__name__,'len',len(m),'first',json.dumps(m[0])[:200] if isinstance(m,list) and m else m)
try:
    o=oc.oma_orthologs('P04637'); P('client oma_orthologs(P04637) n=',len(o))
except Exception as e: P('client oma_orthologs(P04637) raised',type(e).__name__,str(e)[:100])
open('probe_oma3_output.txt','w',encoding='utf-8').write('\n'.join(out))
