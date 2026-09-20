"""Input 5 (Stress / multi-part): MAPQ portability, optional tags and @PG provenance across five aligners.
Prompt: 'I received BAMs from bwa, bwa-mem2, minimap2, bowtie2, hisat2 and STAR. For each: which MAPQ scale is it, what -q
threshold is sane, which of NM/MD/NH/HI/RG/MC/ms are present, which aligner made it (@PG), and does fixmate/markdup
behave the way the Skill says?'   Data: SYNTHETIC repeat-containing genome + reads (make_reads.py), plus the real RNA BAM.
"""
import collections, os, re, sys
os.environ['AUDIT_INPUT'] = '5'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chk import check, note, sh
import pysam

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = RUN + '/data/aln'


def mapqs(bam, extra=''):
    """the Skill's own command: samtools view input.bam | awk '{print $5}' | sort -un | head  (+ counts)"""
    rc, o, e = sh(f"samtools view {extra} {A}/{bam} | awk '{{print $5}}' | sort -n | uniq -c")
    return {int(l.split()[1]): int(l.split()[0]) for l in o.splitlines()}


def tags(bam, region=''):
    rc, o, e = sh(f"samtools view {A}/{bam} {region} | cut -f12- | tr '\\t' '\\n' | cut -d: -f1 | sort | uniq -c")
    return {l.split()[1]: int(l.split()[0]) for l in o.splitlines()}


n_reads = int(sh(f'samtools view -c -F 256 {A}/bwa.bam')[1])
check('bwa BAM has 5000 primary records (2500 pairs)', n_reads == 5000, n_reads)
Q = {b: mapqs(b + '.bam') for b in ('bwa', 'bwamem2', 'mm2', 'bt2', 'hs2', 'star')}
for b, d in Q.items():
    note(f'MAPQ histogram {b}', dict(sorted(d.items())))

# ---- the Skill's MAPQ table, row by row
for b in ('bwa', 'bwamem2', 'mm2'):
    check(f'{b}: MAPQ scale 0-60 with 60 the maximum and present', max(Q[b]) == 60 and min(Q[b]) == 0 and 60 in Q[b], f'max {max(Q[b])} n60={Q[b].get(60)}')
check('HISAT2: 0-60 scale, unique = 60 (values seen are within {0,1,60})', set(Q['hs2']) <= {0, 1, 60} and 60 in Q['hs2'], sorted(Q['hs2']))
check('Bowtie2: 0-42, nothing above 42', max(Q['bt2']) <= 42 and 42 in Q['bt2'], f'max {max(Q["bt2"])}')
share42 = Q['bt2'].get(42, 0) / sum(Q['bt2'].values())
check('Bowtie2 42 is the top and most common MAPQ, as the fixed Skill says (majority of records)', share42 > 0.5 and Q['bt2'][42] == max(Q['bt2'].values()), f'MAPQ 42 = {share42:.1%} of records; Skill text says 97% in its run: {"97%" in open(RUN + "/skill/SKILL.md", encoding="utf-8").read()}')
QL = mapqs('bt2loc.bam')
note('MAPQ histogram bowtie2 --local', dict(sorted(QL.items())))
share44 = QL.get(44, 0) / sum(QL.values())
check('Bowtie2 --local: MAPQ up to 44 (Skill "0-44 with --local", 44 the top and common); nothing above 44', max(QL) == 44 and share44 > 0.5, f'max {max(QL)}; 44 = {share44:.1%}')
rc, o, e = sh(f'samtools view -c -q 60 {A}/bt2.bam; samtools view -c -q 23 {A}/bt2.bam; samtools view -c -q 30 {A}/bt2.bam')
a = [int(x) for x in o.split()]
check('Bowtie2 "-q 60 drops everything"', a[0] == 0, a)
note('bowtie2 -q 23 / -q 30 retained', a[1:])
check('STAR MAPQ set is exactly {0,1,3,255}', set(Q['star']) <= {0, 1, 3, 255} and 255 in Q['star'], sorted(Q['star']))
# STAR MAPQ vs NH
rc, o, e = sh(f"samtools view {A}/star.bam | awk '{{for(i=12;i<=NF;i++) if($i ~ /^NH:i:/){{split($i,a,\":\"); print $5, a[3]}}}}' | sort | uniq -c")
mp = {(int(l.split()[1]), int(l.split()[2])): int(l.split()[0]) for l in o.splitlines()}
note('STAR (MAPQ, NH) pairs', mp)
ok = all((nh == 1 and q == 255) or (nh == 2 and q == 3) or (nh in (3, 4) and q == 1) or (nh >= 5 and q == 0) for (q, nh) in mp)
check('STAR MAPQ = f(NH): 1 locus->255, 2->3, 3-4->1, >=5->0 (STARmanual; Skill lists 0,1,3,255)', ok and any(nh >= 5 for _, nh in mp), mp)
rc, o, e = sh(f'samtools view -c -q 30 {A}/star.bam; samtools view -c -q 255 {A}/star.bam; samtools view -c -q 60 {A}/star.bam')
a = [int(x) for x in o.split()]
check('STAR: "-q 30 accidentally keeps unique only too" and -q 255 keeps unique only (same counts); -q 60 keeps unique too', a[0] == a[1] == a[2] == Q['star'][255], f'{a} vs n255={Q["star"][255]}')
# 255 spec meaning on a non-STAR BAM
check('bwa-family BAMs never emit 255 (so 255 there could only mean "unavailable" per SAM spec)', 255 not in Q['bwa'] and 255 not in Q['mm2'], 'ok')

# ---- HI base
def hi(b):
    rc, o, e = sh(f"samtools view {A}/{b}.bam | grep -o 'HI:i:[0-9]*' | sort | uniq -c")
    return o.replace('\n', ' ')
h1, h0 = hi('star'), hi('star_ih0')
check('STAR HI:i is 1-based by default and 0-based with --outSAMattrIHstart 0', 'HI:i:0' not in h1 and 'HI:i:1' in h1 and 'HI:i:0' in h0, f'default: {h1} | ihstart0: {h0}')

# ---- tags by aligner
T = {b: tags(b + '.bam') for b in ('bwa', 'bwamem2', 'mm2', 'bt2', 'hs2', 'star')}
for b, d in T.items():
    note(f'tags {b}', d)
check('NM:i and MD:Z emitted by bwa (Skill: "NM/MD | bwa")', 'NM' in T['bwa'] and 'MD' in T['bwa'], list(T['bwa']))
check('minimap2 -ax sr emits NM but no MD by default (so MD needs calmd or --MD)', 'NM' in T['mm2'] and 'MD' not in T['mm2'], list(T['mm2']))
check('STAR emits NH and HI; HISAT2 emits NH (Skill table)', 'NH' in T['star'] and 'HI' in T['star'] and 'NH' in T['hs2'], (list(T['star']), list(T['hs2'])))
check('bwa mem -R sets RG:Z on every record and an @RG header line', T['bwa'].get('RG') == sum(T['bwa'].values()) / len(T['bwa']) * 0 + T['bwa'].get('RG') and T['bwa'].get('RG') == int(sh(f'samtools view -c {A}/bwa.bam')[1]) and '@RG\tID:rgA' in sh(f'samtools view -H {A}/bwa.bam')[1],
      f"RG on {T['bwa'].get('RG')} records")
rc, o, e = sh(f'samtools view -H {A}/hs2.bam | grep -c "^@PG"; samtools view {A}/hs2.bam | grep -c "XS:A"')
note('hisat2 @PG count / XS:A records on unspliced DNA reads', o.split())

# ---- @PG: which aligner made it (Skill: samtools view -H | grep '^@PG' | head -1)
exp = {'bwa': 'bwa', 'bwamem2': 'bwa-mem2', 'mm2': 'minimap2', 'bt2': 'bowtie2', 'hs2': 'hisat2', 'star': 'STAR'}
for b, name in exp.items():
    rc, o, e = sh(f"samtools view -H {A}/{b}.bam | grep '^@PG' | head -1")
    check(f"'@PG | head -1' names the aligner for {b}", name.lower() in o.lower(), o.strip()[:90])
# PP chain
rc, o, e = sh(f'samtools view -H {A}/chain.bam | grep "^@PG"')
pg = [dict(kv.split(':', 1) for kv in l.split('\t')[1:] if ':' in kv) for l in o.splitlines()]
note('chain.bam @PG (ID, PP)', [(p['ID'], p.get('PP')) for p in pg])
chain_ok = pg[0].get('PP') is None and all(pg[i].get('PP') == pg[i - 1]['ID'] for i in range(1, len(pg)))
check('@PG chain links through PP (bwa -> samtools -> samtools.1 -> ...), linear, first has no PP', chain_ok and len(pg) == 6, [(p['ID'], p.get('PP')) for p in pg])
check('Skill example IDs are illustrative: real first samtools ID is "samtools" (no ".1"), and bwa ID is "bwa" not "bwa-mem"', pg[1]['ID'] == 'samtools' and pg[0]['ID'] == 'bwa', [p['ID'] for p in pg])

# ---- fixmate -m / markdup tags
Tc = tags('chain.bam')
check('samtools fixmate -m adds ms:i and MC:Z (lowercase "ms", as Skill says)', 'ms' in Tc and 'MC' in Tc and 'MS' not in Tc, {k: v for k, v in Tc.items() if k in ('ms', 'MC', 'MS')})
rc, o, e = sh(f'samtools view -c -f 1024 {A}/chain.bam')
note('markdup flagged reads on random-position synthetic reads', o.strip())
err = open(A + '/nomc_md.err').read().strip()
check('markdup on a BAM without ms/MC fails LOUDLY (rc!=0, message says to run fixmate) -- Skill says "silently wrong (markdup marking nothing)"',
      'ms score tag' in err, err[:120])
rc, o, e = sh(f'cd {A}; samtools view -h -x MC chain.bam | samtools markdup - noMC_only.bam 2>&1 | head -2; echo rc=${{PIPESTATUS[1]}}')
note('markdup with ms present but MC removed', o.strip().replace('\n', ' | '))
rc, o, e = sh(f'cd {A}; samtools view -h -x ms chain.bam | samtools markdup - noms_only.bam 2>&1 | head -2; echo rc=${{PIPESTATUS[1]}}')
note('markdup with MC present but ms removed', o.strip().replace('\n', ' | '))

# ---- Skill claims about MD / M vs =/X for bcftools
def mp(bam, extra=''):
    rc, o, e = sh(f"cd {A}; samtools view -h {extra} {bam} | bcftools mpileup -f g.fa -Ov - 2>/dev/null | grep -v '^##' | md5sum; bcftools mpileup -f g.fa {bam} 2>/dev/null | bcftools call -mv 2>/dev/null | grep -vc '^#'")
    return o.split()
a = mp('bwa.bam')
b = mp('bwa.bam', '-x MD -x NM')
check('bcftools mpileup output identical with and without MD/NM tags (Skill: "MD:Z required by ... bcftools mpileup BAQ" is not true for mpileup)', a[0] == b[0], f'md5 with={a[0][:8]} without={b[0][:8]}; variant records {a[1]}/{b[1]}')
c = mp('mm2.bam')
d = mp('mm2eqx.bam')
note('mpileup on M-CIGAR minimap2 vs --eqx (=/X) BAM: md5, #variants', (c, d))
rc, o, e = sh(f'cd {A}; samtools view mm2eqx.bam | cut -f6 | grep -c "[=X]"; samtools view mm2.bam | cut -f6 | grep -c "[=X]"')
check('minimap2 --eqx BAM really carries =/X ops (and default does not)', int(o.split()[0]) > 0 and int(o.split()[1]) == 0, o.split())
check('bcftools mpileup tolerates =/X CIGARs: pileup identical to the M-CIGAR alignment (Skill: "bcftools / Picard often need M")', c[0] == d[0], f'{c[0][:8]} vs {d[0][:8]}')
# pysam get_tag semantics
with pysam.AlignmentFile(A + '/bwa.bam') as bam:
    r = next(bam)
    ok = r.has_tag('NM') and isinstance(r.get_tag('NM'), int)
    try:
        r.get_tag('ZZ'); keyerr = False
    except KeyError:
        keyerr = True
check("pysam read.get_tag('NM') returns int; missing tag raises KeyError (Skill points at get_tag)", ok and keyerr, r.get_tags()[:3])
rc, o, e = sh(f"samtools view {A}/bwa.bam | head -1 | tr '\\t' '\\n' | tail -7")
check("Skill tag-inspection command `samtools view f | head -1 | tr '\\t' '\\n'` lists one field per line", len(o.strip().splitlines()) == 7 and o.strip().splitlines()[-1].startswith(('RG', 'AS', 'XS', 'MC', 'MD', 'NM', 'XA', 'SA')), o.replace('\n', ' '))

# ---- real RNA BAM (nf-core) tags vs table
RNA = os.environ['AFDATA'] + '/human/test.rna.paired_end.sorted.bam'
rc, o, e = sh(f"samtools view {RNA} | cut -f12- | tr '\\t' '\\n' | cut -d: -f1 | sort | uniq -c; samtools view -H {RNA} | grep '^@PG' | head -2 | cut -c1-80")
note('real RNA BAM tags/PG', o.replace('\n', ' | '))
rc, o, e = sh(f"samtools view {RNA} | awk '$6 ~ /N/' | head -1 | cut -f1-9 | tr '\\t' ' '; samtools view {RNA} | awk '$6 ~ /N/' | wc -l")
note('real RNA BAM spliced reads (CIGAR with N)', o.replace('\n', ' | '))
