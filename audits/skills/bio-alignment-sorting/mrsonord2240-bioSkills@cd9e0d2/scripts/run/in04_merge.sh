#!/bin/bash
# INPUT 4 (variant B, REGRESSION of first audit input 4 against the fixed SKILL): "Merge these per-lane BAMs. Check they are
#   consistently sorted first, dedup @RG/@PG, then merge a region. Also merge the name-sorted versions."
#   Real (human PE + planted dups, 1000G) + synthetic RG-collision BAMs.  NOTE names -n/-N are always distinct (case-insensitive fs).
source /mnt/openscience/audits/bio-alignment-sorting/run/common.sh
W=$WORK/in4; rm -rf $W; mkdir -p $W; cd $W
H=$PD/human/test.paired_end.sorted.bam; P=$PD/derived/planted_dups.bam
cp $H h.bam; cp $H.bai h.bam.bai; cp $P p.bam; cp $P.bai p.bam.bai

echo "### 4.1 SKILL: verify sort-order consistency loop (verbatim) - consistent set, mixed coord/name set, mixed -n/-N set"
mkdir -p ok mix mixnN; cp h.bam p.bam ok/; cp h.bam mix/; samtools sort -n -o mix/nm.bam p.bam
samtools sort -n -o mixnN/a_nat.bam h.bam; samtools sort -N -o mixnN/b_asc.bam p.bam
cat > loop.sh <<'EOP'
#!/bin/bash
cd "$1"
for f in *.bam; do samtools view -H "$f" | head -1; done | sort -u
EOP
echo "-- consistent dir:"; bash loop.sh ok | tee ok.out
eq "consistent set prints exactly ONE line" "$(wc -l < ok.out)" "1"
echo "-- mixed coord/name dir:"; bash loop.sh mix | tee mix.out
eq "mixed set prints 2 lines" "$(wc -l < mix.out)" "2"
echo "-- SKILL comment: '-n and -N inputs print different SS: lines; do not mix them':"; bash loop.sh mixnN | tee mixnN.out
eq "-n + -N inputs print 2 lines" "$(wc -l < mixnN.out)" "2"

echo "### 4.2 SKILL 'Merge (dedup identical @RG and @PG)' samtools merge -c -p -@ 8 (real, identical @RG @SQ)"
samtools merge -c -p -@ 8 merged.bam h.bam p.bam; echo "rc=$?"
eq "merged record count = 5644+500" "$(nrec merged.bam)" "6144"
eq "merged @HD SO" "$(so merged.bam | grep -o 'SO:[a-z]*')" "SO:coordinate"
python $RUN/order_check.py merged.bam | grep -a n=
echo "  @RG lines: $(samtools view -H merged.bam | grep -ac '^@RG')   @PG lines: $(samtools view -H merged.bam | grep -ac '^@PG')"
samtools merge -@ 4 merged_nocp.bam h.bam p.bam
echo "-- without -c -p:  @RG=$(samtools view -H merged_nocp.bam | grep -ac '^@RG') @PG=$(samtools view -H merged_nocp.bam | grep -ac '^@PG')"

echo "### 4.3 RG-ID collision, DIFFERENT read groups (SYNTHETIC rgcollide_A/B: same ID L1, sampleA/lane1 vs sampleB/lane7) - SKILL '-c warning first'"
samtools view -H $DATA/rgcollide_A.bam | grep -a '^@RG'; samtools view -H $DATA/rgcollide_B.bam | grep -a '^@RG'
samtools merge -c -p -f rgc_cp.bam $DATA/rgcollide_A.bam $DATA/rgcollide_B.bam
samtools merge -f rgc_plain.bam $DATA/rgcollide_A.bam $DATA/rgcollide_B.bam
echo "-- with -c -p:"; samtools view -H rgc_cp.bam | grep -a '^@RG'
eq "-c collapses two DIFFERENT read groups into ONE header line (SKILL warning true)" "$(samtools view -H rgc_cp.bam | grep -ac '^@RG')" "1"
echo "   B-reads now labelled: $(samtools view rgc_cp.bam | grep -a '^B_' | grep -ao 'RG:Z:[^[:space:]]*' | sort -u) ; header SM kept: $(samtools view -H rgc_cp.bam | grep -a '^@RG' | grep -o 'SM:[^[:space:]]*')"
echo "-- without -c:"; samtools view -H rgc_plain.bam | grep -a '^@RG'
echo "-- SKILL remedy: make IDs unique upstream with samtools addreplacerg, then merge -c -p"
samtools addreplacerg -r '@RG\tID:L1B\tSM:sampleB\tPL:ILLUMINA\tPU:lane7' -m overwrite_all -o B_fixed.bam $DATA/rgcollide_B.bam; echo "addreplacerg rc=$?"
samtools merge -c -p -f rgc_fixed.bam $DATA/rgcollide_A.bam B_fixed.bam
eq "after addreplacerg: two distinct @RG survive -c -p" "$(samtools view -H rgc_fixed.bam | grep -ac '^@RG')" "2"
eq "A reads keep L1, B reads carry L1B" "$(samtools view rgc_fixed.bam | grep -a '^B_0' | grep -ao 'RG:Z:[^[:space:]]*')" "RG:Z:L1B"

echo "### 4.4 SKILL claim: merge does NOT validate sort order; mismatched inputs silently produce a malformed output (exit 0, header SO:coordinate, records out of order)"
samtools merge -f mixed.bam h.bam mix/nm.bam 2> mixed.err; echo "rc=$? stderr: $(head -2 mixed.err | tr '\n' '|')"
echo "  output header: $(so mixed.bam)"; python $RUN/order_check.py mixed.bam | grep -a n=
python $RUN/order_check.py mixed.bam | grep -q 'coordinate_sorted=True' && echo "  [FAIL] output is coordinate sorted" || echo "  [PASS] SKILL claim confirmed: exit 0, header SO:coordinate, records NOT sorted"
samtools index mixed.bam 2>&1 | head -1

echo "### 4.5 SKILL 'Merge Name-sorted Inputs': merge -n / -N; plain merge does not give name order"
samtools sort -n -o n1_nat.bam h.bam; samtools sort -n -o n2_nat.bam p.bam
samtools sort -N -o n1_asc.bam h.bam; samtools sort -N -o n2_asc.bam p.bam
samtools merge -f nm_plain.bam n1_nat.bam n2_nat.bam; echo "  plain merge of two -n BAMs rc=$?, header: $(so nm_plain.bam)"
python $RUN/order_check.py nm_plain.bam | grep -a n=
samtools merge -f -n nm_nat.bam n1_nat.bam n2_nat.bam; echo "  merge -n rc=$?, header: $(so nm_nat.bam)"
python $RUN/order_check.py nm_nat.bam | grep -a n=
python $RUN/order_check.py nm_nat.bam | grep -q 'qname_natural=True' && echo "  [PASS] merge -n of -n inputs: natural name order" || echo "  [FAIL] merge -n"
samtools merge -f -N nm_asc.bam n1_asc.bam n2_asc.bam; echo "  merge -N rc=$?, header: $(so nm_asc.bam)"
python $RUN/order_check.py nm_asc.bam | grep -a n=
python $RUN/order_check.py nm_asc.bam | grep -q 'qname_ascii=True' && echo "  [PASS] merge -N of -N inputs: ASCII name order" || echo "  [FAIL] merge -N"
echo "  SKILL syntax used: samtools merge -n -o merged_n.bam a_n.bam b_n.bam  (output given via -o, verbatim form):"
samtools merge -n -o merged_nat_o.bam n1_nat.bam n2_nat.bam; echo "  rc=$? n=$(nrec merged_nat_o.bam)"
samtools merge -N -o merged_asc_o.bam n1_asc.bam n2_asc.bam; echo "  rc=$? n=$(nrec merged_asc_o.bam)"
python $RUN/order_check.py nm_plain.bam | grep -q 'qname_natural=True' && echo "  [INFO] plain merge happened to be natural-ordered" || echo "  [INFO] plain merge (no -n) of name-sorted inputs is not name-ordered (SKILL: 'a plain merge does not give name order') - confirmed"
echo "-- Picard on merge -N output (ASCII merge feeds a Picard step):"
picard ValidateSamFile -I nm_asc.bam --MODE SUMMARY > v_mn.txt 2>&1; picard ValidateSamFile -I $P --MODE SUMMARY > v_p.txt 2>&1
grep -a -q 'RECORD_OUT_OF_ORDER' v_mn.txt && echo "  [FAIL] Picard RECORD_OUT_OF_ORDER on merge -N output" || echo "  [PASS] Picard: no RECORD_OUT_OF_ORDER on merge -N output"
echo "  (other Picard ERRORs on merged output come from the planted input itself: input alone gives: $(grep -a '^ERROR' v_p.txt | tr '
' ' '))"
picard ValidateSamFile -I nm_nat.bam --MODE SUMMARY > v_mnat.txt 2>&1; grep -a -q 'RECORD_OUT_OF_ORDER' v_mnat.txt && echo "  [PASS] Picard flags RECORD_OUT_OF_ORDER on merge -n output (as the -n/-N rule predicts)" || echo "  [FAIL] Picard did not flag merge -n"

echo "### 4.6 -b file list; -f overwrite; -R region (SKILL)"
printf 'h.bam\np.bam\n' > files.txt
samtools merge -b files.txt -f merged_b.bam; echo "-b rc=$? records=$(nrec merged_b.bam)"
eq "-b equals positional merge (cols 1-11, RG suffix excluded)" "$(samtools view merged_b.bam | cut -f1-11 | md5sum)" "$(samtools view merged_nocp.bam | cut -f1-11 | md5sum)"
samtools merge -f -s 7 rep3.bam h.bam p.bam; samtools merge -f -s 7 rep4.bam h.bam p.bam
eq "merge -s 7 is reproducible" "$(samtools view rep3.bam | md5sum)" "$(samtools view rep4.bam | md5sum)"
samtools merge merged_b.bam h.bam p.bam 2> nof.err; echo "  no -f onto existing file rc=$? msg: $(head -1 nof.err)"
samtools merge -f merged_region.bam -R chr22:2000-3000 h.bam p.bam; echo "-R (indexed inputs) rc=$?"
exp=$(( $(samtools view -c h.bam chr22:2000-3000) + $(samtools view -c p.bam chr22:2000-3000) ))
eq "merge -R chr22:2000-3000 count == sum of per-file region counts" "$(nrec merged_region.bam)" "$exp"
mkdir -p noidx; cp h.bam p.bam noidx/
samtools merge -f noidx/reg.bam -R chr22:2000-3000 noidx/h.bam noidx/p.bam 2> noidx.err; rc=$?; echo "  -R on UNINDEXED inputs rc=$rc msg: $(head -1 noidx.err)"
grep -a -q 'Could not retrieve index file' noidx.err && echo "  [PASS] SKILL comment quotes the real message" || echo "  [FAIL] message differs"

echo "### 4.7 pysam.merge (SKILL) == CLI; failure raises?"
cat > pymerge.py <<'EOP'
import pysam
pysam.merge('-c', '-p', '-f', 'py_merged.bam', 'h.bam', 'p.bam')
def recs(p):
    with pysam.AlignmentFile(p,'rb') as f: return [r.to_string() for r in f.fetch(until_eof=True)]
a, b = recs('py_merged.bam'), recs('merged.bam')
print('pysam.merge == CLI merge:', a == b, 'n=', len(a)); assert a == b and len(a) == 6144
try:
    pysam.merge('-f', 'x.bam', 'nope1.bam', 'nope2.bam')
    print('pysam.merge on missing inputs: NO EXCEPTION')
except Exception as e:
    print('pysam.merge on missing inputs raised', type(e).__name__, '|', str(e)[:90].replace('\n',' '))
EOP
python pymerge.py
summary
