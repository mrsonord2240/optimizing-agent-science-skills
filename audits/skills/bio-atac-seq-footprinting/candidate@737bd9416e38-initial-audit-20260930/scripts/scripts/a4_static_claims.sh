#!/bin/bash
# A4: live re-check of documented commands/claims: JASPAR URL, one-line install resolution, flag defaults, HINT stranded claim, MA0139.1, tangermeme.
source /mnt/openscience/audits/bio-atac-seq-footprinting/initial-audit-20260930/scripts/common.sh
echo "## JASPAR URLs (HTTP status after redirects)"
for u in JASPAR2024_CORE_vertebrates_non-redundant_pfms.txt JASPAR2024_CORE_vertebrates_non-redundant_pfms_jaspar.txt; do
  echo "$u -> $(curl -sL -o /dev/null -w '%{http_code} %{url_effective}' https://jaspar.genereg.net/download/data/2024/CORE/$u)"; done
echo "## usage-guide one-line install (dry run, conda-forge+bioconda)"
micromamba create -n zz-dryrun2 --dry-run -c conda-forge -c bioconda tobias rgt pydnase samtools bedtools 2>&1 | grep -E "^\s*\+ (python|tobias|rgt|pydnase|samtools|bedtools)[ ]" 
echo "## BINDetect / ATACorrect / PlotAggregate flags"
TOBIAS BINDetect --help 2>&1 | grep -E -A1 "bound-pvalue|cond-names|motif-pvalue" | head -12
TOBIAS ATACorrect --help 2>&1 | grep -E -A1 "read_shift|read-shift|k_flank|k-flank" | head
TOBIAS PlotAggregate --help 2>&1 | grep -E -A1 "share-y|share_y|plot-boundaries" | head
echo "## motif IDs in the JASPAR 2024 non-redundant vertebrate file"
grep -E "^>MA0139|^>MA1929|^>MA1930" $D/motifs/JASPAR2024_CORE_vertebrates_non-redundant_pfms.txt
echo "## HINT-ATAC footprinting options (stranded claim)"
micromamba run -n $P-rgt rgt-hint footprinting --help 2>&1 | grep -iE "strand|paired|atac|organism|region" | head -12
echo "## Wellington options (paired-end claim)"
micromamba run -n $P-pydnase wellington_footprints.py --help 2>&1 | grep -iE "paired|single|shift|atac|-A|-D" | head
echo "## scPrinter: does documented 'pip install ./' at v1.2.0 import? tangermeme versions in env and tools.tomtom presence"
micromamba run -n $P-scprinter pip list 2>/dev/null | grep -iE "^(tangermeme|snapatac2|scprinter|numpy|torch) "
cd $W && rm -rf tm && mkdir tm && cd tm
for v in 0.4.4 1.5.0; do pip download tangermeme==$v --no-deps -q -d d$v 2>&1 | tail -1; unzip -l d$v/*.whl 2>/dev/null | grep -c "tangermeme/tools/tomtom" | sed "s/^/tangermeme $v: files matching tools\/tomtom = /"; done
