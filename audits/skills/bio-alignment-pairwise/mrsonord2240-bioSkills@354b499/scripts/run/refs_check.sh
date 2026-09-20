#!/bin/bash
# Verify the two most recent / riskiest citations in SKILL.md against Crossref (public, unauthenticated).
for q in "GPU-accelerated homology search with MMseqs2 Kallenborn" "Optimal gap-affine alignment in O(s) space Marco-Sola" "Fast gap-affine pairwise alignment using the wavefront algorithm"; do
  curl -s --max-time 30 -G "https://api.crossref.org/works" --data-urlencode "query.bibliographic=$q" --data-urlencode "rows=1" --data-urlencode "select=title,container-title,volume,issue,page,issued,author" | python3 -c "
import sys,json; j=json.load(sys.stdin)['message']['items'][0]
print(j['title'][0][:90],'|',j.get('container-title'),'|vol',j.get('volume'),'iss',j.get('issue'),'p',j.get('page'),'|',j['issued']['date-parts'][0][0],'|',[a.get('family') for a in j.get('author',[])][:12])"
done
