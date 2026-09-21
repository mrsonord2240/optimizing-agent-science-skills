#!/bin/bash
# examples/hmmscan_to_pfamscan.py: error paths and an independent column check against the hmmscan --domtblout it converted (run from the copy in run/skill).
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
RUN=F:/OpenScience/audits/bio-isoform-switching/run; C=$RUN/skill/examples/hmmscan_to_pfamscan.py; W=$RUN/work/conv; rm -rf $W; mkdir -p $W; cd $W
D=$RUN/work/w4s/annot
echo "--- no args"; python $C; echo "rc=$?"
echo "--- missing clans file"; python $C $D/pfam_domtbl.txt out1.txt nope.tsv.gz 2>&1 | tail -1; echo "rc=${PIPESTATUS[0]}"
echo "--- empty domtblout (header only)"; grep '^#' $D/pfam_domtbl.txt > empty_domtbl.txt; python $C empty_domtbl.txt out2.txt $RUN/work/annot_dl/Pfam-A.clans.tsv.gz; echo "rc=$? size=$(wc -c < out2.txt)"
echo "--- non-domtblout input"; printf 'a b c\n' > bad.txt; python $C bad.txt out3.txt $RUN/work/annot_dl/Pfam-A.clans.tsv.gz 2>&1 | tail -1; echo "rc=${PIPESTATUS[0]}"
echo "--- plain (non-gz) clans file"; zcat $RUN/work/annot_dl/Pfam-A.clans.tsv.gz > clans.tsv; python $C $D/pfam_domtbl.txt out4.txt clans.tsv; cmp out4.txt $D/pfam_scanfmt.txt && echo "identical to gz result"
echo "--- independent column check (python): first ubiquitin row"
python - <<'PY'
import io
dom=[l.split() for l in io.open("F:/OpenScience/audits/bio-isoform-switching/run/work/w4s/annot/pfam_domtbl.txt",encoding="utf-8") if not l.startswith("#")]
out=[l.split() for l in io.open("F:/OpenScience/audits/bio-isoform-switching/run/work/w4s/annot/pfam_scanfmt.txt",encoding="utf-8")]
assert len(dom)==len(out), (len(dom),len(out))
bad=0
for d,o in zip(dom,out):
    # pfam_scan cols: seq, ali_from, ali_to, env_from, env_to, hmm_acc, hmm_name, type, hmm_from, hmm_to, hmm_len, bits, evalue, sig, clan
    exp=[d[3],d[17],d[18],d[19],d[20],d[1],d[0],"Domain",d[15],d[16],d[2],d[13],d[12],"1"]
    if o[:14]!=exp: bad+=1
print("rows",len(dom),"mismatching rows",bad)
print("first converted row:",out[0]); print("matching domtblout row:",dom[0][:21])
PY
