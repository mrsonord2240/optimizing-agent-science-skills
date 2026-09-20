#!/bin/bash
# in6 follow-up: the MAJIQ docs pages under getting-started-guide/ (correct URLs from the landing page links); check each MAJIQ statement in the Skill's "MAJIQ V3" section against the docs text.
W=/f/OpenScience/audits/bio-differential-splicing/run/out/in6/docs; rm -rf $W; mkdir -p $W; cd $W
B=https://biociphers.bitbucket.io/majiq-docs
for p in getting-started-guide/quick-overview getting-started-guide/majiq-build getting-started-guide/quantifiers getting-started-guide/moccasin getting-started-guide/installing getting-started-guide/index; do
  f=$(echo $p | tr '/' '_').html
  echo "$p -> HTTP $(curl -s -L -o $f -w '%{http_code}' --max-time 40 $B/$p.html), $(wc -c < $f) bytes"
  sed -e 's/<[^>]*>//g' $f > ${f%.html}.txt
done
cat *.txt > all.txt
for pat in 'majiq build' 'psi-coverage' 'deltapsi' 'heterogen' 'splicegraph.zarr' '\.sj' '--min-experiments' '--mindenovo' '--simplify' '--strandness' '--minreads' '--minbins' '-grp1' '-grp2' '--splicegraph' 'moccasin' 'currently only supports' 'MAJIQ v2' 'experiments_tsv\|experiments.tsv'; do
  echo "docs contain '$pat': $(grep -c -- "$pat" all.txt) lines"
done
echo "--- exact lines: build usage, deltapsi usage, VOILA statement"
grep -a -m3 -i 'majiq build ' all.txt | sed 's/^ *//' | cut -c1-220
grep -a -m4 -i 'deltapsi' all.txt | sed 's/^ *//' | cut -c1-220
grep -a -m3 -i 'only supports' all.txt | sed 's/^ *//' | cut -c1-260
grep -a -m3 -i 'heterogen' all.txt | sed 's/^ *//' | cut -c1-220
echo "--- flags legacy V2 in docs?"; for pat in 'minpos' 'mem-profile' 'settings.ini' '\-c ' ; do echo "'$pat': $(grep -c -- "$pat" all.txt)"; done
curl -s -L --max-time 40 $B/getting-started-guide/statistics.html | sed -e 's/<[^>]*>//g' > stats.txt
echo "--- statistics page (HET vs deltapsi), lines on conservative / deltapsi / sample sizes:"
grep -a -i -n 'conservative\|deltapsi\|5-10\|between 5\|10 ' stats.txt | cut -c1-260 | head
