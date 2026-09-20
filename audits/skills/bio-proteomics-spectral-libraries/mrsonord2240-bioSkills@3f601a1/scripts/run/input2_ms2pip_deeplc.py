"""Input 2 (Variant A): local prediction without a Koina network dependency -
ms2pip for fragment intensities, deeplc (module-level API) for RT.
Tests whether the agent, following the Skill's Version Compatibility section,
adapts the documented `from deeplc import DeepLC` example (broken against
installed deeplc 4.5.0) to the real module-level API.
"""
from psm_utils import PSM, PSMList
import ms2pip
import deeplc

psms = PSMList(psm_list=[
    PSM(peptidoform="LGGNEQVTR/2", spectrum_id="s1"),
    PSM(peptidoform="VEATFGVDESNAK/2", spectrum_id="s2"),
])

results = ms2pip.predict_batch(psms, model="HCD")
print("ms2pip predict_batch results:", len(results), "PSMs")
for r in results:
    print(" ", r.psm.peptidoform, "n_fragments:", None if r.predicted_intensity is None else len(r.predicted_intensity))

# deeplc 4.5.0 has no DeepLC class (SKILL.md/build_library.py example is stale) -
# use the real module-level API instead.
rt_preds = deeplc.predict(psms)
print("deeplc.predict RT predictions:", rt_preds)
