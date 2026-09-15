> **Audit record for `bio-alignment-trimming`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@966f838](https://github.com/mrsonord2240/bioSkills/tree/966f838b0ba32918310bd223a34f71d78f190560/alignment/alignment-trimming) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-trimming (re-audit of the fixed Skill)
Generated: 2026-09-15 · Re-auditor: molecular-phylogenetics-analyst round 2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@966f838b0ba32918310bd223a34f71d78f190560:alignment/alignment-trimming`
Pre-fix: 75 numeric → ⚠️ Beta Only (assertion floor). Fix log read; evidence below is only from `runs_v2/`.
Category Data Analysis · Mode A · Complex → 7 regression + 2 new = **N = 9**.
Tools: ClipKIT 2.14.0, trimAl 1.4.1 (1.5.1 Windows binary does not load), BMGE 1.12 + 2.0 jars, MACSE 2.07, PAML 4.10.10,
PhyIN 1.0, IQ-TREE 2.4.0. Not executable: T-Coffee, HMMcleaner, Divvier, Gblocks, hmmbuild. **All data SYNTHETIC**
(`data/make_data.py`).

## Step 1 — Skill Veto: T1–T4 PASS.
## Step 2 — Static score: 80/100 (pre-fix 70)
| Category | Score | Note |
|---|---|---|
| Functional suitability | 10/12 | flag errors fixed and verified; "BLOSUM62 context" and -automated1 first-line mention remain |
| Reliability | 10/12 | BMGE `test -s`, charset and codeml rows; no caution on sequence-overlap thresholds |
| Performance & context | 5/8 | 330-line monolithic SKILL.md |
| Agent usability | 13/16 | one scoped 20%/40% rule everywhere |
| Human usability | 6/8 | — |
| Security | 11/12 | — |
| Maintainability | 9/12 | examples run on both BMGE versions; no test data |
| Agent-specific | 16/20 | progressive disclosure 2 |

Gate 8: no pointers to missing files; four examples present. PASS.

## Summary Table
| Input | Type | Basic | Spec. | Total | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (regr.) | 37 | 53 | 90 | 5/5 | yes | ✅ |
| 2 | Variant A (regr.) | 36 | 51 | 87 | 5/5 | yes | ✅ |
| 3 | Edge (regr.) | 37 | 53 | 90 | 4/4 | yes | ✅ |
| 4 | Variant B (regr.) | 35 | 50 | 85 | 4/4 | yes | ✅ |
| 5 | Stress (regr.) | 35 | 50 | 85 | 5/5 | yes | ✅ |
| 6 | Scope Boundary (regr.) | 35 | 48 | 83 | 5/5 | yes (TCS not) | ✅ |
| 7 | Adversarial (regr.) | 36 | 51 | 87 | 5/5 | yes | ✅ |
| 8 | NEW PhyIN second pass | 36 | 50 | 86 | 4/4 | yes | ✅ |
| 9 | NEW fragment filtering | 30 | 42 | 72 | 2/4 | yes | ⚠️ |

**Execution average 85.0** · assertions 39/41 (95.1 %) · L1 35.2 · L2 49.8 · executed 9/9. Research Veto M1–M4 PASS.
**Final: 80 × 0.4 + 85.0 × 0.6 = 32.0 + 51.0 = 83 → ✅ Limited Release** (all LR floors met; below the 85 core bar).

## Key outputs (trimmed)
**In1** `clipkit input.fasta -m smart-gap --log -o trimmed.fasta` → `retention 82.1%; light` · first log row `'1 keep constant 0.0'` ·
Skill parser → `(339, 339, True)` · trees RF 0 / 0 (TL 4.74 / 4.60, true 4.29).

**In2** `clipkit supermatrix.fasta -m smart-gap -of phylip` → ` 12 16116` · per-locus smart-gap `16357/17560 = 93.1%; 20 charsets` ·
BMGE 1.12 `-t DNA -m DNAPAM100:2 -h 0.5 -g 0.2 -of` → 15263 (86.9 %) · BMGE 2.0 `-t NT ... -e 0.5 -g 0.2 -o` → 15418 (87.8 %) ·
1.12 flags on 2.0 jar → exit 0 then `BMGE wrote no alignment: check flags against the installed version` · RF 0 for all four trees.

**In3** kpic-smart-gap stem 1.213, pendants 0.107/0.089/0.000 · smart-gap stem 0.439, pendants 0.345/0.260/0.326 · TRUE stem 0.438.

**In4** Skill parser on `gappyout_cols.txt` (218), `kept_columns.txt` (161), `columns.txt` (250) → residues match: True ×3.

**In5**
```
clip_smart-gap 75.8% (20-40% removed) | kpic-smart-gap 49.4% (judge by trees) | trimal_gappyout 49.4% | trimal_strict 40.2%
bmge112_h05 29.2% | bmge200_e05 47.9%   (all four: >40% removed, too aggressive)
RF all 0 | TL: input 14.58, smart-gap 14.58, gappyout 13.00, strict 11.18, BMGE1.12 11.19, BMGE2.0 12.65 (true 12.46)
```
**In6** `sed -e '/^>/!s/!/-/g'` → 0 `!`, 10 headers · MACSE export (+`-codonForInternalFS --- -charForRemainingFS -`) → 0 `!`, 1 NNN ·
codeml M0: lnL −3246.734 (sed) / −3246.576 (MACSE), omega 0.184 (process exit 1 on this build, mlc complete).

**In7** no setting gives 12/12 UFBoot ≥ 95; nogaps RF 2; kpi wRF 2.545.

### Input 8 — NEW
**Prompt:** "After ClipKIT, some loci still look like alignment artefacts. Run PhyIN as a second pass on locus05 and tell me
whether it changes the gene tree." `python phyin.py -input first.fasta -output trimmed.fasta -b 10 -d 2 -p 0.5` →
`Deleted by PhyIN: 20 Retained: 796` · RF 0/0/0, support<95 3/3/2 · protein file: `Deleted by PhyIN: 0`, no warning. 86, 4/4.

### Input 9 — NEW
**Prompt:** "Two of my 15 transcriptome sequences are partial contigs. Remove sequences with poor overlap before trimming,
using the trimAl option from your guide." `trimal -in frag17.fasta -out seqfilt.fasta -resoverlap 0.8 -seqoverlap 75` →
`seqs in: 15 out: 11`, removed `P04 P10 P12 P14`; P04/P10 were the synthetic fragments, P12/P14 are full length. Retention
after smart-gap 99.3 % vs 85.5 %. The Skill gives no threshold guidance or removal check. 72, 2/4.

## Shipped examples (run as written)
All four `py_compile` OK. `clipkit_trim.py` → smart-gap 82.1 %, exit 0. `bmge_trim.py` (1.12 jar) → 72.2 % / 74.1 %, exit 0;
with `version = '2.0'` and the 2.0 jar → 75.3 %, exit 0; unedited script with the 2.0 jar → `RuntimeError: BMGE wrote no
alignment ... check flags for BMGE 1.12`, exit 1 (intended guard). `trimal_modes.py`/`divvier_split.py` unchanged (pre-fix
results stand).

## Recommendations
- [P2] Caution on trimAl sequence-overlap thresholds (Input 9).
- [P2] Remove remaining mixed messages (BLOSUM62, -automated1).
- [P2] Move tool-specific detail to references/.
