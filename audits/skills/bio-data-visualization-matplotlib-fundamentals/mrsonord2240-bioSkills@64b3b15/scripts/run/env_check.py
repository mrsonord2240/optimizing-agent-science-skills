import matplotlib, seaborn, numpy, pandas, sys
print(sys.version)
print('mpl', matplotlib.__version__, 'sns', seaborn.__version__, 'np', numpy.__version__, 'pd', pandas.__version__)
import matplotlib as mpl
print('default pdf.fonttype', mpl.rcParams['pdf.fonttype'], 'ps', mpl.rcParams['ps.fonttype'])
print('default constrained', mpl.rcParams['figure.constrained_layout.use'], 'layout', mpl.rcParams.get('figure.autolayout'))
print('default savefig.dpi', mpl.rcParams['savefig.dpi'], 'figure.dpi', mpl.rcParams['figure.dpi'])
from matplotlib import font_manager as fm
names = sorted({f.name for f in fm.fontManager.ttflist})
print([n for n in names if n in ('Arial','Helvetica','DejaVu Sans','Liberation Sans')])
try:
    import cmcrameri; print('cmcrameri', cmcrameri.__version__)
except Exception as e: print('no cmcrameri', e)
import seaborn.objects
print('so ok')
