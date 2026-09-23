"""Input 5 (Stress / multi-part, REGRESSION + re-verification): "I have a synthetic
feature table of 6 features coming out of ion-family collapsing. Match what you can
against my library with matchms, flag anything MetFrag would need to resolve, assign
each an MSI/Schymanski level, and tell me which ones are safe to carry into pathway
enrichment vs. which would inflate it."

Pre-fix finding being re-tested: the pre-fix audit's synthetic isomer pair
(citrate/isocitrate) did NOT happen to score as tied under matchms, so the
tied-candidate code path was never actually exercised by matchms in that run (only
via MetFrag). This version gives isocitrate the SAME fragment peaks/intensities as
citrate (chemically plausible -- true constitutional isomers routinely fragment
identically, which is exactly the "isomer wall" SKILL.md warns about and is exactly
what the real MetFrag run in Input 3 reproduced: citrate/isocitrate tied at 1.0), so
matchms's ModifiedCosine score for both references is forced to tie for a query that
matches the shared fragmentation pattern -- this exercises the Skill's OWN current
TIE_MARGIN loop (copied verbatim from the fixed SKILL.md) end-to-end via matchms
itself, not just via MetFrag.
"""
import numpy as np
from matchms import Spectrum, calculate_scores
from matchms.filtering import default_filters, normalize_intensities, add_precursor_mz

try:
    from matchms.similarity import ModifiedCosineGreedy as ModifiedCosine
except ImportError:
    from matchms.similarity import ModifiedCosine

TIE_MARGIN = 0.02


def prepare(spectrum):
    return normalize_intensities(add_precursor_mz(default_filters(spectrum)))


def raw_spectrum(name, precursor, mz, intensities):
    return Spectrum(mz=np.array(mz, dtype=float), intensities=np.array(intensities, dtype=float),
                     metadata={'compound_name': name, 'precursor_mz': precursor})


references_raw = [
    raw_spectrum('citrate', 191.0197, [59.01, 87.01, 111.01, 129.02, 147.03, 173.01, 191.02],
                 [0.3, 0.5, 0.4, 0.6, 1.0, 0.35, 0.2]),
    # isocitrate: SAME peaks/intensities as citrate -- true constitutional isomers with
    # identical fragmentation, the exact scenario the isomer-wall failure mode describes
    # and the one Input 3's real MetFrag run reproduced (both scored 1.0).
    raw_spectrum('isocitrate', 191.0197, [59.01, 87.01, 111.01, 129.02, 147.03, 173.01, 191.02],
                 [0.3, 0.5, 0.4, 0.6, 1.0, 0.35, 0.2]),
    raw_spectrum('glutamine', 145.0619, [56.05, 74.02, 84.04, 101.05, 127.05, 145.06],
                 [0.2, 0.6, 1.0, 0.4, 0.3, 0.15]),
]

features = {
    # F1: matches citrate/isocitrate equally -> should now hit the TIE_MARGIN branch -> Level 3
    'F1_isomer_pair': raw_spectrum('F1', 191.0197, [59.01, 87.01, 111.01, 129.02, 147.03, 173.01, 191.02],
                                    [0.31, 0.49, 0.39, 0.58, 1.0, 0.34, 0.19]),
    'F2_promiscuous': raw_spectrum('F2', 191.0197, [91.05, 120.08], [0.9, 1.0]),
    'F3_glutamine_like': raw_spectrum('F3', 145.0619, [56.05, 74.02, 84.04, 101.05, 127.05, 145.06],
                                       [0.22, 0.58, 1.0, 0.41, 0.29, 0.14]),
    'F4_no_library_hit': raw_spectrum('F4', 268.0954, [136.06, 152.06, 268.10], [0.4, 1.0, 0.3]),
}
ms1_only_evidence = {
    'F5_ms1_only_clean': {'unambiguous_formula': True},
    'F6_bare_feature': {},
}


def assign_level(evidence):
    if evidence.get('authentic_standard_same_method'):
        return 1
    if evidence.get('library_match') and evidence['library_match']['score'] >= 0.7 and evidence['library_match']['matches'] >= 6:
        return '2a'
    if evidence.get('candidate_set'):
        return 3
    if evidence.get('unambiguous_formula'):
        return 4
    return 5


references = [prepare(s) for s in references_raw]
results = []

for fid, spec in features.items():
    query = prepare(spec)
    scores = calculate_scores(references, [query], ModifiedCosine(tolerance=0.005))
    pairs = scores.scores_by_query(query)
    if not pairs:
        results.append((fid, None, 0.0, 0, assign_level({}), 0))
        continue
    score_field, match_field = pairs[0][1].dtype.names
    # This is SKILL.md's current "Match MS/MS Against a Spectral Library" loop body,
    # copied verbatim (TIE_MARGIN keep-all-hits-within-margin logic), not a bespoke
    # audit heuristic.
    ranked = sorted(pairs, key=lambda pair: pair[1][score_field], reverse=True)
    top_score = ranked[0][1][score_field]
    passing = [(ref, hit) for ref, hit in ranked
               if hit[score_field] >= top_score - TIE_MARGIN
               and hit[score_field] >= 0.7 and hit[match_field] >= 6]
    if len(passing) > 1:
        names = [ref.get('compound_name') for ref, _ in passing]
        level = 3
        best_ref_name = "+".join(names)
        best_score = float(passing[0][1][score_field])
        best_matches = int(passing[0][1][match_field])
        n_candidates = len(passing)
    elif len(passing) == 1:
        ref, hit = passing[0]
        level = '2a'
        best_ref_name = ref.get('compound_name')
        best_score = float(hit[score_field])
        best_matches = int(hit[match_field])
        n_candidates = 1
    else:
        level = 5
        best_ref_name = None
        best_score = 0.0
        best_matches = 0
        n_candidates = 0
    results.append((fid, best_ref_name, best_score, best_matches, level, n_candidates))

for fid, evidence in ms1_only_evidence.items():
    results.append((fid, None, None, None, assign_level(evidence), 0))

print(f"{'feature':<24}{'best_ref':<24}{'score':>7}{'matches':>9}{'level':>8}{'candidates':>12}  pathway_safe")
for fid, ref, score, matches, level, n_candidates in results:
    safe = level in (1, '2a') and n_candidates <= 1
    score_s = f"{score:.3f}" if isinstance(score, float) else 'n/a'
    matches_s = str(matches) if matches is not None else 'n/a'
    ref_s = ref or '<none>'
    print(f"{fid:<24}{ref_s:<24}{score_s:>7}{matches_s:>9}{str(level):>8}{n_candidates:>12}  {'YES' if safe else 'NO -- flag'}")
