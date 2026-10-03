"""Bisect which Skill rcParam makes a Type 3 PDF save fail (matplotlib 3.11.2): apply each Standard Setup key alone with pdf.fonttype=3."""
import tempfile, matplotlib as mpl, matplotlib.pyplot as plt
std = {'ps.fonttype': 42, 'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'], 'font.size': 7, 'axes.labelsize': 7,
       'axes.titlesize': 8, 'xtick.labelsize': 6, 'ytick.labelsize': 6, 'legend.fontsize': 6, 'figure.dpi': 100, 'savefig.dpi': 300,
       'savefig.bbox': 'tight', 'savefig.pad_inches': 0.05, 'axes.linewidth': 0.5, 'xtick.major.width': 0.5, 'ytick.major.width': 0.5,
       'lines.linewidth': 1.0, 'patch.linewidth': 0.5}
d = tempfile.mkdtemp()
def t(label, rc):
    with mpl.rc_context({'pdf.fonttype': 3, **rc}):
        f, a = plt.subplots(figsize=(3, 2)); a.plot([-1, 0, 1], [-1, 0, 1]); a.set_xlabel('PC1 (45%)')
        try:
            f.savefig(d + '/x.pdf'); r = 'ok'
        except Exception as e:
            r = f'FAIL {type(e).__name__}: {e}'
        plt.close(f)
    print(f'{label:55s} {r}')
t('default rcParams + fonttype 3', {})
for k, v in std.items(): t(f'+ {k}', {k: v})
t('all Standard Setup keys', std)
t('Arial only (font.sans-serif)', {'font.sans-serif': ['Arial']})
t('axes.unicode_minus False + all keys', {**std, 'axes.unicode_minus': False})
