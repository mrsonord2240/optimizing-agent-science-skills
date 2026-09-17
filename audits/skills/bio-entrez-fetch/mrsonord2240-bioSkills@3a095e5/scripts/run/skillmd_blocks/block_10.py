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
