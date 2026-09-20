#!/bin/bash
# The Skill's "Contamination and Sample Swap" block, run on the re-auditor's OWN 60-site synthetic data (make_fp_fixtures.py).
# SYNTHETIC: two 'individuals' differ only at the 60 planted sites.  Asserts on the printed RESULT/LOD and on exit codes.
RUN=/mnt/openscience/audits/bio-alignment-validation/run
PD=/mnt/openscience/audit-envs/alignment-files/public-data
F=$RUN/data/fp; W=$RUN/out/work_fp; rm -rf $W; mkdir -p $W; cd $W
REF=$PD/human/genome.fasta
A() { if [ "$2" = "1" ]; then echo "  ASSERT PASS: $1"; else echo "  ASSERT FAIL: $1"; fi; }
# SKILL.md command, verbatim except file names (the block is `picard CrosscheckFingerprints I=tumor.bam I=normal.bam HAPLOTYPE_MAP=... LOD_THRESHOLD=-5 OUTPUT=crosscheck.metrics`)
cc() { # label bam1 bam2 expected_rc expected_result extra-args
  local lab="$1" b1=$2 b2=$3 erc=$4 eres=$5; shift 5
  rm -f $W/cc.metrics
  picard CrosscheckFingerprints I=$F/$b1 I=$F/$b2 HAPLOTYPE_MAP=$F/hap.txt LOD_THRESHOLD=-5 OUTPUT=$W/cc.metrics "$@" > $W/cc.log 2>&1; rc=$?
  read R L < <(python $RUN/scripts/cc_parse.py $W/cc.metrics 2>/dev/null || echo "NONE NA")
  echo "  [$lab] rc=$rc RESULT=$R LOD_SCORE=$L ($(grep -v '^#' $W/cc.metrics | awk -F'	' 'NR>1{printf "%s|%s|%s; ", $1,$2,$3}' | cut -c1-200)) $(grep -E 'Exception|Caused' $W/cc.log | head -1 | cut -c1-140)"
  A "$lab -> rc $erc, RESULT $eres" "$([ "$rc" = "$erc" ] && [ "$R" = "$eres" ] && echo 1)"
}
echo "== Picard CrosscheckFingerprints (SKILL block), LOD_THRESHOLD=-5"
cc "A vs A2, different SM (same reads)     [default: different samples expected to differ]" A.bam A2.bam 1 UNEXPECTED_MATCH
cc "A vs A2, EXPECT_ALL_GROUPS_TO_MATCH=true" A.bam A2.bam 0 EXPECTED_MATCH EXPECT_ALL_GROUPS_TO_MATCH=true
cc "A vs B, different SM (different individuals)" A.bam B.bam 0 EXPECTED_MISMATCH
cc "A vs B, EXPECT_ALL_GROUPS_TO_MATCH=true (a real tumor/normal swap)" A.bam B.bam 1 UNEXPECTED_MISMATCH EXPECT_ALL_GROUPS_TO_MATCH=true
cc "A vs A_sameSM_as_B (both SM=IND_B? no: A is IND_A) same reads, other name" A.bam A_sameSM_as_B.bam 1 UNEXPECTED_MATCH
cc "B vs A_sameSM_as_B, same SM=IND_B but different genotypes (the SKILL 'give both BAMs the same SM' case)" B.bam A_sameSM_as_B.bam 1 UNEXPECTED_MISMATCH
cc "A vs H (all-het individual, different SM)  [informational: shares only the het third of the sites]" A.bam H.bam 0 EXPECTED_MISMATCH
cc "A vs L (3 reads, same SM IND_A)  [SKILL: between -5 and 5 = ambiguous]" A.bam L.bam 0 INCONCLUSIVE
echo "  (metrics file of the last run:)"; grep -v '^#' $W/cc.metrics | cut -f1-9 | head -3
echo "== NEW: read-group collision. Both BAMs keep the nf-core read group (ID:1 PU:1 LB:testN) (SM differs: IND_A vs IND_B, genotypes differ at 60 sites)"
cc "A_rg1 vs B_rg1 (RG ID 1 in both), the SKILL command as written" A_rg1.bam B_rg1.bam 0 EXPECTED_MISMATCH
cc "A_rg1 vs B_rg1 with EXPECT_ALL_GROUPS_TO_MATCH=true (a true swap must exit 1)" A_rg1.bam B_rg1.bam 1 UNEXPECTED_MISMATCH EXPECT_ALL_GROUPS_TO_MATCH=true
cc "A_rg1 vs B_rg1 with CROSSCHECK_BY=FILE" A_rg1.bam B_rg1.bam 0 EXPECTED_MISMATCH CROSSCHECK_BY=FILE
cc "A_rg1 vs B_rg1 with CROSSCHECK_BY=FILE EXPECT_ALL_GROUPS_TO_MATCH=true" A_rg1.bam B_rg1.bam 1 UNEXPECTED_MISMATCH CROSSCHECK_BY=FILE EXPECT_ALL_GROUPS_TO_MATCH=true
cc "A_rg1 vs B_rg1 with CROSSCHECK_BY=SAMPLE" A_rg1.bam B_rg1.bam 0 EXPECTED_MISMATCH CROSSCHECK_BY=SAMPLE
cc "A_rg1 vs B_rg1 with CROSSCHECK_BY=SAMPLE EXPECT_ALL_GROUPS_TO_MATCH=true" A_rg1.bam B_rg1.bam 1 UNEXPECTED_MISMATCH CROSSCHECK_BY=SAMPLE EXPECT_ALL_GROUPS_TO_MATCH=true
grep -v '^#' $W/cc.metrics | cut -f1-8 | head -3
echo "== the Skill's comment 'LOD > 5 = same individual; < -5 = different' -- LOD values seen above; also Picard's own text:"
picard CrosscheckFingerprints -h 2>&1 | grep -i -m2 'LOD_THRESHOLD\|lod score' | cut -c1-220

echo "== somalier (SKILL block: extract -d -s -f, relate --infer), sites = my 60-site VCF"
mkdir -p ext; rm -f ext/*
for b in A A2 B H; do somalier extract -d ext/ -s $F/sites.vcf.gz -f $REF $F/$b.bam > sx_$b.log 2>&1; echo "  extract $b rc=$? $(grep -c . sx_$b.log) log lines; $(tail -1 sx_$b.log | cut -c1-110)"; done
ls ext | tr '\n' ' '; echo
somalier relate --infer ext/*.somalier -o rel > rel.log 2>&1; echo "  relate rc=$?"; tail -3 rel.log | cut -c1-150
echo "  --- pairs.tsv (relatedness, ibs0, ibs2, n):"; cut -f1-9 rel.pairs.tsv | head -8
echo "  --- samples.tsv:"; cut -f1-8 rel.samples.tsv | head -6
python - <<'PY'
rows=[l.rstrip("\n").split("\t") for l in open("rel.pairs.tsv")]
h=rows[0]; ix={k:i for i,k in enumerate(h)}
d={(r[ix["#sample_a"]] ,r[ix["sample_b"]]):float(r[ix["relatedness"]]) for r in rows[1:]}
print("  pairs:",d)
a=[v for k,v in d.items() if set(k)=={"IND_A","IND_A2"}]
b=[v for k,v in d.items() if set(k)=={"IND_A","IND_B"}]
print("  ASSERT", "PASS" if a and a[0]>0.95 else "FAIL", ": A vs A2 (same reads) relatedness ~1")
print("  ASSERT", "PASS" if b and b[0]<0.2 else "FAIL", ": A vs B (different genotypes) relatedness low / negative")
PY

echo "== VerifyBamID2 (SKILL block), prefix with .dat vs without, on the real 1000G chr20 slice"
G=$PD/1000g
for pre in $PD/resources/1000g.phase3.10k.b38.vcf.gz.dat $PD/resources/1000g.phase3.10k.b38.vcf.gz; do
  verifybamid2 --SVDPrefix $pre --Reference $G/chr20_padded_1500000.fa --BamFile $G/HG00349.chr20_1400000-1500000.bam --Output $W/vb > vb.log 2>&1; echo "  prefix ...$(basename $pre): rc=$? | $(grep -a -m2 -E 'Insufficient|failed|Available|markers|FREEMIX' vb.log | tr '\n' '/' | cut -c1-200)"; done
ls $W/vb* 2>/dev/null | head -3
echo "== done"
