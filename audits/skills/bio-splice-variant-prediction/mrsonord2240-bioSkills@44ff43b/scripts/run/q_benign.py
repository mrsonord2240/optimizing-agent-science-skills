# Find ClinVar-benign / common variants inside GRCh37 chrX genes via Ensembl overlap (public REST); prints candidates for benign controls.
import json, urllib.request, sys
def get(u):
    with urllib.request.urlopen(urllib.request.Request("https://grch37.rest.ensembl.org"+u, headers={"Accept":"application/json"}), timeout=90) as r:
        return json.load(r)
for reg in ["X:100652700-100664000", "X:38220000-38260000"]:
    d = get("/overlap/region/human/%s?feature=variation;content-type=application/json" % reg)
    print(reg, len(d))
    for v in d:
        cs = v.get("clinical_significance") or []
        if any(c in ("benign","likely benign") for c in cs) and v["end"]==v["start"]:
            print(v["id"], v["start"], v["alleles"], cs, v.get("consequence_type"))
