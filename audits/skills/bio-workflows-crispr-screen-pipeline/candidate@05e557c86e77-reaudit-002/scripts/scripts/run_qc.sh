# reaudit-002 qc.py and rra.py runs (Git Bash). Outputs in work/*.log
export PATH=/f/OpenScience/audit-envs/crispr-screen-analyst/Scripts:$PATH
S=F:/OpenScience/wt/recut-crispr-pipeline/skills/bio-workflows-crispr-screen-pipeline/scripts
D=F:/OpenScience/audit-envs/crispr-screen-analyst/public-data/derived/crispr-pipeline
W=F:/OpenScience/fix-evidence/recut-crispr-pipeline/reaudit-002/work
python $S/qc.py $D/qc/hap1.count.txt $W/hap1.tsv plasmid=HAP1_T0
python $S/qc.py $D/cn-correction/a375.count.txt $W/a375d.tsv plasmid=CTRL_ERS717283.plasmid
python $S/qc.py $D/cn-correction/a375.count.txt $W/a375p.tsv plasmid=CTRL_ERS717283.plasmid 'pattern=R\d(?=_P1D14$)'
python $S/qc.py $D/rra-qcpass/hap1.count.txt $W/rraqp.tsv plasmid=HAP1_T0
python $S/qc.py $D/cn-correction-qcpass/a375.count.txt $W/cnqp.tsv plasmid=A375_plasmid
python $S/qc.py $D/qc/hap1.count.txt $W/x.tsv plasmid=Plasmid   # expect exit 1
python $S/rra.py $D/rra-qcpass/hap1.count.txt rra_qp treatment=HAP1_T18A,HAP1_T18B,HAP1_T18C control=HAP1_T0
