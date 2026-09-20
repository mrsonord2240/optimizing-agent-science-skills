import inspect, psix
from psix import score_functions as sf
print([n for n in dir(sf) if not n.startswith('_')])
print(inspect.getsource(sf.compute_psix_scores)[:5000])
