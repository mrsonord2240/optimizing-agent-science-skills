#!/usr/bin/env python3
"""Phase-2 regression of the nine substantive pre-fix audit inputs.

All paths point to the dispatched branch tip, never the archived source copy.  Each check
asserts output content (counts, record identity, or parsed BAM), not merely a zero exit code.
"""
import collections
import os
import pathlib
import shutil
import subprocess
import sys

import pysam


ROOT = pathlib.Path('/mnt/openscience/audits/bio-alignment-filtering/run')
SKILL = pathlib.Path('/mnt/openscience/wt/alignment-files-alignment-filtering/alignment-files/alignment-filtering')
DATA = pathlib.Path(os.environ['AFDATA'])
OUT = ROOT / 'p2_regression'
OUT.mkdir(exist_ok=True)
failed = []
checks = 0


def check(name, ok, detail=''):
    global checks
    checks += 1
    print(('PASS' if ok else 'FAIL'), name, detail)
    if not ok:
        failed.append(name)


def run(args, cwd=OUT):
    p = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    return p.returncode, p.stdout, p.stderr


def count(path, *args):
    rc, out, err = run(['samtools', 'view', '-c', *args, str(path)])
    assert rc == 0, err
    return int(out)


def records(path):
    return [r.to_string() for r in pysam.AlignmentFile(path)]


def invoke(script, *args):
    return run(['python', str(SKILL / script), *map(str, args)])


# Input 1 / 7: canonical quality filter and duplicate-marking prerequisite.
human = DATA / 'human/test.paired_end.sorted.bam'
g1k = DATA / '1000g/HG00349.chr20_1400000-1500000.bam'
planted = DATA / 'derived/planted_dups.bam'
for label, bam in [('human', human), ('1000g', g1k)]:
    out = OUT / f'{label}.filtered.bam'
    rc, _, err = invoke('examples/filter_bam.py', bam, out, '-q', '30', '-d', '-p')
    truth = [r.to_string() for r in pysam.AlignmentFile(bam)
             if not (r.flag & 3332) and r.mapping_quality >= 30]
    check(f'{label}: CLI predicate equals FLAG/MAPQ truth', rc == 0 and records(out) == truth, err[:120])
    check(f'{label}: coordinate output indexed', (OUT / f'{label}.filtered.bam.bai').exists())
check('unmarked duplicate fixture has 500 records and plain -F 1024 is a no-op',
      count(planted) == 500 and count(planted, '-F', '1024') == 500 and count(planted, '-f', '1024') == 0)

# Input 2: every documented flag breakdown, via all 4096 possible flag words.
flags = ROOT / 'data/synthetic_allflags.bam'
all_flags = [r.flag for r in pysam.AlignmentFile(flags)]
for fmask in (4, 20, 1024, 1280, 1284, 1804, 2304, 2308, 3328, 3332):
    got = count(flags, '-F', str(fmask))
    expected = sum(1 for flag in all_flags if not (flag & fmask))
    check(f'flags: -F {fmask} equals bit arithmetic', got == expected, f'{got}/{expected}')
for required, forbidden in ((64, 2308), (128, 2308), (16, 4), (2, 3328)):
    got = count(flags, '-f', str(required), '-F', str(forbidden))
    expected = sum(1 for flag in all_flags if flag & required and not (flag & forbidden))
    check(f'flags: -f {required} -F {forbidden} equals bit arithmetic', got == expected, f'{got}/{expected}')

# Input 3: region and BED script, with overlap and ordering checks.
bed = OUT / 'mixed.bed'
bed.write_text('track name=x\n# comment\nchr22 1951 2100\nchr22\t2000\t2300\nchr22\t3000\t3200\nunknown\t0\t10\n', encoding='utf-8')
bed_out = OUT / 'bed.bam'
rc, _, err = invoke('scripts/filter_by_bed.py', human, bed, bed_out)
rc2, _, err2 = run(['samtools', 'view', '-b', '-L', str(bed), '-o', str(OUT / 'bed_truth.bam'), str(human)])
check('BED script accepts space/tab/header/unknown rows and matches samtools -L record-for-record',
      rc == 0 and rc2 == 0 and records(bed_out) == records(OUT / 'bed_truth.bam'), f'{err[:80]} {err2[:80]}')
for region in ('chr22', 'chr22:1952', 'chr22:1,952-2,100', 'chr22:4617-4700'):
    out = OUT / 'region.bam'
    rc, _, err = invoke('examples/filter_bam.py', human, out, '-r', region)
    rc2, truth, err2 = run(['samtools', 'view', '-F', '4', str(human), region])
    check(f'region parser matches samtools for {region}', rc == 0 and rc2 == 0 and records(out) == truth.splitlines(), err[:100])

# Input 4: deterministic and pair-consistent downsampling, then safe no-upsample guard.
sub_a, sub_b = OUT / 'sub_a.bam', OUT / 'sub_b.bam'
rca, _, erra = invoke('scripts/subsample_pysam.py', g1k, sub_a, '0.1', '42')
rcb, _, errb = invoke('scripts/subsample_pysam.py', g1k, sub_b, '0.1', '42')
full = collections.Counter(r.query_name for r in pysam.AlignmentFile(g1k))
kept = collections.Counter(r.query_name for r in pysam.AlignmentFile(sub_a))
check('pysam subsample is deterministic and retains whole templates',
      rca == rcb == 0 and records(sub_a) == records(sub_b) and all(kept[q] == full[q] for q in kept), f'{erra[:80]} {errb[:80]}')
matched = OUT / 'matched.bam'
rc, _, err = run(['bash', str(SKILL / 'scripts/match_read_count.sh'), str(g1k), str(matched), '--target', '20000'])
check('target above total copies unchanged rather than malformed -s fraction', rc == 0 and records(matched) == records(g1k), err[:100])

# Input 5 / 8: aligner table textual semantics and real STAR uniqueness sentinel.
text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
for fragment in ('| Bowtie2 | `-q 2`', '| **STAR** | `-q 255`', '| HISAT2 | `-q 2`',
                 '| minimap2 short-read (`-x sr`) | `-q 1` | `-q 30`', '| pbmm2 (PacBio) | `-q 1` | `-q 60`'):
    check(f'aligner table contains {fragment}', fragment in text)
rna = DATA / 'human/test.rna.paired_end.sorted.bam'
rc, nh, err = run(['samtools', 'view', '-c', '-e', '[NH]==1', str(rna)])
rc2, mq, err2 = run(['samtools', 'view', '-c', '-q', '255', str(rna)])
check('real STAR: NH==1 and MAPQ 255 select the same records', rc == rc2 == 0 and nh == mq, f'{nh.strip()} / {mq.strip()}')

# Input 6: expressions/read-group versioned behavior and symmetric template length rule.
rc, out, err = run(['samtools', 'view', '-c', '-e', '[NM] >= 2', str(human)])
truth = sum(1 for r in pysam.AlignmentFile(human) if r.has_tag('NM') and r.get_tag('NM') >= 2)
check('NM expression equals tag truth', rc == 0 and int(out) == truth, f'{out.strip()} / {truth}')
rg = OUT / 'rg.bam'
header = {'HD': {'VN': '1.6'}, 'SQ': [{'SN': 'c', 'LN': 1000}], 'RG': [{'ID': 'a'}]}
with pysam.AlignmentFile(rg, 'wb', header=header) as fh:
    for i, tag in enumerate(('a', 'a', None, None)):
        x = pysam.AlignedSegment(fh.header); x.query_name = f'q{i}'; x.flag = 0; x.reference_id = 0; x.reference_start = i * 20; x.mapping_quality = 60; x.cigartuples = [(0, 10)]; x.query_sequence = 'A' * 10; x.query_qualities = pysam.qualitystring_to_array('I' * 10)
        if tag: x.set_tag('RG', tag)
        fh.write(x)
rc, out, err = run(['samtools', 'view', '-c', '-n', '-r', 'a', str(rg)])
check('-n -r removes untagged reads', rc == 0 and out.strip() == '2', err[:100])

# Input 9: phase-1 pbmm2 claim is present and references the real checked result.
check('pbmm2 Phase-1 result is documented as 5/5 unique MAPQ 60 and 4/4 repeat MAPQ 0',
      '5/5 reads drawn from a unique region got MAPQ 60, 4/4 reads drawn from inside the repeat got MAPQ 0' in text)

print(f'ASSERTIONS {checks - len(failed)}/{checks}')
print(f'FAILURES {len(failed)}')
if failed:
    print('\n'.join(failed))
    raise SystemExit(1)
