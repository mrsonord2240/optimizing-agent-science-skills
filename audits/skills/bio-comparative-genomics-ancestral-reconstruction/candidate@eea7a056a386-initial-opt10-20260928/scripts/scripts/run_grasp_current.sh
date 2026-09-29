#!/usr/bin/env bash
set -uo pipefail
root=/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction
env="$root/conda-env"
jar="$root/sources/bnkit_java_19.jar"
run="$root/runs/grasp-current"
rm -rf "$run"; mkdir -p "$run/out"
cp "$root/data/cytochrome-c-aligned.fasta" "$run/alignment.fasta"
cp "$root/data/cytochrome-c-rooted.nwk" "$run/species.nwk"
(cd "$run" && "$env/bin/java" -jar "$jar" -a alignment.fasta -n species.nwk -o out -j -t 2 --save-as FASTA TREE ASR) > "$root/evidence/grasp-current.log" 2>&1
printf '%s\n' "$?" > "$root/evidence/grasp-current.exit-code"
find "$run/out" -maxdepth 1 -type f -printf '%f\t%s\n' | sort > "$root/evidence/grasp-current-outputs.tsv"
"$env/bin/python" - <<'PY' > "$root/evidence/grasp-current-validation.txt"
from Bio import AlignIO, Phylo
import json
from pathlib import Path
p=Path('/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction/runs/grasp-current/out')
a=AlignIO.read(p/'alignment_ancestors.fa','fasta')
assert len(a)==7 and a.get_alignment_length() >= 100
t=Phylo.read(p/'alignment_ancestors.nwk','newick')
assert len(t.get_terminals())==8 and t.count_terminals()==8
x=json.loads((p/'ASR.json').read_text())
assert isinstance(x,dict) and len(x)>0
print('ancestor_sequences',len(a),'alignment_columns',a.get_alignment_length(),'tree_tips',t.count_terminals(),'json_keys',','.join(x.keys()))
PY

# Exercise the candidate command against the official binary through the documented wrapper shape.
shim="$root/runs/grasp-shim"
rm -rf "$shim"; mkdir -p "$shim"
cat > "$shim/grasp" <<EOF
#!/usr/bin/env bash
exec "$env/bin/java" -jar "$jar" "\$@"
EOF
chmod +x "$shim/grasp"
candidate="$root/runs/grasp-candidate-with-current"
rm -rf "$candidate"; mkdir -p "$candidate"
cp "$root/data/cytochrome-c-aligned.fasta" "$candidate/alignment.fasta"
cp "$root/data/cytochrome-c-rooted.nwk" "$candidate/species.nwk"
(cd "$candidate" && PATH="$shim:$PATH" bash /mnt/openscience/wt/opt10-ancestral-reconstruction/skills/bio-comparative-genomics-ancestral-reconstruction/scripts/grasp_asr.sh) > "$root/evidence/grasp-candidate-current.log" 2>&1
printf '%s\n' "$?" > "$root/evidence/grasp-candidate-current.exit-code"

