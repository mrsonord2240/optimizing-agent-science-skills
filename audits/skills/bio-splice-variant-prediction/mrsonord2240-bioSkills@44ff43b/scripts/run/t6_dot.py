# INPUT 6/7: what do the Skill's parsers + classifier do with SpliceAI's un-scoreable output (SpliceAI=ALT|GENE|.|.|.|.|.|.|.|.)?
import sys, importlib.util
sys.dont_write_bytecode = True
import pandas as pd
def load(n, p):
    s = importlib.util.spec_from_file_location(n, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
ex = load('ex', 'skill/examples/spliceai_clingen_classify.py'); md = load('md', 'skill_md_snippets.py')
for name, m in (('example script parser', ex), ('SKILL.md parser', md)):
    df = m.parse_spliceai_vcf('out/sai_aso.vcf')
    print(name, '->', df[['pos', 'DS_AG', 'DS_AL', 'DS_DG', 'DS_DL', 'delta_max']].to_dict('records')[:3])
df = ex.apply_clingen_svi(ex.parse_spliceai_vcf('out/sai_aso.vcf'))
print(df[['pos', 'delta_max', 'acmg_evidence']].to_string())
ok = (df.acmg_evidence.astype(str) == 'BP4').all()
print('CHECK unscoreable records are labelled BP4 (benign supporting) by the Skill code:', ok)
assert ok
