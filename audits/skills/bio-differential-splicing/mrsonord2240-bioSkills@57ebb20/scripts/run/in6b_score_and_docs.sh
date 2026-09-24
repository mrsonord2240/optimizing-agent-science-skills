#!/bin/bash
# in6 follow-up: (1) re-run the scoring step (first attempt hit a pandas concat index bug), (2) list the real link targets of the MAJIQ docs landing page (the sub-page URLs guessed in in6 were 404)
source /mnt/openscience/audits/bio-differential-splicing/run/common.sh
W=$R/out/in6; cd $W
$CORE python $R/in6_score.py $R/data/sim2p/truth.tsv $W
echo "--- links on the MAJIQ docs landing page"
grep -o 'href="[^"]*"' page_majiq-docs.html | sort -u | head -40
echo "--- text lines mentioning v2 / VOILA / heterogen / 3.0.11 on the landing page"
sed -e 's/<[^>]*>//g' page_majiq-docs.html | grep -a -i 'v2\|voila\|heterogen\|3\.0\.11\|experiments' | sed 's/^ *//' | head -20
