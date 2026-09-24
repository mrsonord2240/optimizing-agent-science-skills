# Input 1b: the failure modes the fix claims to guard, all on the auditor's planted data (synthetic).
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-splicing-qc/run; D=$R/data/synthetic
mkdir -p $R/work/in1g; cd $R/work/in1g; cp -r $R/skill/examples .
H="asenv as-core python examples/splicing_qc.py"
echo "--- A. RSeQC without --skip-plot and Rscript absent (--rscript /nonexistent): does the literal tool still fail (the claim) ?"
junction_annotation.py -i $D/se_clean.bam -r $D/synth.bed12 -o a_bad --rscript /nonexistent 2>&1 | tail -2; echo "rc=${PIPESTATUS[0]}"
echo "--- A2. same with --skip-plot"
junction_annotation.py -i $D/se_clean.bam -r $D/synth.bed12 -o a_ok --rscript /nonexistent --skip-plot >/dev/null 2>&1; echo "rc=$?  xls lines: $(wc -l < a_ok.junction.xls)"
echo "--- A3. helper with PATH stripped of Rscript (plot=False default; also --plot with no Rscript on PATH)"
env PATH=$(echo $PATH | tr ':' '\n' | grep -v as-core | tr '\n' ':')$AS/tools/bin $H annotation $D/se_clean.bam $D/synth.bed12 a_h1 2>&1 | tail -1; echo rc=$?
echo "--- B. BED6 gene model"; $H annotation $D/se_clean.bam $D/synth.bed6 b6 2>&1 | tail -2; echo rc=$?
echo "--- C. contig mismatch (BED without chr)"; $H saturation $D/se_sat_mid.bam $D/synth_nochr.bed12 cm 2>&1 | tail -2; echo rc=$?
echo "--- C2. contig mismatch, literal RSeQC (the silent failure the Skill describes)"
junction_saturation.py -i $D/se_sat_mid.bam -r $D/synth_nochr.bed12 -o cm_lit --skip-plot >/dev/null 2>&1; echo rc=$?; grep -E '^(y|z|w)=' cm_lit.junctionSaturation_plot.r | cut -c1-100
echo "--- D. BAM with no spliced reads (planted 100M library built here)"
asenv as-core python - <<'PY'
import pysam
h = pysam.AlignmentHeader.from_dict({'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': 'chrS', 'LN': 700000}]})
with pysam.AlignmentFile('unspliced.bam', 'wb', header=h) as o:
    for i in range(200):
        r = pysam.AlignedSegment(h); r.query_name = f'u{i}'; r.reference_id = 0; r.reference_start = 5000 + i * 3
        r.mapping_quality = 60; r.cigarstring = '100M'; r.query_sequence = 'A' * 100; r.query_qualities = pysam.qualitystring_to_array('I' * 100); r.set_tag('NH', 1); o.write(r)
pysam.index('unspliced.bam'); print('wrote unspliced.bam')
PY
$H annotation unspliced.bam $D/synth.bed12 d1 2>&1 | tail -1; echo rc=$?
$H report unspliced.bam $D/synth.bed12 d2 2>&1 | tail -2; echo rc=$?
$H junctions unspliced.bam; echo rc=$?
echo "--- E. literal old snippet without strip vs new snippet on the same xls (prints)"
asenv as-core python - <<'PY'
import pandas as pd
j = pd.read_csv('a_ok.junction.xls', sep='\t'); print('raw annotation values:', sorted(j['annotation'].unique()))
PY
