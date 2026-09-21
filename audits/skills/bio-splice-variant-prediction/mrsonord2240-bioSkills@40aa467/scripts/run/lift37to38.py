"""Auditor's own GRCh38 panel: lift the auditor's GRCh37 panel (data/panel_grch37.vcf) with Ensembl REST /map and
assert REF against the hg38 FASTA (independent of the fixer's panel). Public service, coordinates only."""
import json, re, sys, urllib.request, time
from pyfaidx import Fasta
fa = Fasta(sys.argv[1])
out = ['##fileformat=VCFv4.2', '##contig=<ID=chr17,length=83257441>', '##contig=<ID=chrX,length=156040895>',
       '#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO']
bad = 0
for l in open('data/panel_grch37.vcf'):
    if l.startswith('#'): continue
    c = l.rstrip('\n').split('\t')
    chrom, pos, vid, ref, alt = c[0], int(c[1]), c[2], c[3], c[4]
    end = pos + len(ref) - 1
    url = f'https://rest.ensembl.org/map/human/GRCh37/{chrom}:{pos}..{end}:1/GRCh38?content-type=application/json'
    for attempt in range(4):
        try:
            j = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'Accept': 'application/json'}), timeout=30)); break
        except Exception as e:
            time.sleep(2); j = None
    m = j['mappings'][0]['mapped']
    assert m['strand'] == 1, (vid, m)
    p38 = m['start']
    got = str(fa['chr' + m['seq_region_name']][p38 - 1:p38 - 1 + len(ref)]).upper()
    ok = got == ref
    print(f'{vid}: GRCh37 {chrom}:{pos} -> GRCh38 chr{m["seq_region_name"]}:{p38} REF vcf {ref} fasta {got} {"OK" if ok else "MISMATCH"}')
    bad += (not ok)
    out.append(f'chr{m["seq_region_name"]}\t{p38}\t{vid}\t{ref}\t{alt}\t.\t.\t.')
# TP53 (auditor's original GRCh38 record)
for l in open('data/tp53_grch38.vcf'):
    if l.startswith('#'): continue
    c = l.rstrip('\n').split('\t')
    if 'usage_guide' in c[2]: continue
    got = str(fa[c[0]][int(c[1]) - 1:int(c[1])]).upper()
    print(f'{c[2]}: {c[0]}:{c[1]} REF vcf {c[3]} fasta {got} {"OK" if got == c[3] else "MISMATCH"}'); bad += got != c[3]
    if c[2].startswith('TP53_c.673'): out.append('\t'.join(c))
open('data/panel_grch38_auditor.vcf', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('MISMATCHES:', bad)
