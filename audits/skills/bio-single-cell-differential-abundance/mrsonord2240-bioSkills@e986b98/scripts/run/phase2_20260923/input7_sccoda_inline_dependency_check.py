"""New independent input: execute the missing-import point of SKILL.md's inline scCODA block."""
import pandas as pd
from sccoda.util import cell_composition_data as dat
from sccoda.util import comp_ana as mod

counts = pd.DataFrame(
    {
        "sample": ["S1", "S2", "S3", "S4"],
        "condition": ["control", "control", "treated", "treated"],
        "B": [50, 51, 45, 46],
        "T": [50, 49, 55, 54],
    }
)
data = dat.from_pandas(counts, covariate_columns=["sample", "condition"])
try:
    tf.random.set_seed(42)  # exactly as printed in SKILL.md; tensorflow is not imported there
except NameError as exc:
    print(f"EXPECTED_SOURCE_FAILURE={exc}")
else:
    print("UNEXPECTED_SUCCESS=tf was available without an import")
    raise SystemExit(2)
print(f"COUNTS_ROWS={len(counts)} DATA_TYPE={type(data).__name__}")
