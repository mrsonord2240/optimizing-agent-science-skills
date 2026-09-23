"""Crossref check (public, unauthenticated) of the Skill's References: title match + volume/page as cited."""
import json, urllib.request, urllib.parse
refs = [("Kallenborn GPU-accelerated homology search with MMseqs2", "Nat Methods 22:2024"),
        ("Marco-Sola Optimal gap-affine alignment in O(s) space", "Bioinformatics 39:btad074"),
        ("Marco-Sola Fast gap-affine pairwise alignment using the wavefront algorithm", "Bioinformatics 37:456"),
        ("Yu Altschul The construction of amino acid substitution matrices for the comparison of proteins with non-standard compositions", "Bioinf 21:902"),
        ("Altschul Erickson Significance of nucleotide sequence alignments: a method for random sequence permutation that preserves dinucleotide and codon usage", "MBE 2:526"),
        ("Daily Parasail: SIMD C library for global, semi-global, and local pairwise sequence alignments", "BMC Bioinf 17:81"),
        ("Sosic Sikic Edlib: a C/C++ library for fast, exact sequence alignment", "Bioinf 33:1394"),
        ("Schaffer Improving the accuracy of PSI-BLAST protein database searches with composition-based statistics", "NAR 29:2994"),
        ("Karlin Altschul Methods for assessing the statistical significance of molecular sequence features by using general scoring schemes", "PNAS 87:2264")]
for q, cited in refs:
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query.bibliographic": q, "rows": 1, "select": "title,container-title,volume,issue,page,issued,article-number"})
    try:
        j = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "audit/1.0 (mailto:none@example.org)"}), timeout=40))['message']['items'][0]
        print(f"cited [{cited}] -> {j['title'][0][:70]!r} | {j.get('container-title')} vol {j.get('volume')} iss {j.get('issue')} p {j.get('page') or j.get('article-number')} | {j['issued']['date-parts'][0][0]}")
    except Exception as e:
        print(f"cited [{cited}] -> lookup error {type(e).__name__}: {e}")
