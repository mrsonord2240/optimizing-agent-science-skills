# Fix log: bio-covalent-design (2026-09-19)

Source: `chemoinformatics/covalent-design` in `F:\OpenScience\external\mrsonord2240__bioSkills`.
Branch `fix/cg-covalent` off `main` (85ca33b). Audit: `F:\OpenScience\audits\bio-covalent-design\`
(88/Limited Release, deployable, no P0). Env: `cheminformatics-hit-triage-analyst`, RDKit 2026.03.6.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| Shipped `WARHEAD_SMARTS` catalog omits 2 of 14 SKILL.md-documented classes (alpha-haloketone, alpha,beta-unsaturated ketone) | P1 | Added `alpha_haloketone` (`[#6][CX3](=[OX1])[CH2][F,Cl,Br]`) and `alpha_beta_unsaturated_ketone` (`[#6][CX3](=[OX1])[CX3]=[CX3]`) to `WARHEAD_SMARTS`/`REACTIVITY_TIER`/`RESIDUE_SELECTIVITY` in `examples/warhead_classifier.py`, scoped with a leading `[#6]` so neither co-matches the amide-based acrylamide/chloroacetamide/bromoacetamide keys | ran: `python examples/warhead_classifier.py` — phenacyl chloride (`ClCC(=O)c1ccccc1`) now matches `alpha_haloketone`, chalcone (`O=C(/C=C/c1ccccc1)c1ccccc1`) now matches `alpha_beta_unsaturated_ketone`; confirmed chloroacetamide/bromoacetamide/acrylamide/methacrylamide compounds do NOT co-match the new keys; added a regression assertion that every SKILL.md table row has a catalog key | Kept "Cysteine-selective heterocycle" (SKILL.md's "various" SMARTS row) out of the catalog — not a single substructure, so not a defect |
| `acrylamide`/`alpha_substituted_acrylamide`/`methacrylamide` SMARTS co-match the same compound, undocumented | P1 | Added a code comment in `warhead_classifier.py` above `WARHEAD_SMARTS` and a paragraph in SKILL.md's Warhead Chemistry section stating the three keys are not mutually exclusive and a single-tier consumer must pick the most specific matched key, never a fixed lookup order | ran: confirmed `C=C(C)C(=O)N1CCCCC1` (methacrylamide) matches all three SMARTS patterns; added a regression assertion for the overlap | |
| No explicit escape hatch for individual-patient/clinical-decision misuse | P1 | Added a `## Scope` section to SKILL.md right after the intro paragraph: this Skill supports lead-optimization/covalent-SAR research design, not diagnosis, individual patient outcome prediction, or oncology clinical judgment; kinact/Ki/GSH/classifier output must not inform an individual patient decision | reviewed against audit input 7's finding (declined only via general model safety, not a Skill instruction) | |
| Covalent docking section is documentation-only, no runnable local workflow | P2 | Not fixed | n/a | Audit itself rates this correctly disclosed, not overclaimed (all 7 tools are commercial/web-service/unimplemented, confirmed against this env's TOOLS.md); no open-source Windows-runnable backend exists to write. Left as-is per the audit's own recommendation. |
| `usage-guide.md` Tips duplicate SKILL.md caveats | P2 | Trimmed `usage-guide.md`'s 5-bullet Tips section to a one-line cross-reference naming the 5 SKILL.md sections (Reactive Residue Taxonomy, Intrinsic Reactivity Assays, Reactivity Surrogates, Kinetics: kinact/Ki, Per-Tool Failure Modes) that already carry the same points | read-diff: confirmed each trimmed bullet's content already exists in the named SKILL.md section | |

## Unfixed

- P2 "covalent docking is documentation-only" — no runnable local backend exists to write; the
  audit itself says this is honest disclosure, not a defect to fix.

## Verification

- `py_compile examples/warhead_classifier.py` — OK.
- Ran the script directly (`Scripts\python.exe examples\warhead_classifier.py`) in the
  `cheminformatics-hit-triage-analyst` env, RDKit 2026.03.6 — exits 0, no `AssertionError`,
  prints the new warhead classifications for phenacyl chloride and chalcone plus the pre-existing
  acrylamide/chloroacetamide demo output.

Nothing needs Sam. Not merged, not re-audited — per brief, that is a separate agent's job.

---

# 2026-09-21 fix pass (Production Ready batch, P2s)

Worktree `F:\OpenScience\wt\chemoinformatics-covalent-design`, branch `fix/chemoinformatics-covalent-design`
off staging `431aa55`. Env `cheminformatics-hit-triage-analyst`, RDKit 2026.03.6. Commits:
`36673a6` (fix), `b7bd357` (redundancy), `41e3766` (scripts). SKILL.md 283 -> 266 lines, no split needed.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| Iodoacetamide (Decision Tree ABPP row) not in `WARHEAD_SMARTS`; `classify_warheads('NC(=O)CI')` returned `{}` | P2 | Added `iodoacetamide` (`[CX3](=[OX1])([NX3])[CH2][I]`) to `WARHEAD_SMARTS`, `REACTIVITY_TIER` (high), `RESIDUE_SELECTIVITY` (Cys) in `examples/warhead_classifier.py`; added an Iodoacetamide row to SKILL.md's Warhead Chemistry table; extended the regression assertion to cover Decision-Tree-named classes | ran `examples/warhead_classifier.py`: `NC(=O)CI` -> `{'iodoacetamide': ...}` only (no chloroacetamide/alpha_haloketone co-match), all assertions pass, exit 0 | |
| Covalent docking documentation-only | P2 | Not fixed | n/a | see Left unfixed |

## Left unfixed

- P2 "covalent docking section is documentation-only, no runnable local workflow": every listed tool
  is commercial (GOLD, CovDock, MOE, ICM-Pro) or a web service (DOCKovalent, HCovDock), and AutoDock 4
  covalent is not installed in the env (TOOLS.md has Vina 1.2.7 only, no AD4); installs are forbidden
  by the brief. The `add_acrylamide` stub is a deliberate hook, not a defect. The audit itself judged
  the disclosure honest.

## Deleted passage -> new home

| deleted | new home |
| --- | --- |
| usage-guide.md Prerequisites code block (`pip install rdkit`; DOCKovalent web service; GOLD commercial; HCovDock standalone) | SKILL.md Version Compatibility (install line, covalent.docking.org, HCovDock standalone note; GOLD already there); guide points at it. Verified by grep. |

## Scripts moved

| old location | script |
| --- | --- |
| SKILL.md "Reactivity Surrogates", inline `acrylamide_alpha_substitution_count` (17 lines) | `scripts/acrylamide_alpha_substitution.py` (SMILES as CLI args). Ran: `C=CC(=O)N1CCCCC1` -> 0, `C=C(C)C(=O)N1CCCCC1` -> 1, `C=C(Cl)C(=O)NC` -> 1, `CCO` -> None, unparsable -> None |

The KRAS workflow block is a `NotImplementedError` stub (API-shape illustration) and stays inline.
