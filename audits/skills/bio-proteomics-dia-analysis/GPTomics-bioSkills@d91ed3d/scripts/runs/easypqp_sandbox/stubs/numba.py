# AUDIT STUB (not the real numba): easypqp.convert decorates functions with numba.njit at import; pass-through.
def njit(*a, **k):
    if a and callable(a[0]):
        return a[0]
    return lambda f: f
jit = njit
