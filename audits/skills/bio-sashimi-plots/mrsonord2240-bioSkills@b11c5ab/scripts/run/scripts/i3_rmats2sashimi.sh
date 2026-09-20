# Input 3: SKILL.md rmats2sashimiplot block (04) run literally: planted 3v3 and real chrX 2v2, then forced failures to make the figure-exists assert fire
source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
export PATH=$RUN/bin:$PATH
PUB=$AS/public-data
runblock() { n=$1; f=$2; bash $f > $n.log 2>&1; echo "[$n] block rc=$?  | $(tr '\r' '\n' < $n.log | grep -a -E 'rmats2sashimiplot wrote|Error|error:|FileNotFound|Must provide' | head -3 | tr '\n' ' ')"; }
W=$RUN/out/i3_planted; rm -rf $W; mkdir -p $W/rmats_output; cd $W
cp $PUB/planted/*.bam $PUB/planted/*.bai .; cp $RUN/data/rmats_planted/SE.MATS.JC.txt rmats_output/
sed -e 's/ctrl1.bam,ctrl2.bam,ctrl3.bam/G1_rep1.bam,G1_rep2.bam,G1_rep3.bam/;s/trt1.bam,trt2.bam,trt3.bam/G2_rep1.bam,G2_rep2.bam,G2_rep3.bam/' $RUN/blocks/04_*.sh > b04.sh
runblock planted b04.sh
echo "figures:"; find sashimi_rmats/Sashimi_plot -name '*.pdf' | xargs ls -l | awk '{print $5,$9}'
micromamba run -n as-core python $RUN/scripts/i3_variants.py
for v in A B C D; do runblock fail$v b04_fail$v.sh; done
echo "pdf counts A-D: $(for v in A B C D; do echo -n "$v=$(find sashimi_fail$v/Sashimi_plot -name '*.pdf' -size +0 2>/dev/null | wc -l) "; done)"
grep -a "colors\|group_info" sashimi_failA/Sashimi_index_G1_1/sashimi_plot_settings.txt 2>/dev/null
# ---- real chrX 2v2 (BAM contig X, rMATS chrX)
W=$RUN/out/i3_real; rm -rf $W; mkdir -p $W/rmats_output; cd $W
cp $RUN/data/rmats_real/SE.MATS.JC.txt rmats_output/
D=$PUB/rnasplice/bam
sed -e "s#ctrl1.bam,ctrl2.bam,ctrl3.bam#$D/ERR188383.Aligned.out.bam,$D/ERR188428.Aligned.out.bam#;s#trt1.bam,trt2.bam,trt3.bam#$D/ERR188454.Aligned.out.bam,$D/ERR204916.Aligned.out.bam#;s#Control: 1-3#Control: 1-2#;s#Treatment: 4-6#Treatment: 3-4#;s#--l1 Control#--l1 GBR#;s#--l2 Treatment#--l2 YRI#" $RUN/blocks/04_*.sh > b04.sh
runblock real b04.sh
find sashimi_rmats/Sashimi_plot -name '*.pdf' | sort | xargs ls -l | awk '{print $5,$9}'
# 2v2 without group-info and 2 colours (SKILL Common Errors row)
python3 - <<'PY'
s = open('b04.sh').read()
gi = "    --group-info grouping.gf \\n"
assert gi in s
open('b04_noGI.sh', 'w', newline='\n').write(s.replace(gi, '').replace('-o sashimi_rmats', '-o sashimi_noGI').replace('sashimi_rmats/Sashimi_plot', 'sashimi_noGI/Sashimi_plot'))
PY
runblock realnoGI b04_noGI.sh
