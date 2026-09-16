# Re-audit 2026-09-15: exec every ```python block of the fork's proteomics-qc SKILL.md VERBATIM into one namespace
# (extracted programmatically, so nothing is retyped). Import: from skill import S; S['raw_sample_qc'](...)
import re
SKILL = r'F:/OpenScience/external/mrsonord2240__bioSkills/proteomics/proteomics-qc/SKILL.md'
text = open(SKILL, encoding='utf-8').read()
BLOCKS = re.findall(r'```python\n(.*?)```', text, flags=re.S)
S = {}
for i, b in enumerate(BLOCKS):
    exec(compile(b, f'SKILL.md python block {i+1}', 'exec'), S)
FUNCS = sorted(k for k, v in S.items() if callable(v) and getattr(v, '__module__', None) is None and not k.startswith('_'))
if __name__ == '__main__':
    print('python blocks:', len(BLOCKS))
    print('functions:', [k for k in S if k in ('strip_contaminant_rows', 'raw_sample_qc', 'contaminant_fraction', 'replicate_correlation',
                                               'median_cv_linear', 'geometric_cv_from_log', 'missingness_profile', 'completeness_filter',
                                               'pca_batch_check', 'tmt_channel_balance')])
