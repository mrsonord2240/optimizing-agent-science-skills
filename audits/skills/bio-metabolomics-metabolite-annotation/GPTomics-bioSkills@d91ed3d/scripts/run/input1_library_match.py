"""Input 1 (Canonical): "Match my MS/MS spectra against a reference library
using modified cosine with a 0.7 score / 6-peak floor, and tell me the
confidence level for each hit."

Follows the SKILL.md 'Match MS/MS Against a Spectral Library' pattern
verbatim (matchms.calculate_scores, ModifiedCosineGreedy with ImportError
fallback, dtype-derived field names, score+matched-peak floor) against a
small SYNTHETIC library of 4 reference spectra and 4 query spectra designed
to cover: a clean match, a promiscuous few-peak match, a below-floor score,
and a query with no precursor m/z set (to check the skill's own warned
failure mode: "ModifiedCosine silently returns zeros without add_precursor_mz").
"""
import numpy as np
from matchms import Spectrum, calculate_scores
from matchms.filtering import default_filters, normalize_intensities, add_precursor_mz

try:
    from matchms.similarity import ModifiedCosineGreedy as ModifiedCosine  # matchms 0.33+
except ImportError:
    from matchms.similarity import ModifiedCosine  # matchms <= 0.32

SCORE_FLOOR = 0.7
MATCH_FLOOR = 6


def prepare(spectrum):
    spectrum = default_filters(spectrum)
    spectrum = add_precursor_mz(spectrum)
    return normalize_intensities(spectrum)


def raw_spectrum(name, precursor, mz, intensities, set_precursor=True):
    meta = {'compound_name': name}
    if set_precursor:
        meta['precursor_mz'] = precursor
    return Spectrum(mz=np.array(mz, dtype=float), intensities=np.array(intensities, dtype=float), metadata=meta)


# --- synthetic library: 4 references (realistic precursor masses, invented fragments) ---
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

# --- synthetic queries ---
queries_raw = [
    # Q1: near-identical to citrate -> should be a clean Level 2a match
    raw_spectrum('Q1_clean_citrate', 191.0197, [59.01, 87.01, 111.01, 129.02, 147.03, 173.01, 191.02],
                 [0.31, 0.48, 0.41, 0.58, 1.0, 0.33, 0.22]),
    # Q2: shares only 2 generic peaks with phenylalanine at high relative intensity
    #     -> the "promiscuous" case the skill's matched-peak floor exists to catch
    raw_spectrum('Q2_promiscuous', 191.0197, [91.05, 120.08], [0.9, 1.0]),
    # Q3: shares peaks with tryptophan but at a lower absolute match quality
    #     (small mass shifts) -> exercises the below-score-floor path
    raw_spectrum('Q3_weak_trp', 203.0821, [91.20, 118.30, 132.20], [0.5, 0.6, 0.4]),
    # Q4: no precursor_mz in metadata at all -> the skill's own documented failure mode
    raw_spectrum('Q4_no_precursor', None, [59.01, 87.01, 111.01, 129.02, 147.03], [0.3, 0.5, 0.4, 0.6, 1.0],
                 set_precursor=False),
]

queries = [prepare(s) for s in queries_raw]
references = [prepare(s) for s in references_raw]

# NOTE (finding, verified two independent ways): SKILL.md's own "Common Errors" table
# claims "ModifiedCosine scores all zero | Missing precursor m/z on spectra" for
# matchms 0.33+ (the version this SKILL.md declares itself compatible with, and the
# version installed here: 0.33.1). Actual behavior is a hard AssertionError raised by
# matchms.similarity._precursor_validation.get_valid_precursor_mz, not a silent zero
# score -- add_precursor_mz cannot invent a precursor_mz that isn't derivable from
# existing metadata, so Q4 (no precursor_mz, no derivable fields) still crashes even
# after the documented fix is applied. Confirmed by running the full batch (crashes)
# and by isolating ModifiedCosine().pair() on a single no-precursor spectrum (also
# crashes, see run/ transcript). The Skill's own version-compatibility guidance
# ("introspect ImportError/AttributeError/TypeError") does not mention AssertionError,
# so an agent following the Skill verbatim would not know to catch this.
print(f"{'query':<20}{'best_ref':<16}{'score':>8}{'matches':>9}  level")
for query in queries:
    try:
        scores = calculate_scores(references, [query], ModifiedCosine(tolerance=0.005))
        pairs = scores.scores_by_query(query)
        if not pairs:
            print(f"{query.get('compound_name'):<20}{'<no hits>':<16}{'n/a':>8}{'n/a':>9}  5 (no candidate scored)")
            continue
        score_field, match_field = pairs[0][1].dtype.names
        ref, hit = max(pairs, key=lambda pair: pair[1][score_field])
        score, matches = float(hit[score_field]), int(hit[match_field])
        if score >= SCORE_FLOOR and matches >= MATCH_FLOOR:
            level = '2a'
        else:
            level = '5 (insufficient evidence)'
        print(f"{query.get('compound_name'):<20}{ref.get('compound_name'):<16}{score:>8.3f}{matches:>9}  {level}")
    except AssertionError as e:
        print(f"{query.get('compound_name'):<20}{'<CRASH>':<16}{'n/a':>8}{'n/a':>9}  ERROR: {e} "
              f"(SKILL.md says this should be a silent zero score, not a crash)")
