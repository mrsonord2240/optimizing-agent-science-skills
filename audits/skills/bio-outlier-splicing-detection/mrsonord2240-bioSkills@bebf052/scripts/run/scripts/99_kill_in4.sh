#!/bin/bash
for p in $(pgrep -f "10_block_fraser.R"); do
  d=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null | grep -o 'run/in[0-9a-z_]*' | head -1)
  echo "$p $d"
  [ "$d" = "run/in4_drop" ] && kill $p
done
sleep 2; echo remaining: $(pgrep -f "run/in4_drop" | wc -l)
