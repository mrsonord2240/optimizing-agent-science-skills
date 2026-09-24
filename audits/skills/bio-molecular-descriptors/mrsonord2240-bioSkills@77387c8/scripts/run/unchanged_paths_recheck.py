"""Recheck the unchanged 2D and library-scale paths against the original hERG fixture."""

import time
from pathlib import Path

import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem import Descriptors, Lipinski, QED, rdFingerprintGenerator


SOURCE = Path(
    r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data"
    r"\chembl_herg_CHEMBL240_ic50.csv"
)


def physchem(mol):
    return {
        "MolWt": Descriptors.MolWt(mol),
        "MolLogP": Descriptors.MolLogP(mol),
        "HBD": Lipinski.NumHDonors(mol),
        "HBA": Lipinski.NumHAcceptors(mol),
        "TPSA": Descriptors.TPSA(mol),
        "RotBonds": Lipinski.NumRotatableBonds(mol),
        "AromRings": Lipinski.NumAromaticRings(mol),
        "FractionCSP3": Descriptors.FractionCSP3(mol),
        "QED": QED.qed(mol),
    }


def main():
    frame = pd.read_csv(SOURCE).dropna(subset=["canonical_smiles"])
    frame = frame.drop_duplicates("molecule_chembl_id")
    mols = [Chem.MolFromSmiles(smiles) for smiles in frame.canonical_smiles]
    mols = [mol for mol in mols if mol is not None]
    assert len(mols) == 3224

    panel = pd.DataFrame(physchem(mol) for mol in mols[:1000])
    assert panel.shape == (1000, 9)
    assert np.isfinite(panel.to_numpy(dtype=float)).all()
    print("Physchem panel: 9 descriptors x 1000; no NaN/inf")

    atenolol = Chem.MolFromSmiles("CC(C)NCC(O)COc1ccc(CC(N)=O)cc1")
    generators = {
        "ECFP4": rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048),
        "ECFP6": rdFingerprintGenerator.GetMorganGenerator(radius=3, fpSize=2048),
        "FCFP4": rdFingerprintGenerator.GetMorganGenerator(
            radius=2,
            fpSize=2048,
            atomInvariantsGenerator=rdFingerprintGenerator.GetMorganFeatureAtomInvGen(),
        ),
        "RDKitFP": rdFingerprintGenerator.GetRDKitFPGenerator(fpSize=2048),
        "AtomPair": rdFingerprintGenerator.GetAtomPairGenerator(fpSize=2048),
        "TopTorsion": rdFingerprintGenerator.GetTopologicalTorsionGenerator(fpSize=2048),
    }
    assert all(generator.GetFingerprint(atenolol).GetNumBits() == 2048
               for generator in generators.values())
    assert (generators["ECFP4"].GetFingerprint(atenolol) !=
            generators["FCFP4"].GetFingerprint(atenolol))
    print("2D taxonomy: six RDKit generators construct; FCFP4 differs from ECFP4")

    losses = []
    for bits in (512, 1024, 2048, 4096, 8192):
        generator = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=bits)
        folded = np.mean([generator.GetFingerprint(mol).GetNumOnBits() for mol in mols[:500]])
        sparse = np.mean([len(generator.GetSparseCountFingerprint(mol).GetNonzeroElements())
                          for mol in mols[:500]])
        losses.append(100 * (1 - folded / sparse))
    assert all(left > right for left, right in zip(losses, losses[1:]))
    print("Collision loss (%): " + ", ".join(f"{loss:.2f}" for loss in losses))

    generator = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    started = time.monotonic()
    matrix = np.zeros((len(mols), 2048), dtype=np.uint8)
    for index, mol in enumerate(mols):
        DataStructs.ConvertToNumpyArray(generator.GetFingerprint(mol), matrix[index])
    elapsed = time.monotonic() - started
    assert matrix.shape == (3224, 2048)
    assert (matrix.sum(axis=0) == 0).sum() < 50
    print(f"Library ECFP4: {matrix.shape}, {matrix.nbytes / 1e6:.1f} MB, "
          f"{len(mols) / elapsed:.0f} mol/s, {(matrix.sum(axis=0) == 0).sum()} dead bits")
    print("ALL UNCHANGED-PATH ASSERTIONS: PASS")


if __name__ == "__main__":
    main()
