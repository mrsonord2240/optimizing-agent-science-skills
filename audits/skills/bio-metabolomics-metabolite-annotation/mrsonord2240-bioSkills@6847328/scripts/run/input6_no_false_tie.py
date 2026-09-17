"""Input 6 (Scope boundary, NEW): "My library has several structurally related
compounds. Match this query and tell me if it's a confident single hit or a tied
isomer candidate set."

Directly tests the second claim the audit brief called out: does the fixed
TIE_MARGIN logic ever demote a genuine single-best match to a false Level-3 tie?
Builds a library where one reference is a clean, clearly-superior match (score
~1.0, matches=7) and two others are only loosely related (lower score, by well
over the 0.02 TIE_MARGIN, and/or below the 6-peak floor) -- exactly the situation
the fix must NOT flag as tied. Uses SKILL.md's current loop body verbatim.
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


# Library: citrate (true target), plus two only loosely related compounds that share
# a couple of low-mass generic fragments with citrate but diverge on the diagnostic
# high-mass peaks -- realistic "not actually an isomer" confusability, not a
# contrived non-match.
references_raw = [
    raw_spectrum('citrate', 191.0197, [59.01, 87.01, 111.01, 129.02, 147.03, 173.01, 191.02],
                 [0.3, 0.5, 0.4, 0.6, 1.0, 0.35, 0.2]),
    raw_spectrum('malate', 133.0142, [59.01, 71.01, 87.01, 115.00, 133.01],
                 [0.4, 0.6, 0.5, 1.0, 0.3]),  # shares only 2 low-mass peaks (59.01, 87.01) with citrate
    raw_spectrum('succinate', 117.0193, [59.01, 73.03, 99.01, 117.02],
                 [0.3, 1.0, 0.5, 0.2]),  # shares only 1 low-mass peak (59.01) with citrate
]

# Query: near-identical to citrate on ALL 7 diagnostic peaks -- should be an
# unambiguous single winner, not a tie with the loosely-related compounds.
query_raw = raw_spectrum('Q_clean_citrate', 191.0197, [59.01, 87.01, 111.01, 129.02, 147.03, 173.01, 191.02],
                          [0.29, 0.51, 0.41, 0.58, 1.0, 0.33, 0.21])

references = [prepare(s) for s in references_raw]
query = prepare(query_raw)

scores = calculate_scores(references, [query], ModifiedCosine(tolerance=0.005))
pairs = scores.scores_by_query(query)
score_field, match_field = pairs[0][1].dtype.names

print("All candidate scores (for inspection):")
for ref, hit in sorted(pairs, key=lambda p: p[1][score_field], reverse=True):
    print(f"  {ref.get('compound_name'):<12} score={float(hit[score_field]):.4f} matches={int(hit[match_field])}")

# SKILL.md's current loop body, verbatim
ranked = sorted(pairs, key=lambda pair: pair[1][score_field], reverse=True)
top_score = ranked[0][1][score_field]
passing = [(ref, hit) for ref, hit in ranked
           if hit[score_field] >= top_score - TIE_MARGIN
           and hit[score_field] >= 0.7 and hit[match_field] >= 6]

print()
if len(passing) > 1:
    names = [ref.get('compound_name') for ref, _ in passing]
    print(f"RESULT: {names} tied -> Level 3 (isomer wall)  [FALSE TIE if only citrate should pass]")
elif len(passing) == 1:
    ref, hit = passing[0]
    print(f"RESULT: {ref.get('compound_name')} score={float(hit[score_field]):.3f} "
          f"matches={int(hit[match_field])} -> Level 2a  [correct: single confident match, not demoted]")
else:
    print("RESULT: no confident candidate -> Level 5")
