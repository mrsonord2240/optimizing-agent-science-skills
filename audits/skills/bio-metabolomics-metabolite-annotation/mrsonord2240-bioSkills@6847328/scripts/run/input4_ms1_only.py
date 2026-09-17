"""Input 4 (Variant B, REGRESSION): "I only have MS1 accurate mass and a clean
isotope pattern for this feature -- no MS/MS. What confidence level is achievable
and why?"

SKILL.md's assign_level() snippet, copied verbatim, run unmodified against the
same three evidence dicts as the pre-fix audit (unchanged code path; re-run to
confirm no regression from the fix's other edits).
"""


def assign_level(evidence):
    if evidence.get('authentic_standard_same_method'):
        return 1
    if evidence.get('library_match') and evidence['library_match']['score'] >= 0.7 and evidence['library_match']['matches'] >= 6:
        return '2a'  # reference library spectrum, no in-house standard
    if evidence.get('diagnostic_fragments') and evidence.get('single_structure_consistent'):
        return '2b'
    if evidence.get('candidate_set') or evidence.get('canopus_class') or evidence.get('network_propagated'):
        return 3  # isomers unresolved, class only, or "related to" an annotated node
    if evidence.get('unambiguous_formula'):
        return 4  # MS1 + isotopes + adduct logic, no structure
    return 5


cases = {
    'MS1 only, clean isotope pattern, unambiguous adduct': {'unambiguous_formula': True},
    'MS1 only, ambiguous adduct (two plausible neutral masses)': {'unambiguous_formula': False},
    'Bare feature, nothing resolved': {},
}

for label, evidence in cases.items():
    print(f"{label:<62} -> Level {assign_level(evidence)}")
