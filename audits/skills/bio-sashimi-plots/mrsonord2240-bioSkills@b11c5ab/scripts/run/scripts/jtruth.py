#!/usr/bin/env python3
"""Independent junction truth (pysam CIGAR scan, no ggsashimi code) and label check against a rendered SVG.

usage: jtruth.py REGION GROUPS_TSV [--M 1] [--agg mean_j|none] [--svg fig.svg] [--strand none|SENSE|ANTISENSE|MATE1_SENSE|MATE2_SENSE]
REGION  chrom:start-end (1-based inclusive, like ggsashimi -c)
GROUPS_TSV  sample<TAB>bam<TAB>group  (relative BAM paths resolve against the TSV directory, like ggsashimi)
Counts every mapped alignment record (incl. secondary; --no-secondary skips them).
Prints, per group and junction, the per-sample counts, the expected label (plain mean of the samples that have the junction
and pass -M, Python round = half to even) and, with --svg, whether that label occurs among the SVG <text> strings.
Exit code 1 if any expected label is missing from the SVG. The assertion count is printed as 'LABELS_OK n/m'.
"""
import argparse, collections, pathlib, re, sys
import xml.etree.ElementTree as ET
import pysam

ap = argparse.ArgumentParser()
ap.add_argument('region'); ap.add_argument('groups')
ap.add_argument('--M', type=int, default=1)
ap.add_argument('--agg', default='mean_j')
ap.add_argument('--svg')
ap.add_argument('--strand', default='none')
ap.add_argument('--no-secondary', action='store_true', help='skip secondary alignments (default: count every alignment record with an N op)')
a = ap.parse_args()
m = re.fullmatch(r'(.+):(\d+)-(\d+)', a.region)
chrom, s, e = m.group(1), int(m.group(2)), int(m.group(3))
gdir = pathlib.Path(a.groups).resolve().parent


def counts(bam):
    d = collections.Counter()
    with pysam.AlignmentFile(bam) as f:
        for r in f.fetch(chrom, max(0, s - 1), e):
            if r.is_unmapped or (a.no_secondary and r.is_secondary):
                continue
            if a.strand != 'none':
                if a.strand == 'SENSE':
                    st = '-' if r.is_reverse else '+'
                elif a.strand == 'ANTISENSE':
                    st = '+' if r.is_reverse else '-'
                else:
                    first = r.is_read1 if a.strand == 'MATE1_SENSE' else r.is_read2
                    st = ('+' if not r.is_reverse else '-') if first else ('-' if not r.is_reverse else '+')
            else:
                st = '.'
            pos = r.reference_start + 1
            for op, ln in r.cigartuples:
                if op == 3 and pos > s - 1 and pos + ln < e:
                    d[(pos, pos + ln, st)] += 1
                if op in (0, 2, 3, 7, 8):
                    pos += ln
    return d


grp = collections.OrderedDict()
for line in open(a.groups):
    if not line.strip():
        continue
    sid, bam, g = line.rstrip('\n').split('\t')[:3]
    p = pathlib.Path(bam)
    p = p if p.is_absolute() else gdir / p
    grp.setdefault(g, []).append((sid, counts(str(p))))

labels = set()
if a.svg:
    for el in ET.parse(a.svg).iter():
        if el.tag.endswith('text'):
            t = ''.join(el.itertext()).strip()
            if t:
                labels.add(t)

ok = tot = 0
for g, samples in grp.items():
    keys = sorted({k for _, d in samples for k in d})
    for k in keys:
        per = [d[k] for _, d in samples if d.get(k, 0) >= a.M]
        if not per:
            continue
        if a.agg == 'mean_j':
            exp = str(round(sum(per) / len(per)))
            tag = f'mean_j={sum(per) / len(per):.2f}->{exp}'
            exps = [exp]
        else:
            exps = [str(x) for x in per]
            tag = 'per-sample'
        line = f'{g}\t{k[0]}-{k[1]}\t{k[2]}\tcounts={[d.get(k, 0) for _, d in samples]}\t{tag}'
        if a.svg:
            for x in exps:
                tot += 1
                hit = x in labels
                ok += hit
                if not hit:
                    line += f'\tMISSING {x}'
        print(line)
if a.svg:
    print(f'LABELS_OK {ok}/{tot}')
    sys.exit(0 if ok == tot else 1)
