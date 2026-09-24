'''Check the "--fasta annotates proteins" assertion: are the protein-group accessions in the library-based real report all present in the shipped FASTA?'''
import re, pandas as pd
F='F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/public-data/PXD070049/fasta/uniprotkb_proteome_HYE_UniversalContaminants.fasta'
acc=set()
for l in open(F,encoding='utf-8'):
    if l.startswith('>'):
        p=l[1:].split()[0].split('|'); acc.add(p[1] if len(p)>1 else p[0])
for lab,p in [('library-based','F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/public-work/diann_libbased_mzml/diann_out/report.parquet'),
              ('predicted-lib','F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/public-work/diann_predlib_mzml/diann_out/report.parquet')]:
    r=pd.read_parquet(p,columns=['Protein.Group','Genes','Protein.Names'])
    g=set(a.strip() for s in r['Protein.Group'].unique() for a in s.split(';'))
    print(f'{lab}: {len(g)} accessions in report | not in FASTA: {len(g-acc)} {sorted(g-acc)[:5]} | rows with empty Genes: {int((r["Genes"].fillna("")=="").sum())}/{len(r)}')
