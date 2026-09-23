"""
Input 3 (Edge): "Download the series matrix for GSE470 and dump every unique
value of !Sample_data_processing, per the Skill's 'Submitter-data-processing
audit' usage-guide prompt. GSE470 is a small, quiet standalone series (not a
SuperSeries) -- an edge case for whether the parser handles a field that may
simply not exist in a real series."

Uses SKILL.md's own parse_series_matrix() verbatim (the .get()-based safe
version shown in SKILL.md's "Download series matrix with submitter caveat"
section), against the real cached GSE470_series_matrix.txt.gz (fetched live
2026-09-17 by the tooling pass; reused here rather than re-hitting FTP).

Then repeats using literal bracket access on the SKILL.md-documented dict key
--the way the usage-guide's own prompt phrasing ("dump every unique value of
!Sample_data_processing") would naturally be implemented by an agent that
takes SKILL.md's own field name at face value -- to check whether a real
series without that field raises KeyError as TOOLS.md's tooling notes warned.
"""
import gzip
import pandas as pd
import shutil

SRC = r'F:\OpenScience\audit-envs\database-access\public-data\geo-data\GSE470_series_matrix.txt.gz'
LOCAL = 'GSE470_matrix.txt.gz'
shutil.copyfile(SRC, LOCAL)


def parse_series_matrix(path):
    metadata = {}
    with gzip.open(path, 'rt') as f:
        for line in f:
            if line.startswith('!series_matrix_table_begin'):
                break
            if line.startswith('!'):
                key, *vals = line.rstrip('\n').split('\t')
                metadata[key] = [v.strip('"') for v in vals]
        expr = pd.read_csv(f, sep='\t', index_col=0, comment='!')
    return metadata, expr


meta, expr = parse_series_matrix(LOCAL)
print(f'expr.shape = {expr.shape}')
print(f'!Series_geo_accession = {meta.get("!Series_geo_accession")}')
print(f'columns (first 3) = {list(expr.columns[:3])}')

print('\n--- SKILL.md-documented .get() access (safe form) ---')
notes = set(meta.get('!Sample_data_processing', []))
print(f'unique !Sample_data_processing values via .get(): {notes!r}')
if not notes:
    print('  -> empty: this real series has NO !Sample_data_processing field at all.')

print('\n--- Bracket access as a literal reading of the usage-guide prompt ---')
try:
    notes2 = set(meta['!Sample_data_processing'])
    print(f'unique values via bracket access: {notes2!r}')
except KeyError as e:
    print(f'KeyError: {e!r}  -- confirms bracket access crashes on this real series')
