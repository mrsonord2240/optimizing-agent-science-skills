from Bio import Entrez
import os
import time

Entrez.email = 'researcher@institution.edu'       # NCBI requires; sets User-Agent
Entrez.api_key = os.environ.get('NCBI_API_KEY')   # 3 -> 10 req/sec; get at ncbi.nlm.nih.gov/account/settings/
Entrez.tool = 'project-name'                      # appears in NCBI usage logs; helps if rate-throttled
