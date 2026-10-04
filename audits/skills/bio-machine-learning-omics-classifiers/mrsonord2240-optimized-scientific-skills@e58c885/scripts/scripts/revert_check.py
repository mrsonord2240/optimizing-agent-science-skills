import json,sys,io
p=r'F:/OpenScience/audits/bio-machine-learning-omics-classifiers/reaudit-delta-20261003/scratch/rev/SKILL.md'
edits=json.load(open(r'F:/OpenScience/audits/bio-machine-learning-omics-classifiers/fix-description-20261003/edits.json',encoding='utf-8'))
b=open(p,'rb').read(); print('crlf' , b'\r\n' in b)
t=b.decode('utf-8')
for e in edits:
    assert e['file']=='SKILL.md'
    assert t.count(e['new'])==1
    t=t.replace(e['new'],e['old'])
open(p,'wb').write(t.encode('utf-8'))
import yaml
fm=t.split('---')[1]; print(yaml.safe_load(fm).keys())
