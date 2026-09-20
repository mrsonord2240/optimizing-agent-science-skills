#!/usr/bin/env python3
"""List / extract fenced code blocks of the Skill's SKILL.md so they can be run VERBATIM.
Usage: extract_blocks.py list                      -> index, language, first line
       extract_blocks.py get <idx> <outfile>       -> write block <idx> to outfile"""
import os, re, sys
txt = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skill', 'SKILL.md'), encoding='utf-8').read()
blocks = [(m.group(1), m.group(2)) for m in re.finditer(r'```(\w*)\n(.*?)```', txt, re.S)]
if sys.argv[1] == 'list':
    for i, (lang, body) in enumerate(blocks):
        print(i, lang or '-', len(body.splitlines()), 'lines |', body.strip().splitlines()[0][:90])
else:
    open(sys.argv[3], 'w', encoding='utf-8', newline='\n').write(blocks[int(sys.argv[2])][1])
