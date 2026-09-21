import os, traceback, warnings; warnings.filterwarnings('ignore'); os.chdir('/mnt/openscience/audits/bio-single-cell-splicing/run/out/in6_scquint/var_C')
code = open('/mnt/openscience/audits/bio-single-cell-splicing/run/blocks/S07_python.py').read().replace("'neuron'", "'GBR'").replace("'glia'", "'YRI'"); ns = {'cell_types': ['GBR', 'GBR', 'YRI', 'YRI']}
try: exec(code, ns)
except Exception: traceback.print_exc()
