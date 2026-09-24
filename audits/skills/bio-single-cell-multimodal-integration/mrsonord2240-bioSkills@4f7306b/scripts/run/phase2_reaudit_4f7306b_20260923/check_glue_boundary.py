import importlib.util
assert importlib.util.find_spec("scglue") is None
print("glue_boundary_clean_exit scglue_not_installed_in_private_runtime=true supported_host_required=true")
