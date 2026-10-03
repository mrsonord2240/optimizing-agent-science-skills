import sys
sys.path.insert(0, r'F:\OpenScience\wt\dbaccess-ortholog-inference\skills\bio-ortholog-inference\scripts')
import ortholog_clients as oc
df=oc.batch_compara(['TP53','NOTAGENE123'],'human','mouse')
print(df.to_string())
