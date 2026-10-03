"""Print installed versions and the declared pandas / scikit-learn / numpy constraints of scikit-survival, lifelines and pycox (verifies SKILL.md Version Compatibility)."""
import importlib.metadata as m, re
for p in ('scikit-survival', 'lifelines', 'pycox'):
    try:
        reqs = [r for r in (m.requires(p) or []) if re.match(r'(pandas|scikit-learn|numpy|torch)\b', r, re.I) and 'extra' not in r]
        print(p, m.version(p), reqs)
    except m.PackageNotFoundError:
        print(p, 'not installed')
print('pandas', m.version('pandas'), 'scikit-learn', m.version('scikit-learn'))
