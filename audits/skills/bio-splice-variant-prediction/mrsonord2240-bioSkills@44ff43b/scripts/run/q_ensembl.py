# Look up GRCh37 coordinates + ClinVar significance for named chrX variants via Ensembl GRCh37 REST (public, unauthenticated).
import json, urllib.request, urllib.parse, sys
def vep(h):
    u = "https://grch37.rest.ensembl.org/vep/human/hgvs/" + urllib.parse.quote(h, safe=":>+-_.()=") + "?content-type=application/json"
    with urllib.request.urlopen(urllib.request.Request(u, headers={"Accept":"application/json"}), timeout=60) as r:
        return json.load(r)
for h in sys.argv[1:]:
    try:
        d = vep(h)[0]
        cv = [(c.get("id"), c.get("clin_sig"), c.get("allele_string")) for c in d.get("colocated_variants", []) if c.get("clin_sig")]
        tc = [(t["gene_symbol"] if "gene_symbol" in t else "", t["consequence_terms"]) for t in d["transcript_consequences"] if t.get("transcript_id") == h.split(":")[0]]
        print(h, "X:%s" % d["start"], d["allele_string"], "strand", d["strand"], "|", cv, "|", tc)
    except Exception as e:
        print(h, "ERR", repr(e)[:150])
