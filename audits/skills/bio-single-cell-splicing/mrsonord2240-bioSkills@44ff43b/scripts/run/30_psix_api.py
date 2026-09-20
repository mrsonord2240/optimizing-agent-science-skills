import inspect, psix, sys
print('psix', getattr(psix,'__version__',None), psix.__file__)
print([x for x in dir(psix) if not x.startswith('_')])
P = getattr(psix,'Psix',None)
print('Psix class:', P)
if P:
    print('init sig:', inspect.signature(P.__init__))
    print('methods:', [m for m in dir(P) if not m.startswith('_')])
    for m in ['run_psix','compute_psix_scores','psix_results']:
        print(m, hasattr(P,m))
    src = inspect.getsource(P.__init__); print(src[:2500])
