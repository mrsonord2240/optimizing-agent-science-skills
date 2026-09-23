"""Document the local FR-Perturb dependency boundary without installing from prohibited channels."""
import importlib.util
import shutil

print(f"spams_importable={importlib.util.find_spec('spams') is not None}")
print(f"conda_on_path={shutil.which('conda') is not None}")
print("decision=not_executed_no_supported_python312_install_in_this_env")
