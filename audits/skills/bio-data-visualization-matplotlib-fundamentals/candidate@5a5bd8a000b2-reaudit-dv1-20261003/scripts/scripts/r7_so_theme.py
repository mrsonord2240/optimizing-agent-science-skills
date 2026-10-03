"""Re-audit 7: does so.Plot override rcParams without .theme(...)? (SKILL.md claim). Usage: py.sh r7_so_theme.py"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.objects as so

mpl.rcParams.update({'font.size': 7, 'axes.labelsize': 7, 'xtick.labelsize': 6, 'ytick.labelsize': 6, 'font.sans-serif': ['Arial'], 'font.family': 'sans-serif'})
rng = np.random.default_rng(0)
df = pd.DataFrame({'a': rng.normal(size=50), 'b': rng.normal(size=50), 'c': rng.choice(['x', 'y'], 50)})


def sizes(p):
    f = p.plot()._figure
    ax = f.axes[0]
    s = (ax.xaxis.label.get_fontsize(), ax.get_xticklabels()[0].get_fontsize(), ax.get_xticklabels()[0].get_fontname())
    plt.close(f)
    return s


plain = sizes(so.Plot(df, x='a', y='b').add(so.Dots(), color='c').label(x='x'))
themed = sizes(so.Plot(df, x='a', y='b').add(so.Dots(), color='c').theme({**sns.axes_style('ticks'), **mpl.rcParams}).label(x='x'))
print("axis-label size, tick size, font: rcParams set to 7 / 6 / Arial")
print("without .theme:", plain)
print("with .theme   :", themed)
print("claim holds (plain differs from rcParams, themed matches):", plain[:2] != (7.0, 6.0) and themed[:2] == (7.0, 6.0))
