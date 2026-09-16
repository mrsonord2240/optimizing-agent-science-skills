"""
Input 4 (Stress / shipped-file check) -- run the Skill's OWN shipped examples/run_jacks.py
(copied here as skill_example_run_jacks.py, unmodified) against real JACKS output from
Input 1, exactly as a researcher who trusts the shipped example would. Tests gate 8
(shipped-means-present) at the level of "does the shipped code actually run", not just
"does the file exist".
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import skill_example_run_jacks as ex

OUT1 = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out1\whp_false_as_skillmd_recommends"

try:
    genes, guides = ex.analyze_results(
        f"{OUT1}_gene_JACKS_results.txt",
        f"{OUT1}_grna_JACKS_results.txt",
    )
    print("\nanalyze_results() SUCCEEDED")
except Exception as e:
    print("\nanalyze_results() RAISED:", type(e).__name__, "--", e)
    raise
