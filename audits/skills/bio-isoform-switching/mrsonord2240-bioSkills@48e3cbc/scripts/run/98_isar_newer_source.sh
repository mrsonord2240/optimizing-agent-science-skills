#!/bin/bash
# Does a NEWER IsoformSwitchAnalyzeR choose the DTU test automatically? Read the source of the Bioconductor 3.22 (2.10.0) and 3.23 (2.12.0, current release) tarballs
# (public; downloaded to work/isar_src with the curl lines below). Not installable in this R 4.4 / Bioc 3.20 env (2.12.0 needs Seqinfo, see 97 log).
cd F:/OpenScience/audits/bio-isoform-switching/run/work; mkdir -p isar_src; cd isar_src
for pair in "3.22 2.10.0" "3.23 2.12.0"; do set -- $pair
  [ -f isar_$2.tar.gz ] || curl -sS -L --max-time 200 -o isar_$2.tar.gz https://bioconductor.org/packages/$1/bioc/src/contrib/IsoformSwitchAnalyzeR_$2.tar.gz
  [ -d IsoformSwitchAnalyzeR_$2 ] || { tar xzf isar_$2.tar.gz; mv IsoformSwitchAnalyzeR IsoformSwitchAnalyzeR_$2; }
  echo "=== $2: $(grep '^Version' IsoformSwitchAnalyzeR_$2/DESCRIPTION)"
  echo "-- exports for annotators / tests:"; grep -E "export\('(analyze(NetSurf|SignalP|IUPred|DeepTM|PFAM|CPC2)|isoformSwitchTest)" IsoformSwitchAnalyzeR_$2/NAMESPACE
  echo "-- test-selection lines in test_isoform_switches.R (warnings only? any switch between DEXSeq and satuRn inside a test function?):"
  sed -n '60,75p;398,410p' IsoformSwitchAnalyzeR_$2/R/test_isoform_switches.R
  echo "-- any call of satuRn::/DEXSeq:: inside importRdata or preFilter (auto-selection would need one):"
  grep -n "isoformSwitchTestSatuRn(\|isoformSwitchTestDEXSeq(" IsoformSwitchAnalyzeR_$2/R/*.R | grep -v "^.*#" | head
  echo "-- default of calculateCountsFromAbundance:"; grep -n "calculateCountsFromAbundance=TRUE\|calculateCountsFromAbundance = TRUE" IsoformSwitchAnalyzeR_$2/R/import_data.R | head -3
done
