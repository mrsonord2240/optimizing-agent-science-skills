t = open('blocks/B10.sh', encoding='utf-8').read().split('\n')
out = []
for l in t:
    if l.startswith('geneBody'): continue
    l = l.replace('SECOND_READ_TRANSCRIPTION_STRAND', 'NONE')
    if 'RIBOSOMAL_INTERVALS' in l: continue
    out.append(l)
s = '\n'.join(out).rstrip()
if s.endswith(chr(92)): s = s[:-1].rstrip()
open('work/b10_real_picard.sh', 'w', encoding='utf-8', newline='\n').write(s + '\n'); print(s)
