from Bio import Entrez, SeqIO
Entrez.email = 'researcher@institution.edu'
Entrez.api_key = 'optional_api_key'  # raises rate to 10 req/sec
