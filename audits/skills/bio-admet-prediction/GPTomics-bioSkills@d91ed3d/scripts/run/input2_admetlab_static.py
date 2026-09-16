# bio-admet-prediction -- Input 2 (Variant A): the ADMETlab 3.0 route.
# The Skill deliberately hard-codes no API route ("follow the live official API
# tutorial"), so the network call CANNOT be executed from what the Skill ships.
# What CAN be executed is the one function it does provide.
import ast
import os
import sys
import pandas as pd

EX = (r"F:\OpenScience\external\mrsonord2240__bioSkills\chemoinformatics"
      r"\admet-prediction\examples\predict_admet.py")
src = open(EX, encoding='utf-8').read()
tree = ast.parse(src)
fns = [n.name for n in tree.body if isinstance(n, ast.FunctionDef)]
print(f"example parses: True; functions: {fns}")

# Import from a LOCAL COPY of the example (predict_admet.py is copied into this
# run/ directory). Importing it from the read-only clone would create a
# __pycache__ inside F:\OpenScience\external\, which the brief forbids.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from predict_admet import load_admetlab_results          # noqa: E402

# a plausible ADMETlab-shaped CSV, invented here purely to exercise the loader
pd.DataFrame({'smiles': ['CCO'], 'hERG': [0.12], 'hERG_uncertainty': [0.03],
              'Caco2': [-4.9], 'Lipinski': ['Accepted']}).to_csv('fake_admetlab.csv', index=False)
r = load_admetlab_results('fake_admetlab.csv')
print(f"load_admetlab_results on a non-empty file -> shape {r.shape}, columns {list(r.columns)}")
pd.DataFrame(columns=['smiles']).to_csv('empty_admetlab.csv', index=False)
try:
    load_admetlab_results('empty_admetlab.csv')
    print("empty file -> NO ERROR RAISED (defect)")
except ValueError as e:
    print(f"empty file -> ValueError raised as documented: {e}")
try:
    load_admetlab_results('does_not_exist.csv')
except Exception as e:                                       # noqa: BLE001
    print(f"missing file -> {type(e).__name__} (unhandled by the Skill)")

print("\nWhat the loader does NOT do:")
print("  - it asserts no column contract, so ANY csv passes:",
      load_admetlab_results('fake_admetlab.csv').shape)
pd.DataFrame({'unrelated': [1, 2]}).to_csv('wrong_shape.csv', index=False)
print("  - a completely unrelated CSV also passes:",
      load_admetlab_results('wrong_shape.csv').shape)
print("  - the Skill's instruction 'Preserve the uncertainty columns and task")
print("    identifier in downstream reports' has no code behind it and no check.")
