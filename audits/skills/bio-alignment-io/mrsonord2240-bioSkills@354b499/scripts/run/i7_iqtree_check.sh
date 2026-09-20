#!/bin/bash
# SKILL claim: 'iqtree2 -s file.phy --check' validates the input only. iqtree3 lives in WSL env bio (login shell). Real Pfam relaxed PHYLIP.
D=/mnt/openscience/audits/bio-alignment-io/run/data; cd $D; mkdir -p iq; cd iq
which iqtree2 iqtree3 iqtree 2>&1 | head
echo "== --check"; timeout 120 iqtree3 -s ../pf_relaxed.phy --check --prefix chk </dev/null 2>&1 | tail -5
echo "== -n 0 -m LG (does relaxed PHYLIP with '/' names load?)"; timeout 300 iqtree3 -s ../pf_relaxed.phy -m LG -n 0 -T 2 --prefix ok </dev/null 2>&1 | grep -E "Alignment most|Number of|ERROR|Best|Input data" | head
