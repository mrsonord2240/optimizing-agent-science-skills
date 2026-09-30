# Re-open the h5ad from snap_pipeline.py and call snap.tl.macs3 exactly as documented (default n_jobs), to test the tooling-phase "worker process died" observation
import os, snapatac2 as snap, time
SCA=os.environ["SCA"]; os.chdir(f"{SCA}/work/snap")
d = snap.read("out2.h5ad", backed="r+"); print("cells", d.n_obs)
t=time.time()
try:
    snap.tl.macs3(d, groupby="leiden"); print("macs3 default n_jobs OK", round(time.time()-t), "s")
except BaseException as e:
    print("macs3 default FAILED:", type(e).__name__, str(e)[:300])
d.close()
