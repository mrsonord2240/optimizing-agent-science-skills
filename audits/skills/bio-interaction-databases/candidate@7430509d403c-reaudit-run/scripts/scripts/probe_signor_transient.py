import requests, time
seen = {}
for i in range(12):
    r = requests.get('https://signor.uniroma2.it/getData.php', params={'organism': 9606, 'id': 'P04637'}, timeout=60)
    k = (r.status_code, len(r.text) if len(r.text) > 200 else r.text[:120])
    seen[k] = seen.get(k, 0) + 1
print(seen)
