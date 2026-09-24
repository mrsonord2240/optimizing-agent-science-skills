# Compare contig names and lengths, and M5 wherever the BAM header carries it. Exit 1 on any difference.
awk -F'\t' '
  function parse(   i,k,v) { sn=ln=m5=""; for (i=2;i<=NF;i++) { k=substr($i,1,2); v=substr($i,4); if (k=="SN") sn=v; else if (k=="LN") ln=v; else if (k=="M5") m5=v } }
  FNR==NR { if ($1=="@SQ") { parse(); rlen[sn]=ln; rm5[sn]=m5 } ; next }
  $1=="@SQ" { parse(); if (m5!="") nm5++
      if (!(sn in rlen))      { print "NOT IN REFERENCE:", sn; bad=1 }
      else if (rlen[sn]!=ln)  { print "LENGTH DIFFERS:", sn, ln, "vs", rlen[sn]; bad=1 }
      else if (m5!="" && m5!=rm5[sn]) { print "M5 DIFFERS:", sn; bad=1 } }
  END { if (!nm5) print "no M5 in BAM header: only names and lengths were compared"; exit bad }
' <(samtools dict '/mnt/openscience/audits/bio-alignment-validation/run/out/work/sp dir/ref exact.fa') <(samtools view -H /mnt/openscience/audits/bio-alignment-validation/run/data/ref/bam_m5.bam)
