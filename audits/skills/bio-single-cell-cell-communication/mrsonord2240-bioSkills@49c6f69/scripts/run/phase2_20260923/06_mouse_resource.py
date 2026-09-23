"""Phase 2 Input 7: verify the mouse alternative named by the current Skill exists in LIANA."""
import liana as li

resource = li.rs.select_resource("mouseconsensus")
assert resource is not None and len(resource) > 0
columns = set(resource.columns)
assert {"ligand", "receptor"}.issubset(columns)
print("MOUSECONSENSUS_ROWS", len(resource))
print("COLUMNS", sorted(columns))
