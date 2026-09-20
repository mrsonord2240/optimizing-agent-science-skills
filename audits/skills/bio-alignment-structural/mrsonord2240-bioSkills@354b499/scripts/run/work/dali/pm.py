from pymol import cmd
cmd.load('/mnt/openscience/audits/bio-alignment-structural/run/data/real_pdb/1MBN.pdb','ref')
cmd.load('/mnt/openscience/audits/bio-alignment-structural/run/data/real_pdb/1A3N.pdb','mob')
r = cmd.super('mob and chain A','ref')
print('PYMOL super  RMSD=%.3f n_atoms=%d' % (r[0], r[1]))
r = cmd.cealign('ref','mob and chain A')
print('PYMOL cealign RMSD=%.3f n_aligned=%d' % (r['RMSD'], r['alignment_length']))
