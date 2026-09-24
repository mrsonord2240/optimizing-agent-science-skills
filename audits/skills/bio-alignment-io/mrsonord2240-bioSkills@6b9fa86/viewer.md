> **Audit record for `bio-alignment-io`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6b9fa86](https://github.com/mrsonord2240/bioSkills/tree/6b9fa869af695c9dcd745c6bca830d6aebe58f68/alignment/alignment-io) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-io final pass

Generated: 2026-09-24  
Source: `mrsonord2240/bioSkills@6b9fa869af695c9dcd745c6bca830d6aebe58f68:alignment/alignment-io`  
Final-pass declaration: `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md.

## Result

| Metric | Result |
|---|---|
| Final score | **94/100** |
| Grade | **⭐ Production Ready** |
| Deployable | **true** |
| Vetoes | none (Skill Veto PASS; Research Veto PASS) |
| Assertions | **31/31 PASS** |
| Execution | **10/10 inputs executed** |
| Open P0 / P1 / P2 | **0 / 0 / 0** |

The static score is 93/100 and the execution average is 94.7/100. All Production Ready floors pass: static ≥80, execution ≥85, Layer 1 average ≥32, Layer 2 average ≥48, and assertion pass rate 100%.

## Inputs

| # | Type | Scenario | Basic /40 | Specialized /60 | Total /100 | Assertions |
|---|---|---|---:|---:|---:|---|
| 1 | Canonical | Copied shipped examples | 37 | 57 | 94 | 3/3 PASS |
| 2 | Variant A | NEXUS conversion across alphabets | 38 | 58 | 96 | 4/4 PASS |
| 3 | Edge | Clustal identifier collision | 37 | 57 | 94 | 3/3 PASS |
| 4 | Variant B | MAF minus-strand coordinates | 37 | 57 | 94 | 3/3 PASS |
| 5 | Stress | MrBayes-safe NEXUS identifiers | 38 | 57 | 95 | 3/3 PASS |
| 6 | Scope Boundary | Progressive-disclosure references | 37 | 56 | 93 | 3/3 PASS |
| 7 | Adversarial | Ragged A2M rows | 37 | 57 | 94 | 3/3 PASS |
| 8 | Regression edge | IUPAC and X-masked DNA | 38 | 57 | 95 | 3/3 PASS |
| 9 | Fresh invalid input | Contradictory RNA override | 38 | 58 | 96 | 3/3 PASS |
| 10 | Fresh invalid input | Mixed T/U alignment | 38 | 58 | 96 | 3/3 PASS |

`run/final_pass_verify.py` executed all eight archived audit scenario areas (canonical examples, NEXUS alphabets, Clustal IDs, MAF coordinates, MrBayes IDs, reference links, ragged A2M, and IUPAC/X inference) plus two fresh invalid-input cases (contradictory override and mixed T/U). It ran copied examples so the source worktree stayed clean. `run/final_pass_verify.out` records the 31 passing assertions.

## Fixed findings verified

- IUPAC/X nucleotide classification, mixed T/U rejection, and DNA/RNA/protein override checks occur before output publication.
- NEXUS output is re-read before the temporary conversion set is published.
- The conversion example warns for identifiers that require the documented MrBayes safe-id recipe.
- Clustal 30-character truncation and the full tree-tool safe-id regex are documented.
- MAF, A2M/A3M, and streaming material moved to three linked reference files; every link resolves.

## Remaining issues

None in the scoped final-pass findings. No recommendation remains open.
