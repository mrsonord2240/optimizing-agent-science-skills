# Probe: do the SMARTS in SKILL.md and in examples/substructure_search.py agree,
# and does the example's documented visualization path actually run?
from rdkit import Chem, RDLogger
RDLogger.DisableLog('rdApp.*')

PAIRS = [
    ('ester',  'SKILL.md', '[CX3](=O)[OX2][!H]', 'example', '[CX3](=O)[OX2][C]'),
    ('nitro',  'SKILL.md', '[N+](=O)[O-]',       'example', '[N+]([O-])=O'),
    ('amide',  'SKILL.md', '[CX3](=[OX1])[NX3]', 'example', '[CX3](=O)[NX3]'),
    ('sulfonamide', 'SKILL.md', '[SX4](=[OX1])(=[OX1])[NX3]', 'example', '[S](=O)(=O)[NX3]'),
]
CASES = ['CC(=O)OC', 'CC(=O)OCC', 'CC(=O)O', 'CC(=O)OC(C)C', 'CC(=O)Oc1ccccc1',
         'CC(=O)N', 'CC(=O)NC', 'C[N+](=O)[O-]', 'CS(=O)(=O)N', 'CC(=O)OC(F)(F)F']
for name, la, sa, lb, sb in PAIRS:
    pa, pb = Chem.MolFromSmarts(sa), Chem.MolFromSmarts(sb)
    diffs = []
    for smi in CASES:
        m = Chem.MolFromSmiles(smi)
        a, b = m.HasSubstructMatch(pa), m.HasSubstructMatch(pb)
        if a != b:
            diffs.append((smi, a, b))
    verdict = 'IDENTICAL on all probes' if not diffs else f'DIFFER on {len(diffs)}'
    print(f"{name:12} {la} {sa:32} vs {lb} {sb:26} -> {verdict}")
    for smi, a, b in diffs:
        print(f"              {smi:22} SKILL.md={a}  example={b}")

print("\nWhat does [!H] mean in '[CX3](=O)[OX2][!H]'?  ([!H] = NOT exactly-one-attached-H)")
for smi, note in [('CC(=O)OC', 'methyl ester, ester O-C has 3 H -> !H true'),
                  ('CC(=O)OC(C)C', 'isopropyl ester, that C has 1 H -> !H FALSE'),
                  ('CC(=O)OCC', 'ethyl ester, that C has 2 H -> !H true')]:
    m = Chem.MolFromSmiles(smi)
    print(f"  {smi:14} SKILL.md ester pattern matches: "
          f"{m.HasSubstructMatch(Chem.MolFromSmarts('[CX3](=O)[OX2][!H]'))}   ({note})")

print("\nDoes the example's draw_with_highlight path import and run?")
try:
    from rdkit.Chem.Draw import rdMolDraw2D
    d = rdMolDraw2D.MolDraw2DCairo(400, 300)
    m = Chem.MolFromSmiles('c1ccc(O)cc1CC(=O)O')
    match = m.GetSubstructMatch(Chem.MolFromSmarts('[CX3](=O)[OX2H1]'))
    d.DrawMolecule(m, highlightAtoms=match)
    d.FinishDrawing()
    png = d.GetDrawingText()
    print(f"  MolDraw2DCairo OK -- wrote {len(png)} bytes of PNG, highlighted atoms {match}")
except Exception as exc:                                     # noqa: BLE001
    print(f"  FAILED: {type(exc).__name__}: {exc}")
