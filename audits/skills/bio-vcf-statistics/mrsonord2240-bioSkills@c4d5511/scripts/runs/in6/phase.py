import sys
k = 0
out = open('phased.vcf', 'w', newline='\n')
for line in open(sys.argv[1]):
    if line.startswith('#'):
        out.write(line); continue
    f = line.rstrip('\n').split('\t')
    gi = f[8].split(':').index('GT')
    for j in range(9, len(f)):
        p = f[j].split(':')
        if p[gi] == '0/1':
            p[gi] = '0|1' if k % 2 == 0 else '1|0'; k += 1
        f[j] = ':'.join(p)
    out.write('\t'.join(f) + '\n')
