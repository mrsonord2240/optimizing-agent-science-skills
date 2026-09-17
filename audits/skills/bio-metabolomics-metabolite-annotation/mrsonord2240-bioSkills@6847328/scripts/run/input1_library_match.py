"""Input 1 (Canonical, REGRESSION): "Match my MS/MS spectra against a reference
library using modified cosine with a 0.7 score / 6-peak floor, and tell me the
confidence level for each hit."

This is the fixed Skill's current "Match MS/MS Against a Spectral Library" code
block, copied verbatim (TIE_MARGIN loop included -- this is the exact pattern an
agent following the current SKILL.md would produce), run against the SAME
synthetic library/queries as the pre-fix audit so the precursor_mz regression is
directly comparable. Reuses references from `bio-metabolomics-metabolite-annotation`
pre-fix audit's Input 1 (see data/README.md) plus the Q4 no-precursor case that
the fix's Common Errors table rewrite is about.
"""
import numpy as np
from matchms import Spectrum, calculate_scores
from matchms.filtering import default_filters, normalize_intensities, add_precursor_mz

try:
    from matchms.similarity import ModifiedCosineGreedy as ModifiedCosine  # matchms 0.33+
except ImportError:
    from matchms.similarity import ModifiedCosine  # matchms <= 0.32


def prepare(spectrum):
    spectrum = default_filters(spectrum)
    spectrum = add_precursor_mz(spectrum)  # required for ModifiedCosine; a spectrum with no
                                            # derivable precursor_mz still raises AssertionError
                                            # here, it does not silently score zero
    return normalize_intensities(spectrum)


def raw_spectrum(name, precursor, mz, intensities, set_precursor=True):
    meta = {'compound_name': name}
    if set_precursor:
        meta['precursor_mz'] = precursor
    return Spectrum(mz=np.array(mz, dtype=float), intensities=np.array(intensities, dtype=float), metadata=meta)


references_raw = [
    raw_spectrum('citrate', 191.0197, [59.01, 87.01, 111.01, 129.02, 147.03, 173.01, 191.02],
                 [0.3, 0.5, 0.4, 0.6, 1.0, 0.35, 0.2]),
    raw_spectrum('glutamine', 145.0619, [56.05, 74.02, 84.04, 101.05, 127.05, 145.06],
                 [0.2, 0.6, 1.0, 0.4, 0.3, 0.15]),
    raw_spectrum('phenylalanine', 164.0712, [74.02, 91.05, 103.05, 120.08, 147.08, 164.07],
                 [0.25, 0.5, 0.35, 1.0, 0.45, 0.2]),
    raw_spectrum('tryptophan', 203.0821, [91.05, 118.06, 132.08, 146.06, 159.09, 188.07, 203.08],
                 [0.2, 0.35, 1.0, 0.4, 0.3, 0.25, 0.15]),
]

queries_raw = [
    raw_spectrum('Q1_clean_citrate', 191.0197, [59.01, 87.01, 111.01, 129.02, 147.03, 173.01, 191.02],
                 [0.31, 0.48, 0.41, 0.58, 1.0, 0.33, 0.22]),
    raw_spectrum('Q2_promiscuous', 191.0197, [91.05, 120.08], [0.9, 1.0]),
    raw_spectrum('Q3_weak_trp', 203.0821, [91.20, 118.30, 132.20], [0.5, 0.6, 0.4]),
    raw_spectrum('Q4_no_precursor', None, [59.01, 87.01, 111.01, 129.02, 147.03], [0.3, 0.5, 0.4, 0.6, 1.0],
                 set_precursor=False),
]

references = [prepare(s) for s in references_raw]

print(f"{'query':<20}{'result':<70}")
for q in queries_raw:
    query = prepare(q)  # add_precursor_mz() itself only warns for a spectrum with no
                         # derivable precursor_mz -- it does NOT raise here. The
                         # AssertionError SKILL.md documents fires later, inside
                         # ModifiedCosine.pair() at scoring time (see try/except below).
                         # Confirms the Version Compatibility section's wording
                         # ("raises ... afterward") but the inline code comment on the
                         # add_precursor_mz() line ("raises AssertionError here") could
                         # be misread as firing on that exact call -- see P2 finding.

    TIE_MARGIN = 0.02  # candidates within this margin of the top score are tied, not resolved
    try:
        scores = calculate_scores(references, [query], ModifiedCosine(tolerance=0.005))
    except AssertionError as e:
        print(f"{query.get('compound_name'):<20}ERROR at scoring time: {e}  "
              f"[REGRESSION CHECK: SKILL.md's fixed Common Errors table + Version "
              f"Compatibility note now correctly describe this as an AssertionError, "
              f"not a silent zero score -- confirmed.]")
        continue
    pairs = scores.scores_by_query(query)
    if not pairs:
        print(f"{query.get('compound_name'):<20}no candidate scored -> Level 5")
        continue
    score_field, match_field = pairs[0][1].dtype.names
    ranked = sorted(pairs, key=lambda pair: pair[1][score_field], reverse=True)
    top_score = ranked[0][1][score_field]
    passing = [(ref, hit) for ref, hit in ranked
               if hit[score_field] >= top_score - TIE_MARGIN
               and hit[score_field] >= 0.7 and hit[match_field] >= 6]
    if len(passing) > 1:
        names = [ref.get('compound_name') for ref, _ in passing]
        print(f"{query.get('compound_name'):<20}{names} tied -> Level 3 (isomer wall)")
    elif len(passing) == 1:
        ref, hit = passing[0]
        print(f"{query.get('compound_name'):<20}{ref.get('compound_name')} "
              f"score={float(hit[score_field]):.3f} matches={int(hit[match_field])} -> Level 2a")
    else:
        print(f"{query.get('compound_name'):<20}no confident candidate -> Level 5")
