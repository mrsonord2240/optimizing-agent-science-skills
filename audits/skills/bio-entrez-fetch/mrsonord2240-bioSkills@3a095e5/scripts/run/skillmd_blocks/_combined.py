from Bio import Entrez, SeqIO
Entrez.email = 'researcher@institution.edu'
Entrez.api_key = 'optional_api_key'  # raises rate to 10 req/sec


def fetch_genbank(accession):
    h = Entrez.efetch(db='nucleotide', id=accession, rettype='gb', retmode='text')
    record = SeqIO.read(h, 'genbank'); h.close()
    return record

gb = fetch_genbank('NM_007294.4')
for feat in gb.features:
    if feat.type == 'CDS':
        print(feat.location, feat.qualifiers.get('product', ['?'])[0])


def bulk_summaries(db, ids, chunk=500):
    out = []
    for i in range(0, len(ids), chunk):
        h = Entrez.esummary(db=db, id=','.join(ids[i:i+chunk]))
        out.extend(Entrez.read(h)); h.close()
        time.sleep(0.1 if Entrez.api_key else 0.34)
    return out

def organism_of(s):
    '''No direct Organism field on current nucleotide docsums -- derive from Title.'''
    org = s.get('Organism')
    if org:
        return org
    words = s.get('Title', '').split()
    return ' '.join(words[:2]) if len(words) >= 2 else s.get('Title', '?')

records = bulk_summaries('nucleotide', uid_list)
for s in records:
    print(s['AccessionVersion'], s['Length'], organism_of(s))


def cds_proteins(accession):
    h = Entrez.efetch(db='nucleotide', id=accession, rettype='fasta_cds_aa', retmode='text')
    return list(SeqIO.parse(h, 'fasta'))

proteins = cds_proteins('NC_000913.3')  # E. coli K-12 genome
print(f'{len(proteins)} CDS-translated proteins')


def pubmed_full(pmid):
    h = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')
    records = Entrez.read(h); h.close()
    article = records['PubmedArticle'][0]
    citation = article['MedlineCitation']
    mesh = [m['DescriptorName'] for m in citation.get('MeshHeadingList', [])]
    title = citation['Article']['ArticleTitle']
    # ArticleIdList entries are StringElement (a str subclass with .attributes), not
    # {'#text': ...} dicts, on Biopython 1.88 -- id['#text'] raises TypeError. Use str(id).
    ids = article.get('PubmedData', {}).get('ArticleIdList', [])
    pmc_id = next((str(i) for i in ids if i.attributes.get('IdType') == 'pmc'), None)
    return {'pmid': pmid, 'title': title, 'mesh': mesh, 'pmc_id': pmc_id}


h = Entrez.esearch(db='nucleotide', term='Homo sapiens[ORGN] AND srcdb_refseq[PROP] AND biomol_mrna[PROP]',
                   usehistory='y', retmax=0)
r = Entrez.read(h); h.close()
total = int(r['Count'])

with open('out.fasta', 'w') as out:
    for start in range(0, total, 500):
        h = Entrez.efetch(db='nucleotide', rettype='fasta', retmode='text',
                          retstart=start, retmax=500,
                          webenv=r['WebEnv'], query_key=r['QueryKey'])
        out.write(h.read()); h.close()
        time.sleep(0.1 if Entrez.api_key else 0.34)


def sra_runinfo(uids):
    h = Entrez.efetch(db='sra', id=','.join(uids), rettype='runinfo', retmode='text')
    raw = h.read(); h.close()
    # db='sra' returns bytes here despite retmode='text' (Biopython 1.88) -- decode first.
    text = raw.decode() if isinstance(raw, bytes) else raw
    lines = text.strip().split('\n')
    header = lines[0].split(',')
    return [dict(zip(header, row.split(','))) for row in lines[1:]]


def lineage(txid):
    h = Entrez.efetch(db='taxonomy', id=str(txid), retmode='xml')
    record = Entrez.read(h)[0]; h.close()
    return record['Lineage'], record['ScientificName']


import xml.etree.ElementTree as ET

def clinvar_record(uid):
    h = Entrez.efetch(db='clinvar', id=uid, rettype='vcv', retmode='xml')
    raw = h.read(); h.close()
    text = raw.decode() if isinstance(raw, bytes) else raw
    archive = ET.fromstring(text).find('.//VariationArchive')
    sig = archive.find('.//Classifications/GermlineClassification/Description')
    return {
        'accession': archive.get('Accession'),
        'variation_name': archive.get('VariationName'),
        'clinical_significance': sig.text if sig is not None else None,
    }


def snp_record(uid):
    h = Entrez.efetch(db='snp', id=uid, rettype='xml', retmode='xml')
    raw = h.read(); h.close()
    text = raw.decode() if isinstance(raw, bytes) else raw
    ns = {'s': 'https://www.ncbi.nlm.nih.gov/SNP/docsum'}
    doc = ET.fromstring(text).find('s:DocumentSummary', ns)
    gene = doc.find('.//s:GENE_E/s:NAME', ns)
    sig = doc.find('s:CLINICAL_SIGNIFICANCE', ns)
    return {
        'chr': doc.findtext('s:CHR', default=None, namespaces=ns),
        'gene': gene.text if gene is not None else None,
        'clinical_significance': sig.text if sig is not None else None,
    }
