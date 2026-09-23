"""Fresh regression of the short SKILL.md evidence-to-level helper across all confidence branches."""
def assign_level(evidence):
    if evidence.get('authentic_standard_same_method'):
        return 1
    if evidence.get('library_match') and evidence['library_match']['score'] >= 0.7 and evidence['library_match']['matches'] >= 6:
        return '2a'
    if evidence.get('diagnostic_fragments') and evidence.get('single_structure_consistent'):
        return '2b'
    if evidence.get('candidate_set') or evidence.get('canopus_class') or evidence.get('network_propagated'):
        return 3
    if evidence.get('unambiguous_formula'):
        return 4
    return 5

cases = {
    'authentic standard': ({'authentic_standard_same_method': True}, 1),
    'library with score and peak floors': ({'library_match': {'score': 0.7, 'matches': 6}}, '2a'),
    'high score but only two peaks': ({'library_match': {'score': 0.99, 'matches': 2}}, 5),
    'diagnostic fragments': ({'diagnostic_fragments': True, 'single_structure_consistent': True}, '2b'),
    'candidate set': ({'candidate_set': ['citrate', 'isocitrate']}, 3),
    'formula only': ({'unambiguous_formula': True}, 4),
    'bare feature': ({}, 5),
}
for label, (evidence, expected) in cases.items():
    observed = assign_level(evidence)
    print(f'{label}: Level {observed}')
    assert observed == expected, (label, observed, expected)
print('ASSERTIONS: all evidence branches assign the documented confidence caps.')
