#!/bin/bash
# INPUT 6 (scope boundary, NEW data): (a) MAJIQ V3 / VOILA (licence-gated): judge the hedging against the public MAJIQ docs; (b) paired tumor-normal `rMATS --paired-stats` with PAIRADISE
# in the new env as-pairadise on SYNTHETIC sim2p (5 patients, private per-patient logit offsets ~N(0,0.8), 28 strong planted true DS among 100 genes), incl. the fork-profile workaround,
# the silent failure in as-core (no PAIRADISE) and the Skill's install path; (c) leafcutterMD hand-off target.
source /mnt/openscience/audits/bio-differential-splicing/run/common.sh
S=$R/data/sim2p
W=$R/out/in6; rm -rf $W; mkdir -p $W; cd $W
echo "=== (a) MAJIQ / VOILA availability (Skill: licence-gated, not run)"
for t in majiq voila; do which $t >/dev/null 2>&1 && echo "$t on PATH" || echo "$t: not on PATH"; done
micromamba run -n as-core pip download majiq --no-deps -d /tmp/majiq_dl > majiq_pip.log 2>&1; echo "pip download majiq rc=$?"; tail -2 majiq_pip.log | cut -c1-200
echo "--- MAJIQ documentation pages named in the Skill (public, unauthenticated)"
for u in https://biociphers.bitbucket.io/majiq-docs/ https://biociphers.bitbucket.io/majiq-docs/quick-overview.html https://biociphers.bitbucket.io/majiq-docs/majiq-build.html https://biociphers.bitbucket.io/majiq-docs/quantifiers.html; do
  code=$(curl -s -L -o page_$(basename $u).html -w '%{http_code}' --max-time 40 $u); echo "$u -> HTTP $code, $(wc -c < page_$(basename $u).html) bytes"
done
for pat in 'psi-coverage' 'heterogen' 'deltapsi' 'grp1' 'splicegraph.zarr' 'experiments' 'VOILA' 'v2' 'mindenovo' 'min-experiments' 'simplify' 'strandness' 'minreads' 'minbins' '3.0.11'; do
  echo "docs mention '$pat': $(cat page_*.html | grep -c -- "$pat")"
done
echo "--- do the V2-era flags the Skill says are unverified appear? (--minpos, --mem-profile, settings.ini)"
for pat in 'minpos' 'mem-profile' 'settings.ini'; do echo "docs mention '$pat': $(cat page_*.html | grep -c -- "$pat")"; done

echo "=== (b) rMATS --paired-stats"
echo "--- Skill install path: does PAIRADISE/pairadise/src/pairadise_model exist in the public repo?"
rm -rf /tmp/PAIRADISE_chk; git clone --depth 1 -q https://github.com/Xinglab/PAIRADISE /tmp/PAIRADISE_chk 2>&1 | tail -2; ls /tmp/PAIRADISE_chk/pairadise/src/pairadise_model | head; grep -E '^(Imports|Depends)' -A4 /tmp/PAIRADISE_chk/pairadise/src/pairadise_model/DESCRIPTION | head -12
lst() { local pre=$1 n=$2; local o=""; for i in $(seq 1 $n); do o="$o,$S/$pre$i.bam"; done; echo "${o#,}"; }
lst N 5 > b1.txt; lst T 5 > b2.txt      # entry i of b1 pairs with entry i of b2 (patient i)
cat b1.txt b2.txt | tr ',' '\n' | head -3
echo "--- (b1) as-core (no PAIRADISE): Skill says logs 'no package called PAIRADISE', exits 0, header-only, no FDR column"
mkdir -p pc/tmp pc/out
$CORE rmats.py --b1 b1.txt --b2 b2.txt --gtf $S/sim.gtf -t single --readLength 50 --libType fr-unstranded --nthread 4 --od pc/out --tmp pc/tmp --novelSS --paired-stats > pc.log 2>&1; echo "rc=$?"
grep -a 'PAIRADISE' pc.log | head -3 | cut -c1-200
echo "SE.MATS.JC.txt rows: $(($(wc -l < pc/out/SE.MATS.JC.txt)-1)); header has FDR column: $(head -1 pc/out/SE.MATS.JC.txt | grep -c FDR)"
echo "--- (b2) as-pairadise with the fork profile (Skill workaround)"
mkdir -p pf/tmp pf/out
s0=$(date +%s); R_PROFILE_USER=$FORK_PROFILE $PA rmats.py --b1 b1.txt --b2 b2.txt --gtf $S/sim.gtf -t single --readLength 50 --libType fr-unstranded --nthread 4 --od pf/out --tmp pf/tmp --novelSS --paired-stats > pf.log 2>&1; echo "rc=$? after $(( $(date +%s) - s0 )) s"
cat $FORK_PROFILE
echo "SE.MATS.JC.txt rows: $(($(wc -l < pf/out/SE.MATS.JC.txt)-1)); header has FDR column: $(head -1 pf/out/SE.MATS.JC.txt | grep -c FDR)"
echo "--- (b3) as-pairadise, default PSOCK cluster, 3 attempts with a 150 s timeout (Skill: hung 3 of 6 runs)"
for k in 1 2 3; do
  mkdir -p ps$k/tmp ps$k/out
  s0=$(date +%s); timeout 150 $PA rmats.py --b1 b1.txt --b2 b2.txt --gtf $S/sim.gtf -t single --readLength 50 --libType fr-unstranded --nthread 4 --od ps$k/out --tmp ps$k/tmp --novelSS --paired-stats > ps$k.log 2>&1; rc=$?
  echo "attempt $k: rc=$rc (124 = hung, killed) after $(( $(date +%s) - s0 )) s; status: $(cat ps$k/out/tmp/JC_SE/pairadise_status.txt 2>/dev/null | tr '\r\n' '  ' | tail -c 60); FDR column: $(head -1 ps$k/out/SE.MATS.JC.txt 2>/dev/null | grep -c FDR)"
  echo "   leftover pairadise processes of this attempt: $(pgrep -af "ps$k/out" | grep -vc pgrep)"
done
echo "--- (b4) unpaired rMATS on the same 10 BAMs (5 vs 5, no --paired-stats) for contrast"
mkdir -p up/tmp up/out
$CORE rmats.py --b1 b1.txt --b2 b2.txt --gtf $S/sim.gtf -t single --readLength 50 --libType fr-unstranded --nthread 4 --od up/out --tmp up/tmp --novelSS > up.log 2>&1; echo "rc=$?"
echo "--- (c) leafcutterMD.R hand-off target"
leafcutterMD.R -h 2>&1 | tr '\r' '\n' | head -6
echo "=== score paired vs unpaired against planted truth"
$CORE python $R/in6_score.py $S/truth.tsv $W
