import re
src = 'F:/OpenScience/external/mrsonord2240__bioSkills/workflows/proteomics-pipeline/SKILL.md'
out = 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline/runs/blocks'
lines = open(src, encoding='utf-8').read().split('\n'); h = 'top'; n = 0; i = 0
while i < len(lines):
    l = lines[i]
    if l.startswith('#'): h = re.sub(r'[^A-Za-z0-9]+', '_', l.strip('# ')).strip('_')[:30]
    m = re.match(r'^```(\w+)\s*$', l)
    if m:
        j = i + 1
        while not lines[j].startswith('```'): j += 1
        n += 1; ext = {'r': 'R', 'python': 'py', 'bash': 'sh'}.get(m.group(1), 'txt')
        open(f'{out}/b{n:02d}_{h}.{ext}', 'w', encoding='utf-8', newline='\n').write('\n'.join(lines[i+1:j]) + '\n'); print(f'b{n:02d}_{h}.{ext}', j - i - 1); i = j
    i += 1
