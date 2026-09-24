# Second check of the HTTP 500 seen in run.py: repeat the request, show the body, and try the correct GRCh38 chr13 accession.
import requests, time
for h in ('NC_000013.14:g.32316461G>A', 'NC_000013.11:g.32316461G>A'):
    for attempt in (1, 2):
        r = requests.get('https://reg.clinicalgenome.org/allele', params={'hgvs': h}, timeout=30)
        print(h, 'attempt', attempt, 'HTTP', r.status_code, r.text[:220].replace('\n', ' '))
        time.sleep(1)
