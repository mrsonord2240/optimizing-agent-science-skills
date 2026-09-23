#!/usr/bin/env bash
# Phase-2 new inputs: multi-run pooling and independently documented MS-GF+.
set -euo pipefail
ROOT='F:/OpenScience/audits/bio-proteomics-peptide-identification'
ENV='F:/OpenScience/audit-envs/mass-spec-proteomics-analyst'
SKILL="$ROOT/run/skill"
export DECOYDB="$ENV/tools/openms/bin/DecoyDatabase.exe"
export SAGE="$ENV/tools/sage/sage-v0.14.7-x86_64-pc-windows-msvc/sage.exe"
export PERCOLATOR="$ENV/tools/percolator/percolator.exe"
export FASTA="$ENV/public-data/PXD070049/fasta/uniprotkb_proteome_HYE_UniversalContaminants.fasta"
MZML_A="$ENV/public-work/mzml/dda/LFQ_Astral_DDA_5min_250pg_Condition_A_REP1.mzML"
MZML_B="$ENV/public-work/mzml/dda/LFQ_Astral_DDA_5min_250pg_Condition_B_REP1.mzML"
MZML_C="$ENV/public-work/mzml/dda/LFQ_Astral_DDA_5min_250pg_Condition_C_REP1.mzML"

echo 'INPUT 11 (new): three-run Sage pooling through the shipped example'
MZML="$MZML_A $MZML_B $MZML_C" FASTA="$FASTA" OUT="$ROOT/run/input11_pool" ENGINE=sage THREADS=8 bash "$SKILL/examples/dda_search.sh"
python - "$ROOT/run/input11_pool" <<'PY'
import sys
import pandas as pd
def percolator(path):
    rows=[x.rstrip('\n').split('\t') for x in open(path, encoding='utf-8')]
    header, n=rows[0], len(rows[0])
    body=[r[:n-1]+[';'.join(r[n-1:])] for r in rows[1:]]
    return pd.DataFrame(body, columns=header).astype({'q-value':float})
p=sys.argv[1]
psm=percolator(p+'/psms.target.tsv')
pep=percolator(p+'/peptides.target.tsv')
assert (psm['q-value']<=.01).sum()==5006
assert (pep['q-value']<=.01).sum()==2760
print('ASSERT input11: pooled PSMs=5006, peptides=2760')
PY

echo 'INPUT 12 (new): documented MS-GF+ command on public DDA data'
OUT="$ROOT/run/input12_msgf"
mkdir -p "$OUT"
cat > "$OUT/mods.txt" <<'EOF'
NumMods=2
C2H3N1O1,C,fix,any,Carbamidomethyl
O1,M,opt,any,Oxidation
EOF
"$ENV/tools/openms/bin/DecoyDatabase.exe" -in "$FASTA" -out "$OUT/target_decoy.fasta" -decoy_string DECOY_ -decoy_string_position prefix -method reverse -enzyme Trypsin -threads 8
java -Xmx8g -jar "$ENV/tools/msgfplus/MSGFPlus.jar" -s "$MZML_A" -d "$OUT/target_decoy.fasta" -decoy DECOY_ -o "$OUT/sample.mzid" -t 10ppm -ti 0,1 -tda 0 -m 3 -inst 3 -e 1 -ntt 2 -mod "$OUT/mods.txt" -minLength 7 -maxLength 30 -maxMissedCleavages 2 -n 1 -addFeatures 1 -thread 8
java -cp "$ENV/tools/msgfplus/MSGFPlus.jar" edu.ucsd.msjava.ui.MzIDToTsv -i "$OUT/sample.mzid" -o "$OUT/sample.tsv" -showDecoy 1
python - "$OUT/sample.tsv" <<'PY'
import sys
import pandas as pd
x=pd.read_csv(sys.argv[1], sep='\t')
assert len(x)==6806, len(x)
assert x['SpecEValue'].notna().all()
print('ASSERT input12: MS-GF+ rank-1 rows=6806 and SpecEValue populated')
PY
