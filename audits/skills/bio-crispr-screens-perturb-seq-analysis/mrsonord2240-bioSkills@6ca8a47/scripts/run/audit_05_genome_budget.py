"""Fresh arithmetic check for the shipped genome-scale Perturb-seq budgeting formula."""
genes = 19000
replogle_genes = 9866
base_cost = (50000, 100000)
base_channels = (10, 30)
scale = genes / replogle_genes
cost = tuple(round(x * scale) for x in base_cost)
channels = tuple(round(x * scale) for x in base_channels)
assert 1.92 < scale < 1.93
assert 96000 <= cost[0] <= 97000
assert 192000 <= cost[1] <= 193000
assert channels == (19, 58)
for cells_per_pert, cells_per_channel in [(500, 5000), (1000, 10000)]:
    channels_needed = genes * cells_per_pert / cells_per_channel
    print(f"cells_per_pert={cells_per_pert} cells_per_channel={cells_per_channel} channels_needed={channels_needed:.0f}")
print(f"scale={scale:.6f} cost=${cost[0]:,}-${cost[1]:,} channels={channels[0]}-{channels[1]}")
