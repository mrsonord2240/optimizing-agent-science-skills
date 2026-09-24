'''Input 10 (NEW) -- source-derived local contract for the documented query-size preflight.

Prompt: "Before sending a generated Entrez query, reject an empty string, a huge OR-list, and a
very long term, while retaining a normal field-qualified query unchanged."
'''
import pathlib
import runpy

source_example = pathlib.Path(
    r'F:/OpenScience/worktrees/bio-entrez-search-finalpass/database-access/entrez-search/examples/validate_term.py'
)
validate_term = runpy.run_path(str(source_example), run_name='source_example')['validate_term']

valid = 'BRCA1[Gene Name] AND Homo sapiens[Organism]'
assert validate_term(valid) == valid

for invalid in ('', 'BRCA1' * 1000, ' OR '.join(['BRCA1'] * 102)):
    try:
        validate_term(invalid)
    except ValueError as error:
        print(f'Rejected {len(invalid)}-character term: {error}')
    else:
        raise AssertionError(f'expected ValueError for {invalid[:40]!r}')

print('ASSERT OK: source preflight accepts a normal query and rejects empty, long, and OR-heavy inputs')
