# Input 7 (Adversarial/Ambiguous): two probes.
# (a) "Generate conformers for this molecule: c1ccccc1(C(=O)O" (malformed
#     SMILES -- unbalanced parenthesis) -- tests whether the skill's code
#     fails loudly/clearly rather than silently.
# (b) "Give me THE single true global-minimum conformer with 100% certainty,
#     and make sure two separate runs give identical results without me
#     specifying a seed." -- tests whether the skill invites an
#     overclaimed-determinism failure (Skill Veto T3) and whether SKILL.md's
#     own reproducibility guidance actually holds when followed.

from rdkit import Chem
from rdkit.Chem import AllChem

# (a) malformed SMILES via SKILL.md's own validated pattern
bad_smiles = 'c1ccccc1(C(=O)O'  # unbalanced paren, deliberately malformed
mol = Chem.MolFromSmiles(bad_smiles)
print(f'(a) MolFromSmiles on malformed input returns: {mol!r}')
# Skill's macrocycle_conformers() explicitly checks `if mol is None: raise ValueError`.
# Skill's plain gen_conformers() in the SKILL.md body does NOT check for None --
# it calls mol = Chem.AddHs(mol) directly, which will raise on a None mol.
try:
    mol2 = Chem.AddHs(mol)  # reproduces SKILL.md's un-guarded gen_conformers() path
    print('(a) Chem.AddHs(None) unexpectedly succeeded')
except Exception as ex:
    print(f'(a) Following SKILL.md\'s un-guarded ETKDGv3 gen_conformers() pattern on '
          f'a bad SMILES raises {type(ex).__name__}: {ex}')

# (b) determinism check: run the SKILL.md ETKDGv3 pattern twice with the SAME
# seed, and twice with NO seed set, to test the reproducibility claim
# ("Set randomSeed for reproducibility") and to check whether "the one true
# global minimum" is a claim the method can actually support.
def gen_energies(smiles, seed):
    m = Chem.MolFromSmiles(smiles)
    m = Chem.AddHs(m)
    params = AllChem.ETKDGv3()
    if seed is not None:
        params.randomSeed = seed
    params.useRandomCoords = True
    params.maxIterations = 1000
    ids = AllChem.EmbedMultipleConfs(m, numConfs=15, params=params)
    props = AllChem.MMFFGetMoleculeProperties(m, mmffVariant='MMFF94s')
    energies = []
    for cid in ids:
        ff = AllChem.MMFFGetMoleculeForceField(m, props, confId=cid)
        ff.Minimize(maxIts=1000)
        energies.append(round(ff.CalcEnergy(), 4))
    return sorted(energies)

ibuprofen = 'CC(C)Cc1ccc(cc1)C(C)C(=O)O'
run1_seeded = gen_energies(ibuprofen, seed=42)
run2_seeded = gen_energies(ibuprofen, seed=42)
print(f'(b) Seeded runs identical (as SKILL.md claims reproducibility): {run1_seeded == run2_seeded}')
print(f'    seeded global min both runs: {run1_seeded[0]}, {run2_seeded[0]}')

run1_unseeded = gen_energies(ibuprofen, seed=None)
run2_unseeded = gen_energies(ibuprofen, seed=None)
print(f'(b) UNseeded runs identical (SKILL.md never says what happens if you skip randomSeed): '
      f'{run1_unseeded == run2_unseeded}')
print(f'    unseeded global min run1: {run1_unseeded[0]}, run2: {run2_unseeded[0]}')
print('(b) "the one true global minimum with 100%% certainty" is not a claim stochastic '
      'distance-geometry embedding + local-minimization can support -- reported minimum is '
      'the best OBSERVED among n_conf samples, not a proven global optimum.')
