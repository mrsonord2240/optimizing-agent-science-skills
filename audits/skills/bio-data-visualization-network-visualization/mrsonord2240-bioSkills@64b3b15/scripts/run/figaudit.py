import numpy as np, matplotlib
from matplotlib.collections import PathCollection, LineCollection
from matplotlib.patches import FancyArrowPatch
def audit(fig):
    out={'n_pts':0,'n_edges':0,'n_arrows':0,'sizes':None,'labels':[],'fc':None}
    for ax in fig.axes:
        for c in ax.collections:
            if isinstance(c,PathCollection) and len(c.get_offsets())>0:
                out['n_pts']=len(c.get_offsets()); out['sizes']=np.array(c.get_sizes()); out['offsets']=np.array(c.get_offsets())
                out['fc']=c.get_facecolor(); out['array']=c.get_array()
            elif isinstance(c,LineCollection):
                
                if len(c.get_segments())>0: out['n_edges']+=len(c.get_segments()); out['seg_lw']=np.array(c.get_linewidths())
        out['n_arrows']+=sum(isinstance(p,FancyArrowPatch) for p in ax.patches)
        out['labels']+= [t.get_text() for t in ax.texts]
    return out
