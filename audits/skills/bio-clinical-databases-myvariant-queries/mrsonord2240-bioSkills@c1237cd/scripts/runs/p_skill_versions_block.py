# SKILL.md '/v1/metadata' block verbatim (fork commit c1237cdb)
import requests

meta = requests.get('https://myvariant.info/v1/metadata', timeout=30).json()
versions = {name: src.get('version') for name, src in meta.get('src', {}).items()}
print(versions['dbnsfp'], versions['clinvar'], versions['gnomad'])  # '4.8a' '2025-05' '2.1.1' on 2026-09-15
