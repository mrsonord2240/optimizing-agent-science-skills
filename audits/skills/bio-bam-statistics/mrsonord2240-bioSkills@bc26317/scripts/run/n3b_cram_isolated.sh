#!/bin/bash
# NEW: repeat the CRAM-without-reference cases with the htslib reference cache disabled (n3 showed own_ctg.cram decoding with no reference: ~/.cache/hts-ref had been filled by earlier runs).
# Also verify how samtools stats treats templates longer than -i (clamp vs drop).
export LC_ALL=C PYTHONIOENCODING=utf-8
R=/mnt/openscience/audits/bio-bam-statistics/run; N=$R/data/new; cd $R/work; rm -rf cb2; mkdir cb2; cd cb2
export REF_PATH=$R/work/cb2/norefs REF_CACHE=$R/work/cb2/nocache; mkdir -p norefs
Q="python $R/skill/examples/qc_report.py"
ls ~/.cache/hts-ref 2>/dev/null | head -3 | sed 's/^/(default cache dir has entries, now bypassed): /'
for f in own_ctg.cram own_ctg_embed.cram own_ctg_noidx.cram; do
  echo "--- $f : samtools flagstat, cache bypassed"; timeout 60 samtools flagstat -O tsv $N/$f 2>&1 | sed -n '1,2p' | cut -f1-3 | cut -c1-200
  echo "--- $f : qc_report.py WITHOUT reference, cache bypassed"; timeout 120 $Q $N/$f 2>&1 | grep -v cram_index_load | sed -n '1,4p;/Mapped/p' | cut -c1-260; echo "rc=${PIPESTATUS[0]}"
  echo "--- $f : qc_report.py WITH reference"; timeout 120 $Q $N/$f $N/own_ctg.fa 2>&1 | grep -v cram_index_load | sed -n '1,4p;/Mapped/p'| cut -c1-200; echo "rc=${PIPESTATUS[0]}"
done
echo "--- Count Reads snippet (block 027) on own_ctg.cram, cache bypassed (Skill: OSError: truncated file)"; sed "s#'input.bam'#'$N/own_ctg.cram'#" $R/blocks/027_python.py > c.py; timeout 60 python c.py 2>&1 | tail -2 | cut -c1-200
echo "--- and with reference_filename (Skill: the fix)"; sed "s#'input.bam', 'rb', check_sq=False#'$N/own_ctg.cram', 'rb', check_sq=False, reference_filename='$N/own_ctg.fa'#" $R/blocks/027_python.py > c2.py; grep -c reference_filename c2.py; timeout 60 python c2.py 2>&1 | tail -3
echo "--- qc_report on wrong reference, cache bypassed"; timeout 60 $Q $N/own_ctg.cram $N/wrong.fa 2>&1 | tail -3 | cut -c1-260; echo "rc=${PIPESTATUS[0]}"
echo "--- human CRAM (real, header UR points at a missing path): qc_report without / with reference"
CR=$AFDATA/human/test.paired_end.sorted.cram
timeout 60 $Q $CR 2>&1 | tail -1 | cut -c1-260; timeout 60 $Q $CR $AFDATA/human/genome.fasta 2>&1 | sed -n '3,6p'
echo "########## samtools stats -i behaviour: clamp or drop? own_insert: 300x10, 7000x3, 7999, 8000, 8001, 8500x2"
python - <<'PY'
t=[300]*10+[7000]*3+[7999,8000,8001]+[8500]*2
for i in (8000,7000,400):
    cl=sum(min(x,i) for x in t)/len(t); dr=[x for x in t if x<=i]
    print(f'-i {i}: predicted mean if CLAMPED {cl:.1f} | if DROPPED (<=i) {sum(dr)/len(dr):.1f}')
PY
for i in 8000 7000 400; do echo -n "samtools stats -i $i: "; samtools stats -i $i $N/own_insert.bam | grep -E '^SN\s+insert size average' | cut -f3; done
