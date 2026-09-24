import sys, time, resource
from skillfns import is_coordinate_sorted
p=sys.argv[1]; t=time.time(); v=is_coordinate_sorted(p); dt=time.time()-t
print("%s is_coordinate_sorted=%s  %.1fs  maxRSS=%.0f MB" % (p, v, dt, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024))
