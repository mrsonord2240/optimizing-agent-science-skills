"""Record exact Python tool versions used by the Phase 2 audit."""
import importlib.metadata as metadata
import sys

for package in ("liana", "cellphonedb", "scanpy", "anndata", "pandas", "numpy"):
    print(package, metadata.version(package))
print("python", sys.version)
