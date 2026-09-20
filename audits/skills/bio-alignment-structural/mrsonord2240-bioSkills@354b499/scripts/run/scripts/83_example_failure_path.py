"""Failure path of examples/tm_align_pairwise.py: TM-align exits 0 with no data row for a too-short / ligand-only structure.
Also: max(TM1,TM2) on a SYNTHETIC 10-residue helix vs 1MBN. cwd = run/."""
import sys, os, shutil, subprocess
sys.dont_write_bytecode = True
sys.path.insert(0, 'skill/examples'); import tm_align_pairwise as t
w = 'work/err2'; shutil.rmtree(w, ignore_errors=True); os.makedirs(w)
shutil.copy('data/real_pdb/1MBN.pdb', w+'/reference.pdb'); shutil.copy('data/synthetic/ligand_only.pdb', w+'/mobile.pdb')
r = t.tm_align(w+'/reference.pdb', w+'/mobile.pdb')
print('tm_align() on ligand-only mobile returned:', r)
try:
    max(r['tm1'], r['tm2'])
except Exception as e:
    print('example __main__ next line would raise:', type(e).__name__, e)
assert r is None
h = t.parse_outfmt2(subprocess.run(['TMalign', 'data/synthetic/helix10.pdb', 'data/real_pdb/1MBN.pdb', '-outfmt', '2'], capture_output=True, text=True).stdout)
print('SYNTHETIC 10-res helix vs 1MBN:', h, '->', t.interpret_tmscore(max(h['tm1'], h['tm2'])))
