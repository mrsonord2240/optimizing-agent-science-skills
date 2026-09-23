#!/bin/bash
# Re-audit: verify determinism of -method reverse/pseudo-reverse vs shuffle,
# and confirm -method shift still fails, on a FRESH TraML (2 peptides, distinct
# from the fixer's LGGNEQVTR/VEATFGVDESNAK set, built by reaudit_input4a_make_library_fresh_peptides.py).
OPENMS="/f/OpenScience/audit-envs/mass-spec-proteomics-analyst/tools/openms/bin"

# 1. TargetedFileConverter: convert real (Annotation + real fragment m/z) vs
#    placeholder (blank Annotation + fake round-number ProductMz) transition lists.
"$OPENMS/TargetedFileConverter.exe" -in reaudit_real_library_fresh_peptides.tsv -in_type tsv -out real3.TraML -out_type TraML
"$OPENMS/TargetedFileConverter.exe" -in reaudit_placeholder_library_fresh_peptides.tsv -in_type tsv -out placeholder3.TraML -out_type TraML

# 2. Decoy generation: placeholder must fail (0 decoys); real must succeed (2/2).
echo "=== placeholder (expect 0 decoys / threshold failure) ==="
"$OPENMS/OpenSwathDecoyGenerator.exe" -in placeholder3.TraML -out placeholder_decoy3.TraML -method pseudo-reverse
echo "=== real (expect success) ==="
"$OPENMS/OpenSwathDecoyGenerator.exe" -in real3.TraML -out real_decoy3.TraML -method pseudo-reverse

# 3. Determinism: 5 repeated runs each of reverse / pseudo-reverse / shuffle.
for method in reverse pseudo-reverse shuffle; do
  echo "=== method: $method (5 repeated runs, threads=1) ==="
  for i in 1 2 3 4 5; do
    "$OPENMS/OpenSwathDecoyGenerator.exe" -in real3.TraML -out "${method}_$i.TraML" -method "$method" -threads 1 >/dev/null 2>&1
  done
  md5sum "${method}_1.TraML" "${method}_2.TraML" "${method}_3.TraML" "${method}_4.TraML" "${method}_5.TraML"
done

# 4. -method shift: confirmed broken on this OpenMS 3.5.0 build (rejects every peptide as duplicate).
echo "=== method: shift (expect failure) ==="
"$OPENMS/OpenSwathDecoyGenerator.exe" -in real3.TraML -out shift_decoy.TraML -method shift
