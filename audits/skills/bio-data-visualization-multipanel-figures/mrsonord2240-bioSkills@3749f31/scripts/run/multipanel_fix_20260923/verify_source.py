"""Static contract checks for the exact multipanel corrective commit."""
from pathlib import Path

root = Path(r"F:\OpenScience\wt\data-visualization-multipanel-figures")
skill = (root / "data-visualization/multipanel-figures/SKILL.md").read_text(encoding="utf-8")
r_example = (root / "data-visualization/multipanel-figures/examples/multi_panel_figure.R").read_text(encoding="utf-8")
py_example = (root / "data-visualization/multipanel-figures/examples/multipanel_matplotlib.py").read_text(encoding="utf-8")
guide = (root / "data-visualization/multipanel-figures/usage-guide.md").read_text(encoding="utf-8")

assert len(skill.splitlines()) <= 300
assert 'patchwork >= 1.3' in skill
assert 'wrap_plots(' in skill and 'axes = "collect"' in skill
assert '&\n  theme(plot.tag = element_text(size = 8, face = "bold")' in skill
assert 'gridExtra::arrangeGrob' in skill or 'arrangeGrob' in skill
assert 'subplot_mosaic' in skill and 'fig.subfigures()' in skill
assert 'matplotlib.rcParams["pdf.fonttype"] = 42' in skill
assert 'Do not use `bbox_inches="tight"`' in skill
assert 'not a global default' in skill
assert '183' in skill and '140' in skill

assert 'width_mm <- 183' in r_example and 'height_mm <- 140' in r_example
assert 'Cairo::CairoPDF' in r_example and 'wrap_plots' in r_example
assert 'guides = "collect"' in r_example and 'axes = "collect"' in r_example
assert 'plot.tag = element_text(size = 8, face = "bold")' in r_example

assert 'matplotlib.rcParams["pdf.fonttype"] = 42' in py_example
assert 'WIDTH_MM, HEIGHT_MM, DPI = 183, 140, 300' in py_example
assert 'layout="constrained"' in py_example and 'bbox_inches' not in py_example
assert 'fig.legend' in py_example and 'subplot_mosaic' in py_example
assert 'offset_copy' in py_example and 'units="points"' in py_example

assert len(guide.splitlines()) < 80
print("Source contract verification PASS")
