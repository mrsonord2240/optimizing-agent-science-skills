"""Input 5 (Stress / multi-part): "I have a synthetic feature table of 6 features
coming out of ion-family collapsing. Match what you can against my small library
with matchms, flag anything MetFrag would need to resolve, assign each an
MSI/Schymanski level, and tell me which ones are safe to carry into pathway
enrichment vs. which would inflate it."

Exercises the Skill's full chain: library match -> assign_level -> the
"Database-mapping inflation poisons pathway analysis" failure mode (SKILL.md),
i.e. carrying candidate-set size forward as a pathway-safety flag. Reuses the
SYNTHETIC library/queries from input1 (same data, documented synthetic) plus
two additional MS1-only / no-evidence features to round out the level range.
"""
import numpy as np
from matchms import Spectrum, calculate_scores
from matchms.filtering import default_filters, normalize_intensities, add_precursor_mz

try:
    from matchms.similarity import ModifiedCosineGreedy as ModifiedCosine
except ImportError:
    from matchms.similarity import ModifiedCosine

SCORE_FLOOR = 0.7
MATCH_FLOOR = 6


def prepare(spectrum):
    return normalize_intensities(add_precursor_mz(default_filters(spectrum)))


def raw_spectrum(name, precursor, mz, intensities):
    return Spectrum(mz=np.array(mz, dtype=float), intensities=np.array(intensities, dtype=float),
                     metadata={'compound_name': name, 'precursor_mz': precursor})


references_raw = [
    raw_spectrum('citrate', 191.0197, [59.01, 87.01, 111.01, 129.02, 147.03, 173.01, 191.02],
                 [0.3, 0.5, 0.4, 0.6, 1.0, 0.35, 0.2]),
    raw_spectrum('isocitrate', 191.0197, [59.01, 87.01, 129.02, 147.03],
                 [0.32, 0.51, 0.61, 1.0]),  # near-identical fragmentation to citrate on purpose (isomer wall)
    raw_spectrum('glutamine', 145.0619, [56.05, 74.02, 84.04, 101.05, 127.05, 145.06],
                 [0.2, 0.6, 1.0, 0.4, 0.3, 0.15]),
]

# Feature table: 6 features post-ion-family-collapsing. F1-F3 have MS/MS, F4 has MS/MS
# with no library counterpart (would route to MetFrag/SIRIUS), F5 is MS1-only with a
# clean isotope/adduct call, F6 is a bare feature.
features = {
    'F1_citrus_like': raw_spectrum('F1', 191.0197, [59.01, 87.01, 111.01, 129.02, 147.03, 173.01, 191.02],
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
    if evidence.get('library_match') and evidence['library_match']['score'] >= SCORE_FLOOR and evidence['library_match']['matches'] >= MATCH_FLOOR:
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
        results.append((fid, None, 0.0, 0, assign_level({}), 1))
        continue
    score_field, match_field = pairs[0][1].dtype.names
    # candidate_set size = number of distinct references tied within 0.02 of the top score
    # (this is what the SKILL.md "Database-mapping inflation" failure mode is about:
    # an ambiguous feature should carry its whole tied candidate set forward, not just
    # the single argmax hit, or pathway enrichment gets a phantom single ID)
    scored = [(ref, float(hit[score_field]), int(hit[match_field])) for ref, hit in pairs]
    top_score = max(s for _, s, _ in scored)
    tied = [r for r, s, m in scored if s >= top_score - 0.02 and s >= SCORE_FLOOR]
    best_ref, best_score, best_matches = max(scored, key=lambda t: t[1])
    if best_score >= SCORE_FLOOR and best_matches >= MATCH_FLOOR:
        if len(tied) > 1:
            level = 3  # tied isomer candidates -> tentative candidate SET, not a single 2a name
        else:
            level = '2a'
    else:
        level = assign_level({})
    results.append((fid, best_ref.get('compound_name'), best_score, best_matches, level, len(tied)))

for fid, evidence in ms1_only_evidence.items():
    results.append((fid, None, None, None, assign_level(evidence), 0))

print(f"{'feature':<20}{'best_ref':<14}{'score':>7}{'matches':>9}{'level':>8}{'candidates':>12}  pathway_safe")
for fid, ref, score, matches, level, n_candidates in results:
    # pathway-safety flag per SKILL.md: only Level 1/2a with a single resolved candidate
    # is safe to carry as a single compound ID into enrichment; anything Level 3 (or a
    # tied candidate set) must carry the whole set or be excluded, never collapsed to one ID.
    safe = level in (1, '2a') and n_candidates <= 1
    score_s = f"{score:.3f}" if isinstance(score, float) else 'n/a'
    matches_s = str(matches) if matches is not None else 'n/a'
    ref_s = ref or '<none>'
    print(f"{fid:<20}{ref_s:<14}{score_s:>7}{matches_s:>9}{str(level):>8}{n_candidates:>12}  {'YES' if safe else 'NO -- flag'}")
