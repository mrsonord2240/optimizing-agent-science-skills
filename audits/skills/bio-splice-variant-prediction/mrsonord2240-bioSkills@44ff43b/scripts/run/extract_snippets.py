# Extract python blocks from the Skill's SKILL.md (copy) verbatim so they can be executed.
import re
t = open('skill/SKILL.md', encoding='utf-8').read()
blocks = re.findall(r'```python\n(.*?)```', t, re.S)
for i, b in enumerate(blocks): print(i, b[:60].replace('\n', ' | '))
open('blocks_dump.txt', 'w', encoding='utf-8', newline='\n').write('\n#=====\n'.join(blocks))
open('skill_md_snippets.py', 'w', encoding='utf-8', newline='\n').write(blocks[0].split("df = parse_spliceai_vcf")[0])
