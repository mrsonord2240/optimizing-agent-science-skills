"""Skill table: edlib 'Edit distance only'; caveat 'It returns edit distance only'. Does edlib.align(task='path') return an alignment? (independent check of that wording)"""
import edlib
r = edlib.align('ACGTACGT', 'ACGTTCGT', mode='NW', task='path')
print(r)
print(edlib.getNiceAlignment(r, 'ACGTACGT', 'ACGTTCGT'))
assert r['cigar'] is not None and r['editDistance'] == 1
print("PASS edlib returns an alignment path/CIGAR with task='path' (unit-cost scoring only): the Skill's 'edit distance only' is about scoring, not output")
