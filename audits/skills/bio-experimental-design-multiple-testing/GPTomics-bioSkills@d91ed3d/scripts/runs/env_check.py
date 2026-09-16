import inspect, statsmodels, scipy, numpy, pandas
from statsmodels.stats.multitest import multipletests
print("statsmodels", statsmodels.__version__, "| scipy", scipy.__version__, "| numpy", numpy.__version__)
sig = inspect.signature(multipletests)
print("multipletests signature:", sig)
print("DEFAULT method ->", sig.parameters['method'].default)
