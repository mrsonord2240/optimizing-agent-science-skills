import sys, threading, json
from http.server import BaseHTTPRequestHandler, HTTPServer
sys.path.insert(0, r'F:\OpenScience\wt\dbaccess-ortholog-inference\skills\bio-ortholog-inference\scripts')
import ortholog_clients as oc
class H(BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def do_GET(self):
        p=self.path
        if '/OK?' in p:
            body={'data':[{'homologies':[{'source':{'id':'S','perc_id':50},'target':{'id':'T','species':'mouse','perc_id':60},'type':'ortholog_one2one','taxonomy_level':'Mammalia'}]}]}
        elif '/EMPTY?' in p: body={'data':[]}
        elif '/BAD?' in p:
            self.send_response(400); self.end_headers(); self.wfile.write(b'{"error":"x"}'); return
        else: body={}
        b=json.dumps(body).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(b)
s=HTTPServer(('127.0.0.1',0),H); threading.Thread(target=s.serve_forever,daemon=True).start()
oc.ENSEMBL=f'http://127.0.0.1:{s.server_port}'
df=oc.batch_compara(['OK','BAD','EMPTY'],'human','mouse',sleep=0)
print(df.to_string()); print(list(df.columns))
df2=oc.batch_compara(['BAD'],sleep=0); print(df2.to_string()); print((df2['type']=='ortholog_one2one').sum())
# snippet from SKILL.md on partial batch
print(df[df['type']=='ortholog_one2one'][['symbol','target_id','taxonomy_level','target_pid']].to_string())
