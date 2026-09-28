"""Print versions and optional-dependency availability before the re-audit."""
from __future__ import annotations

import importlib

packages = [
    "anndata", "scanpy", "sklearn", "umap", "openTSNE", "phate", "igraph", "skmisc"
]
for name in packages:
    try:
        module = importlib.import_module(name)
        print(f"{name}: {getattr(module, '__version__', 'version unavailable')}")
    except Exception as exc:
        print(f"{name}: IMPORT ERROR {type(exc).__name__}: {exc}")
