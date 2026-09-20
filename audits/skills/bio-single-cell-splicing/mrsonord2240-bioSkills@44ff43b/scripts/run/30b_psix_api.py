import inspect, psix
P = psix.Psix
print(inspect.signature(P.run_psix)); print(inspect.getsource(P.run_psix)[:6000])
print('---- results columns hint'); 
src = inspect.getsource(P.run_psix)
import re; print(re.findall(r"psix_results\[?[^\n]*", src)[:10])
