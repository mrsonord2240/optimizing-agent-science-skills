# Exercise the exact filter logic shipped in examples/virtual_screen.py's virtual_screen()
# and SKILL.md's dock_single(), against a deliberately bad (positive-energy) pose list.

# dock_single()-style filter (SKILL.md):
def dock_single_filter(energies):
    valid = [i for i, e in enumerate(energies) if e[0] < 0]
    if len(valid) < len(energies):
        energies = [energies[i] for i in valid]
    return energies

# virtual_screen()-style filter (examples/virtual_screen.py):
def virtual_screen_filter(energies):
    energies = [e for e in energies if e[0] < 0] or energies
    return energies

# Deliberately bad pose set: mode 1 has a nonsensical +68.69 kcal/mol affinity
# (this is the exact value the original audit observed from a real Vina run),
# planted as the *first* (best-ranked-by-Vina-order) mode to check the filter
# doesn't just trust rank order.
bad_energies = [
    (68.69, 0.0, 0.0),
    (-5.978, 2.6, 3.8),
    (-5.153, 2.7, 3.9),
    (-5.054, 3.2, 4.0),
]

r1 = dock_single_filter(list(bad_energies))
r2 = virtual_screen_filter(list(bad_energies))

print("dock_single filter result:", r1)
assert 68.69 not in [e[0] for e in r1], "FAIL: positive-energy mode not removed by dock_single filter"
assert len(r1) == 3, f"FAIL: expected 3 remaining modes, got {len(r1)}"

print("virtual_screen filter result:", r2)
assert 68.69 not in [e[0] for e in r2], "FAIL: positive-energy mode not removed by virtual_screen filter"
assert len(r2) == 3, f"FAIL: expected 3 remaining modes, got {len(r2)}"

# All-positive edge case: virtual_screen_filter falls back to the original list
# (documented "or energies" behavior) rather than returning an empty list.
all_bad = [(12.0, 0, 0), (5.0, 1, 1)]
r3 = virtual_screen_filter(list(all_bad))
print("virtual_screen filter, all-positive input:", r3)
assert r3 == all_bad, "FAIL: all-positive fallback behavior changed"

print("ALL FILTER ASSERTIONS PASSED")
