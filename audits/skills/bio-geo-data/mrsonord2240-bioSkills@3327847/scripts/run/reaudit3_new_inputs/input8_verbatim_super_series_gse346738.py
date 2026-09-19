import gzip
import urllib.request


def check_super_or_sub_series(gse):
    prefix = gse[:-3] + 'nnn'
    url = f'https://ftp.ncbi.nlm.nih.gov/geo/series/{prefix}/{gse}/soft/{gse}_family.soft.gz'
    urllib.request.urlretrieve(url, f'{gse}.soft.gz')
    super_of = []
    sub_of = None
    with gzip.open(f'{gse}.soft.gz', 'rt', encoding='utf-8', errors='replace') as f:
        for line in f:
            if line.startswith('!Series_relation'):
                if 'SuperSeries of' in line:
                    super_of.append(line.split('SuperSeries of: ')[1].strip())
                elif 'SubSeries of' in line:
                    sub_of = line.split('SubSeries of: ')[1].strip()
            if line.startswith('^SAMPLE'):
                break   # Speed: don't read past header
    return {'super_of': super_of, 'sub_of': sub_of}


print(check_super_or_sub_series('GSE346738'))
