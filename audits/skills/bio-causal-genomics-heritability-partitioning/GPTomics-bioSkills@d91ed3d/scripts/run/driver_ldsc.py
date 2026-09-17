"""
Driver that runs ldsc.py's CLI dispatch after patching the missing function
aliases that abdenlab/ldsc-python3 (v2.0.0, commit b6176a4) leaves broken.

Real bug found during this audit: ldsc.py's dispatch (lines 844-849) calls
    sumstats.estimate_rg / sumstats.estimate_h2 / sumstats.cell_type_specific
but ldscore/sumstats.py only defines
    estimate_genetic_correlation / estimate_heritability /
    estimate_cell_type_specific_heritability
so every one of --h2, --rg, --h2-cts raises AttributeError out of the box.
This contradicts SKILL.md's explicit claim that abdenlab/ldsc-python3 v2.0.0
"retains the working --h2 / --rg / --h2-cts CLI" (unlike belowlab/ldsc v3.0.1).

This driver monkeypatches the three aliases (a one-line fix a user would have
to discover for themselves) so we can test whether the underlying regression
implementation is otherwise correct, exercising the Skill's own documented
CLI flags and cross-checking against its documented output format
(intercept, mean chi^2, ratio, h2, SE).

Usage: python driver_ldsc.py <argv...>   (same flags as ldsc.py)
"""
import runpy
import sys

LDSC_DIR = r"F:\OpenScience\audit-envs\mendelian-randomization-analyst\ldsc-python3"
sys.path.insert(0, LDSC_DIR)

import ldscore.sumstats as sumstats  # noqa: E402

sumstats.estimate_h2 = sumstats.estimate_heritability
sumstats.estimate_rg = sumstats.estimate_genetic_correlation
sumstats.cell_type_specific = sumstats.estimate_cell_type_specific_heritability

sys.argv = ["ldsc.py"] + sys.argv[1:]
runpy.run_path(LDSC_DIR + r"\ldsc.py", run_name="__main__")
