"""Find a real regulatory feature id and test the SKILL.md endpoint form versus the real one."""
import sys, time
sys.dont_write_bytecode = True
import requests
H = {'Accept': 'application/json'}
B = 'https://rest.ensembl.org'
r = requests.get(f'{B}/overlap/region/human/17:43000000-43200000', params={'feature': 'regulatory'}, headers=H, timeout=60)
print('overlap regulatory status', r.status_code)
regs = r.json() if r.ok else []
print('n regulatory in 17:43.0-43.2Mb:', len(regs), [(g['id'], g.get('feature_type')) for g in regs[:3]])
if regs:
    rid = regs[0]['id']
    for label, url in [('SKILL.md form', f'{B}/regulatory/species/human/feature/{rid}'),
                       ('regulatory/human/ID', f'{B}/regulatory/human/{rid}'),
                       ('regulatory/species/human/id/ID', f'{B}/regulatory/species/human/id/{rid}')]:
        x = requests.get(url, headers=H, params={'activity': 1}, timeout=60)
        print(label, x.status_code, x.text[:160].replace('\n', ' '))
        time.sleep(0.15)
