# Real-size inputs (VMat-shaped) repeated: uninitialised accumulator in calculateCov gives inconsistent/NaN output vs exact
import numpy as np
from nucleoatac.multinomial_cov import calculateCov
rs = np.random.RandomState(2)
k = 251 * 251 // 4
p = rs.dirichlet(np.ones(k)); v = rs.randn(k); n = 53
exact = n * (np.sum(p * v**2) - np.sum(p * v)**2)
print('exact %.6g' % exact)
vals = [calculateCov(p, v, float(n)) for _ in range(6)]
print('calculateCov x6', ['%.6g' % x for x in vals])
print('n_nan', sum(1 for x in vals if np.isnan(x)), 'n_close_to_exact', sum(1 for x in vals if abs(x - exact) < 1e-6 * max(1, abs(exact))))
