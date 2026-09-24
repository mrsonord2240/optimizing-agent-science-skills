# prints "<name> skill_fn=<True|False|ERR:...> " for each path given
import sys, time
from skillfns import is_coordinate_sorted
for p in sys.argv[1:]:
    t=time.time()
    try:
        v = is_coordinate_sorted(p)
    except Exception as e:
        v = "ERR:%s:%s" % (type(e).__name__, str(e)[:70].replace('\n',' '))
    print("%s\t%s\t%.2fs" % (p, v, time.time()-t))
