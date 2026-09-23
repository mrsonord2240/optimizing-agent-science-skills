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
