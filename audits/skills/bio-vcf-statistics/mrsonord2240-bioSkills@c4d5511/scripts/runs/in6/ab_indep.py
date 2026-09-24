import sys, collections
s = collections.defaultdict(float); n = collections.Counter()
for line in open(sys.argv[1]):
    if line.startswith('##'): continue
    f = line.rstrip('\n').split('\t')
    if line.startswith('#'): names = f[9:]; continue
    keys = f[8].split(':'); gi, ai = keys.index('GT'), keys.index('AD')
    for name, v in zip(names, f[9:]):
        p = v.split(':')
        gt = p[gi].replace('|', '/')
        if gt in ('0/1', '1/0') and len(p) > ai and p[ai] != '.':
            r, a = (int(x) for x in p[ai].split(',')[:2])
            if r + a > 0: s[name] += a / (r + a); n[name] += 1
for k in sorted(n): print(f"{k}\tmean het AB: {s[k]/n[k]:.3f} (n={n[k]})")
