"""Check the two independently trained totalVI latent arrays saved by this audit."""
import numpy as np

a = np.load('latent_1.npy')
b = np.load('latent_2.npy')
print('TOTALVI_DETERMINISM', a.shape, float(np.max(np.abs(a - b))), bool(np.array_equal(a, b)))
if not np.array_equal(a, b):
    raise SystemExit('Seeded totalVI arrays differ')
