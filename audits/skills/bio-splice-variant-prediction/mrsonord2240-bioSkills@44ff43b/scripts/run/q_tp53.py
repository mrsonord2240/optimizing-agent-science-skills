# Check the usage-guide TP53 example (chr17:g.7676154A>G, GRCh38) and SKILL.md's NM_000546.6:c.673-2A>G against GRCh38 (Ensembl REST + FLAIR-test hg38 chr17 FASTA).
import json, urllib.request, urllib.parse
def get(u):
    with urllib.request.urlopen(urllib.request.Request("https://rest.ensembl.org"+u, headers={"Accept":"application/json"}), timeout=60) as r:
        return json.load(r)
for h in ["ENST00000269305:c.673-2A>G", "ENST00000269305:c.215C>G"]:
    d = get("/vep/human/hgvs/" + urllib.parse.quote(h, safe=":>+-_.()=") + "?content-type=application/json")[0]
    cv = [(c.get("id"), c.get("clin_sig"), c.get("allele_string")) for c in d.get("colocated_variants", [])]
    print(h, "GRCh38 chr%s:%s" % (d["seq_region_name"], d["start"]), d["allele_string"], "strand", d["strand"], d["most_severe_consequence"], cv[:3])
