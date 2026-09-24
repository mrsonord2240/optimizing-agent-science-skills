import sys, time, random
sys.path.insert(0, sys.argv[1]); import splicing_qc as sq
rng = random.Random(1)
d = [''.join(rng.choice('ACGT') for _ in range(9)) for _ in range(300)]; a = [''.join(rng.choice('ACGT') for _ in range(23)) for _ in range(300)]
t = time.time(); sq.score_splice_sites(d, []); t1 = time.time() - t
t = time.time(); sq.score_splice_sites([], a); t2 = time.time() - t
print('300 donors %.2fs, 300 acceptors %.2fs' % (t1, t2))
