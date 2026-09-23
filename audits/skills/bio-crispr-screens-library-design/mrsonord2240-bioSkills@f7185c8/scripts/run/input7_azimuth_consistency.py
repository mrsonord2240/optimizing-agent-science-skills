# Input 7 (Scope Boundary) regression test: SKILL.md vs usage-guide.md Azimuth 2.0
# consistency, and a live re-reproduction of the import failure both docs now describe.
# Pre-fix finding: SKILL.md instructed calling azimuth.model_comparison.predict(...) as
# if usable; usage-guide.md said the opposite. Fix: SKILL.md's Version Compatibility
# section was rewritten to match usage-guide.md's (correct) position.
import re

skill_md = open('../run/library-design-src/SKILL.md', encoding='utf-8').read()
usage_guide = open('../run/library-design-src/usage-guide.md', encoding='utf-8').read()

print('=== INPUT 7: Azimuth 2.0 SKILL.md/usage-guide.md consistency (post-fix regression) ===')

# 1. SKILL.md must now state plainly that Azimuth is not usable (not instruct calling it)
assert 'Azimuth 2.0 is not usable and must not be called' in skill_md, \
    'SKILL.md no longer states Azimuth is unusable -- regression'
assert 'azimuth.model_comparison.predict(' not in skill_md, \
    'SKILL.md still instructs calling the broken azimuth.model_comparison.predict(...) entry point'
print('DOC CHECK PASS: SKILL.md states Azimuth 2.0 must not be called and no longer instructs '
      'calling azimuth.model_comparison.predict(...)')

# 2. Both docs must recommend the same alternative (CRISPick / crisprScore)
for name, text in [('SKILL.md', skill_md), ('usage-guide.md', usage_guide)]:
    assert 'CRISPick' in text and 'crisprScore' in text, f'{name} missing the CRISPick/crisprScore alternative'
print('DOC CHECK PASS: both SKILL.md and usage-guide.md recommend the same alternative (CRISPick / crisprScore::getAzimuthScores())')

# 3. usage-guide.md's original (correct, pre-fix) statement is preserved
assert 'Python-2 only and archived' in usage_guide
print('DOC CHECK PASS: usage-guide.md still correctly describes Azimuth as Python-2-only/archived')

# 4. Live re-reproduction of the import failure both docs now describe (independent of
#    TOOLS.md and of the fix author's own verification -- a fresh import attempt here)
print('\nLive import check:')
import azimuth
print(f'  import azimuth: OK ({azimuth.__file__})')
try:
    import azimuth.model_comparison as mc
    raise AssertionError('azimuth.model_comparison imported successfully -- docs would be WRONG')
except SyntaxError as e:
    print(f'  import azimuth.model_comparison: SyntaxError (matches both docs) -> {e}')
    print('ASSERT PASS: the documented failure is real and reproduces live, and both docs now agree on it')
