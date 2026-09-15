> **Audit record for `bio-phylo-species-trees`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@966f838](https://github.com/mrsonord2240/bioSkills/tree/966f838b0ba32918310bd223a34f71d78f190560/phylogenetics/species-trees) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-species-trees (re-audit of the fixed Skill)
Generated: 2026-09-15 · Re-auditor: molecular-phylogenetics-analyst round 2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@966f838b0ba32918310bd223a34f71d78f190560:phylogenetics/species-trees`
Pre-fix: 82 numeric → ⚠️ Beta Only (assertion floor). Fix log read; evidence is `runs_v2/` only.
Category Data Analysis · Mode A · Complex → 7 regression + 2 new = **N = 9**.
Environment: ASTER Windows build (astral 1.25.4.8, wastral, astral-pro), Java ASTRAL 5.7.8, IQ-TREE 2.4.0, DendroPy, SciPy.
Per-locus gene trees reused from the pre-fix audit (`runs/inN/loci.treefile`, seeded; command unchanged except the binary
name); all ASTER/CF/asymmetry steps and the shipped example re-run. Not executed: PAUP*/SVDQuartets, BPP, StarBEAST2 (no Skill
command). **All data SYNTHETIC** (`data/make_data.py`).

## Step 1 — Skill Veto: T1–T4 PASS.
## Step 2 — Static: 85/100 (pre-fix 80)
| Category | Score | Note |
|---|---|---|
| Functional suitability | 10/12 | fixes verified; description still says ASTRAL lengths are coalescent units; SVDQuartets/BPP/StarBEAST2 no commands |
| Reliability | 9/12 | no leaf-name consistency check (Input 9) |
| Performance & context | 7/8 | — |
| Agent usability | 14/16 | description / Approach line lag the body |
| Human usability | 6/8 | — |
| Security | 11/12 | — |
| Maintainability | 10/12 | example now completes |
| Agent-specific | 18/20 | circular StarBEAST2 routing removed |

Gate 8: PASS (example present; sibling Skills present).

## Summary Table
| Input | Type | Basic | Spec. | Total | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (regr.) | 37 | 53 | 90 | 5/5 | yes | ✅ |
| 2 | Variant A (regr.) | 37 | 53 | 90 | 5/5 | yes | ✅ |
| 3 | Edge (regr.) | 34 | 48 | 82 | 3/4 | yes | ✅ |
| 4 | Variant B (regr.) | 37 | 55 | 92 | 5/5 | yes | ✅ |
| 5 | Stress (regr.) | 37 | 53 | 90 | 5/5 | yes | ✅ |
| 6 | Scope Boundary (regr.) | 35 | 48 | 83 | 3/4 | yes (units only) | ✅ |
| 7 | Adversarial (regr.) | 37 | 53 | 90 | 5/5 | yes | ✅ |
| 8 | NEW ILS in CU | 36 | 51 | 87 | 4/4 | yes | ✅ |
| 9 | NEW inconsistent names | 33 | 46 | 79 | 3/4 | yes | ✅ |

**Execution average 87.0** · assertions 38/41 (92.7 %) · L1 35.9 · L2 51.1 · executed 9/9. Research Veto M1–M4 PASS.
Floors (Production Ready): static 85 ≥ 80 ✓ · execution 87.0 ≥ 85 ✓ · L1 ≥ 32 ✓ · L2 ≥ 48 ✓ · assertions ≥ 90 % ✓.
**Final: 85 × 0.4 + 87.0 × 0.6 = 34.0 + 52.2 = 86 → ⭐ Production Ready.**

## Key outputs (trimmed)
**In1 (rad)** `wastral` / `astral -t 4` / `astral -u 2` / `astral --root S10` / `astral --length CULength` exit 0 ·
`iqtree2 -t species.tre --gcf gene_trees.nwk --prefix cf_g` exit 0 · `iqtree2 -te species.tre -s concat.fasta --scfl 100 --prefix cf_s`
exit 0 · RF 0/14 for wastral, astral, rooted, concat · gCF per branch 48, 12, 17.3, 34, 50, 27.3, 44 (gN 150); localPP 0.970–1.

**In2 (az)** RF 0/6 all · gCF 25 / 20.5 / 76.75 · localPP 0.786 / 0.761 · Java `-t 10`: `(Sp_E,Sp_O)0 ... Sp_D)0.36978 ... )0.16001` ·
estimated gene trees: anomalous 0.087 vs species topology 0.060.

**In3 (short)** `collapsed 2 internal branches` · RF 0/14 all · gCF 11.4–42.9 (gN 136–149) vs sCF 27.6–56.3.

**In4 (intro)** `astral -u 3` → `freqQuad.csv`; N2 row: t1 107.9, t2 19.4 `{G,F,H}|{C}#{D,E}|{B,A}`, t3 72.7 `{B,A}|{G,F,H}#{D,E}|{C}`.
Skill's test (binomial gDF1 vs gDF1+gDF2):
```
ID gCF  gDF1_N gDF2_N p          verdict
11 83.0 13     11     8.39e-01   symmetric
12 64.5 15     16     1.00e+00   symmetric
13 44.5  9     58     6.81e-10   ASYMMETRIC   (A,B,C branch; simulated C->(D,E) introgression)
14 55.5 30     40     2.82e-01   symmetric
15 71.0 13      7     2.63e-01   symmetric
```
First symtest run crashed on the `NA` root row (auditor script bug), fixed and re-run.

**In5 (fam)** `astral-pro -a gene2species.txt -i family_trees.nwk -o species_pro.tre` →
`(((((Sp_A,Sp_B)0.999998,Sp_C)1,(Sp_E,Sp_D)1)1,(Sp_F,Sp_G)1),Sp_H);` RF 0/10.

**In6 (units)** S01,S02 branch: default `0.00641878` (SULength) · `--length CULength` `0.152496` · wastral `0.16444` · true 0.20 CU.

**In7** `-t 4` tree labels 0.979163, 0.970286 … (localPP, no q) · `-u 2` labels `q1=0.430476 …`.

### Input 8 — NEW
**Prompt:** "Before choosing a method, tell me how short the internodes of my 6-taxon radiation are in coalescent units and
whether I'm in anomaly-zone territory (outgroup Sp_O)."
`astral --root Sp_O --length CULength -u 2 -i gene_trees.nwk -o az_cu_rooted.tre` →
`(Sp_B,Sp_A)[CULength=0.0537902 … localPP=0.785818 …]`, `Sp_C … CULength=0.0462529`. Two successive internodes < 0.1 CU → anomaly-zone
risk per the Skill's threshold table (true 0.03/0.03). 87, 4/4.

### Input 9 — NEW
**Prompt:** "I merged gene trees from two labs; please build the species tree for my 10 species." (30 of 150 trees name S03 as
`S03_b`, synthetic.) `astral -i gene_trees_mixed.nwk` → exit 0, log `#Species: 11`, `S03_b` grouped with S06–S08 at localPP 0.553;
`wastral` same (0.600). `astral -a name2species.txt` → RF 0/14. The Skill gives no leaf-set consistency check. 79, 3/4.

## Shipped example
`bash examples/astral_pipeline.sh` (rad loci + concat.fasta; thread-cap shims) → **exit 0 after 306 s** (pre-fix exit 2),
writes `cf_g.cf.stat` and `cf_s.cf.tree`; `species_wastral.tre` and `species_astral.tre` RF 0/14; closing units message now
correct.

## Recommendations
- [P2] Leaf-name consistency check / `astral -a` for renamed samples (Input 9).
- [P2] Align description and Approach line with the fixed body.
- [P2] Minimal SVDQuartets and BPP commands (Inputs 3, 6).
