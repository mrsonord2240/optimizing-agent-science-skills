from Bio import Entrez

Entrez.email = 'audit@example.org'


def expect_start(text, prefix):
    if not text.lstrip().startswith(prefix):
        raise RuntimeError(f'Unexpected EFetch response, starts {text[:80]!r}')
    return text


try:
    expect_start('<?xml version="1.0"?><ERROR>backend unavailable</ERROR>', 'Run,')
except RuntimeError:
    print('ERROR_GUARD PASS')
else:
    raise AssertionError('backend error body was accepted as SRA CSV')


exec(open('references/sra.md', encoding='utf-8').read().split('```python')[1].split('```')[0])
rows = sra_runinfo(['8', '7'])
assert len(rows) >= 2 and rows[0]['Run'].startswith('SRR')
print('SRA_ROWS', len(rows), rows[0]['Run'])
exec(open('references/gene-taxonomy-gds.md', encoding='utf-8').read().split('```python')[1].split('```')[0])
line, name = lineage(9606)
assert name == 'Homo sapiens' and 'Eukaryota' in line
print('LINEAGE', name)
