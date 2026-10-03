"""Run the SKILL.md inline rMATS snippet verbatim (extracted) and check the effective-length formula (SQ-08) on JC and JCEC."""
import re, os, csv
SK = '/mnt/openscience/wt/norm-bio-splicing-quantification/skills/bio-splicing-quantification'
O = '/mnt/openscience/audits/bio-splicing-quantification/run-reaudit-1/out'
txt = open(SK + '/SKILL.md', encoding='utf-8').read()
blocks = re.findall(r'```python\n(.*?)```', txt, re.S)
print('python blocks in SKILL.md:', len(blocks))
os.chdir(SK)  # the snippet's sys.path entry 'scripts' is relative to the Skill dir
code = blocks[0].replace("'rmats_output'", "'" + O + "/rmats_real/out'")
ns = {}
exec(code, ns)
r = ns['reliable']
print('snippet OK; rows', len(r))
print(r[['ID', 'geneSymbol', 'mean_PSI_group1', 'mean_PSI_group2', 'mean_PSI', 'min_reads_per_replicate']].head(5).to_string())
for tag, root in (('real', O + '/rmats_real/out'), ('planted', O + '/rmats_planted/out')):
    for cnt in ('JC', 'JCEC'):
        mx = 0
        n = 0
        lens = set()
        with open(f'{root}/SE.MATS.{cnt}.txt') as f:
            for r in csv.DictReader(f, delimiter='\t'):
                lens.add((r['IncFormLen'], r['SkipFormLen']))
                for g in '12':
                    for i, s, p in zip(r['IJC_SAMPLE_' + g].split(','), r['SJC_SAMPLE_' + g].split(','), r['IncLevel' + g].split(',')):
                        if p == 'NA':
                            continue
                        i, s = int(i), int(s)
                        a, b = float(r['IncFormLen']), float(r['SkipFormLen'])
                        psi = (i / a) / (i / a + s / b)
                        mx = max(mx, abs(psi - float(p)))
                        n += 1
        print(f'{tag} {cnt} SE formula check n={n} maxabs={mx:.4f} distinct(IncFormLen,SkipFormLen) n={len(lens)} first={sorted(lens)[:3]}')

# delta additions: new SKILL.md text claims on real JC SE output
import collections
rows = list(csv.DictReader(open(O + '/rmats_real/out/SE.MATS.JC.txt'), delimiter='\t'))
c = collections.Counter((r['IncFormLen'], r['SkipFormLen']) for r in rows)
print('JC SE rows', len(rows), '148/74:', c[('148', '74')], 'max inc', max(int(r['IncFormLen']) for r in rows), 'max skip', max(int(r['SkipFormLen']) for r in rows))
byE = collections.defaultdict(set)
for r in rows:
    byE[int(r['exonEnd']) - int(r['exonStart_0base'])].add((r['IncFormLen'], r['SkipFormLen']))
print('exons >=75 with inc!=148:', sum(1 for r in rows if int(r['exonEnd']) - int(r['exonStart_0base']) >= 75 and r['IncFormLen'] != '148'))
print('exon len 74 ->', byE[74], '; exon len 1 ->', byE[1])
print('rows with SkipFormLen != 74:', sum(1 for r in rows if r['SkipFormLen'] != '74'))
