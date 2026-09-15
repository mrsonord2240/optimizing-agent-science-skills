# Input 6 (NEW, re-audit 2026-09-15, Variant C): "Resolve these three GRCh38 HGVS strings to ClinGen CA IDs and pull the
# linked ClinVar summary: NC_000017.11:g.43106487A>C, NC_000017.11:g.43094464G>A, NC_000013.14:g.32316461G>A."
# Shipped examples/clinvar_query.py batch_resolve_to_car_then_clinvar (fork commit copy; cyvcf2 import stubbed on Windows).
import sys, types, importlib.util, subprocess
sys.modules['cyvcf2'] = types.SimpleNamespace(VCF=None)   # the batch function does not use cyvcf2
src = subprocess.run(['git', '-C', 'F:/OpenScience/external/mrsonord2240__bioSkills', 'show',
                      'c1237cdbc9bb199947696f3909de26a55d259116:clinical-databases/clinvar-lookup/examples/clinvar_query.py'],
                     capture_output=True, text=True, encoding='utf-8').stdout
open('clinvar_query.fork_copy.py', 'w', encoding='utf-8', newline='\n').write(src)
spec = importlib.util.spec_from_file_location('ex', 'clinvar_query.fork_copy.py')
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
import pandas as pd
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 20)
df = ex.batch_resolve_to_car_then_clinvar(['NC_000017.11:g.43106487A>C', 'NC_000017.11:g.43094464G>A', 'NC_000013.14:g.32316461G>A'])
print(df[[c for c in ['hgvs', 'ca_id', 'variation_id', 'error', 'vcv', 'germline_class', 'germline_review_status', 'star_rating'] if c in df.columns]].to_string(index=False))
print('\n== __main__ block ==')
print(subprocess.run([sys.executable, '-c', "import sys,types; sys.modules['cyvcf2']=types.SimpleNamespace(VCF=None); exec(open('clinvar_query.fork_copy.py',encoding='utf-8').read())"], capture_output=True, text=True).stdout)
