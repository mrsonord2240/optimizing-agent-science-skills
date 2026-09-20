# M1 check: verify a sample of the Skill's literature citations (journal/volume/page) against Crossref + PMID 36306325 against NCBI esummary. Public APIs.
import json, urllib.request, urllib.parse
def cr(q):
    u = 'https://api.crossref.org/works?rows=1&select=title,container-title,volume,page,article-number,issued,author&query.bibliographic=' + urllib.parse.quote(q)
    d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'audit/1.0 (mailto:none@example.org)'}), timeout=60))['message']['items'][0]
    return '%s | %s | vol %s | p/art %s | %s | %s' % (d['title'][0][:90], d.get('container-title', ['?'])[0], d.get('volume'), d.get('page') or d.get('article-number'), d['issued']['date-parts'][0][0], d['author'][0].get('family'))
Q = ['Smith Kitzman benchmarking splice prediction MPSA SpliceAI Pangolin Genome Biology 2023',
     'You SpliceTransformer tissue-specific splicing prediction Nature Communications 2024',
     'Strauch CI-SpliceAI improving machine learning predictions of disease-causing splicing variants curated alternative splice sites PLoS One 2022',
     'Riepe Benchmarking deep learning splice prediction tools using functional splice assays Human Mutation 2021',
     'Dawes SpliceVault predicts the precise nature of variant-associated mis-splicing Nature Genetics 2023',
     'Using the ACMG/AMP framework to capture evidence related to predicted and observed impact on splicing: recommendations from the ClinGen SVI Splicing Subgroup Walker 2023',
     'Zeng Li Predicting RNA splicing from DNA sequence using Pangolin Genome Biology 2022',
     'Lefter Mutalyzer 2 Bioinformatics 2021',
     'Roberts Advances in oligonucleotide drug delivery / therapeutic approaches Duchenne muscular dystrophy Nature Reviews Drug Discovery 2023',
     'Zhang BPHunter branchpoint PNAS 2022']
for q in Q:
    try: print('-', q[:50], '=>', cr(q))
    except Exception as e: print('-', q[:50], 'ERR', e)
d = json.load(urllib.request.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=36306325&retmode=json', timeout=60))['result']['36306325']
print('PMID 36306325 =>', d['title'][:110], '|', d['source'], d['pubdate'])
