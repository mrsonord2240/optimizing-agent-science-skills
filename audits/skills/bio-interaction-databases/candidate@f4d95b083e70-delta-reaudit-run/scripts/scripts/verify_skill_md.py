import hashlib, json
T = 'F:/OpenScience/wt/dbaccess-interaction-databases/skills/bio-interaction-databases/SKILL.md'
OLD = 'F:/OpenScience/audits/bio-interaction-databases/reaudit-run-2/source-identity.json'
c = {f['path']: f['sha256'] for f in json.load(open(OLD, encoding='utf-8'))['files']}
cur = open(T, 'rb').read()
new = b"(self-interactions, i.e. homodimers, are excluded from the aggregate, so a gene whose only evidence is a self-interaction is not a node; those `gene_a == gene_b` rows remain in `biogrid_lt_physical` output)"
old = b"(self-interactions are dropped)"
assert cur.count(new) == 1
print('SKILL.md reverted == certified sha:', hashlib.sha256(cur.replace(new, old)).hexdigest() == c['SKILL.md'])
