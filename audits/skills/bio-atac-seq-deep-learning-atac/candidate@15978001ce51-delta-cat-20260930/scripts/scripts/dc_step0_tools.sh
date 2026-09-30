#!/bin/bash
# Delta re-audit (DLA-015): execute the candidate's step 0 tool check, unmodified, from a scratch cwd.
# Pass case: all three tools on PATH -> step 0 passes and the next guard (missing BAM) fires.
# Fail cases: PATH-filtered shell with one tool withheld -> exit 1 with "<tool> not on PATH ...".
# No training runs: every case stops at a step-0 / input guard in seconds.
set -u
SK=/mnt/openscience/wt/atac-deep-learning-atac/skills/bio-atac-seq-deep-learning-atac/scripts/chrombpnet_pipeline.sh
E=/home/sci/micromamba/envs/dlatac-tf/bin      # this Skill's `chrombpnet` env (TOOLS.md: dlatac-tf)
W=/tmp/dc_step0_$$; rm -rf "$W"; mkdir -p "$W"; cd "$W"
echo "candidate script sha256: $(sha256sum "$SK" | cut -d' ' -f1)"
bash -n "$SK" && echo "bash -n: ok"
echo "--- step 0 as shipped:"; sed -n '/^# 0\./,/^done/p' "$SK"
echo "--- tools in env $E:"; for t in chrombpnet bedtools bedGraphToBigWig; do ls -l "$E/$t" 2>&1 | awk '{print $NF}'; done
echo "--- same tools in /usr/bin or /bin (must be absent for the filtered test to be valid):"
for t in chrombpnet bedtools bedGraphToBigWig; do for d in /usr/bin /bin; do [ -e "$d/$t" ] && echo "PRESENT $d/$t"; done; done; echo "(end)"

run_case() {  # $1 label, $2 PATH
    local t0=$(date +%s.%N)
    env -i HOME="$HOME" PATH="$2" bash "$SK" >out.txt 2>err.txt; local rc=$?
    local dt=$(echo "$(date +%s.%N) - $t0" | bc)
    printf '%-28s rc=%s  %.2fs  stderr: %s\n' "$1" "$rc" "$dt" "$(tr '\n' '|' <err.txt)"
    ls -A | grep -vxE 'out.txt|err.txt|bin_.*' | sed 's/^/  created: /'
}

# Pass: full env first on PATH
run_case "all three present" "$E:/usr/bin:/bin"

# Filtered PATH: ONE shim dir linking every env binary and every /usr/bin binary except the
# withheld tool(s); PATH is that dir only, so a system copy (/usr/bin/bedtools exists) cannot mask it.
mk() { local d="$W/bin_$1"; mkdir -p "$d"
       for f in "$E"/* /usr/bin/*; do b=$(basename "$f"); [ -e "$d/$b" ] && continue
           case " $2 " in *" $b "*) ;; *) ln -s "$f" "$d/$b";; esac; done; echo "$d"; }
for t in chrombpnet bedtools bedGraphToBigWig; do
    d=$(mk "no_$t" "$t")
    [ -e "$d/$t" ] && echo "ERROR shim still has $t"
    run_case "without $t" "$d"
done
d=$(mk none ""); run_case "shim with all three (ctrl)" "$d"
d=$(mk no_two "bedtools bedGraphToBigWig"); run_case "without bedtools+bG2BW" "$d"
rm -rf "$W"
