from cyvcf2 import VCF

ann_fields = ['Allele', 'Annotation', 'Impact', 'Gene_Name', 'Gene_ID',
              'Feature_Type', 'Feature_ID', 'Transcript_BioType', 'Rank',
              'HGVS_c', 'HGVS_p', 'cDNA_pos', 'CDS_pos', 'Protein_pos', 'Distance']

for variant in VCF('snpeff_output.vcf'):
    ann = variant.INFO.get('ANN')
    if not ann:
        continue
    for block in ann.split(','):
        parsed = dict(zip(ann_fields, block.split('|')[:len(ann_fields)]))
        # Impact is a SnpEff triage bucket, not ACMG evidence; check the SO Annotation term
        if parsed['Impact'] == 'HIGH':
            print(variant.CHROM, variant.POS, parsed['Gene_Name'], parsed['Annotation'])
