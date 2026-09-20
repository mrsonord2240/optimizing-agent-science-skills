#!/bin/bash
# probe: does Skill's `foldseek easy-multimercluster *.pdb out tmp/ --multimer-tm-threshold 0.65` cluster all inputs?
source /mnt/openscience/audit-envs/alignment/wsl_env.sh
cd /mnt/openscience/audits/bio-alignment-structural/run/work/in5
run() { tag=$1; shift; rm -rf tmpx_$tag; foldseek easy-multimercluster "$@" mx_$tag tmpx_$tag -v 1 > mx_$tag.log 2>&1; echo "== $tag rc=$? clusters=$(cut -f1 mx_$tag_cluster.tsv 2>/dev/null | sort -u | wc -l) rows=$(wc -l < mx_${tag}_cluster.tsv 2>/dev/null)"; cat mx_${tag}_cluster.tsv 2>/dev/null | head -12; }
run oligos 1A3N.pdb 1HBA.pdb 1IRD.pdb --multimer-tm-threshold 0.65
run oligos_nothr 1A3N.pdb 1HBA.pdb 1IRD.pdb
run oligos_plus_mono 1A3N.pdb 1HBA.pdb 1IRD.pdb 1MBN.pdb 1ATP.pdb 1HCK.pdb 1DIW.pdb 2ITZ.pdb 2LHB.pdb --multimer-tm-threshold 0.65
# directory input instead of a file list
mkdir -p cdir; cp 1A3N.pdb 1HBA.pdb 1IRD.pdb 1MBN.pdb 1ATP.pdb 1HCK.pdb 2LHB.pdb cdir/
rm -rf tmpx_dir; foldseek easy-multimercluster cdir mx_dir tmpx_dir -v 1 > mx_dir.log 2>&1; echo "== directory input rc=$?"; cat mx_dir_cluster.tsv
echo "== plain easy-cluster with the same file list (monomer chains)"; ls mx_oligos.log >/dev/null
