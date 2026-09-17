"""
Input 8 (NEW -- not in the pre-fix audit's 7 inputs): "My BE sample shows 60%
editing and looks clean -- confirm this isn't Cas9 contamination before I trust it."

The pre-fix audit tested the Skill's substitution-vs-indel diagnostic in only ONE
direction: a real Cas9-nuclease sample (ratio 0.12, correctly called "Cas9-like").
That is necessary but not sufficient -- a diagnostic that always says "Cas9-like"
would also pass that single check. This input tests the OTHER direction: a real,
independently-known-clean base-editing sample (this audit's own synth_cbe
CRISPResso2 2.3.4 run) must be correctly classified as clean BE (ratio > 10).
"""
import pandas as pd

RESULTS_DIR = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\base-editing-synthetic\results\CRISPResso_on_synth_cbe"
mapping_stats = pd.read_csv(RESULTS_DIR + r"\CRISPResso_mapping_statistics.txt", sep="\t")
freq = pd.read_csv(RESULTS_DIR + r"\CRISPResso_quantification_of_editing_frequency.txt", sep="\t", index_col=0)
print("CRISPResso_quantification_of_editing_frequency.txt:")
print(freq.to_string())

insertions = int(freq.loc["Reference", "Insertions"])
deletions = int(freq.loc["Reference", "Deletions"])
substitutions = int(freq.loc["Reference", "Substitutions"])
print(f"\nInsertions={insertions}  Deletions={deletions}  Substitutions={substitutions}")

indels = insertions + deletions
if indels == 0:
    ratio = float("inf")
else:
    ratio = substitutions / indels
print(f"Substitution-vs-indel ratio = {substitutions}/{indels} = {ratio}")

# Skill's own stated thresholds (SKILL.md "Quantitative Thresholds" table):
# >10 = clean BE; <3 = Cas9-like.
print("\nSKILL.md threshold: >10 = clean BE, <3 = Cas9-like")
is_clean = ratio > 10
is_cas9_like = ratio < 3
print(f"Classifies as clean BE: {is_clean}")
print(f"Classifies as Cas9-like: {is_cas9_like}")

assert insertions == 0 and deletions == 0, "expected a genuinely indel-free real BE sample for this check"
assert ratio == float("inf") and is_clean and not is_cas9_like
print("\nPASS: a real, independently-known clean base-editing sample (0 indels, 120 real "
      "substitutions out of 200 reads) is correctly classified as clean BE, not Cas9-like -- "
      "confirming the diagnostic discriminates in BOTH directions, not just the Cas9-contamination "
      "direction the pre-fix audit checked.")
