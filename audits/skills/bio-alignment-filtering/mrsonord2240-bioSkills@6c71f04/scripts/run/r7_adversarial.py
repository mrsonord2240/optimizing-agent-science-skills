#!/usr/bin/env python3
"""Input 7 (regression, Adversarial): "Clean my BAM: remove duplicates, keep only unique high-confidence properly-paired
primary reads, and I will run Manta on it." on a BAM whose duplicates are UNMARKED (planted, real reads).
Follows the FIXED SKILL.md: extracted Remove-Duplicates snippet, SV recipe, breakdown text, related-skill hints.
Manta itself is not installed (no caller is), so caller behaviour is judged by inspection, never by a run."""
import collections, os, shutil, sys
import pysam
from lib import check, sh, block, finish

AFD = os.environ['AFDATA']; W = sys.argv[1]; SK = sys.argv[2]; SYN = sys.argv[3]
MD = f'{SK}/SKILL.md'
shutil.rmtree(W, ignore_errors=True); os.makedirs(W)
PD = f'{AFD}/derived/planted_dups.bam'
def c(args, bam): return int(sh(f'samtools view -c {args} {bam}')[1])

print('== A. the trap the first audit hit: -F 1024 on an unmarked BAM')
check('unmarked planted BAM: 500 records, 0 dup-flagged, plain -F 1024 keeps 500 (silent no-op)', c('', PD) == 500 and c('-f 1024', PD) == 0 and c('-F 1024', PD) == 500)
txt = open(MD, encoding='utf-8').read()
i = txt.index('### Remove Duplicates')
check('text now warns BEFORE the command that -F 1024 silently removes nothing on an unmarked BAM', 'silently removes nothing' in txt[i:i + 700])
# the extracted snippet, on three kinds of input: unmarked coordinate-sorted, unmarked NAME-sorted, unmarked unsorted (shuffled)
snip = block(MD, 'Remove Duplicates', 'bash')
def dedup(label, src):
    d = f'{W}/{label}'; os.makedirs(d); shutil.copy(src, f'{d}/input.bam')
    rc, so, se = sh(snip, cwd=d)
    n = int(sh(f'samtools view -c {d}/nodup.bam')[1]) if os.path.exists(f'{d}/nodup.bam') else -1
    return rc, n, se
rc, n, se = dedup('coord', PD)
check('snippet on coordinate-sorted unmarked BAM: 400 kept', rc == 0 and n == 400, f'rc={rc} n={n}')
sh(f'samtools sort -n -o {W}/pd_name.bam {PD}')
rc, n, se = dedup('name', f'{W}/pd_name.bam')
check('snippet on NAME-sorted unmarked BAM: 400 kept', rc == 0 and n == 400, f'rc={rc} n={n} err={se.strip()[:80]}')
sh(f'(samtools view -H {PD}; samtools view {PD} | shuf --random-source=<(yes)) | samtools view -b -o {W}/pd_shuf.bam - ')
check('shuffled fixture is a valid 500-record BAM, header @HD not coordinate-sorted after shuffle', c('', f'{W}/pd_shuf.bam') == 500)
rc, n, se = dedup('shuf', f'{W}/pd_shuf.bam')
check('snippet on shuffled (unsorted, order random) unmarked BAM: 400 kept', rc == 0 and n == 400, f'rc={rc} n={n} err={se.strip()[:100]}')
# duplicates of the Alignment-of-interest: a template loses BOTH mates (no orphans created by dedup)
cnt = collections.Counter(r.query_name for r in pysam.AlignmentFile(f'{W}/coord/nodup.bam'))
check('after markdup+-F 1024 every remaining template still has both mates', set(cnt.values()) == {2}, f'{len(cnt)} templates, sizes {sorted(set(cnt.values()))}')

print('\n== B. the SV half of the request')
S = SYN
supp_all = c('-f 2048', S)
for a, keep in [('-F 1024', True), ('-F 3332 -q 30', False), ('-F 2308', False), ('-F 3328 -q 1', False), ('-F 2304', False), ('-F 1280 -q 1', True)]:
    n = c(f'-f 2048 {a}', S)
    check(f'synthetic flags: {a} {"keeps" if keep else "removes"} supplementary records ({supp_all} present)', (n > 0) == keep, f'{n}')
i = txt.index('SV calling: KEEP supplementary')
check('text warns SV callers need supplementary reads and gives -F 1024 only', 'NOT -F 2304, 2308, 3328 or 3332' in txt[i:i + 200] and 'Cost of getting this wrong' in txt)
print('   text on -f 2 / -q for SV callers:', [l.strip() for l in txt.splitlines() if 'SV' in l and ('-f 2' in l or 'proper' in l.lower() or 'discordant' in l.lower())])
has_disc = 'discordant' in txt.lower()
check('text explains that -f 2 (proper pair) would also discard the discordant-pair SV signal', has_disc, 'no mention of discordant pairs' if not has_disc else '')
g = f'{AFD}/1000g/HG00349.chr20_1400000-1500000.bam'
print(f'   real 1000G BAM: supplementary {c("-f 2048", g)}, not-proper-pair mapped {c("-F 2 -F 4", g)} of {c("", g)}; -F 1024 keeps {c("-F 1024", g)}, -f 2 -F 3332 -q 30 keeps {c("-f 2 -F 3332 -q 30", g)}')

print('\n== C. orphaned mates after read-level filtering (not addressed in the text)')
sh(f'samtools view -b -F 3332 -q 30 -o {W}/f.bam {g}')
cn = collections.Counter(); meta = {}
for r in pysam.AlignmentFile(f'{W}/f.bam'):
    cn[r.query_name] += 1; meta[r.query_name] = r.flag
orph = sum(1 for q, n in cn.items() if n == 1 and meta[q] & 1 and not meta[q] & 8)
print(f'   1000G after -F 3332 -q 30: {orph} single-record templates whose mate was mapped (of {len(cn)} templates)')
mention = [l for l in txt.splitlines() if any(w in l.lower() for w in ('orphan', 'singleton', 'fixmate'))]
print('   lines mentioning orphan/singleton/fixmate in SKILL.md:', len(mention), [m.strip()[:80] for m in mention][:3])

print('\n== D. "Primary is not unique"')
rna = f'{AFD}/human/test.rna.paired_end.sorted.bam'
p = c('-F 2304', rna); nh = c("-F 2304 -e '[NH] > 1'", rna); q255 = c('-F 2304 -q 255', rna)
check('STAR real BAM: -F 2304 keeps multi-mapped primaries (text: "Primary is not unique")', nh > 0 and q255 == p - nh, f'primary {p}, of which NH>1 {nh}; -q 255 {q255}')
finish()
