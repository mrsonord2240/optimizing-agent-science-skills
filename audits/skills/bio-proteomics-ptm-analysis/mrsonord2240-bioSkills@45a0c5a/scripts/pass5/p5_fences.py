import re, py_compile, tempfile, os, subprocess, sys
S='F:/OpenScience/external/mrsonord2240__bioSkills/proteomics/ptm-analysis/SKILL.md'
t=open(S,encoding='utf-8').read()
py=re.findall(r'```python\n(.*?)```',t,re.S); r=re.findall(r'```r\n(.*?)```',t,re.S)
print('python fences:',len(py),'| r fences:',len(r),'| SKILL.md lines:',t.count('\n')+1)
for i,b in enumerate(py):
    f=os.path.join(tempfile.gettempdir(),f'ptmfence{i}.py'); open(f,'w',encoding='utf-8').write(b)
    try:
        py_compile.compile(f,doraise=True); print(f'  python fence {i+1}: compiles')
    except Exception as e: print(f'  python fence {i+1}: FAIL {e}')
ex='F:/OpenScience/external/mrsonord2240__bioSkills/proteomics/ptm-analysis/examples/phospho_analysis.py'
print('example exists:',os.path.exists(ex))
try:
    py_compile.compile(ex,doraise=True); print('  example compiles')
except Exception as e: print('  example FAIL',e)
