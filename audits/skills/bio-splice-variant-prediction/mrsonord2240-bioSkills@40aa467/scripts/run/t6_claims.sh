#!/bin/bash
# Input 6: verify externally checkable claims in SKILL.md (network, public, HEAD/GET only)
echo "== BPHunter standalone page (SKILL.md: redirects to GitHub, 404)"
curl -sIL -o /dev/null -w "final=%{url_effective} code=%{http_code}\n" https://hgidsoft.rockefeller.edu/BPHunter/standalone.html
echo "== SpliceVault Ensembl file size (SKILL.md: 884 MB)"; curl -sI https://ftp.ensembl.org/pub/current_variation/SpliceVault/SpliceVault_data_GRCh38.tsv.gz | grep -i content-length
echo "== SpliceVault Shiny portal"; curl -sI -o /dev/null -w "%{http_code}\n" https://kidsneuro.shinyapps.io/splicevault
echo "== SpliceTransformer repo / weights id"; curl -sI -o /dev/null -w "repo %{http_code}\n" https://github.com/ShenLab-Genomics/SpliceTransformer
echo "== Pangolin repo"; curl -sI -o /dev/null -w "%{http_code}\n" https://github.com/tkzeng/Pangolin
echo "== PyPI cispliceai, spliceai"; for p in cispliceai spliceai mmsplice; do curl -s https://pypi.org/pypi/$p/json | python3 -c "import json,sys; j=json.load(sys.stdin); print('$p', j['info']['version'])"; done
echo "== Crossref/PubMed spot-check of 4 citations"
curl -s "https://api.crossref.org/works?query.bibliographic=SpliceVault+predicts+the+precise+nature+of+variant-associated+mis-splicing&rows=1&select=title,container-title,volume,page,issued" | python3 -c "import json,sys; i=json.load(sys.stdin)['message']['items'][0]; print(i['title'][0][:90], '|', i.get('container-title'), i.get('volume'), i.get('page'), i['issued'])"
curl -s "https://api.crossref.org/works?query.bibliographic=Predicting+splicing+from+primary+sequence+with+deep+learning+Jaganathan&rows=1&select=title,container-title,volume,page,issued" | python3 -c "import json,sys; i=json.load(sys.stdin)['message']['items'][0]; print(i['title'][0][:90], '|', i.get('container-title'), i.get('volume'), i.get('page'), i['issued'])"
curl -s "https://api.crossref.org/works?query.bibliographic=Predicting+splicing+from+primary+sequence+with+deep+learning+Pangolin+Zeng+Li+Genome+Biology+2022&rows=1&select=title,container-title,volume,page,issued" | python3 -c "import json,sys; i=json.load(sys.stdin)['message']['items'][0]; print(i['title'][0][:90], '|', i.get('container-title'), i.get('volume'), i.get('page'), i['issued'])"
curl -s "https://api.crossref.org/works?query.bibliographic=Accurate+splice+site+prediction+using+SpliceTransformer+You+2024+Nature+Communications&rows=1&select=title,container-title,volume,page,issued" | python3 -c "import json,sys; i=json.load(sys.stdin)['message']['items'][0]; print(i['title'][0][:90], '|', i.get('container-title'), i.get('volume'), i.get('page'), i['issued'])"
