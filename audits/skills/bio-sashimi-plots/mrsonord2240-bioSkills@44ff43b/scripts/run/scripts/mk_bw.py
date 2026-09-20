import pyBigWig, sys
bg, bw, chrom, size = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
b = pyBigWig.open(bw, 'w'); b.addHeader([(chrom, size)])
rows = [l.split() for l in open(bg)]
b.addEntries([r[0] for r in rows], [int(r[1]) for r in rows], ends=[int(r[2]) for r in rows], values=[float(r[3]) for r in rows]); b.close()
print('bigwig written', bw, len(rows), 'intervals')
