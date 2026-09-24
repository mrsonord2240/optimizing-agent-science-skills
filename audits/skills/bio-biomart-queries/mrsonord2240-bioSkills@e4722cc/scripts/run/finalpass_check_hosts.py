"""Record BioMart registry availability while rerunning the final pass."""

import requests


HOSTS = [
    "https://www.ensembl.org",
    "https://useast.ensembl.org",
    "https://asia.ensembl.org",
    "https://grch37.ensembl.org",
    "https://nov2020.archive.ensembl.org",
    "https://jul2023.archive.ensembl.org",
]

for host in HOSTS:
    try:
        response = requests.get(f"{host}/biomart/martservice?type=registry", timeout=15)
        prefix = response.text[:80].replace("\n", " ")
        print(host, response.status_code, response.headers.get("content-type"), len(response.content), prefix)
    except requests.RequestException as exc:
        print(host, type(exc).__name__, str(exc))
