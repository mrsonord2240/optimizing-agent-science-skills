#!/bin/bash
# Bounded smoke of the usage-guide seq2PRINT training route in the FRESH footprint-scprinter env.
# The three fenced blocks of the "seq2PRINT model training" section are EXTRACTED from the candidate usage-guide.md.
# Substitutions (only): prep input paths + splits (the staged real data is hg38 chr1:1-30 Mb cut into pseudo chr1/2/3 = 16/7/7 Mb,
# a test device the guide itself describes), SCPRINTER_DATA -> existing model cache. Config peaks thinned to 1500/250/250 as the
# guide states. Hard cap 45 min. GPU memory sampled every 2 s.
export MAMBA_ROOT_PREFIX=/home/sci/micromamba PATH=/home/sci/.local/bin:$PATH PYTHONDONTWRITEBYTECODE=1
export PATH=/home/sci/micromamba/envs/footprint-scprinter/bin:$PATH   # python3 for the config/thinning helpers
Q=bio-atac-seq-footprinting; SKILL=/mnt/openscience/wt/atac-footprinting/skills/$Q; UG=$SKILL/references/usage-guide.md
E=/mnt/openscience/audit-envs/$Q; T=$E/tooling-scprinter/s2p
W=$E/reaudit-final/s2p_run; rm -rf $W; mkdir -p $W; cd $W
L=/mnt/openscience/audits/$Q/reaudit-final-20260930/logs
for f in pseudo.fa pseudo.fa.fai genes.gtf bl.bed frags.tsv.gz frags.tsv.gz.tbi; do cp $T/$f .; done
python3 - "$UG" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
sec = t.split("### seq2PRINT model training")[1].split("\n## ")[0]
blocks = re.findall(r"```(\w+)\n(.*?)```", sec, re.S)
print("blocks:", [b[0] for b in blocks])
assert [b[0] for b in blocks] == ["bash", "python", "bash"]
for i, (lang, body) in enumerate(blocks, 1):
    open(f"block{i}.{'py' if lang == 'python' else 'sh'}", "w").write(body)
PY
cp block2.py block2.orig.py
sed -i 's#^work, fa, gtf, bl, frags = .*#work, fa, gtf, bl, frags = os.path.abspath("s2p"), "pseudo.fa", "genes.gtf", "bl.bed", "frags.tsv.gz"#; s#^splits = .*#splits = [{"train": ["chr1"], "valid": ["chr2"], "test": ["chr3"]}] * 5#' block2.py
cp block2.py prep_seq2print.py
sed -i "s#export SCPRINTER_DATA=.*#export SCPRINTER_DATA=$E/scprinter#" block1.sh
diff block2.orig.py block2.py > $L/r7_prep_substitutions.diff; echo "prep diff:"; cat $L/r7_prep_substitutions.diff
echo "block1:"; cat block1.sh; echo "block3:"; cat block3.sh
( while true; do echo "$(date +%T) $(nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader)"; sleep 2; done ) > $L/r7_gpu_mem.log 2>&1 &
MON=$!
echo "=== prep start $(date -Is)"
( time bash -e block1.sh ) > $L/r7_prep.log 2>&1; echo "prep rc=$? $(date -Is)"; grep -v "it/s\|%|" $L/r7_prep.log | tail -4
python3 - <<'PY'
import json, pandas as pd
p = pd.read_csv("s2p/peaks.bed", sep="\t", header=None); print("cleaned peaks", len(p), p[0].value_counts().to_dict())
q = pd.concat([p[p[0] == c].sample(n=k, random_state=5) for c, k in {"chr1": 1500, "chr2": 250, "chr3": 250}.items()]).sort_values([0, 1])
q.to_csv("s2p/peaks_thin.bed", sep="\t", header=False, index=False)
c = json.load(open("s2p/cfg_fold0.json")); print("config", {k: c.get(k) for k in ("peaks", "signals", "genome", "split", "epochs", "batch_size", "early_stopping")})
c["peaks"] = "peaks_thin.bed"; json.dump(c, open("s2p/cfg_fold0.json", "w"), indent=4)
PY
echo "=== train start $(date -Is)"
( time timeout -k 30 2700 bash -e block3.sh ) > $L/r7_train.log 2>&1; echo "train rc=$? end $(date -Is)"
kill $MON
grep -v "it/s\|%|" $L/r7_train.log | grep -iE "pearson|loss|epoch|error|real" | tail -25
awk '{split($2,a," "); gsub(/ MiB,?/,"",$2); print}' $L/r7_gpu_mem.log | sort -t' ' -k2,2n | tail -1
echo alldone
