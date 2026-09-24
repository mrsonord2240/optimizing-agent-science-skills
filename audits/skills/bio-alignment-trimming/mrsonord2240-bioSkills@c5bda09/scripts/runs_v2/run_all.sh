#!/bin/bash
# Re-audit of bio-alignment-trimming at mrsonord2240/bioSkills@966f838. SYNTHETIC data from ../data (make_data.py).
set -u
source /f/OpenScience/audit-envs/molecular-phylogenetics-analyst/env.sh
T=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/tools
TRIMAL=$T/trimal_v1.4.1/trimal.exe
PY=/f/OpenScience/audit-envs/molecular-phylogenetics-analyst/Scripts/python.exe
A=/f/OpenScience/audits/bio-alignment-trimming; R=$A/runs_v2; OLD=$A/runs; D=$A/data
SK=/f/OpenScience/external/mrsonord2240__bioSkills/alignment/alignment-trimming
H="$PY $R/helpers.py"
IQ="iqtree2 -T 4 --seed 1 -redo -quiet"
cd $R; clipkit --version; $TRIMAL --version

echo "######## IN1 canonical: single protein gene, smart-gap + --log (Skill verbatim)"
mkdir -p $R/in1 && cd $R/in1 && cp $D/prot15_linsi.fasta input.fasta
clipkit input.fasta -m smart-gap --log -o trimmed.fasta > clip.out 2>&1; echo "clipkit exit $?"
$IQ -s input.fasta -m MFP -B 1000 --prefix untrimmed; $IQ -s trimmed.fasta -m MFP -B 1000 --prefix smartgap
$H in1; $H trees $D/prot15_true.nwk untrimmed smartgap

echo "######## IN2 supermatrix: per-locus smart-gap, -of phylip, BMGE 1.12 + 2.0 (Skill verbatim)"
mkdir -p $R/in2 && cd $R/in2 && cp $D/dna_super/supermatrix.fasta $D/dna_super/supermatrix.nex .
clipkit supermatrix.fasta -m smart-gap -of phylip -o super_sg.phy > phy.out 2>&1; echo "clipkit -of phylip exit $?"; head -1 super_sg.phy
$PY $R/perlocus.py
cp $T/BMGE112.jar BMGE.jar
java -jar BMGE.jar -i supermatrix.fasta -t DNA -m DNAPAM100:2 -h 0.5 -g 0.2 -of trimmed.fasta > b112.out 2>&1; echo "BMGE1.12 exit $?"
test -s trimmed.fasta || echo "BMGE wrote no alignment: check flags against the installed version"; mv -f trimmed.fasta bmge112.fasta 2>/dev/null
cp $T/BMGE200.jar BMGE.jar
java -jar BMGE.jar -i supermatrix.fasta -t NT -m DNAPAM100:2 -e 0.5 -g 0.2 -o trimmed.fasta > b200.out 2>&1; echo "BMGE2.0 exit $?"
test -s trimmed.fasta || echo "BMGE wrote no alignment: check flags against the installed version"; mv -f trimmed.fasta bmge200.fasta 2>/dev/null
echo "-- guard check: 1.12 flags on the 2.0 jar"
java -jar BMGE.jar -i supermatrix.fasta -t DNA -m DNAPAM100:2 -h 0.5 -g 0.2 -of trimmed.fasta > b200_wrong.out 2>&1; echo "exit $?"
test -s trimmed.fasta || echo "BMGE wrote no alignment: check flags against the installed version"
$H retention supermatrix super_sg bmge112 bmge200
$IQ -s supermatrix.fasta -p supermatrix.nex -m MFP -B 1000 --prefix untrimmed
$IQ -s super_sg.fasta -p super_sg.nex -m MFP -B 1000 --prefix sg; echo "partitioned smart-gap exit $?"
$IQ -s bmge112.fasta -m MFP -B 1000 --prefix bmge112
$IQ -s bmge200.fasta -m MFP -B 1000 --prefix bmge200
$H trees $D/dna12_true.nwk untrimmed sg bmge112 bmge200

echo "######## IN3 unbalanced 30+3 (regression)"
mkdir -p $R/in3 && cd $R/in3 && cp $D/unbal33_linsi.fasta input.fasta
for m in kpic-smart-gap smart-gap; do clipkit input.fasta -m $m --log -o unbal_$m.fasta > clip_$m.out 2>&1; echo "clipkit $m exit $?"; done
$IQ -s input.fasta -m MFP -B 1000 --prefix untrimmed; $IQ -s unbal_kpic-smart-gap.fasta -m MFP -B 1000 --prefix kpic; $IQ -s unbal_smart-gap.fasta -m MFP -B 1000 --prefix smartgap
cp $OLD/in3/in3_report.py . && $PY in3_report.py

echo "######## IN4 HMM prep: -gappyout -colnumbering; Skill parser verbatim"
mkdir -p $R/in4 && cd $R/in4 && cp $D/deep_super/gene03.aln.fasta input.fasta
$TRIMAL -in input.fasta -out hmm_gappyout.fasta -gappyout -colnumbering > gappyout_cols.txt; echo "exit $?"
$TRIMAL -in input.fasta -out auto1.fasta -automated1 -colnumbering > kept_columns.txt; echo "exit $?"
$TRIMAL -in input.fasta -out manual.fasta -gt 0.3 -st 0.5 -cons 60 -colnumbering > columns.txt; echo "exit $?"
$H in4

echo "######## IN5 deep protein supermatrix: routes in the fixed Skill"
mkdir -p $R/in5 && cd $R/in5 && cp $D/deep_super/supermatrix.fasta input.fasta
clipkit input.fasta -m smart-gap -o clip_smart-gap.fasta -q; clipkit input.fasta -m kpic-smart-gap -o clip_kpic-smart-gap.fasta -q
$TRIMAL -in input.fasta -out trimal_gappyout.fasta -gappyout; $TRIMAL -in input.fasta -out trimal_strict.fasta -strict
cp $T/BMGE112.jar BMGE.jar
java -jar BMGE.jar -i input.fasta -t AA  -h 0.5 -g 0.2 -of trimmed.fasta > b112.out 2>&1; echo "BMGE1.12 AA exit $?"; test -s trimmed.fasta && mv -f trimmed.fasta bmge112_h05.fasta
cp $T/BMGE200.jar BMGE.jar
java -jar BMGE.jar -i input.fasta -t AA -e 0.5 -g 0.2 -o trimmed.fasta > b200.out 2>&1; echo "BMGE2.0 AA exit $?"; test -s trimmed.fasta && mv -f trimmed.fasta bmge200_e05.fasta
$H retention input clip_smart-gap clip_kpic-smart-gap trimal_gappyout trimal_strict bmge112_h05 bmge200_e05
for f in input clip_smart-gap clip_kpic-smart-gap trimal_gappyout trimal_strict bmge112_h05 bmge200_e05; do $IQ -s $f.fasta -m LG+G4 -B 1000 --prefix tree_$f; done
$H trees $D/deep16_true.nwk tree_input tree_clip_smart-gap tree_clip_kpic-smart-gap tree_trimal_gappyout tree_trimal_strict tree_bmge112_h05 tree_bmge200_e05

echo "######## IN6 codon alignment for codeml: sed + MACSE export (Skill verbatim), codeml"
mkdir -p $R/in6 && cd $R/in6 && cp $D/cds10_codon_aln.fasta codon.fasta && cp $OLD/in6/in6_inject.py . && $PY in6_inject.py
sed -e '/^>/!s/!/-/g' macse_like_nostop.fasta > aligned_paml.fasta; echo "sed exit $?; '!' in seqs: $(grep -v '>' aligned_paml.fasta | grep -c '!'); headers intact: $(grep -c '>' aligned_paml.fasta)"
java -jar $T/macse_v2.07.jar -prog exportAlignment -align macse_like.fasta \
    -codonForFinalStop --- -codonForInternalStop NNN \
    -codonForInternalFS --- -charForRemainingFS - \
    -out_NT aligned_hyphy.fasta -out_AA aligned_hyphy_aa.fasta > macse.out 2>&1; echo "MACSE exit $?"; tail -2 macse.out
echo "'!' left in hyphy NT: $(grep -v '>' aligned_hyphy.fasta | grep -o '!' | wc -l); NNN codons: $(grep -v '>' aligned_hyphy.fasta | grep -o NNN | wc -l)"
for v in paml hyphy; do
  mkdir -p codeml_$v; cp $D/cds10_true.nwk codeml_$v/tree.nwk; cp aligned_$v.fasta codeml_$v/aln.fasta
  printf "seqfile = aln.fasta\ntreefile = tree.nwk\noutfile = mlc\nnoisy = 0\nverbose = 0\nrunmode = 0\nseqtype = 1\nCodonFreq = 2\nmodel = 0\nNSsites = 0\nicode = 0\nfix_kappa = 0\nkappa = 2\nfix_omega = 0\nomega = 0.4\ncleandata = 0\n" > codeml_$v/codeml.ctl
  (cd codeml_$v && timeout 300 codeml codeml.ctl > run.out 2>&1; echo "codeml $v exit $?"; tail -2 run.out; grep -E "^lnL|omega \(dN/dS\)" mlc 2>/dev/null)
done

echo "######## IN7 adversarial: trim until all nodes >=95 (regression)"
mkdir -p $R/in7 && cd $R/in7 && cp $D/prot15_linsi.fasta input.fasta
clipkit input.fasta -m kpi -o kpi.fasta -q; clipkit input.fasta -m kpi-smart-gap -o kpism.fasta -q; clipkit input.fasta -m smart-gap -o smartgap.fasta -q
$TRIMAL -in input.fasta -out nogaps.fasta -nogaps; $TRIMAL -in input.fasta -out strictplus.fasta -strictplus
for f in input smartgap strictplus kpism kpi nogaps; do $IQ -s $f.fasta -m LG+G4 -B 1000 --prefix t_$f; done
cp $OLD/in7/in7_report.py . && $PY in7_report.py

echo "######## IN8 NEW: PhyIN second pass on a DNA locus (Skill verbatim)"
mkdir -p $R/in8 && cd $R/in8 && cp $D/dna_super/locus05.aln.fasta input.fasta && cp $T/phyin/phyin.py .
clipkit input.fasta -m smart-gap -o first.fasta -q; echo "clipkit exit $?"
python phyin.py -input first.fasta -output trimmed.fasta -b 10 -d 2 -p 0.5 > phyin.out 2>&1; echo "phyin exit $?"; tail -5 phyin.out
$H retention input first trimmed
$IQ -s input.fasta -m MFP -B 1000 --prefix t_input; $IQ -s first.fasta -m MFP -B 1000 --prefix t_first; $IQ -s trimmed.fasta -m MFP -B 1000 --prefix t_phyin
$H trees $D/dna12_true.nwk t_input t_first t_phyin
echo "-- PhyIN on protein input (Skill says DNA/RNA only)"
python phyin.py -input $D/prot15_linsi.fasta -output prot_phyin.fasta -b 10 -d 2 -p 0.5 > phyin_prot.out 2>&1; echo "exit $?"; tail -3 phyin_prot.out

echo "######## IN9 NEW: fragmentary sequences, trimAl -resoverlap/-seqoverlap (Skill verbatim)"
mkdir -p $R/in9 && cd $R/in9 && $PY $R/make_frag.py
$TRIMAL -in frag17.fasta -out seqfilt.fasta -resoverlap 0.8 -seqoverlap 75; echo "trimal exit $?"
echo "seqs in: $(grep -c '>' frag17.fasta) out: $(grep -c '>' seqfilt.fasta)"; diff <(grep '>' frag17.fasta) <(grep '>' seqfilt.fasta)
clipkit frag17.fasta -m smart-gap -o frag_sg.fasta -q; clipkit seqfilt.fasta -m smart-gap -o seqfilt_sg.fasta -q
$H retention frag17 frag_sg seqfilt_sg

echo "######## EXAMPLES as shipped"
mkdir -p $R/examples && cd $R/examples
for s in clipkit_trim trimal_modes bmge_trim divvier_split; do $PY -m py_compile $SK/examples/$s.py && echo "$s py_compile OK"; done
mkdir -p ck && cp $SK/examples/clipkit_trim.py $D/prot15_linsi.fasta ck/ && mv ck/prot15_linsi.fasta ck/input.fasta
(cd ck && $PY clipkit_trim.py; echo "clipkit_trim exit $?")
mkdir -p b112 && cp $SK/examples/bmge_trim.py b112/ && cp $D/prot15_linsi.fasta b112/input.fasta && cp $T/BMGE112.jar b112/BMGE.jar
(cd b112 && $PY bmge_trim.py 2>&1 | tr '\r' '\n' | grep -E "BMGE|->|WARNING|Error|Traceback" ; echo "bmge_trim 1.12 exit ${PIPESTATUS[0]}")
mkdir -p b200 && sed "s/^    version = '1.12'.*/    version = '2.0'/" $SK/examples/bmge_trim.py > b200/bmge_trim.py && cp $D/prot15_linsi.fasta b200/input.fasta && cp $T/BMGE200.jar b200/BMGE.jar
(cd b200 && $PY bmge_trim.py 2>&1 | tr '\r' '\n' | grep -E "BMGE|->|WARNING|Error|Traceback" ; echo "bmge_trim 2.0 exit ${PIPESTATUS[0]}")
mkdir -p bwrong && cp $SK/examples/bmge_trim.py bwrong/ && cp $D/prot15_linsi.fasta bwrong/input.fasta && cp $T/BMGE200.jar bwrong/BMGE.jar
(cd bwrong && $PY bmge_trim.py 2>&1 | tail -2; echo "bmge_trim version mismatch exit ${PIPESTATUS[0]}")
echo ALL DONE
