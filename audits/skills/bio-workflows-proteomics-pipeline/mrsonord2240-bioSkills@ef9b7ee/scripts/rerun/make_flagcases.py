"""Re-audit new Input B: two MaxQuant proteinGroups.txt variants to test the `%in%` flag-column fix.
B1 = no row flagged in any of the three flag columns (a clean search with no decoys/contaminants kept)
     -> read.delim types those columns logical NA, and `NA != '+'` used to NA the whole table.
B2 = mixed: some rows flagged, some not -> the filter must still remove exactly the flagged rows.
SYNTHETIC: derived from the audit's synthetic proteinGroups.txt."""
P = 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
src = open(P + '/data/proteinGroups.txt', encoding='utf-8').read().split('\n')
hdr = src[0].split('\t'); rows = [l for l in src[1:] if l.strip()]
flags = ['Reverse', 'Potential contaminant', 'Only identified by site']
idx = [hdr.index(f) for f in flags]
b1, b2 = [], []
nflag = {f: 0 for f in flags}
for k, l in enumerate(rows):
    c = l.split('\t')
    c1 = list(c)
    for i in idx: c1[i] = ''
    b1.append('\t'.join(c1))
    c2 = list(c1)
    if k % 50 == 7:  c2[idx[0]] = '+'; nflag['Reverse'] += 1
    elif k % 50 == 17: c2[idx[1]] = '+'; nflag['Potential contaminant'] += 1
    elif k % 50 == 27: c2[idx[2]] = '+'; nflag['Only identified by site'] += 1
    b2.append('\t'.join(c2))
open(P + '/rerun/workB1/proteinGroups.txt', 'w', encoding='utf-8', newline='\n').write(src[0] + '\n' + '\n'.join(b1) + '\n')
open(P + '/rerun/workB2/proteinGroups.txt', 'w', encoding='utf-8', newline='\n').write(src[0] + '\n' + '\n'.join(b2) + '\n')
print('rows', len(rows), '| B1 flagged 0 | B2 flagged', nflag, 'total', sum(nflag.values()))
