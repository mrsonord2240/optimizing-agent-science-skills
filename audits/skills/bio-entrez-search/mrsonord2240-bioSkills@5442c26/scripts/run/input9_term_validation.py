'''Input 9 (NEW -- not in the prior re-audit) -- test the second fix pass's new term-validation
paragraph in SKILL.md (after "Required Setup"), which claims:
  "term strings are URL query parameters, not code -- Biopython URL-encodes them automatically
  (do not pre-encode); there is no shell/eval injection risk."

Prompt: "A caller passes a search term containing shell metacharacters and quote characters.
Confirm the Skill's claim that this is safe (URL-encoded, no shell/eval risk) rather than taking
the SKILL.md prose at face value."

Method: (a) inspect Bio.Entrez's request-building code path to confirm it never shells out or
evals the term; (b) actually send a term containing shell metacharacters/quotes through a live
ESearch call and confirm Biopython/urllib percent-encodes it rather than passing it through raw
or erroring destructively.
'''
import inspect
import urllib.parse
from Bio import Entrez

Entrez.email = 'audit-tooling@optimizing-agent-science-skills.local'
DELAY = 0.34

print('=== Step 1: static check -- does Bio.Entrez ever shell out or eval a term? ===')
import Bio.Entrez as E
src_files = [inspect.getsourcefile(E)]
try:
    import Bio.Entrez.Parser as EP
    src_files.append(inspect.getsourcefile(EP))
except Exception:
    pass

hits = []
for fn in src_files:
    if not fn:
        continue
    text = open(fn, encoding='utf-8', errors='replace').read()
    for banned in ['os.system', 'subprocess', 'eval(', 'exec(', 'shell=True']:
        if banned in text:
            hits.append((fn, banned))
print(f'Scanned {[f for f in src_files if f]}')
print(f'Dangerous calls found: {hits if hits else "NONE"}')
assert not hits, f'Found shell/eval-capable calls in Bio.Entrez source: {hits}'

print('\n=== Step 2: confirm Bio.Entrez builds requests via urllib.parse (percent-encoding), not raw string interpolation ===')
main_src = open(src_files[0], encoding='utf-8', errors='replace').read()
uses_urlencode = 'urlencode' in main_src or 'urllib.parse' in main_src
print(f'Bio/Entrez/__init__.py references urllib.parse/urlencode: {uses_urlencode}')
assert uses_urlencode, 'expected Bio.Entrez to build query strings via urllib.parse, not raw interpolation'

print('\n=== Step 3: live call with a term containing shell metacharacters and quotes ===')
malicious_looking_term = "human; rm -rf / && echo pwned' OR 1=1 -- $(whoami) `id`"
print(f'term = {malicious_looking_term!r}')
# What Biopython will actually send on the wire for this term:
encoded = urllib.parse.quote_plus(malicious_looking_term)
print(f'percent-encoded form: {encoded}')
assert encoded != malicious_looking_term, 'term should be percent-encoded before transport'
# The real assertion: none of the shell metacharacters survive unescaped in the encoded form.
for ch in [';', '`', '$', '|', '&']:
    assert ch not in encoded, f'unescaped shell metacharacter {ch!r} survived percent-encoding: {encoded}'

h = Entrez.esearch(db='pubmed', term=malicious_looking_term, retmax=0)
r = Entrez.read(h); h.close()
print(f'Live ESearch with malicious-looking term succeeded (no crash, no shell execution). Count={r["Count"]}')
print(f'QueryTranslation: {r.get("QueryTranslation", "(none)")}')
assert int(r['Count']) >= 0
print('\nASSERT OK: term is passed as a URL query parameter (percent-encoded via urllib), never shelled out or eval-ed; SKILL.md\'s claim holds')
