pip install spliceai tensorflow "setuptools<81"     # SpliceAI imports pkg_resources; weights and grch37/grch38 gene tables ship in the package

# Pangolin: GitHub, NOT the PyPI/bioconda 'pangolin' (SARS-CoV-2 lineages). Its setup.py declares no dependencies:
pip install torch gffutils pyfaidx pyfastx biopython pandas "PyVCF3==1.0.0"   # PyVCF3 >= 1.0.2 breaks vcf.parser._Info
git clone https://github.com/tkzeng/Pangolin && pip install ./Pangolin     # also puts create_db.py on PATH

pip install mmsplice       # needs setuptools<81 and a cyvcf2 built for the installed numpy (else: pip install --force-reinstall --no-deps cyvcf2)
