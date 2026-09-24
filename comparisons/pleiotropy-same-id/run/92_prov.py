import hashlib
T='F:/OpenScience/comparisons/_theirs/bio-causal-genomics-pleiotropy-detection/'
U='F:/OpenScience/external/GPTomics__bioSkills/causal-genomics/pleiotropy-detection/'
def L(p): return [l.rstrip('\r') for l in open(p,encoding='utf-8').read().splitlines()]
for f in ['SKILL.md','usage-guide.md']:
    t=L(T+f);u=L(U+f);us=set(x.strip() for x in u)
    common=[l for l in t if l.strip() and l.strip() in us]
    print(f,'theirs nonblank',len([l for l in t if l.strip()]),'in upstream',len(common))
    for c in common: print('   ',c[:100])
