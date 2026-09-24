# Exact-commit re-audit input 2: current Python routes and warning behavior.
# Run with: F:/OpenScience/audit-envs/data-visualization/py.sh reaudit_i2_python_current.py <source-test>
import pathlib
import subprocess
import sys
import tempfile
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import ptitprince as pt
import seaborn as sns

source_test = pathlib.Path(sys.argv[1]).resolve()
assert source_test.is_file()
completed = subprocess.run([sys.executable, str(source_test)], text=True, capture_output=True, check=True)
print(completed.stdout.strip())

rng = np.random.default_rng(20260923)
frame = pd.DataFrame({"group": np.repeat(["Control", "Treated"], 40),
                      "value": np.r_[rng.normal(5, .7, 40), rng.normal(6, .8, 40)]})
palette = {"Control": "#0072B2", "Treated": "#D55E00"}
out = pathlib.Path(tempfile.mkdtemp(prefix="distribution-plots-reaudit-py-"))
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    fig, ax = plt.subplots(figsize=(5, 3.5))
    pt.RainCloud(x="group", y="value", data=frame, hue="group", palette=palette,
                 bw="scott", cut=0, width_viol=.6, orient="h", ax=ax)
    rain = out / "raincloud.png"
    fig.savefig(rain, dpi=120)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(4, 3.5))
    sns.boxenplot(data=frame, x="group", y="value", hue="group", palette=palette,
                  legend=False, ax=ax)
    boxen = out / "boxen.png"
    fig.savefig(boxen, dpi=120)
    plt.close(fig)
assert rain.stat().st_size > 2000 and boxen.stat().st_size > 2000
# ptitprince itself still warns on Matplotlib's soon-removed orientation API; its documented limit is present.
messages = [str(w.message) for w in caught]
assert not any("Passing `palette` without assigning `hue`" in message for message in messages)
assert any("vert" in message.lower() for message in messages), messages
print(f"PASS i2: source Python test; rain={rain.stat().st_size}; boxen={boxen.stat().st_size}; ptitprince_matplotlib_warning=observed")
