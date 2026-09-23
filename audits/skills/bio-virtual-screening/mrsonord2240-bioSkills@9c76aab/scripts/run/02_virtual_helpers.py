import importlib.util
from pathlib import Path
p=Path(r'F:\OpenScience\wt\chemoinformatics-virtual-screening\chemoinformatics\virtual-screening\examples\virtual_screen.py');spec=importlib.util.spec_from_file_location('vs',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
o=Path(r'F:\OpenScience\audits\bio-virtual-screening\data\fresh2_lig.pdbqt');m.prepare_ligand('NC(=[NH2+])c1ccccc1',o);assert o.exists() and o.stat().st_size>0
try:m.prepare_ligand('NOT_A_SMILES',o)
except ValueError:print('INVALID_SMILES=REJECTED')
else:raise AssertionError('invalid smiles accepted')
print('VIRTUAL_HELPERS=PASS')
