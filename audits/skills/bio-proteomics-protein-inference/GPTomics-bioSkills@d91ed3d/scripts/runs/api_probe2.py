import pyopenms
p = pyopenms.BasicProteinInferenceAlgorithm().getParameters()
for k in p.keys():
    print(k, '|', p.getDescription(k))
print(pyopenms.BayesianProteinInferenceAlgorithm.__doc__)
prot, pep = [], []
try:
    pyopenms.IdXMLFile().load('nonexistent.idXML', prot, pep)
except Exception as e:
    print('load with [] ->', type(e).__name__, str(e)[:300])
print([m for m in dir(pyopenms.PeptideIdentificationList) if not m.startswith('_')])
print([m for m in dir(pyopenms.ProteinIdentification) if 'roup' in m or 'Indist' in m])
print([m for m in dir(pyopenms.FalseDiscoveryRate) if not m.startswith('_')])
print(pyopenms.FalseDiscoveryRate.applyPickedProteinFDR.__doc__ if hasattr(pyopenms.FalseDiscoveryRate,'applyPickedProteinFDR') else 'no applyPickedProteinFDR')
pf = pyopenms.FalseDiscoveryRate().getParameters()
for k in pf.keys():
    print('FDR param', k, '=', pf.getValue(k), '|', pf.getDescription(k))
