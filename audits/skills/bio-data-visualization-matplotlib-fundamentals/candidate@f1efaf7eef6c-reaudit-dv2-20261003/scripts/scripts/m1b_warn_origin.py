"""Where does the Pandas4Warning raised while running matplotlib_phd.py come from? Usage: py.sh m1b_warn_origin.py <skilldir> <outdir>"""
import sys, os, warnings, traceback, runpy
from pathlib import Path
skill, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import matplotlib; matplotlib.use("Agg")
import pandas as pd
print("pandas", pd.__version__)
seen = []
def show(message, category, filename, lineno, file=None, line=None):
    seen.append((category.__name__, str(message)[:80], filename, lineno)); print("WARN", category.__name__, str(message)[:100], "@", filename, lineno)
    print("  stack (innermost last):"); [print("   ", f"{os.path.basename(f.filename)}:{f.lineno} {f.name}") for f in traceback.extract_stack()[-8:-1]]
warnings.showwarning = show; warnings.simplefilter("always")
runpy.run_path(str(skill/'scripts'/'matplotlib_phd.py'), run_name='__main__')
print("distinct warnings:", len({(s[0], s[3]) for s in seen}), "total", len(seen))
