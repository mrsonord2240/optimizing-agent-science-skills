# AUDITOR CHECK for Input 5: --keeplength preserved the reference; accuracy of the reference MSA (sampled)
# and of fragment placement, both scored against the simulated TRUE alignment.
import difflib, itertools, random
from Bio import AlignIO, SeqIO
ref = AlignIO.read('ref1000_fftns2.fasta', 'fasta'); upd = AlignIO.read('updated1050.fasta', 'fasta')
print('reference columns', ref.get_alignment_length(), '-> after --addfragments --keeplength', upd.get_alignment_length())
print('reference rows unchanged:', all(str(a.seq) == str(b.seq) for a, b in zip(ref, upd)))
true = {r.id: str(r.seq).upper() for r in SeqIO.parse('../../data/big1050_true_aln.fa', 'fasta')}
orig = {r.id[:-4]: str(r.seq).upper() for r in SeqIO.parse('new50_amplicons.fa', 'fasta')}
est = {r.id: str(r.seq).upper() for r in upd}
def res2col(s):
    out, k = {}, 0
    for j, c in enumerate(s):
        if c != '-': out[k] = j; k += 1
    return out
def col2res(s):
    return {j: k for k, j in res2col(s).items()}
rng = random.Random(3)
refids = rng.sample([i for i in est if not i.endswith('_amp')], 60)
# (a) sampled sum-of-pairs recall of the reference MSA
ok = tot = 0
for a, b in itertools.combinations(refids[:40], 2):
    ta, tb, ea, eb = res2col(true[a]), col2res(true[b]), res2col(est[a]), col2res(est[b])
    for k, j in ta.items():
        if j in tb:
            tot += 1; ok += (eb.get(ea[k]) == tb[j])
print(f'reference MSA sampled SP recall (40 seqs): {ok/tot:.3f}')
# (b) fragment placement
ok = tot = dropped = 0
for fid, fo in orig.items():
    fa = est[fid + '_amp']; fu = fa.replace('-', '')
    dropped += len(fo) - len(fu)
    off = true[fid].replace('-', '').find(fo)
    sm = difflib.SequenceMatcher(None, fu, fo, autojunk=False)
    m = {}
    for blk in sm.get_matching_blocks():
        for i in range(blk.size): m[blk.a + i] = blk.b + i
    tcol, ecol = res2col(true[fid]), res2col(fa)
    for rid in refids[:20]:
        tmap, emap = col2res(true[rid]), col2res(est[rid])
        for k in range(0, len(fu), 5):
            if k not in m: continue
            tj = tcol[off + m[k]]
            if tj in tmap:
                tot += 1; ok += (emap.get(ecol[k]) == tmap[tj])
print(f'fragment residues dropped by --keeplength (insertions vs reference): {dropped}')
print(f'fragment-to-reference homologous pairs recovered: {ok}/{tot} = {ok/tot:.3f}')
