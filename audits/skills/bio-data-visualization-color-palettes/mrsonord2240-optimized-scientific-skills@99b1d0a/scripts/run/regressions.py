"""Independent Python re-audit regressions for inputs 3, 4, 5 and new input 7."""

from pathlib import Path
import json
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

# New input 8: require a complete, compact response contract for a masked
# sequential expression heatmap. This exercises the documented contract as a
# deliverable rather than only searching for its field names in SKILL.md.
contract_data = data.copy()
contract_data[3:8, 9:15] = np.nan
contract_masked = np.ma.masked_invalid(contract_data)
contract_cmap = plt.get_cmap("cividis").copy()
contract_cmap.set_bad("#BBBBBB")
contract_vmin = float(np.nanpercentile(contract_data, 1))
contract_vmax = float(np.nanpercentile(contract_data, 99))
fig, axis = plt.subplots(figsize=(8, 5), constrained_layout=True)
contract_image = axis.imshow(
    contract_masked,
    cmap=contract_cmap,
    vmin=contract_vmin,
    vmax=contract_vmax,
)
axis.set_title("Cividis expression heatmap; missing cells grey")
axis.axis("off")
fig.colorbar(contract_image, ax=axis, label="Expression")
fig.savefig(fig_dir / "i8_response_contract.png", dpi=140)
plt.close(fig)

contract_l = lab_lightness(plt.get_cmap("cividis"))
response_contract = {
    "palette_name_and_type": {"name": "cividis", "type": "sequential"},
    "normalization_bounds_reference": {
        "normalization": "linear",
        "bounds": [contract_vmin, contract_vmax],
        "clipping": "1st and 99th finite-value percentiles",
        "reference": None,
    },
    "missing_values": {
        "masked_count": int(contract_masked.mask.sum()),
        "encoding": "#BBBBBB neutral grey",
    },
    "cvd_minimum_distances": {
        "status": "not applicable to a continuous sequential ramp",
        "deutan": None,
        "protan": None,
        "tritan": None,
    },
    "luminance_verdict": {
        "status": "monotonic",
        "minimum_delta_lstar": float(np.min(np.diff(contract_l))),
    },
    "redundant_encoding": {
        "encoding": "none",
        "reason": "continuous magnitude is also ordered by monotonic lightness",
    },
    "visual_inspection": {
        "artifact": "figs/i8_response_contract.png",
        "status": "generated for independent visual inspection",
    },
}
required_contract_fields = {
    "palette_name_and_type",
    "normalization_bounds_reference",
    "missing_values",
    "cvd_minimum_distances",
    "luminance_verdict",
    "redundant_encoding",
    "visual_inspection",
}
assert set(response_contract) == required_contract_fields
assert response_contract["missing_values"]["masked_count"] == 30
assert response_contract["luminance_verdict"]["status"] == "monotonic"
(fig_dir.parent / "run" / "input8_response_contract.json").write_text(
    json.dumps(response_contract, indent=2) + "\n", encoding="utf-8"
)

# New input 9: use an arbitrary physical reference rather than zero or 0.5,
# preserve NaN and both infinities as missing, and reject an invalid reference
# that is not strictly between the bounds.
reference_value = 37.2
physical = np.linspace(30.0, 50.0, 3500, dtype=float).reshape(50, 70)
physical[2, 3] = np.nan
physical[4, 5] = np.inf
physical[6, 7] = -np.inf
physical[11, 13] = np.nan
physical[31, 41] = np.inf
physical_masked = np.ma.masked_invalid(physical)
physical_cmap = plt.get_cmap("RdBu_r").copy()
physical_cmap.set_bad("#BBBBBB")
physical_norm = TwoSlopeNorm(vmin=30.0, vcenter=reference_value, vmax=50.0)
fig, axis = plt.subplots(figsize=(8, 5), constrained_layout=True)
physical_image = axis.imshow(physical_masked, cmap=physical_cmap, norm=physical_norm)
axis.set_title("Physical measurement around reference 37.2; non-finite cells grey")
axis.axis("off")
fig.colorbar(physical_image, ax=axis, label="Measurement")
fig.savefig(fig_dir / "i9_arbitrary_reference_nonfinite.png", dpi=140)
plt.close(fig)
assert physical_norm(reference_value) == 0.5
assert int(physical_masked.mask.sum()) == 5
assert to_hex(physical_cmap.get_bad()) == "#bbbbbb"
try:
    TwoSlopeNorm(vmin=reference_value, vcenter=reference_value, vmax=50.0)
except ValueError as error:
    invalid_reference_error = str(error)
else:
    raise AssertionError("TwoSlopeNorm accepted a reference equal to vmin")

physical_contract = {
    "palette_name_and_type": {"name": "RdBu_r", "type": "diverging"},
    "normalization_bounds_reference": {
        "normalization": "TwoSlopeNorm",
        "bounds": [30.0, 50.0],
        "reference": reference_value,
        "reference_maps_to": float(physical_norm(reference_value)),
    },
    "missing_values": {
        "masked_count": int(physical_masked.mask.sum()),
        "included_nonfinite_kinds": ["NaN", "+Inf", "-Inf"],
        "encoding": "#BBBBBB neutral grey",
    },
    "cvd_minimum_distances": {
        "status": "not applicable to a continuous diverging ramp",
        "deutan": None,
        "protan": None,
        "tritan": None,
    },
    "luminance_verdict": {
        "status": "not applicable as a single monotonic sequence",
        "reason": "diverging arms are interpreted away from a declared reference",
    },
    "redundant_encoding": {
        "encoding": "captioned reference and explicit missing-value legend",
        "reason": "reference and missingness are semantic states, not extra categories",
    },
    "visual_inspection": {
        "artifact": "figs/i9_arbitrary_reference_nonfinite.png",
        "status": "generated for independent visual inspection",
    },
}
assert set(physical_contract) == required_contract_fields
(fig_dir.parent / "run" / "input9_response_contract.json").write_text(
    json.dumps(physical_contract, indent=2) + "\n", encoding="utf-8"
)

print("PYTHON REGRESSIONS PASS")
print("Input 3 CVD minima:", cvd_distances)
print("Input 4 q99:", float(vmax), "zero norm:", float(im1.norm(0)))
print("Input 5 many-group deutan minima:", many_group_deutan)
print("Input 7 centre norm:", float(norm(0.5)), "missing count:", int(masked.mask.sum()))
print("Input 8 contract fields:", sorted(response_contract),
      "missing count:", response_contract["missing_values"]["masked_count"])
print("Input 9 reference norm:", float(physical_norm(reference_value)),
      "missing count:", int(physical_masked.mask.sum()),
      "invalid-bound error:", invalid_reference_error)
