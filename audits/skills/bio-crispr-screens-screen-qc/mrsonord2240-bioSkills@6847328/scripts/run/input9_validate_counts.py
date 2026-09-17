"""Input 9 -- NEW (adversarial/malformed input). Independently re-implements the checks
described in SKILL.md's "Input Validation" table and tests them against the ACTUAL
validate_counts() function shipped in the fixed examples/screen_qc.py (imported from the byte
copy in run/skill_copy/, not the external clone), on five malformed count tables: missing Gene
column, non-numeric sample column, negative counts, duplicate sgRNA IDs, and an all-zero
('dead') sample. Checks that each documented failure raises/reports what SKILL.md says it
should, not just that the function runs."""
import sys, importlib.util
import pandas as pd, numpy as np

SPEC_PATH = r'F:\OpenScience\audits\bio-crispr-screens-screen-qc\run\skill_copy\examples\screen_qc.py'
src = open(SPEC_PATH, encoding='utf-8').read()
# Pull out just validate_counts() (the module-level script does file I/O and plotting on import,
# which we don't want here) plus gini_index for the earlier P1 regression check below.
import re
func_src = re.search(r"def validate_counts\(.*?\n\n\n", src, re.S).group()
ns = {'pd': pd, 'np': np}
exec(func_src, ns)
validate_counts = ns['validate_counts']

gini_src = re.search(r"def gini_index\(.*?\n\n\n", src, re.S).group()
exec(gini_src, ns)
gini_index = ns['gini_index']


def base_table(n=20):
    rng = np.random.default_rng(5)
    return pd.DataFrame({
        'Gene': [f'G{i}' for i in range(n)],
        'S1': rng.integers(50, 500, n).astype(float),
        'S2': rng.integers(50, 500, n).astype(float),
    })


stage_map = {'S1': 'endpoint', 'S2': 'endpoint'}
results = []

# 1. Missing Gene column -> SKILL.md: "name the missing column; do not guess"
t = base_table().drop(columns=['Gene'])
try:
    validate_counts(t, stage_map)
    results.append(('missing_gene_column', 'FAIL (no error raised)'))
except ValueError as e:
    ok = 'Gene' in str(e)
    results.append(('missing_gene_column', f'PASS -- ValueError: {e}' if ok else f'WRONG MESSAGE: {e}'))

# 2. Non-numeric sample column -> SKILL.md: "report which column is non-numeric and the first offending value"
t = base_table()
t['S1'] = t['S1'].astype(object)
t.loc[3, 'S1'] = 'not_a_number'
try:
    validate_counts(t, stage_map)
    results.append(('non_numeric_column', 'FAIL (no error raised)'))
except ValueError as e:
    ok = 'S1' in str(e) or 'non-numeric' in str(e)
    results.append(('non_numeric_column', f'PASS -- ValueError: {e}' if ok else f'WRONG MESSAGE: {e}'))

# 3. Negative counts -> SKILL.md: "reject the file; these are not counts"
t = base_table()
t.loc[0, 'S1'] = -5.0
try:
    validate_counts(t, stage_map)
    results.append(('negative_counts', 'FAIL (no error raised)'))
except ValueError as e:
    results.append(('negative_counts', f'PASS -- ValueError: {e}'))

# 4. Duplicate sgRNA IDs -> SKILL.md: "report the duplicates"
t = base_table()
t.index = ['sg0'] + ['sg1'] * (len(t) - 1)
try:
    validate_counts(t, stage_map)
    results.append(('duplicate_sgrna_ids', 'FAIL (no error raised)'))
except ValueError as e:
    ok = 'duplicat' in str(e).lower()
    results.append(('duplicate_sgrna_ids', f'PASS -- ValueError: {e}' if ok else f'WRONG MESSAGE: {e}'))

# 5. All-zero ('dead') sample -> SKILL.md: "report the sample as failed at sequencing, and skip
#    (not nan-propagate) its Gini and correlation" -- documented as a WARNING + exclusion, not
#    a raised error, so this is checked differently (captured stdout + returned columns).
import io, contextlib
t = base_table()
t['S1'] = 0.0
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    out = validate_counts(t, stage_map)
printed = buf.getvalue()
dead_reported = 'S1' in printed and ('WARNING' in printed or 'warn' in printed.lower())
dead_excluded = 'S1' not in out.columns
results.append(('all_zero_dead_sample',
                 f'PASS -- reported={dead_reported}, excluded_from_matrix={dead_excluded}, stdout={printed.strip()!r}'
                 if dead_reported and dead_excluded else
                 f'FAIL -- reported={dead_reported}, excluded={dead_excluded}, stdout={printed.strip()!r}'))
# also confirm gini_index doesn't crash if handed the (now-excluded) all-zero column directly
g_dead = gini_index(np.array([0.0, 0.0, 0.0]))
results.append(('gini_index_all_zero_input', f"{'PASS -- returns nan' if np.isnan(g_dead) else 'FAIL -- ' + str(g_dead)}"))

print('=== validate_counts() / gini_index() documented-failure checks ===')
all_pass = True
for name, res in results:
    print(f'{name}: {res}')
    if not res.startswith('PASS'):
        all_pass = False
print('\nALL PASS' if all_pass else '\nSOME FAILED -- see above')

# --- Extra check: SKILL.md's Input Validation table row 1 says a REQUIRED column is "an sgRNA
# identifier column (index)". validate_counts() only checks for the 'Gene' column -- does it also
# catch a table with no meaningful sgRNA-identifier index (e.g. a bare default RangeIndex)?
print('\n=== Extra: is the sgRNA-identifier-column requirement actually enforced? ===')
t = base_table()
t.index = pd.RangeIndex(len(t))  # no sgRNA IDs at all, just 0..n-1
try:
    out = validate_counts(t, stage_map)
    print('validate_counts() ACCEPTED a table with a bare RangeIndex (no real sgRNA IDs) -- '
          'the documented "sgRNA identifier column (index)" requirement is not actually checked.')
except ValueError as e:
    print('Correctly rejected:', e)
