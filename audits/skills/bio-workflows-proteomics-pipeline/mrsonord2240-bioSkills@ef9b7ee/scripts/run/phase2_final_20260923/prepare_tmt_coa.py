"""Rename the historical position-only audit CoA to the channel names required by the shipped script."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

path = Path(sys.argv[1])
coa = pd.read_csv(path, index_col=0)
channels = ['126', '127N', '127C', '128N', '128C', '129N', '129C', '130N', '130C', '131']
assert coa.shape == (10, 10)
coa.index = channels
coa.columns = channels
coa.to_csv(path)
print(f'Prepared named-channel CoA: {path}')
