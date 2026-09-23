"""
Re-audit: run the fixed SKILL.md's new ESPSim example verbatim (EmbedAlignScore),
on a fresh molecule pair (ibuprofen vs a chloro-analog) different from the fixer's
acetanilide/fluoro-acetanilide pair, to confirm the example is not overfit to one
input and that shape_sim/esp_sim behave as documented (shape in [0,1], esp
unbounded under default metric='carbo').
"""
from rdkit import Chem
from espsim import EmbedAlignScore

query = Chem.AddHs(Chem.MolFromSmiles('CC(C)Cc1ccc(cc1)C(C)C(=O)O'))       # ibuprofen
target = Chem.AddHs(Chem.MolFromSmiles('CC(Cl)Cc1ccc(cc1)C(C)C(=O)O'))     # chloro-analog

shape_sim, esp_sim = EmbedAlignScore(target, [query], prbNumConfs=10, refNumConfs=10)
print("shape_sim =", shape_sim)
print("esp_sim (carbo, unbounded) =", esp_sim)

shape_sim = shape_sim[0] if hasattr(shape_sim, '__len__') else shape_sim
esp_sim_v = esp_sim[0] if hasattr(esp_sim, '__len__') else esp_sim

assert 0.0 <= float(shape_sim) <= 1.0, "shape_sim should be bounded [0,1] as documented"
print(f"\nPASS: shape_sim={float(shape_sim):.4f} in [0,1]; esp_sim={float(esp_sim_v):.4f} (carbo, can be outside [0,1] per docs)")

# Also confirm renormalize=True bounds esp_sim as documented
shape_sim2, esp_sim2 = EmbedAlignScore(target, [query], prbNumConfs=10, refNumConfs=10, renormalize=True)
esp_sim2_v = esp_sim2[0] if hasattr(esp_sim2, '__len__') else esp_sim2
print(f"renormalize=True esp_sim = {float(esp_sim2_v):.4f}")
assert 0.0 <= float(esp_sim2_v) <= 1.0, "renormalize=True should bound esp_sim to [0,1]"
print("PASS: renormalize=True produces a bounded esp_sim as documented")
