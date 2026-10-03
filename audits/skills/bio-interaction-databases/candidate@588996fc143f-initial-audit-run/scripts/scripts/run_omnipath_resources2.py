"""Print OmniPath's own license metadata for sources that appear under license=commercial."""
import sys, json
sys.dont_write_bytecode = True
import requests
res = requests.get('https://omnipathdb.org/resources', params={'format': 'json'}, timeout=90).json()
for n in ('PhosphoSite', 'DIP', 'HPRD', 'KEGG-MEDICUS', 'IntAct', 'SIGNOR', 'BioGRID'):
    x = res.get(n)
    print(n, json.dumps(x.get('license') if x else None)[:260])
