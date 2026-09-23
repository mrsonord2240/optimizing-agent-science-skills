"""New input: quality-validation function on a fresh synthetic matcher and edge checks."""
def pharmacophore_enrichment(query_pharmacophore, actives, inactives, matches_pharmacophore):
    if not actives or not inactives:
        raise ValueError('actives and inactives must both be non-empty')
    n_active_match = sum(bool(matches_pharmacophore(mol, query_pharmacophore)) for mol in actives)
    n_inactive_match = sum(bool(matches_pharmacophore(mol, query_pharmacophore)) for mol in inactives)
    active_rate = n_active_match / len(actives)
    inactive_rate = n_inactive_match / len(inactives)
    return float('inf') if inactive_rate == 0 else active_rate / inactive_rate

query = {"required": "aromatic-donor"}
actives = ["propranolol", "atenolol", "metoprolol"]
inactives = ["hexane", "cyclohexanol", "pyridine"]
matches = {"propranolol", "atenolol"}
score = pharmacophore_enrichment(query, actives, inactives, lambda mol, _: mol in matches)
print("ENRICHMENT", score)
assert score == float("inf")
try:
    pharmacophore_enrichment(query, [], inactives, lambda *_: False)
except ValueError as exc:
    print("EMPTY_ACTIVE_ERROR", str(exc))
else:
    raise AssertionError("empty active set must be rejected")
print("ASSERT correct no-inactive-match handling and empty-set rejection: PASS")
