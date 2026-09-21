import re,pathlib
t=pathlib.Path('run/skill/data-visualization/network-visualization/SKILL.md').read_text(encoding='utf-8')
for i,(lang,code) in enumerate(re.findall(r'```(\w*)\n(.*?)```',t,re.S),1):
    pathlib.Path(f'run/blocks/b{i:02d}_{lang}.{"py" if lang=="python" else "R" if lang=="r" else "txt"}').write_text(code,encoding='utf-8')
    print(i,lang,len(code.splitlines()),'lines |',code.splitlines()[0][:70])
