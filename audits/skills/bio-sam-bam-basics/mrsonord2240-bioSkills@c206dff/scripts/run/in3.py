"""Input 3 (Edge): hand-built SYNTHETIC alignments covering the corners of the SAM spec.
Prompt: 'This BAM came from a pipeline I do not trust: unmapped reads with positions, secondary/supplementary records,
hard-clipped reads, RNA introns, MAPQ 255/0, a 66,000-op CIGAR, and there is also an empty BAM. Explain each read's
FLAG and CIGAR, tell me how many reference/query bases each consumes, and make sure my view/pysam commands behave.'
"""
import os, re, sys, subprocess
os.environ['AUDIT_INPUT'] = '3'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chk import check, note, sh
import pysam

RUN = os.path.dirname(os.path.abspath(__file__))
S = RUN + '/data/synth'
sh(f'python {RUN}/make_synth.py')
rc, o, e = sh(f'samtools sort -o {S}/synth.bam {S}/synth.sam && samtools index {S}/synth.bam && samtools view -c {S}/synth.bam')
check('synthetic SAM -> sorted+indexed BAM; 15 records', o.strip() == '15', f'{o.strip()} {e.strip()[:100]}')

# ---------- independent CIGAR model straight from the SAM spec table (Sec 1.4.6) ----------
CONSUMES_QUERY = set('MIS=X')
CONSUMES_REF = set('MDN=X')
def parse(c):
    return [(int(n), op) for n, op in re.findall(r'(\d+)([MIDNSHP=X])', c)]
def spec_lengths(c):
    p = parse(c)
    q = sum(n for n, o in p if o in CONSUMES_QUERY)
    q_with_hard = q + sum(n for n, o in p if o == 'H')
    r = sum(n for n, o in p if o in CONSUMES_REF)
    lead = 0
    for n, o in p:
        if o == 'H': continue
        if o == 'S': lead += n
        break
    trail = 0
    for n, o in reversed(p):
        if o == 'H': continue
        if o == 'S': trail += n
        break
    return q, q_with_hard, r, lead, trail

# the usage-guide's own example strings
for cig, exp_q, exp_r in (('50M2I30M', 82, 80), ('10M2I30M5D20M', 62, 65)):
    q, qh, r, *_ = spec_lengths(cig)
    a = pysam.AlignedSegment()
    a.cigarstring = cig
    a.query_sequence = 'A' * q
    a.reference_start = 0
    check(f'usage-guide CIGAR {cig}: spec query={exp_q}, ref={exp_r}; pysam reference_length agrees',
          (q, r) == (exp_q, exp_r) and a.reference_length == r and a.query_length == q, f'{q},{r} pysam ref_len={a.reference_length}')

recs = {}
with pysam.AlignmentFile(S + '/synth.bam', 'rb') as bam:
    for r in bam.fetch(until_eof=True):
        recs[r.query_name + ('/2' if r.is_read2 else '')] = r
    check('until_eof fetch returns all 15 records incl. the unplaced unmapped read', len(recs) == 15, len(recs))

# ---------- per-read consumption + attribute semantics ----------
for name, r in recs.items():
    if r.cigarstring is None:
        continue
    q, qh, rl, lead, trail = spec_lengths(r.cigarstring) if len(r.cigartuples) < 100 else spec_lengths(r.cigarstring)
    seq_len = 0 if r.query_sequence is None else len(r.query_sequence)
    ok = (r.reference_length == rl and r.reference_end == r.reference_start + rl and r.infer_read_length() == qh)
    if r.query_sequence is not None:
        ok &= (r.query_length == q == seq_len)
        ok &= (r.query_alignment_start == lead and r.query_alignment_end == q - trail)
        ok &= (len(r.get_reference_positions()) == sum(n for n, o in parse(r.cigarstring) if o in 'M=X'))
    check(f'{name}: pysam lengths/attributes match spec CIGAR model', ok,
          f'cigar={r.cigarstring[:24]} ref_len={r.reference_length} (spec {rl}) qlen={r.query_length} (spec {q}) infer_read_length={r.infer_read_length()} (spec incl H {qh})')

r = recs['r2_spliced']
pos = r.get_reference_positions()
check('N (intron) is NOT counted as covered: get_reference_positions has 50 entries though reference_end-start=1050 (Skill claim)',
      len(pos) == 50 and r.reference_end - r.reference_start == 1050, f'{len(pos)} positions, span {r.reference_end - r.reference_start}')
check('N jump visible in positions: 128 -> 1129 (0-based; POS 100 -> 0-based 99, 30M ends at 128)', pos[29] == 128 and pos[30] == 1129, f'{pos[29]}, {pos[30]}')
r = recs['r3_hardclip']
check('hard clip: bases absent from SEQ (query_length 30) but infer_read_length 50 (Skill: "sequence not in SEQ")', r.query_length == 30 and r.infer_read_length() == 50, f'{r.query_length}/{r.infer_read_length()}')
r = recs['r1_clips_indels']
check('soft clip bases stay in SEQ (query_length 56) while query_alignment_length 47', r.query_length == 56 and r.query_alignment_length == 47, f'{r.query_length}/{r.query_alignment_length}')
check('reference_end for 5S20M2I10M3D15M4S at POS 10 is 57 (0-based excl); 1-based last base 57', r.reference_end == 57 and r.reference_start == 9, (r.reference_start, r.reference_end))

# ---------- unmapped with a position ----------
r = recs['r4_unmapped_placed']
check('unmapped-but-placed read: is_unmapped, reference_name ctg1, reference_start 49 (POS 50 - 1), cigar None, reference_end None',
      r.is_unmapped and r.reference_name == 'ctg1' and r.reference_start == 49 and r.cigarstring is None and r.reference_end is None,
      (r.reference_name, r.reference_start, r.cigarstring, r.reference_end))
n_fetch = [x.query_name for x in pysam.AlignmentFile(S + '/synth.bam').fetch('ctg1', 45, 55)]
rc, o, e = sh(f'samtools view {S}/synth.bam ctg1:46-55 | cut -f1')
check('region query returns the placed unmapped read (both samtools and pysam)', 'r4_unmapped_placed' in o.split() and 'r4_unmapped_placed' in n_fetch, f'{o.split()} / {n_fetch}')
rc, o, e = sh(f'samtools view -c -F 4 {S}/synth.bam; samtools view -c -f 4 {S}/synth.bam; samtools idxstats {S}/synth.bam')
note('-F 4 count, -f 4 count, idxstats', o.replace('\n', ' | '))
with pysam.AlignmentFile(S + '/synth.bam') as bam:
    note('view_bam.py-style stats: bam.mapped / bam.unmapped (idxstats-derived)', f'{bam.mapped} / {bam.unmapped}; iteration count {sum(1 for _ in bam)}')
    check('bam.mapped counts records not flagged unmapped (13) and bam.unmapped 2 (placed + unplaced)', (bam.mapped, bam.unmapped) == (13, 2), (bam.mapped, bam.unmapped))
r = recs['r5_unmapped_unplaced']
check('unplaced unmapped: reference_name None, reference_id -1, reference_start -1', r.reference_name is None and r.reference_id == -1 and r.reference_start == -1, (r.reference_name, r.reference_id, r.reference_start))

# ---------- secondary/supplementary, seq * ----------
r = recs['r6_secondary_noseq']
check('secondary record with SEQ/QUAL "*": query_sequence None, query_qualities None (Skill snippet prints "None"), is_secondary', r.is_secondary and r.query_sequence is None and r.query_qualities is None, (r.query_sequence, r.query_qualities))
rc, o, e = sh(f'samtools view {S}/synth.bam | awk \'$1=="r6_secondary_noseq"{{print $10, $11}}\'')
check('samtools view prints "* *" for absent SEQ/QUAL', o.strip() == '* *', o.strip())
r = recs['r7_supplementary']
check('supplementary flag 2048: is_supplementary and not is_secondary; SA tag readable', r.is_supplementary and not r.is_secondary and r.get_tag('SA').startswith('ctg2,100,+'), r.get_tag('SA'))
rc, a, e = sh(f'samtools view -c -F 256 {S}/synth.bam; samtools view -c -F 2304 {S}/synth.bam; samtools view -c -F 2048 {S}/synth.bam')
check('Skill: -F 256 removes secondary only (14), -F 2304 removes both (13), -F 2048 removes supplementary (14)', a.split() == ['14', '13', '14'], a.split())
rc, a, e = sh(f'samtools flags 2304; samtools flags 2048; samtools flags 1536')
note('flags 2304/2048/1536', a.replace('\n', ' | '))
# each record flag: samtools flags == spec
SPEC = [(1, 'PAIRED'), (2, 'PROPER_PAIR'), (4, 'UNMAP'), (8, 'MUNMAP'), (16, 'REVERSE'), (32, 'MREVERSE'), (64, 'READ1'), (128, 'READ2'), (256, 'SECONDARY'), (512, 'QCFAIL'), (1024, 'DUP'), (2048, 'SUPPLEMENTARY')]
okf = True
for f in sorted({r.flag for r in recs.values()}):
    o = sh(f'samtools flags {f}')[1].split('\t')[2].strip()
    okf &= o == ','.join(n for b, n in SPEC if f & b)
check('samtools flags matches spec for every synthetic flag (0,4,99,147,256,512+1024,2048)', okf, sorted({r.flag for r in recs.values()}))

# ---------- MAPQ ----------
rc, a, e = sh(f'samtools view -q 30 {S}/synth.bam | cut -f1,5 | tr "\\t" " " | tr "\\n" ";"')
note('view -q 30 keeps', a)
rc, a, e = sh(f'samtools view -c -q 255 {S}/synth.bam; samtools view -c -q 1 {S}/synth.bam; samtools view -c -q 0 {S}/synth.bam')
note('-q 255 / -q 1 / -q 0 counts', a.split())
check('MAPQ 255 read: mapping_quality 255; a -q 255 filter keeps exactly it', recs['r8_mapq255'].mapping_quality == 255 and a.split()[0] == '1', a.split())
check('MAPQ 0 multimapper: mapping_quality 0', recs['r9_mapq0_multi'].mapping_quality == 0, recs['r9_mapq0_multi'].mapping_quality)

# ---------- mate fields, TLEN sign ----------
a = recs['pair1']; b = recs['pair1/2']
check('pair: TLEN +90 on leftmost, -90 on rightmost; PNEXT cross-referenced; RNEXT "="', a.template_length == 90 and b.template_length == -90 and a.next_reference_start == 59 and b.next_reference_start == 19 and a.next_reference_name == 'ctg1',
      (a.template_length, b.template_length, a.next_reference_start, b.next_reference_start))
check('Skill flag 99 = READ1 fwd, mate reverse; 147 = READ2 reverse: pysam is_reverse/mate_is_reverse consistent', (not a.is_reverse) and a.mate_is_reverse and b.is_reverse and (not b.mate_is_reverse), 'ok')
# spec: TLEN = rightmost end - leftmost start + 1  (1-based)
check('TLEN equals rightmost end - leftmost start + 1 computed from CIGAR', (b.reference_end) - (a.reference_start) == 90, (b.reference_end, a.reference_start))

# ---------- =/X, P, big CIGAR ----------
r = recs['r12_eqx']
check('=/X CIGAR 10=1X9= : cigartuples ops 7,8,7 (pysam codes) and reference_length 20', [c for c, n in r.cigartuples] == [7, 8, 7] and r.reference_length == 20, r.cigartuples)
r = recs['r13_padding']
check('P consumes neither: 5M2P5M -> ref len 10, query len 10', r.reference_length == 10 and r.query_length == 10, (r.reference_length, r.query_length))
r = recs['r14_bigcigar']
check('66000-op CIGAR read through sort->BAM: pysam sees 66000 ops (htslib expands the CG tag), ref_len 33000, query_len 66000',
      len(r.cigartuples) == 66000 and r.reference_length == 33000 and r.query_length == 66000, (len(r.cigartuples), r.reference_length, r.query_length))
rc, o, e = sh(f'samtools view {S}/synth.bam ctg3:1-10 | cut -f6 | head -c 20; echo; samtools view {S}/synth.bam ctg3:1-10 | cut -f6 | wc -c')
note('samtools view CIGAR text of 66000 ops (first 20 chars, then length)', o.replace('\n', ' | '))
rc, o, e = sh(f'samtools view -c {S}/synth.bam ctg3:100-200')
check('region query on the 66000-op read works (reference span 1..33000)', o.strip() == '1', o.strip())
r = recs['r15_dup_qcfail']
check('flag 1536 -> is_duplicate and is_qcfail true (bits 0x400 and 0x200)', r.is_duplicate and r.is_qcfail, r.flag)

# ---------- tag claims on synthetic data ----------
r = recs['r1_clips_indels']
check('SA:Z tag string structure "rname,pos,strand,CIGAR,mapQ,NM;" (Skill calls it "Comma-list of supplementary coords")', recs['r7_supplementary'].get_tag('SA').count(';') == 1 and len(recs['r7_supplementary'].get_tag('SA').rstrip(';').split(',')) == 6, recs['r7_supplementary'].get_tag('SA'))
# calmd on =/X
rc, o, e = sh(f'samtools calmd -e {S}/synth.bam {S}/synth.fa 2>&1 | grep r12_eqx | cut -f6,12-')
note('samtools calmd -e on =/X read (does calmd rebuild MD/NM from = / X ops?)', o.strip())
rc, o, e = sh(f'samtools calmd {S}/synth.bam {S}/synth.fa 2>&1 | grep r12_eqx | cut -f6,12-')
check('calmd (no -e) rebuilds MD/NM for =/X read: NM:i:1 and MD 10 + mismatch + 9', 'NM:i:1' in o and 'MD:Z:' in o, o.strip())

# ---------- empty BAM ----------
open(S + '/empty.sam', 'w').write('@HD\tVN:1.6\tSO:coordinate\n@SQ\tSN:ctg1\tLN:300\n')
sh(f'rm -f {S}/empty.bam {S}/empty.bam.bai; samtools view -b -o {S}/empty.bam {S}/empty.sam')
rc, o, e = sh(f'samtools view -c {S}/empty.bam; samtools view -H {S}/empty.bam | wc -l; samtools view {S}/empty.bam | wc -l')
check('empty BAM: view -c 0, header 2 lines (+PG) , no records', o.split()[0] == '0' and o.split()[2] == '0', o.split())
with pysam.AlignmentFile(S + '/empty.bam') as bam:
    check('empty BAM: pysam iteration yields 0 reads without error', sum(1 for _ in bam) == 0, 'ok')
rc, o, e = sh(f'python {RUN}/skill/examples/view_bam.py {S}/empty.bam; echo rc=$?')
check('view_bam.py on an empty, unindexed BAM works', 'Mapped' in o, (o + e)[-160:])
sh(f'samtools index {S}/empty.bam')
rc, o, e = sh(f'python {RUN}/skill/examples/view_bam.py {S}/empty.bam; echo rc=$?')
check('view_bam.py on an empty, indexed BAM prints References: 1 / Mapped: 0 / Unmapped: 0', 'Mapped: 0' in o and 'Unmapped: 0' in o, o.replace('\n', ' | '))
# view_bam.py on the synthetic BAM: unmapped reads print reference_start -1?
rc, o, e = sh(f'python {RUN}/skill/examples/view_bam.py {S}/synth.bam 20')
lines = [l for l in o.splitlines() if l.startswith('r')]
note('view_bam.py rows for unmapped/hard-clip records', ' || '.join(l for l in lines if 'r4' in l or 'r5' in l or 'r6' in l))
check('view_bam.py prints unmapped record as "None:-1 ... None" (no crash, but no indication it is unmapped)', any(l.startswith('r5') and 'None:-1' in l for l in lines), [l for l in lines if l.startswith('r5')])
# SAM-in with view_bam.py (mode 'rb')
rc, o, e = sh(f'python {RUN}/skill/examples/view_bam.py {S}/synth.sam 2; echo rc=$?')
note('view_bam.py given a SAM (opens with rb)', (o + e).replace('\n', ' | ')[-250:])
