"""Verify the numeric planning examples stated in SKILL.md (audit evidence)."""
focused_pre = 2_000_000 / 8_000
focused_endpoint_range = (focused_pre / 10, focused_pre / 5)
star_transduction = 30_000_000 / 30_000
star_per_mouse = 10_000_000 / 30_000
genomewide = 1_000_000 / 80_000

assert focused_pre == 250
assert focused_endpoint_range == (25, 50)
assert star_transduction == 1000
assert round(star_per_mouse) == 333
assert genomewide == 12.5
print(f"focused_pre={focused_pre:.0f}x; endpoint_range={focused_endpoint_range[0]:.0f}-{focused_endpoint_range[1]:.0f}x")
print(f"crispr_star_preimplant={star_transduction:.0f}x; per_mouse={star_per_mouse:.1f}x")
print(f"genomewide_without_star={genomewide:.1f}x")
