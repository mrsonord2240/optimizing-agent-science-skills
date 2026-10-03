import requests,gzip
r=requests.get('https://rest.uniprot.org/uniprotkb/stream',params={'query':'proteome:UP000005640 AND reviewed:true','format':'fasta','compressed':'true'},timeout=300)
d=gzip.decompress(r.content)
h=[l for l in d.split(b'\n') if l.startswith(b'>')]
print(len(r.content),len(h),sum(l.startswith(b'>sp|') for l in h),sum(l.startswith(b'>tr|') for l in h))
