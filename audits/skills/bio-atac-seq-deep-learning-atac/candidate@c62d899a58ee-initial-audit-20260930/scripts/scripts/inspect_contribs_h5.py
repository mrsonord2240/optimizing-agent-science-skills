import h5py, numpy as np, sys
f = h5py.File(sys.argv[1], 'r')
def walk(n, o):
    if isinstance(o, h5py.Dataset): print(n, o.shape, o.dtype)
f.visititems(walk)
for k in f: 
    if isinstance(f[k], h5py.Group):
        for kk in f[k]: print(k, kk, f[k][kk].shape)
