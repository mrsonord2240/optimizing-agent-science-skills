"""Map MrBayes .parts dot/star patterns to taxon sets and print PP + SD for every informative split, flagging a named split.
Usage: split_pp.py <prefix> [comma-separated taxa of the split of interest]"""
import sys

prefix = sys.argv[1]
target = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else None


def rows(path):
    out, hdr = [], None
    for line in open(path, encoding='utf-8', errors='replace'):
        if not line.strip() or line.startswith('['):
            continue
        parts = [p.strip() for p in line.rstrip('\n').split('\t') if p.strip() != '']
        if hdr is None:
            hdr = parts; continue
        out.append(dict(zip(hdr, parts)))
    return out

# taxon order from the NEXUS matrix used by the run (same folder)
import glob, re
nex = [f for f in glob.glob('*.nex') if 'matrix' in open(f, encoding='utf-8').read().lower()][0]
txt = open(nex, encoding='utf-8').read()
mat = txt.lower().split('matrix', 1)[1].split(';', 1)[0]
taxa = [l.split()[0] for l in txt.split('matrix', 1)[1].split(';', 1)[0].strip().splitlines() if l.strip()]
parts = {r['ID']: r['Partition'] for r in rows(prefix + '.parts')}
alltaxa = set(taxa)
for r in rows(prefix + '.tstat'):
    pat = parts[r['ID']]
    star = {taxa[i] for i, c in enumerate(pat) if c == '*'}
    side = star if len(star) <= len(alltaxa) / 2 else alltaxa - star
    flag = ''
    if target and (star == target or alltaxa - star == target):
        flag = '  <== split of interest'
    print('%-4s PP=%s SD=%s  {%s}%s' % (r['ID'], r['Probability(=s)'], r['Stddev(s)'], ','.join(sorted(side)), flag))
