#!/usr/bin/env bash
# Phase-2 regressions for prior real-data CLI inputs 8--10, from copied Skill.
set -euo pipefail
ROOT='F:/OpenScience/audits/bio-proteomics-peptide-identification'
ENV='F:/OpenScience/audit-envs/mass-spec-proteomics-analyst'
SKILL="$ROOT/run/skill"
export DECOYDB="$ENV/tools/openms/bin/DecoyDatabase.exe"
export SAGE="$ENV/tools/sage/sage-v0.14.7-x86_64-pc-windows-msvc/sage.exe"
export COMET="$ENV/tools/comet/comet.win64.exe"
export PERCOLATOR="$ENV/tools/percolator/percolator.exe"
export MZML_A="$ENV/public-work/mzml/dda/LFQ_Astral_DDA_5min_250pg_Condition_A_REP1.mzML"
export FASTA="$ENV/public-data/PXD070049/fasta/uniprotkb_proteome_HYE_UniversalContaminants.fasta"

echo 'INPUT 8: Sage + Percolator single-run route'
MZML="$MZML_A" FASTA="$FASTA" OUT="$ROOT/run/input8_sage" ENGINE=sage THREADS=8 bash "$SKILL/examples/dda_search.sh"
python - "$ROOT/run/input8_sage" <<'PY'
import sys
import pandas as pd
def percolator(path):
    rows=[x.rstrip('\n').split('\t') for x in open(path, encoding='utf-8')]
    header, n=rows[0], len(rows[0])
    body=[r[:n-1]+[';'.join(r[n-1:])] for r in rows[1:]]
    return pd.DataFrame(body, columns=header).astype({'q-value':float})
p=sys.argv[1]
s=pd.read_csv(p+'/sage/results.sage.tsv', sep='\t')
k=s[(s.label==1)&(s.spectrum_q<=.01)]
q=percolator(p+'/psms.target.tsv')
assert len(k)==1406, len(k)
assert (q['q-value']<=.01).sum()==1398
assert not q.iloc[:,-1].astype(str).str.contains('rev_').any()
print('ASSERT input8: Sage own=1406, Percolator=1398, no target result decoys')
PY

echo 'INPUT 9: Comet + Percolator single-run route'
MZML="$MZML_A" FASTA="$FASTA" OUT="$ROOT/run/input9_comet" ENGINE=comet THREADS=8 bash "$SKILL/examples/dda_search.sh"
python - "$ROOT/run/input9_comet" <<'PY'
import sys
import pandas as pd
def percolator(path):
    rows=[x.rstrip('\n').split('\t') for x in open(path, encoding='utf-8')]
    header, n=rows[0], len(rows[0])
    body=[r[:n-1]+[';'.join(r[n-1:])] for r in rows[1:]]
    return pd.DataFrame(body, columns=header).astype({'q-value':float})
p=sys.argv[1]
q=percolator(p+'/psms.target.tsv')
assert (q['q-value']<=.01).sum()==1144
assert (percolator(p+'/peptides.target.tsv')['q-value']<=.01).sum()==1138
print('ASSERT input9: Comet/Percolator PSMs=1144, peptides=1138')
PY

echo 'INPUT 10: adversarial decoy absence stops before Percolator'
mkdir -p "$ROOT/run/input10_tools"
cat > "$ROOT/run/input10_tools/no_decoy_database.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
in=''; out=''
while (($#)); do case "$1" in -in) in="$2"; shift 2;; -out) out="$2"; shift 2;; *) shift;; esac; done
cp "$in" "$out"
SH
chmod +x "$ROOT/run/input10_tools/no_decoy_database.sh"
set +e
MZML="$MZML_A" FASTA="$FASTA" OUT="$ROOT/run/input10_nodecoy" ENGINE=comet THREADS=8 DECOYDB="$ROOT/run/input10_tools/no_decoy_database.sh" bash "$SKILL/examples/dda_search.sh" > "$ROOT/run/input10.stdout" 2> "$ROOT/run/input10.stderr"
rc=$?
set -e
cat "$ROOT/run/input10.stdout"
cat "$ROOT/run/input10.stderr" >&2
test "$rc" -eq 1
grep -q 'no target or no decoy rows' "$ROOT/run/input10.stderr"
test ! -e "$ROOT/run/input10_nodecoy/psms.target.tsv"
echo 'ASSERT input10: missing decoys raised explicit error before Percolator output'
