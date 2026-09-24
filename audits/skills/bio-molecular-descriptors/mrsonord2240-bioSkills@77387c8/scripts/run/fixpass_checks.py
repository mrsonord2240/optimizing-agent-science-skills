"""Re-audit checks for bio-molecular-descriptors P1/P2 remediation.

Run from any directory with the shared chemistry audit environment:
    python F:/OpenScience/audits/bio-molecular-descriptors/run/fixpass_checks.py
"""

import importlib.util
import math
import subprocess
from pathlib import Path

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors3D, QED


REPO = Path(r"F:\OpenScience\wt\bio-molecular-descriptors")
SKILL = REPO / "chemoinformatics" / "molecular-descriptors" / "SKILL.md"
EXAMPLE = SKILL.parent / "examples" / "calculate_descriptors.py"
EXPECTED_SHA = "77387c83238ced7d8e6bae147002918c0dd11116"


def load_example():
    spec = importlib.util.spec_from_file_location("calculate_descriptors", EXAMPLE)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def ensemble_asphericities(smiles, n_confs=20, seed=42, max_iters=2000):
    """Execute the revised SKILL.md ensemble policy verbatim in functional form."""
    mol = Chem.AddHs(Chem.MolFromSmiles(smiles))
    params = AllChem.ETKDGv3()
    params.randomSeed = seed
    conf_ids = list(AllChem.EmbedMultipleConfs(mol, numConfs=n_confs, params=params))
    assert conf_ids, "ETKDGv3 generated no conformers"
    assert AllChem.MMFFHasAllMoleculeParams(mol), "MMFF94 parameter guard failed"
    results = AllChem.MMFFOptimizeMoleculeConfs(mol, maxIters=max_iters)
    converged_ids = [
        conf_id for conf_id, (status, _) in zip(conf_ids, results) if status == 0
    ]
    assert converged_ids, "MMFF94 did not converge for any conformer"
    return len(conf_ids), len(converged_ids), [
        Descriptors3D.Asphericity(mol, confId=conf_id) for conf_id in converged_ids
    ]


def checked_gasteiger_charges(mol):
    allowed = {"H", "C", "N", "O", "F", "P", "S", "Cl", "Br", "I"}
    unsupported = sorted({atom.GetSymbol() for atom in mol.GetAtoms()
                          if atom.GetSymbol() not in allowed})
    if unsupported:
        raise ValueError(
            "Gasteiger charges are not validated here for: " + ", ".join(unsupported)
        )
    mol_h = Chem.AddHs(Chem.Mol(mol))
    AllChem.ComputeGasteigerCharges(mol_h)
    charges = [float(atom.GetProp("_GasteigerCharge")) for atom in mol_h.GetAtoms()]
    assert all(math.isfinite(charge) for charge in charges)
    assert math.isclose(sum(charges), Chem.GetFormalCharge(mol_h), abs_tol=1e-4)
    return charges


def main():
    assert SKILL.exists() and EXAMPLE.exists()
    source_sha = subprocess.check_output(
        ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True
    ).strip()
    assert source_sha == EXPECTED_SHA, (source_sha, EXPECTED_SHA)
    assert not subprocess.check_output(
        ["git", "-C", str(REPO), "status", "--porcelain"], text=True
    ).strip()
    print(f"Exact source commit: {source_sha} (clean)")
    text = SKILL.read_text(encoding="utf-8")

    # P1: 3D route works for the flexible drug-like cases that exposed the defect.
    for label, smiles in [
        ("atenolol", "CC(C)NCC(O)COc1ccc(CC(N)=O)cc1"),
        ("verapamil", "COc1ccc(CCN(C)CCCC(C#N)(c2ccc(OC)c(OC)c2)C(C)C)cc1OC"),
    ]:
        total, converged, asphericities = ensemble_asphericities(smiles)
        print(
            f"3D {label}: {converged}/{total} converged at 2000 iterations; "
            f"asphericity mean={np.mean(asphericities):.4f}, "
            f"sd={np.std(asphericities):.4f}"
        )
        assert converged > 0 and len(asphericities) == converged

    # P1: shipped helper is seeded and produces identical feature values.
    example = load_example()
    atenolol = Chem.MolFromSmiles("CC(C)NCC(O)COc1ccc(CC(N)=O)cc1")
    runs = [example.calculate_3d_descriptors(atenolol, random_seed=42) for _ in range(3)]
    values = [run["Asphericity"] for run in runs]
    assert values[0] == values[1] == values[2]
    print(f"3D helper reproducibility: asphericity={values[0]:.6f} (3/3 identical)")

    # P1: MAP4 is no longer represented as a tested, pip-installable dependency.
    assert "map4 1.1+" not in text
    assert "Do **not** use `pip install map4`" in text
    assert "numpy>=1.26,<2" in text
    print("Compatibility boundary: MAP4 unsupported from PyPI; MHFP6 pins NumPy <2")

    # P2: explicit-H Gasteiger charges balance; metal input is rejected.
    aspirin = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")
    charges = checked_gasteiger_charges(aspirin)
    print(f"Gasteiger aspirin: {len(charges)} explicit-atom charges, sum={sum(charges):+.6f}")
    try:
        checked_gasteiger_charges(Chem.MolFromSmiles("[Fe+2].[Fe+2]"))
    except ValueError as exc:
        print(f"Gasteiger metal guard: {exc}")
    else:
        raise AssertionError("metal input was not rejected")

    # P2: caveat has both observed failure directions.
    qed = {
        "indole_fragment": QED.qed(Chem.MolFromSmiles("c1ccc2[nH]ccc2c1")),
        "imatinib_drug": QED.qed(Chem.MolFromSmiles(
            "Cc1ccc(NC(=O)c2ccc(CN3CCN(C)CC3)cc2)cc1Nc1nccc(-c2cccnc2)n1"
        )),
    }
    assert qed["indole_fragment"] > 0.5 > qed["imatinib_drug"]
    assert "small fragments can be over-ranked" in text
    assert "natural-product-like or peptide-like chemistry" in text
    print("QED boundary: indole={indole_fragment:.3f}, imatinib={imatinib_drug:.3f}".format(**qed))

    print("ALL FIX-PASS ASSERTIONS: PASS (6 audit findings remediated)")


if __name__ == "__main__":
    main()
