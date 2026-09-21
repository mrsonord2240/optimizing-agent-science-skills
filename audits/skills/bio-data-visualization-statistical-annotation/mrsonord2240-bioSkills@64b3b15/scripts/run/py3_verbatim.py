# Extract the python code block(s) from SKILL.md and run them VERBATIM on SYNTHETIC data
import re, warnings, pandas as pd, matplotlib.pyplot as plt
D = "F:/OpenScience/audits/bio-data-visualization-statistical-annotation"
md = open(D + "/run/skill/data-visualization/statistical-annotation/SKILL.md", encoding="utf-8").read()
blocks = re.findall(r"```python\n(.*?)```", md, re.S)
print("python blocks:", len(blocks))
df = pd.read_csv(D + "/data/three_group.csv")
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    g = {"df": df}
    exec(blocks[0], g)
    print("warnings:", sorted({str(x.message)[:110] for x in w}))
ax = g["ax"]; print("texts:", [t.get_text() for t in ax.texts]); ax.figure.savefig(D + "/figs/py_skill_verbatim.png", dpi=100)
