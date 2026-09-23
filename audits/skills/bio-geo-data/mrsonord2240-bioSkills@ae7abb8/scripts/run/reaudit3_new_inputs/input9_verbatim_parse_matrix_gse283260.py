import gzip
import urllib.request
import pandas as pd
import sys


def download_series_matrix(gse):
    prefix = gse[:-3] + 'nnn'
    url = f'https://ftp.ncbi.nlm.nih.gov/geo/series/{prefix}/{gse}/matrix/{gse}_series_matrix.txt.gz'
    urllib.request.urlretrieve(url, f'{gse}_matrix.txt.gz')
    return f'{gse}_matrix.txt.gz'


def parse_series_matrix(path):
    metadata = {}
    with gzip.open(path, 'rt', encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.startswith('!series_matrix_table_begin'):
                break
            if line.startswith('!'):
                key, *vals = line.rstrip('\n').split('\t')
                metadata[key] = [v.strip('"') for v in vals]
        expr = pd.read_csv(f, sep='\t', index_col=0, comment='!')
    return metadata, expr


gse = sys.argv[1] if len(sys.argv) > 1 else 'GSE346738'
path = download_series_matrix(gse)
meta, expr = parse_series_matrix(path)
print('shape:', expr.shape)
print('geo_accession:', meta.get('!Series_geo_accession'))

# Scan raw bytes for any byte >= 0x80 (non-ASCII) to prove this fixture actually exercises the encoding path
with gzip.open(path, 'rb') as f:
    raw = f.read()
nonascii = [b for b in set(raw) if b >= 0x80]
print('non-ASCII byte values present in raw file:', sorted(nonascii)[:20], '... total distinct:', len(nonascii))
