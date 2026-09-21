# SKILL.md "CVD Simulation" python block, verbatim, then what it takes to get an actual simulation
from colorspacious import cspace_converter
print("import ok; cspace_converter =", cspace_converter)
import numpy as np, colorspacious as cs
# the block above never simulates anything; the working call is cspace_convert with an sRGB1+CVD source space
viridis_end = np.array([[0.267, 0.005, 0.329],[0.993, 0.906, 0.144]])
sim = cs.cspace_convert(viridis_end, {"name":"sRGB1+CVD","cvd_type":"deuteranomaly","severity":100}, "sRGB1")
print("deutan-simulated viridis ends:", np.round(sim,3).tolist())
# matplotlib 'colorblind' style per SKILL.md line 113
import matplotlib.pyplot as plt
try: plt.style.use("colorblind"); print("style ok")
except Exception as e: print("plt.style.use('colorblind') ->", type(e).__name__, str(e)[:120])
plt.style.use("seaborn-v0_8-colorblind"); print("seaborn-v0_8-colorblind cycle:", plt.rcParams["axes.prop_cycle"].by_key()["color"][:8])
