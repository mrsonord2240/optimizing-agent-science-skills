# Input 4 (Edge/boundary) -- "My LPC 16:0 signal is unexpectedly high in my
# shotgun (direct-infusion) lipidomics data. Is this real biology or an
# in-source fragment of PC?"
# Per SKILL.md's "In-source-fragment phantom lyso-/DG-lipidome" failure mode:
# the diagnostic test is RT co-elution against the parent class, and shotgun
# data has NO retention-time axis to run it. The honest answer is: this
# cannot be resolved from shotgun data alone.
#
# To make the answer actionable, this also demonstrates what the RT
# co-elution test looks like on LC-MS data (synthetic), for the follow-up
# recommendation to re-acquire on an LC-MS platform.
import pandas as pd

print("=== Shotgun data: RT co-elution test is NOT APPLICABLE ===")
print("No retention-time axis exists in direct-infusion (shotgun) data.")
print("Per SKILL.md: 'never report elevated lyso-lipids from direct infusion")
print("without the in-source-fragment caveat.' -> flag as UNRESOLVED, recommend")
print("re-acquisition on RP-LC-MS if the elevated LPC pool needs to be trusted.\n")

print("=== Demonstration: RT co-elution test on synthetic LC-MS data ===")
lcms_rt = pd.DataFrame([
    {"Molecule": "PC 16:0/18:1", "RT_min": 8.2, "Area": 2.1e6},
    {"Molecule": "LPC 16:0",     "RT_min": 8.2, "Area": 4.5e5},  # same RT as parent PC -> phantom
    {"Molecule": "LPC 18:1",     "RT_min": 5.1, "Area": 3.0e5},  # own distinct RT -> real lyso species
])

parent_class_prefix = {"LPC": "PC"}  # lyso -> parent class map (extend as needed)
tol_min = 0.05

def classify(row, df):
    cls = row["Molecule"].split()[0]
    parent = parent_class_prefix.get(cls)
    if parent is None:
        return "n/a"
    same_rt = df[(df["Molecule"].str.startswith(parent)) &
                 (abs(df["RT_min"] - row["RT_min"]) <= tol_min)]
    return "IN-SOURCE FRAGMENT (co-elutes with parent)" if len(same_rt) > 0 else "real (own RT)"

lcms_rt["verdict"] = lcms_rt.apply(lambda r: classify(r, lcms_rt), axis=1)
print(lcms_rt.to_string(index=False))
