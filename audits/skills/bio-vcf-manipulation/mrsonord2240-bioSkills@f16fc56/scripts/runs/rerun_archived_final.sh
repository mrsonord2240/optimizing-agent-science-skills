#!/usr/bin/env bash
set +e
root=/mnt/f/OpenScience/audits/bio-vcf-manipulation/runs
for d in p_in1 p_in2 p_in3 p_in4 p_in5 in6 in7; do
  bash -lc "cd '$root/$d' && bash run.sh" > "$root/$d/final_20260924.out" 2>&1
  rc=$?
  printf "%s\t%s\n" "$d" "$rc"
done
