# Probe pyOpenMS 3.5.0 protein-inference API names used by SKILL.md
import pyopenms, inspect
print('pyopenms', pyopenms.__version__ if hasattr(pyopenms,'__version__') else '?')
for name in ['EpifanyAlgorithm','BayesianProteinInferenceAlgorithm','BasicProteinInferenceAlgorithm',
             'IdXMLFile','ProteinIdentification','PeptideIdentification','PeptideIdentificationList',
             'FalseDiscoveryRate','PeptideProteinResolution','IDBoostGraph','ProteinInference']:
    print(f'{name:40s}', hasattr(pyopenms, name))
print([n for n in dir(pyopenms) if 'nfer' in n or 'pifany' in n.lower() or 'Bayes' in n])
b = pyopenms.BasicProteinInferenceAlgorithm()
p = b.getParameters()
print('\nBasicProteinInferenceAlgorithm params:')
for k in p.keys():
    print('  ', k.decode() if isinstance(k, bytes) else k, '=', p.getValue(k))
print('\nrun doc:\n', pyopenms.BasicProteinInferenceAlgorithm.run.__doc__)
bb = pyopenms.BayesianProteinInferenceAlgorithm()
pb = bb.getParameters()
print('\nBayesianProteinInferenceAlgorithm params:')
for k in pb.keys():
    print('  ', k.decode() if isinstance(k, bytes) else k, '=', pb.getValue(k))
print('\ninferPosteriorProbabilities doc:\n', pyopenms.BayesianProteinInferenceAlgorithm.inferPosteriorProbabilities.__doc__)
g = pyopenms.ProteinIdentification.ProteinGroup() if hasattr(pyopenms.ProteinIdentification,'ProteinGroup') else pyopenms.ProteinGroup()
print('\nProteinGroup attrs:', [a for a in dir(g) if not a.startswith('_')])
print('IdXMLFile.load doc:\n', pyopenms.IdXMLFile.load.__doc__)
