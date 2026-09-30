# Direct test of nucleoatac.multinomial_cov.calculateCov against a numpy-computed multinomial variance (py2.7 atac-nucleo, read-only)
import numpy as np
from nucleoatac.multinomial_cov import calculateCov
rs = np.random.RandomState(1)
p = rs.dirichlet(np.ones(30)); v = rs.randn(30); n = 53
# analytic variance of sum(count_i * v_i) for multinomial(n,p): n*(sum p v^2 - (sum p v)^2)
exact = n * (np.sum(p * v**2) - np.sum(p * v)**2)
print('exact', exact)
for name, args in [('float reads', (p, v, float(n))), ('int reads', (p, v, int(n))), ('np.float64 reads', (p, v, np.float64(n)))]:
    try:
        print(name, calculateCov(*args))
    except Exception as e:
        print(name, 'ERR', repr(e))
