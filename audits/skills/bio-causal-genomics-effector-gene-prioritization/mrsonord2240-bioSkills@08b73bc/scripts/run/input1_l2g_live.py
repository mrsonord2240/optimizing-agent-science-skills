"""Phase-2 regression runner for the shipped, live Open Targets L2G example."""
import runpy
import sys

sys.argv = [
    "opentargets_l2g_query.py",
    "000011d495b34f3b3969399fac6d3299",
]
runpy.run_path(
    r"F:\OpenScience\audits\bio-causal-genomics-effector-gene-prioritization\run\skill_copy\examples\opentargets_l2g_query.py",
    run_name="__main__",
)
