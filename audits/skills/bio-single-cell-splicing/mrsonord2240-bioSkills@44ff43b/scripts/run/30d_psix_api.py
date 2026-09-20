import inspect, psix
print(inspect.getsource(psix.Psix.get_cell_metric)[:2500])
from psix import score_functions as sf
print(inspect.getsource(sf.compute_pvalues)[:2500])
