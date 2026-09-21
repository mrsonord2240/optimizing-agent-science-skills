import re
SKILL = r'F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\run\skill\data-visualization\matplotlib-fundamentals\SKILL.md'
def blocks():
    t = open(SKILL, encoding='utf-8').read()
    return re.findall(r'```python\n(.*?)```', t, re.S)
if __name__ == '__main__':
    for i, b in enumerate(blocks()):
        print(i, '|', b.strip().splitlines()[0][:80], '|', len(b.splitlines()), 'lines')
