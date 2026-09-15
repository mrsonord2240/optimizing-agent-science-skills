# Inspect the pyopenms 3.1.0 win_amd64 wheel (downloaded with `pip download pyopenms==3.1.0 --no-deps`, NOT installed)
# for the class names and IdXMLFile.load signature the Skill relies on ("tested with pyOpenMS 3.1+").
import sys, zipfile, re
z = zipfile.ZipFile(sys.argv[1])
names = z.namelist()
hits = dict.fromkeys(['EpifanyAlgorithm', 'BayesianProteinInferenceAlgorithm', 'BasicProteinInferenceAlgorithm', 'PeptideIdentificationList'], 0)
loadsig = []
for n in names:
    if n.endswith(('.pyi', '.py')):
        t = z.read(n).decode('utf-8', 'ignore')
        for k in hits: hits[k] += t.count(k)
        for m in re.finditer(r'class IdXMLFile.*?(?=\nclass )', t, re.S):
            loadsig += re.findall(r'def load\(self[^\n]*', m.group(0))
    elif n.endswith('.pyd'):
        b = z.read(n)
        for k in hits:
            if k.encode() in b: hits[k] += 1
print('occurrences in 3.1.0 stubs + binaries:', hits)
print('IdXMLFile.load in 3.1.0:', loadsig[0] if loadsig else None)
