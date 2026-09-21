"""Input 2 add-on: boxplot medians vs numpy, and the version status of boxplot(labels=)."""
import numpy as np, matplotlib.pyplot as plt, warnings
rng = np.random.default_rng(1)
a, b, c = rng.normal(0,1,40), rng.normal(1,1,40), rng.normal(2,1,40)
fig, ax = plt.subplots()
bp = ax.boxplot([a, b, c], tick_labels=['A','B','C'], patch_artist=True)
print('box medians', [round(float(m.get_ydata()[0]),3) for m in bp['medians']], 'numpy', [round(float(np.median(g)),3) for g in (a,b,c)])
for kw in ('labels', 'tick_labels'):
    fig, ax = plt.subplots()
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always'); ax.boxplot([a,b,c], **{kw: ['A','B','C']}); print(kw, 'OK', [str(x.message)[:80] for x in w])
    except Exception as e: print(kw, 'FAILS', e)
