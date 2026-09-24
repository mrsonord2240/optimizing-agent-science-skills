> **Audit record for `bio-alignment-structural`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@17418eb](https://github.com/mrsonord2240/bioSkills/tree/17418ebd37abd18d522f23899fae008fd118b79a/alignment/structural-alignment) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-structural

## Canonical final summary

**Final:** 92/100 — ⭐ Production Ready; deployable: true.

Source: `mrsonord2240/bioSkills@17418ebd37abd18d522f23899fae008fd118b79a:alignment/structural-alignment`
Auditor independent: `false`
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

Generated: 2026-09-23. Source: `mrsonord2240/bioSkills@17418ebd37abd18d522f23899fae008fd118b79a:alignment/structural-alignment`.

This is the required final-pass exception: `auditor_independent: false`; see the Phase 1 [checkpoint](../_final_pass/bio-alignment-structural/CHECKPOINT.md). The prior report was preserved at `F:\OpenScience\audits\_pre-fix-20260923\bio-alignment-structural` before this report was written.

| Input | Type | What ran | Basic /40 | Specialized /60 | Total | Assertions |
|---|---|---|---:|---:|---:|---|
| 1 | Canonical | TM-align example, TM-align, US-align | 37 | 57 | 94 | 3/3 |
| 2 | Variant A | Foldseek types 2 and 1 | 37 | 56 | 93 | 3/3 |
| 3 | Edge | Biopython superposition and refusal | 37 | 56 | 93 | 3/3 |
| 4 | Variant B | Seeded Foldmason MSA + JSON | 36 | 56 | 92 | 3/3 |
| 5 | Stress | US-align and Foldseek-Multimer | 37 | 56 | 93 | 3/3 |
| 6 | Scope Boundary | TMscore `-seq` | 36 | 56 | 92 | 3/3 |
| 7 | Adversarial | One-residue TM-align no-row handling | 36 | 55 | 91 | 3/3 |
| 8 | Variant B | Kinase TM-align and DaliLite | 37 | 57 | 94 | 3/3 |
| 9 | Edge | Foldseek pLDDT-masked database | 36 | 56 | 92 | 3/3 |
| 10 | Variant A, fresh | MUSTANG three-structure MSA | 37 | 56 | 93 | 3/3 |
| 11 | Stress, fresh | Headless PyMOL superposition/render | 37 | 56 | 93 | 3/3 |

Execution average: **92.7/100**. Assertion pass rate: **33/33**. Static score: **91/100**. Final: **92/100, Production Ready, deployable**. Skill Veto T1-T4: PASS. Research Veto M1-M4: PASS. No P0 or P1.

## Evidence

The replay script, static checks, source snapshot, command logs, generated structural artifacts, and provenance assertion are all under [run](run/). The output-dependent highlights are:

- 1MBN/1A3N: TM-align and US-align both yielded TM1/TM2 0.8356/0.9000, RMSD 1.56 A, 141 aligned residues; the example wrote `superposed.pdb`.
- The Biopython example returned 0.483 A over 151 CA pairs for co-numbered 1MBN/1A6M and refused offset-numbered 1MBN/1A3N with 116/141 mismatched residue names.
- Foldmason recorded seed 42, wrote its AA/3Di MSAs and JSON, and reported 153 scored of 294 columns in this three-structure run.
- US-align reported hemoglobin-dimer-in-tetramer containment at 0.9769/0.4943 and Foldseek-Multimer created `mm_report`.
- The fresh MUSTANG run created a three-row FASTA; fresh PyMOL produced `super.png` and 0.409 A over 934 atoms.

`run/phase2_static.sh` compiled all four shipped examples and checked the source’s frontmatter, references, Foldmason `scores` extraction, and seed wiring. `run/phase2_provenance.ps1` asserted the dispatched commit and SHA-256 snapshot match. No source files were changed.
