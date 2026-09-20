# exit code of rmats2sashimiplot itself on the failure modes named in the Skill (assert removed)
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/out/i3_planted
B1=G1_rep1.bam,G1_rep2.bam,G1_rep3.bam; B2=G2_rep1.bam,G2_rep2.bam,G2_rep3.bam
for v in "A|" "B|--group-info nofile.gf" "C|--group-info grouping.gf"; do
  n=${v%%|*}; extra=${v#*|}
  rm -rf tool_$n
  if [ $n = C ]; then flag="-t SE"; else flag="--event-type SE"; fi
  rmats2sashimiplot --b1 $B1 --b2 $B2 $flag -e sig.SE.MATS.JC.txt --l1 Control --l2 Treatment -o tool_$n --exon_s 1 --intron_s 5 $extra --color '#1f77b4,#ff7f0e' > tool_$n.log 2>&1
  echo "[$n] tool rc=$?  pdfs=$(find tool_$n -name '*.pdf' -size +0 2>/dev/null | wc -l)"
done
