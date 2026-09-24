from Bio import Entrez
import os
import time

Entrez.email = 'researcher@institution.edu'       # NCBI requires; sets User-Agent
Entrez.api_key = os.environ.get('NCBI_API_KEY')   # 3 -> 10 req/sec; get at ncbi.nlm.nih.gov/account/settings/
Entrez.tool = 'project-name'                      # appears in NCBI usage logs; helps if rate-throttled

def validate_term(term, max_chars=2000, max_or_clauses=100):
    """Reject malformed or impractically large query strings before an API call."""
    if not isinstance(term, str) or not term.strip():
        raise ValueError('term must be a non-empty string')
    if len(term) > max_chars or term.upper().count(' OR ') > max_or_clauses:
        raise ValueError('term is too large; EPost IDs in batches instead')
    return term
