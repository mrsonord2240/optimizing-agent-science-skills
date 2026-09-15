> **Audit record for `bio-phylo-modern-tree-inference`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@966f838](https://github.com/mrsonord2240/bioSkills/tree/966f838b0ba32918310bd223a34f71d78f190560/phylogenetics/modern-tree-inference) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-modern-tree-inference (re-audit of the fixed Skill)
Generated: 2026-09-15 · Re-auditor: molecular-phylogenetics-analyst round 2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@966f838b0ba32918310bd223a34f71d78f190560:phylogenetics/modern-tree-inference`
Pre-fix report: `audits/_pre-fix-20260915/bio-phylo-modern-tree-inference/` (86, Production Ready). Fix log read
(`round2/fixes/bio-phylo-modern-tree-inference.md`); only the runs below are evidence.
Category: Data Analysis · Mode A · Complexity Complex → 7 regression inputs + 2 new = **N = 9**.
Environment: IQ-TREE 2.4.0 (Windows), Biopython 1.88, DendroPy 5.0.13. IQ-TREE 3 is not installed: the Skill's literal
`iqtree3` exits 127 (`runs_v2/iqtree3_literal.out`); the Skill says `iqtree2` on 2.x, which is what ran. RAxML-NG: no
Windows build, not executed. **All data SYNTHETIC** (AliSim/DendroPy, `data/make_synthetic.py`). Runs: `runs_v2/`.

## What changed (fork diff d91ed3d..966f838)
SKILL.md: `--gcf`/`--scfl` split into two calls, output files renamed, two Common Errors rows, `iqtree3` naming.
Examples: binary resolver `iqtree3 || iqtree2 || iqtree`; partitioned example uses the two calls.

## Step 1 — Skill Veto
T1 PASS (all commands and both IQ-TREE examples exit 0) · T2 PASS · T3 PASS (`--seed` used) · T4 PASS.

## Step 2 — Static score: 86/100 (pre-fix 83)
| Category | Score | Note |
|---|---|---|
| Functional suitability | 10/12 | CF command fixed. Still false: "Do NOT write `--alrt`", "Unknown argument --alrt", "-bb/-nt not recognized" (help lists `--alrt`/`--bnni`; `-bb 1000 -nt 1 --alrt 1000` exit 0, `runs_v2/flagtest.out`). No PMSF command |
| Reliability | 10/12 | New CF and iqtree3 rows; two wrong rows remain |
| Performance & context | 7/8 | 211 lines |
| Agent usability | 14/16 | `iqtree3` commands vs "checked on 2.4.0"; flag warning contradicts help |
| Human usability | 6/8 | unchanged |
| Security | 11/12 | unchanged |
| Maintainability | 10/12 | both examples now run end to end; no test data |
| Agent-specific | 18/20 | unchanged |

Gate 8: no `references/`/`scripts/` pointers; three examples present. PASS.

## Summary Table
| Input | Type | Basic | Spec. | Total | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 37 | 54 | 91 | 5/5 | yes | ✅ |
| 2 | Variant A (regression) | 37 | 53 | 90 | 4/4 | yes | ✅ |
| 3 | Edge (regression) | 34 | 46 | 80 | 3/4 | yes | ✅ |
| 4 | Variant B (regression) | 38 | 55 | 93 | 4/4 | yes | ✅ |
| 5 | Stress (regression) | 37 | 54 | 91 | 5/5 | yes | ✅ |
| 6 | Scope Boundary (regression) | 38 | 49 | 87 | 4/4 | no (routing) | ✅ |
| 7 | Adversarial (regression) | 36 | 56 | 92 | 5/5 | yes | ✅ |
| 8 | NEW — PMSF protein | 34 | 49 | 83 | 3/4 | yes | ✅ |
| 9 | NEW — CF with missing taxa | 37 | 53 | 90 | 4/4 | yes | ✅ |

**Execution average 88.6** · assertions 37/39 (94.9 %) · Layer 1 avg 36.4 · Layer 2 avg 52.1 · executed 8/9.
Research Veto: M1–M4 PASS. Floors (Production Ready): static 86 ≥ 80 ✓, execution 88.6 ≥ 85 ✓, L1 ≥ 32 ✓, L2 ≥ 48 ✓,
assertions ≥ 90 % ✓.

**Final: 86 × 0.4 + 88.6 × 0.6 = 34.4 + 53.2 = 87.6 → 88 → ⭐ Production Ready.**

## Detailed outputs

### Inputs 1–4, 6, 7 — regression
Same prompts as the pre-fix report. Commands re-run with `iqtree2` (Skill's 2.x name); every printed number reproduced:
```
in1  Best-fit model according to BIC: K2P+G4 | 9/9 internal branches pass SH-aLRT>=80 AND UFBoot>=95 | RF 0 (max 18)
in2  HKY+F+G4 x 2 merged subsets | (Sp_F,(Sp_G,Sp_H)) 92.2/88 (fails UFBoot>=95)
in3  33 parsimony-informative, 30 singleton, 187 constant | NOTE: Homo_sapiens_isolate2 is identical ... kept
in4  tree 2 deltaL 7.8789  p-AU 0.0303 -   (constrained Euarchontoglires rejected)
in7  JC: A+C together (UFBoot 100) | K2P+G4: (Fast_C,Slow_D)87.8/86 ... 38.3/58 | AU tree2 p-AU 0.108 | noC: Fast_A with Slow_B
```
Input 6 remains a routing answer (not executed). Input 3 still fails "guidance comes from the Skill".

### Input 5 — Stress (regression; the fixed defect)
Fork commands, verbatim apart from the binary name:
```bash
iqtree2 -t concat.treefile --gcf loci.treefile --prefix concord_g                 # exit 0
iqtree2 -te concat.treefile -s concat.fasta --scfl 100 -T 4 --prefix concord_s    # exit 0
```
```
ID gCF  gDF1 gDF2 gDFP Label     | sCF
9  85   2.5  5    7.5  100/100   | 71.93
10 20   22.5 22.5 35   61.6/72   | 41.10
11 62.5 2.5  2.5  32.5 100/100   | 45.22
12 50   35   15   0    100/100   | 44.71
13 57.5 10   5    27.5 100/100   | 40.60
concat.treefile RF 2 (max 10)
```
Interpretation unchanged: branch 10 is an effective polytomy and is the wrong split; 11–13 are contested despite UFBoot
100; route to species-trees. All 5 assertions pass (pre-fix 4/5).

### Input 8 — NEW, Variant B
**Prompt:** "15 kinase homologs, 300 aa (`prot15.fa`). Reviewers want a site-heterogeneous model because our clade is
deep. Run PMSF the way your guide recommends and tell me whether it changes the tree."
```bash
iqtree2 -s prot15.fa -m LG+F+G --seed 12345 --prefix guide
iqtree2 -s prot15.fa -m LG+C20+F+G -ft guide.treefile -B 1000 -bnni -alrt 1000 --seed 12345 --prefix pmsf
iqtree2 -s prot15.fa -m MFP -B 1000 -bnni -alrt 1000 --seed 12345 --prefix mfp
```
```
guide LG+F+G4   lnL -6176.60 | PMSF LG+SSF+F+G4 lnL -6092.52 (site freqs -> pmsf.sitefreq) | MFP LG+G4 lnL -6175.71
RF to simulated tree: guide 0, pmsf 0, mfp 0 (max 24)
pmsf supports: 95.3/99 91.4/100 98.3/100 98.7/100 95.4/100 87.5/91 89.7/89 82.6/98 100/100 ...
mfp  supports: 95/98   91.8/100 98.1/100 98.8/100 95.4/99  88.1/91 89.8/89 83.3/97 100/100 ...
```
Interpretation: PMSF fits far better (ΔlnL 83) but leaves topology and support unchanged on this shallow gene; its value
is at depth/LBA, where it should be compared with the homogeneous tree. C20 used instead of C60 for runtime (stated).
The Skill names PMSF and `LG+C60+F+G` but gives no `-ft` command. **Scores** 34 + 49 = **83** · Assertions 3/4.

### Input 9 — NEW, Edge
**Prompt:** "Same 40 loci, but 14 of them are missing one or two species. Can I still compute gCF/sCF on the concatenated
tree, and does the missing data change anything?" (auditor dropped taxa synthetically, `runs_v2/make_missing.py`)
```bash
iqtree2 -S loci_missing -m MFP -B 1000 -T AUTO --prefix locim
iqtree2 -t ../in5/concat.treefile --gcf locim.treefile --prefix cgm
iqtree2 -te ../in5/concat.treefile -s ../in5/concat.fasta --scfl 100 -T 4 --seed 12345 --prefix csm
```
```
ID gCF   gDF1  gDF2  gDFP  gN | sCF
9  82.86 2.86  5.71  8.57  35 | 71.79
10 16.67 27.78 25    30.56 36 | 40.56
11 64.71 0     2.94  32.35 34 | 45.25
12 51.43 34.29 14.29 0     35 | 44.54
13 57.58 9.09  9.09  24.24 33 | 40.47
```
Interpretation: gCF is computed over decisive trees only (gN 33–36 of 40), as the Skill's definition says; readings are
unchanged from the complete data. **Scores** 37 + 53 = **90** · Assertions 4/4.

## Shipped examples (run as written)
- `iqtree_basic.sh gene12_aln.fa` → exit 0, resolver chose iqtree2, `Best-fit model according to BIC: K2P+G4`.
- `partitioned_analysis.sh concatenated.fasta` → **exit 0** (pre-fix exit 2); writes `concord_g.cf.*` and `concord_s.cf.*`.
- `raxml_analysis.sh` → `bash -n` OK; not executed (no RAxML-NG Windows build).

## Recommendations
- [P2] Remove the false `--alrt` / `-bb` / `-nt` warnings (static; flag test).
- [P2] Give the PMSF command (Input 8).
- [P2] Add small-data / duplicate-sequence guidance (Input 3).
