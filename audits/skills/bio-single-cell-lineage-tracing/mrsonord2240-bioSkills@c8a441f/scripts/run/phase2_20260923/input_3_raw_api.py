"""Phase 2 Input 3: execute the raw-read API contract checks in the current Skill."""
import inspect
import cassiopeia as cas

names = ["resolve_umi_sequence", "align_sequences", "call_alleles", "call_lineage_groups", "convert_alleletable_to_character_matrix"]
for name in names:
    fn = getattr(cas.pp, name)
    print(name, inspect.signature(fn))
assert all(hasattr(cas.pp, name) for name in names)
sig = inspect.signature(cas.pp.convert_alleletable_to_character_matrix)
assert "alleletable" in sig.parameters and "missing_data_state" in sig.parameters
print("input3 PASS signatures available; no raw-read fixture was supplied, so full pipeline is not claimed executed")
