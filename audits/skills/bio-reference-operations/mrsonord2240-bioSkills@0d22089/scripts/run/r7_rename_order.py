#!/usr/bin/env python
"""NEW INPUT 7: multi-contig headers with mismatched names / lengths / order and a CRAM round trip, on MY planted 3-contig reference (planted.fa).
The SKILL's 'Rename Contigs Without Re-aligning' recipe (awk + samtools reheader + Check line) is run verbatim on a BAM that has pairs whose mate is
on another contig, an unplaced-mate read (RNAME set, unmapped) and a fully unmapped read; then on the CRAM made from it (with M5 in the @SQ lines)."""
import os, shutil, sys
sys.path.insert(0, '/mnt/openscience/audits/bio-reference-operations/run')
from auditlib import *
import pysam
D = f'{W}/work/r7'; shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
P = f'{W}/data/planted'
shutil.copy(f'{P}/planted.fa', f'{D}/planted.fa')
fa = parse_fasta(f'{D}/planted.fa')
def blk(n): return open(f'{W}/snippets/{n}.txt').read()
lines = blk('skill_12_bash').split('\n')
i_start = next(i for i, l in enumerate(lines) if l.startswith('samtools view -H sample.bam | awk'))
i_end = next(i for i, l in enumerate(lines) if l.startswith('samtools reheader'))
recipe = '\n'.join(lines[i_start:i_end + 1])
chk = next(l for l in lines if l.startswith('diff <('))

# ---- build mix.bam: pairs across contigs, unmapped-with-position, fully unmapped ----
hd = {'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': 'ctgA', 'LN': 6000}, {'SN': 'ctgB', 'LN': 1500}, {'SN': 'ctgC', 'LN': 800}], 'PG': [{'ID': 'audit', 'PN': 'audit'}], 'RG': [{'ID': 'rg1', 'SM': 's1', 'PL': 'ILLUMINA'}]}
reads = []
def mk(out, name, tid, pos, seq, flag, ntid, npos, tlen=0, cig=None, mapq=60):
    a = pysam.AlignedSegment(out.header); a.query_name = name; a.query_sequence = seq; a.flag = flag; a.reference_id = tid; a.reference_start = pos
    a.mapping_quality = mapq if not flag & 4 else 0; a.cigartuples = cig if cig is not None else ([(0, len(seq))] if not flag & 4 else None)
    a.next_reference_id = ntid; a.next_reference_start = npos; a.template_length = tlen; a.query_qualities = pysam.qualitystring_to_array('I' * len(seq)); a.set_tag('RG', 'rg1'); return a
with pysam.AlignmentFile(f'{D}/mix_u.bam', 'wb', header=hd) as out:
    for k in range(30):                         # pairs: mate 1 on ctgA, mate 2 on ctgB (inter-contig)
        s1 = fa['ctgA'][100 + 10 * k:150 + 10 * k].upper().replace('N', 'A'); s2 = fa['ctgB'][300 + 10 * k:350 + 10 * k]
        out.write(mk(out, 'x%d' % k, 0, 100 + 10 * k, s1, 65, 1, 300 + 10 * k)); out.write(mk(out, 'x%d' % k, 1, 300 + 10 * k, s2, 129, 0, 100 + 10 * k))
    for k in range(10):                         # proper pairs on ctgA
        s1 = fa['ctgA'][2000 + 10 * k:2050 + 10 * k]; s2 = fa['ctgA'][2100 + 10 * k:2150 + 10 * k]
        out.write(mk(out, 'p%d' % k, 0, 2000 + 10 * k, s1, 99, 0, 2100 + 10 * k, 150)); out.write(mk(out, 'p%d' % k, 0, 2100 + 10 * k, s2, 147, 0, 2000 + 10 * k, -150))
    for k in range(5):                          # mapped read + unmapped mate placed at its position
        s1 = fa['ctgC'][100 + 10 * k:150 + 10 * k]
        out.write(mk(out, 'u%d' % k, 2, 100 + 10 * k, s1, 73, 2, 100 + 10 * k)); out.write(mk(out, 'u%d' % k, 2, 100 + 10 * k, 'ACGTACGTAC' * 5, 133, 2, 100 + 10 * k))
    for k in range(5):                          # fully unmapped
        out.write(mk(out, 'z%d' % k, -1, -1, 'ACGT' * 12, 77, -1, -1)); out.write(mk(out, 'z%d' % k, -1, -1, 'TTGA' * 12, 141, -1, -1))
# write() above needs sorted input: sort with samtools
sh('samtools sort -o mix.bam mix_u.bam && samtools index mix.bam && rm mix_u.bam', D)
n = int(sh('samtools view -c mix.bam', D)[1]); print('mix.bam records:', n)
check('fixture: 30 inter-contig pairs + 10 proper pairs + 5 mapped/unmapped-mate pairs + 5 unmapped pairs = 100 records', n == 100, n)
# ---- renamed reference planted_ren.fa: ctgA->1 ctgB->2 ctgC->3 (same sequences, same case) ----
sh("sed -e 's/^>ctgA/>1/' -e 's/^>ctgB/>2/' -e 's/^>ctgC/>3/' planted.fa > planted_ren.fa; samtools faidx planted_ren.fa", D)
open(f'{D}/map.tsv', 'w').write('ctgA\t1\nctgB\t2\nctgC\t3\n')
shutil.copy(f'{D}/mix.bam', f'{D}/sample.bam'); shutil.copy(f'{D}/mix.bam.bai', f'{D}/sample.bam.bai')
open(f'{D}/rec.sh', 'w').write(recipe + '\n')
rc, o, e = sh('bash rec.sh; echo rc=$?', D)
check('SKILL recipe (awk + reheader + index) on the mixed BAM: rc 0', 'rc=0' in o and os.path.exists(f'{D}/renamed.bam.bai'), o + e[:200])
def recs(bam): return [l.split('\t') for l in sh(f'samtools view {bam}', D)[1].splitlines()]
a = recs('mix.bam'); b = recs('renamed.bam')
m = {'ctgA': '1', 'ctgB': '2', 'ctgC': '3', '*': '*', '=': '=', '': ''}
ok = len(a) == len(b) == 100
if ok:
    for x, y in zip(a, b):
        ok &= (m[x[2]] == y[2] and m[x[6]] == y[6] and x[:2] + x[3:6] + x[7:] == y[:2] + y[3:6] + y[7:])
check('renamed.bam: every one of 100 records identical except RNAME/RNEXT mapped through the table (inter-contig mates, "=" mates, unmapped-with-position, "*" unmapped)', ok)
check('unmapped-with-position and fully unmapped reads survive (flags 4/8 present): flagstat mapped count unchanged', sh('samtools flagstat mix.bam | head -1', D)[1] .split()[0] == sh('samtools flagstat renamed.bam | head -1', D)[1].split()[0] and sh('samtools view -c -f 4 mix.bam', D)[1] == sh('samtools view -c -f 4 renamed.bam', D)[1])
rc, o, e = sh('picard ValidateSamFile I=renamed.bam R=planted_ren.fa MODE=SUMMARY IGNORE_WARNINGS=true 2>&1 | grep -E "No errors found|^ERROR" | head -3', D)
check('Picard 3.5.0 ValidateSamFile: renamed.bam vs reference with names 1/2/3: No errors found', 'No errors found' in o, o)
chkf = f'{D}/chk_ok.sh'; open(chkf, 'w').write('#!/bin/bash\n' + chk.replace('ref.fa.fai', 'planted_ren.fa.fai') + '\n')
rc, o, e = sh('bash chk_ok.sh', D); check('SKILL Check line prints OK against planted_ren.fa.fai', o.strip() == 'OK', o)

# ---- order / length / name mismatches: the Check line must NOT print OK ----
sh("samtools faidx planted_ren.fa 3 1 2 > order.fa; samtools faidx order.fa", D)              # same names, different order
sh("python3 - <<'E'\ns=open('planted_ren.fa').read().split('>')[1:]\nd={x.split(chr(10))[0]:''.join(x.split(chr(10))[1:]) for x in s}\nopen('len.fa','w').write('>1\\n'+d['1']+'\\n>2\\n'+d['2']+'A\\n>3\\n'+d['3']+'\\n')\nE\nsamtools faidx len.fa", D)
for nm, fai in (('order', 'order.fa.fai'), ('length', 'len.fa.fai'), ('oldnames', 'planted.fa.fai')):
    open(f'{D}/chk_{nm}.sh', 'w').write('#!/bin/bash\n' + chk.replace('ref.fa.fai', fai) + '\n')
    rc, o, e = sh(f'bash chk_{nm}.sh', D); check(f'SKILL Check line does NOT print OK for a reference with {nm} mismatch', 'OK' not in o.split('\n')[-2:] and o.strip() != '', o.strip()[:100].replace('\n', ' | '))
# what the downstream tools say for the order mismatch (informational: the SKILL is silent on reordering)
rc, o, e = sh('picard ValidateSamFile I=renamed.bam R=order.fa MODE=SUMMARY IGNORE_WARNINGS=true 2>&1 | grep -E "No errors found|ERROR|Exception|dictionar" | head -4', D)
print('    Picard vs reordered reference:', o.strip().replace('\n', ' | ')[:300])
rc, o, e = sh("mkdir -p go; cp order.fa order.fa.fai go/; cd go; samtools dict order.fa -o order.dict; gatk --java-options -Xmx2g CountReads -R order.fa -I ../renamed.bam 2>&1 | grep -i -E 'USER ERROR|incompatible|contigs|Reads' | grep -v -E '^ +java|INFO' | head -4 | cut -c1-300", D)
print('    GATK CountReads vs reordered reference:', o.strip().replace('\n', ' | ')[:300])

# ---- CRAM round trip with M5 in the header ----
sh('samtools view -C -T planted.fa -o mix.cram mix.bam && samtools index mix.cram', D)
hdr = sh('samtools view -H mix.cram | grep "^@SQ"', D)[1]
check('fixture: the CRAM made with -T carries M5 (and UR) in every @SQ line', hdr.count('M5:') == 3, hdr.replace('\t', ' ')[:200])
shutil.copy(f'{D}/mix.cram', f'{D}/sample.cram')
sh("samtools view -H sample.cram | awk -F'\\t' -v OFS='\\t' 'NR==FNR{m[$1]=$2; next} /^@SQ/{for(i=2;i<=NF;i++) if($i~/^SN:/){n=substr($i,4); if(n in m) $i=\"SN:\" m[n]}} {print}' map.tsv - > cram.hdr", D)
rc, o, e = sh('samtools reheader cram.hdr sample.cram > renamed.cram; echo rc=$?; samtools view -H renamed.cram | grep "^@SQ" | cut -f2-4', D)
print('    CRAM reheader:', o.strip().replace('\n', ' | ')[:250], '| stderr:', e.strip()[:200])
check('CRAM reheader (SKILL: works on CRAM): rc 0 and the @SQ names are 1/2/3 with the M5 tags of the original', 'rc=0' in o and 'SN:1' in o and 'SN:3' in o and 'M5:' in o, o + e[:150])
warn = 'Failed to populate reference' in e
print('    SKILL says reheader warns "Failed to populate reference" without REF_PATH/cache for the renamed reference; observed warning:', warn)
r_old = sh('samtools view -T planted.fa mix.cram | md5sum', D)[1].split()[0]
r_new = sh("samtools view -T planted_ren.fa renamed.cram | sed -e 's/\\tctgA\\t/\\t1\\t/' | md5sum", D)[1].split()[0]
print('    md5 decode original:', r_old[:8], ' renamed (RNAME normalised for the compare only):', r_new[:8])
# compare precisely with a python normaliser instead of sed: cut RNAME/RNEXT
a = [l.split('\t') for l in sh('samtools view -T planted.fa mix.cram', D)[1].splitlines()]; b = [l.split('\t') for l in sh('samtools view -T planted_ren.fa renamed.cram', D)[1].splitlines()]
ok = len(a) == len(b) == 100 and all(m[x[2]] == y[2] and m[x[6]] == y[6] and x[:2] + x[3:6] + x[7:] == y[:2] + y[3:6] + y[7:] for x, y in zip(a, b))
check('renamed CRAM decodes with the renamed reference (-T planted_ren.fa) to 100 records identical to the original apart from RNAME/RNEXT', ok, (len(a), len(b)))
rc, o, e = sh('samtools view -T planted.fa renamed.cram | wc -l', D)
print('    renamed CRAM decoded with the OLD-named reference:', rc, o.strip(), e.strip()[:200])
check('OBSERVATION: renamed CRAM + OLD-named reference does not decode silently (names no longer match): error text or 0 records', ('E::' in e or o.strip() == '0'), (o.strip(), e.strip()[:120]))
# length mismatch: CRAM decode with a reference whose ctgB is 1 base longer
rc, o, e = sh('samtools view -T len.fa renamed.cram | wc -l', D)
print('    renamed CRAM with the longer-ctg 2 reference:', rc, o.strip(), e.strip()[:200])
check('OBSERVATION: a longer contig-2 reference is only WARNED about (Header @SQ length mismatch) and the 100 records still decode, because CRAM checks the M5 of the slice region, not of the whole contig (a whole-contig M5 comparison needs the header M5 vs samtools dict)', 'length mismatch' in e and o.strip() == '100', e.strip()[:160])
# whole-contig identity is what samtools dict M5 gives: header M5 (from the CRAM) vs dict M5 of each candidate reference
hm5 = dict((l.split('	')[1][3:], l.split('	')[3][3:]) for l in sh('samtools view -H renamed.cram | grep "^@SQ"', D)[1].splitlines())
sh('samtools dict len.fa -o len.dict; samtools dict planted_ren.fa -o ren.dict', D)
dm5 = lambda f: dict((l.split('	')[1][3:], l.split('	')[3][3:]) for l in open(f'{D}/{f}').read().splitlines() if l.startswith('@SQ'))
check('SKILL advice "M5 is the only definitive reference-identity check": header M5 == samtools dict M5 for the right reference, and differs for the 1-base-longer contig 2 only', hm5 == dm5('ren.dict') and dm5('len.dict')['2'] != hm5['2'] and dm5('len.dict')['1'] == hm5['1'], (hm5, dm5('len.dict')))
# does reheader warn when nothing can resolve the renamed reference?
rc, o, e = sh('REF_PATH=/nonexistent REF_CACHE=/nonexistent samtools reheader cram.hdr sample.cram > renamed2.cram; echo rc=$?', D)
print('    reheader with REF_PATH/REF_CACHE pointing nowhere: rc/out', o.strip(), '| stderr:', e.strip()[:200])
# in-place claim is not made; samtools reheader -i exists? (informational)
summary()
