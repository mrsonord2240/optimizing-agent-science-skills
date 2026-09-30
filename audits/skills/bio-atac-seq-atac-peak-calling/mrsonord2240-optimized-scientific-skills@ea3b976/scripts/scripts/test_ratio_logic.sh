# Extract the script's own ratio/verdict block (lines idr_n() .. VERDICT=) and drive it with synthetic IDR files.
S=/mnt/openscience/wt/atac-atac-peak-calling/skills/bio-atac-seq-atac-peak-calling/scripts/call_atac_peaks.sh
T=$(mktemp -d); mkdir -p $T/idr
a=$(grep -n '^idr_n()' $S | cut -d: -f1); b=$(grep -n '^    print (br && bs)' $S | cut -d: -f1)
sed -n "${a},${b}p" $S > $T/block.sh
mk() { name=$1; n=$2; awk -v n=$n 'BEGIN{for(i=1;i<=n;i++) printf "chr1\t%d\t%d\tp%d\t%d\t.\n",i*10,i*10+5,i,700}' > $T/idr/$name.idr; # 700 >= 540
       # add 5 sub-threshold rows (score 400) which must be excluded
       for i in 1 2 3 4 5; do printf "chr1\t1\t2\tx\t400\t.\n" >> $T/idr/$name.idr; done; }
run() { # label Nt N1 N2 Np expected
  mk true_reps $2; mk rep1_pseudoreps $3; mk rep2_pseudoreps $4; mk pooled_pseudoreps $5
  OUTDIR=$T IDR_T=0.05
  eval "$(cat $T/block.sh; echo 'NT=$(idr_n true_reps); N1=$(idr_n rep1_pseudoreps); N2=$(idr_n rep2_pseudoreps); NP=$(idr_n pooled_pseudoreps)
RESCUE=$(ratio "$NP" "$NT"); SELF=$(ratio "$N1" "$N2")')"
  V=$VERDICT
  echo "$1: Nt=$NT N1=$N1 N2=$N2 Np=$NP rescue=$RESCUE self=$SELF verdict=$V expected=$6"
}
run pass_case 1197 1143 1249 1036 PASS
run borderline_rescue 100 200 210 500 BORDERLINE
run borderline_self 500 100 400 480 BORDERLINE
run fail_both 100 400 100 500 FAIL
run fail_zero_Nt 0 300 100 400 FAIL
run zero_both_ok 0 0 0 0 FAIL
run boundary_exactly_2 100 200 100 200 PASS
