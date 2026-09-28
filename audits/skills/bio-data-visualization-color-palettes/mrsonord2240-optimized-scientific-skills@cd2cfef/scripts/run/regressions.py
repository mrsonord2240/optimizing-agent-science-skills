"""Independent Python re-audit regressions for inputs 3, 4, 5 and new input 7."""

from pathlib import Path
import sys

from cmcrameri import cm
from colorspacious import cspace_convert
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, TwoSlopeNorm, to_hex, to_rgb
import numpy as np
from scipy.spatial.distance import pdist


if len(sys.argv) != 3:
    raise SystemExit("usage: regressions.py <data-dir> <fig-dir>")
data_dir = Path(sys.argv[1])
fig_dir = Path(sys.argv[2])


def lab_lightness(cmap, n=256):
    rgb = cmap(np.linspace(0, 1, n))[:, :3]
    return cspace_convert(rgb, "sRGB1", "CIELab")[:, 0]


def cvd_minimum(palette, cvd_type):
    rgb = np.array([to_rgb(color) for color in palette])
    spec = {"name": "sRGB1+CVD", "cvd_type": cvd_type, "severity": 100}
    sim = np.clip(cspace_convert(rgb, spec, "sRGB1"), 0, 1)
    return float(pdist(cspace_convert(sim, "sRGB1", "CAM02-UCS")).min())


# Input 3: luminance claims and complete Python CVD simulation.
viridis_l = lab_lightness(plt.get_cmap("viridis"))
turbo_l = lab_lightness(plt.get_cmap("turbo"))
assert np.all(np.diff(viridis_l) >= 0)
assert not (np.all(np.diff(turbo_l) >= 0) or np.all(np.diff(turbo_l) <= 0))
okabe_grey = [
    "#E69F00", "#56B4E9", "#009E73", "#F0E442",
    "#0072B2", "#D55E00", "#CC79A7", "#BBBBBB",
]
cvd_distances = {
    name: cvd_minimum(okabe_grey, name)
    for name in ("deuteranomaly", "protanomaly", "tritanomaly")
}
assert all(np.isfinite(value) and value > 0 for value in cvd_distances.values())

# Input 4: migrate sequential, signed, and cyclic maps from jet.
data = np.load(data_dir / "synthetic_spatial_expr.npy")
signed = data - np.nanmean(data)
vmax = np.nanpercentile(np.abs(signed), 99)
phase_y, phase_x = np.mgrid[0 : data.shape[0], 0 : data.shape[1]]
phase = np.arctan2(phase_y - data.shape[0] / 2, phase_x - data.shape[1] / 2) % (2 * np.pi)
assert np.isfinite(vmax) and vmax > 0

fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), constrained_layout=True)
im0 = axes[0].imshow(data, cmap=cm.batlow)
axes[0].set_title("Sequential: batlow")
im1 = axes[1].imshow(signed, cmap=cm.vik, vmin=-vmax, vmax=vmax)
axes[1].set_title("Signed: vik, symmetric q99")
im2 = axes[2].imshow(phase, cmap=cm.romaO, vmin=0, vmax=2 * np.pi)
axes[2].set_title("Cyclic: romaO")
for axis, image in zip(axes, (im0, im1, im2)):
    axis.axis("off")
    fig.colorbar(image, ax=axis, fraction=0.046)
fig.savefig(fig_dir / "i4_jet_migration_fixed.png", dpi=130)
plt.close(fig)
assert im1.norm.vmin == -im1.norm.vmax
for name, cmap in (("romaO", cm.romaO), ("vikO", cm.vikO),
                   ("twilight", plt.get_cmap("twilight"))):
    ends = np.array([cmap(0.0)[:3], cmap(1.0)[:3]])
    seam = np.linalg.norm(cspace_convert(ends, "sRGB1", "CAM02-UCS")[0]
                          - cspace_convert(ends, "sRGB1", "CAM02-UCS")[1])
    assert seam < 2, (name, seam)

# Input 5: confirm hue-only many-group candidates have close CVD pairs.
many_group = {
    "tab20": [to_hex(c) for c in plt.get_cmap("tab20").colors],
    "Paired": [to_hex(c) for c in plt.get_cmap("Paired").colors],
    "Set3": [to_hex(c) for c in plt.get_cmap("Set3").colors],
}
many_group_deutan = {
    name: cvd_minimum(palette, "deuteranomaly")
    for name, palette in many_group.items()
}
assert all(value < 10 for value in many_group_deutan.values())

# New input 7: a nonzero scientific reference point and missing values.
rng = np.random.default_rng(20260927)
fraction = np.clip(rng.normal(0.5, 0.16, size=(45, 60)), 0, 1)
fraction[8:14, 12:20] = np.nan
fraction[25:30, 42:48] = 0.5
masked = np.ma.masked_invalid(fraction)
cmap = plt.get_cmap("RdBu_r").copy()
cmap.set_bad("#BBBBBB")
norm = TwoSlopeNorm(vmin=0.0, vcenter=0.5, vmax=1.0)
fig, axis = plt.subplots(figsize=(8, 5), constrained_layout=True)
image = axis.imshow(masked, cmap=cmap, norm=norm)
axis.set_title("Fraction around reference 0.5; missing values grey")
axis.axis("off")
fig.colorbar(image, ax=axis, label="Fraction")
fig.savefig(fig_dir / "i7_nonzero_midpoint_missing.png", dpi=140)
plt.close(fig)
assert norm(0.5) == 0.5
assert to_hex(cmap.get_bad()) == "#bbbbbb"
assert int(masked.mask.sum()) == 48

print("PYTHON REGRESSIONS PASS")
print("Input 3 CVD minima:", cvd_distances)
print("Input 4 q99:", float(vmax), "zero norm:", float(im1.norm(0)))
print("Input 5 many-group deutan minima:", many_group_deutan)
print("Input 7 centre norm:", float(norm(0.5)), "missing count:", int(masked.mask.sum()))
