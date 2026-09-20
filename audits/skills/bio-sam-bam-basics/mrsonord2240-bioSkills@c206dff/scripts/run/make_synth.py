"""SYNTHETIC data (not real reads): reference + hand-written SAM with edge cases, ground truth known from the SAM spec.
Writes data/synth/{synth.fa, synth.sam, truth.json}. Seeded (random.Random(20260920)) so runs are reproducible."""
import json, os, random, re
RUN = os.path.dirname(os.path.abspath(__file__))
OUT = RUN + '/data/synth'
os.makedirs(OUT, exist_ok=True)
rng = random.Random(20260920)
comp = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
ref = {'ctg1': ''.join(rng.choice('ACGT') for _ in range(300)),
       'ctg2': ''.join(rng.choice('ACGT') for _ in range(2000)),
       'ctg3': ''.join(rng.choice('ACGT') for _ in range(40000))}
with open(OUT + '/synth.fa', 'w') as fh:
    for k, v in ref.items():
        fh.write(f'>{k}\n' + '\n'.join(v[i:i + 60] for i in range(0, len(v), 60)) + '\n')


def build_seq(contig, pos1, cigar, mismatch_at=None):
    """query sequence implied by a CIGAR against the reference (H excluded from SEQ)."""
    r = ref[contig]
    p = pos1 - 1
    q = []
    for n, op in re.findall(r'(\d+)([MIDNSHP=X])', cigar):
        n = int(n)
        if op in 'M=':
            q.append(r[p:p + n]); p += n
        elif op == 'X':
            q.append(''.join(next(b for b in 'ACGT' if b != r[p + i]) for i in range(n))); p += n
        elif op in 'DN':
            p += n
        elif op in 'IS':
            q.append(''.join(rng.choice('ACGT') for _ in range(n)))
    return ''.join(q)


recs = []
def add(name, flag, contig, pos, mapq, cigar, rnext='*', pnext=0, tlen=0, seq=None, tags=(), qual_char='I'):
    if seq is None:
        seq = build_seq(contig, pos, cigar) if cigar != '*' else 'ACGTACGTAC'
    if seq == '*':
        qual = '*'
    else:
        qual = qual_char * len(seq)
    recs.append('\t'.join(map(str, [name, flag, contig, pos, mapq, cigar, rnext, pnext, tlen, seq, qual, *tags])))

add('r1_clips_indels', 0, 'ctg1', 10, 60, '5S20M2I10M3D15M4S', tags=['NM:i:5'])
add('r2_spliced', 0, 'ctg2', 100, 60, '30M1000N20M')
add('r3_hardclip', 0, 'ctg2', 1200, 60, '10H30M10H')
add('r4_unmapped_placed', 4, 'ctg1', 50, 0, '*', seq='ACGTACGTAC')          # mate-placed unmapped read
add('r5_unmapped_unplaced', 4, '*', 0, 0, '*', seq='ACGTACGTAC')
add('r6_secondary_noseq', 256, 'ctg1', 120, 0, '20M', seq='*')
add('r7_supplementary', 2048, 'ctg1', 200, 30, '20M30H', tags=['SA:Z:ctg2,100,+,30S20M,60,0;'])
add('r8_mapq255', 0, 'ctg1', 150, 255, '25M')
add('r9_mapq0_multi', 0, 'ctg1', 160, 0, '25M', tags=['XA:Z:ctg2,+500,25M,0;'])
# proper pair: read1 fwd at 20 (50M), read2 reverse at 60 (50M); span 20..109 => TLEN = +90 / -90
add('pair1', 99, 'ctg1', 20, 60, '50M', '=', 60, 90)
add('pair1', 147, 'ctg1', 60, 60, '50M', '=', 20, -90)
add('r12_eqx', 0, 'ctg2', 300, 60, '10=1X9=', tags=['NM:i:1'])
add('r13_padding', 0, 'ctg2', 400, 60, '5M2P5M')
add('r14_bigcigar', 0, 'ctg3', 1, 60, '1M1I' * 33000)     # 66000 ops (> 65535 -> BAM uses CG tag)
add('r15_dup_qcfail', 1024 + 512, 'ctg2', 500, 60, '30M')
with open(OUT + '/synth.sam', 'w') as fh:
    fh.write('@HD\tVN:1.6\tSO:unsorted\n')
    for k, v in ref.items():
        fh.write(f'@SQ\tSN:{k}\tLN:{len(v)}\n')
    fh.write('@RG\tID:rg1\tSM:synthetic\n@PG\tID:synth\tPN:make_synth.py\tVN:1\n')
    fh.write('\n'.join(recs) + '\n')
print('wrote', OUT, len(recs), 'records')
