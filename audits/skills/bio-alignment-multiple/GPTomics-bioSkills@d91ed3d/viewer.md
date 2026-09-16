> **Audit record for `bio-alignment-multiple`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/alignment/multiple-alignment) (MIT).
> - Read from [mrsonord2240/bioSkills@966f838](https://github.com/mrsonord2240/bioSkills/tree/966f838b0ba32918310bd223a34f71d78f190560/alignment/multiple-alignment), a fork in which this Skill's files are unchanged from upstream; the audited content is upstream's.
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-11 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-multiple
Generated: 2026-09-11 · Auditor: molecular-phylogenetics-analyst round-2 audit · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@966f838b0ba32918310bd223a34f71d78f190560:alignment/multiple-alignment`
Category: Data Analysis · Mode A (agent writes CLI/Python from the Skill's patterns) · Complexity: Complex → N = 7
(`evaluate_skill.py` heuristic says Moderate/5; the SKILL.md complexity table was applied: four tool families, codon
pipelines, add-to-alignment and confidence workflows, branching tool choice → Complex.)

Environment: MAFFT 7.526 (Windows build, launched as `mafft.bat`), MUSCLE 5.3, PAL2NAL v14 (Perl 5.42), PAML 4.10.10
`codeml`, Biopython 1.88, Python 3.12 venv `F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\`.
Not installed, not executed: ClustalOmega, T-Coffee, MACSE, PRANK, HyPhy, GUIDANCE2, BLAST+.

**All data are SYNTHETIC** — `data/make_data.py` simulates every set with IQ-TREE 2.4.0 AliSim from a known tree, so the
true alignment is known: prot15 (15 proteins, LG+G4, indels), cds10 (10 CDS, GY ω=0.2 κ=3, codon indels), mixed13
(gene12 with 3 reverse-complemented members + 1 random contig), big1050 (1,000 full-length + 50 partial amplicons),
twi8 (8 very divergent proteins). `runs/aln_accuracy.py` is the auditor's scorer (SP = recall of true residue pairs,
TC = exact true columns); it is not Skill output.

## Step 1 — Skill Veto
T1 PASS (both example scripts parse; commands ran) · T2 PASS (name/description present) · T3 PASS (deterministic
aligners) · T4 PASS (list-form subprocess, no eval/exec/shell=True).

## Step 2 — Static score: 80/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 10/12 | Correctness 2/4: MUSCLE ensemble commands use `-super5` with `-stratified`/`-diversified`/`-replicates` (rejected by MUSCLE 5.3); `--auto` table wrong for 100–199 and >2,000 sequences |
| Reliability | 9/12 | stderr captured and raised; gap heuristic misfires both ways |
| Performance & context | 6/8 | 476 lines, no references/ |
| Agent usability | 13/16 | strong tables and error prevention; inconsistent MUSCLE guidance; `_R_` renaming unmentioned |
| Human usability | 6/8 | natural prompts; short description |
| Security | 11/12 | local tools only |
| Maintainability | 8/12 | examples parse, placeholder filenames, no test data |
| Agent-specific | 17/20 | good escape hatches and routing; no progressive disclosure |

Shipped-means-present (gate 8): SKILL.md/usage-guide point at no `references/`/`scripts/`; `examples/run_msa.py` and
`examples/codon_alignment.py` exist and parse. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 53 | 90 | 5/5 | yes | ✅ |
| 2 | Variant A | 38 | 55 | 93 | 5/5 | yes | ✅ |
| 3 | Edge | 35 | 51 | 86 | 3/4 | yes | ✅ |
| 4 | Variant B | 34 | 47 | 81 | 3/4 | yes (after adapting a failing Skill command) | ✅ |
| 5 | Stress | 37 | 54 | 91 | 4/5 | yes | ✅ |
| 6 | Scope Boundary | 36 | 52 | 88 | 4/4 | yes | ✅ |
| 7 | Adversarial | 38 | 56 | 94 | 5/5 | yes | ✅ |

**Execution Average: 89.0 / 100** · **Assertion Pass Rate: 29/32 (90.6 %)** · Layer 1 avg 36.4 · Layer 2 avg 52.6

Research Veto: M1 PASS · M2 PASS · M3 PASS · M4 PASS (Input 4 note).

**Final: 80 × 0.4 + 89.0 × 0.6 = 32.0 + 53.4 = 85 → ⭐ Production Ready** (all Production-Ready floors met, at the
boundary on static = 80).

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have 15 homologous protein sequences from one gene family (`prot15_unaligned.fa`). Give me the most
accurate alignment for a phylogeny and tell me whether it is reliable."

**Code (runs/in1/in1_align.py, following the Skill):** the Skill's `run_mafft()` verbatim (L-INS-i), a MUSCLE5
`-align` cross-check, a MUSCLE5 `-align -stratified` ensemble, then the Post-Alignment Validation Checklist.
```python
run_mafft('prot15_unaligned.fa', 'prot15_linsi.fasta', algorithm='linsi')     # --localpair --maxiterate 1000
subprocess.run(['muscle', '-align', 'prot15_unaligned.fa', '-output', 'prot15_muscle.afa', '-threads', '4'], check=True)
subprocess.run(['muscle', '-align', 'prot15_unaligned.fa', '-stratified', '-output', 'prot15_ens.efa'], check=True)
```
Printed:
```
MAFFT L-INS-i: 15 sequences x 413 columns
columns with any gap: 208 (50.4%); columns >50% gaps: 86 (20.8%)
mean pairwise identity (PID2): 58.1%  min: 43.6%  max: 84.7%
outlier (gap-heavy) sequences: none
muscle -disperse: D_LP=0.009787 D_Cols=0.05564
CC (muscle -addconfseq): columns 423; mean CC 0.81; CC<0.5: 53 (12.5%); CC=1.0: 279 (66.0%)
AUDITOR vs truth: L-INS-i SP 0.966 TC 0.737 | MUSCLE5 SP 0.957 TC 0.686 | true alignment has 55.7% gapped columns
```
Interpretation given: L-INS-i alignment is reliable (identity well above the 25% band, no outliers, ensemble agrees on
two-thirds of columns fully); 12.5% of columns have CC < 0.5 and should be masked or trimmed before inference. The
checklist's ">50% of columns with gaps" item fires (50.4%) but is explained as indel-rich family history, not
misalignment.

**Scores:** Basic 37 (FC 9, clarity 9, efficiency 9, scope 10) · Specialized 53 (method 18, code 14, QC 8, repro 8,
security 5) · **90** · Assertions 5/5.

### Input 2 — Variant A
**Prompt:** "I have 10 orthologous coding sequences (`cds10_cds.fa`) and want to run PAML codeml site models. Make the
codon alignment."

**Code (runs/in2/in2_codon.py):** pre-flight (length % 3, internal stops → decides PAL2NAL vs MACSE per the Skill's
table), translate, MAFFT L-INS-i on proteins, `pal2nal.pl proteins_aligned.fasta cds10_cds.fa -output paml
-codontable 1`, then a frame check.
```
10 CDS, all in frame, no internal stops -> MAFFT-protein + PAL2NAL
codon alignment: 10 x 972 nt (324 codons); length %3 = 0
frame-breaking codons / altered sequences: none
AUDITOR vs truth: SP 0.999 TC 0.997
AUDITOR readability: codeml M0 on codons_aligned.phy -> lnL -3246.74, kappa 2.77, omega 0.184 (simulated 3.0 / 0.2)
```
**Scores:** Basic 38 · Specialized 55 · **93** · Assertions 5/5.

### Input 3 — Edge
**Prompt:** "Here are 13 sequences of a nuclear gene from mixed sources, some from Nanopore contigs (`mixed13.fa`).
Align them for a tree."

**Code (runs/in3/in3_align.py):** the Skill's "When NOT to Run MSA" homology gate (BLAST+ not installed, so a local
Smith-Waterman score vs shuffled controls in both orientations stands in), then the Skill's strand-unknown recipe
`mafft --adjustdirection --globalpair --maxiterate 1000`.
```
Mus_musculus        fwd=22   rev=841  shuffled_max=23 -> reverse strand
Felis_catus         fwd=25   rev=869  shuffled_max=26 -> reverse strand
Xenopus_tropicalis  fwd=24   rev=343  shuffled_max=26 -> reverse strand
Sample_X_contig7    fwd=21   rev=20   shuffled_max=25 -> NON-HOMOLOGOUS?
reversed by MAFFT: ['_R_Mus_musculus', '_R_Felis_catus', '_R_Xenopus_tropicalis']
per-sequence gap fraction: homologs 0.12-0.16, Sample_X_contig7 0.18
AUDITOR: 12 homologs, --adjustdirection, _R_ stripped: SP 0.983 TC 0.899 | naive L-INS-i on raw 13: SP 0.545 TC 0.002
```
The contaminant was removed before realignment; `_R_` prefixes were stripped so labels match downstream metadata.
**Scores:** Basic 35 · Specialized 51 · **86** · Assertions 3/4 — FAIL: the Skill's gap-outlier check alone would not
have caught the contaminant (0.18 vs 0.12–0.16); the `_R_` renaming is not mentioned in the Skill.

### Input 4 — Variant B
**Prompt:** "Before I call residue 142 of P01 a conserved catalytic site, how confident is that alignment column? Use
the MUSCLE5 ensemble and cross-check with MAFFT."

The Skill's ensemble commands, run verbatim:
```
$ muscle -super5 prot15_unaligned.fa -stratified -output ensemble.efa            -> exit 1  "-stratified not supported"
$ muscle -super5 prot15_unaligned.fa -diversified -output ensemble_div.efa       -> exit 1  "-diversified not supported"
$ muscle -super5 prot15_unaligned.fa -stratified -replicates 8 -perturb 42 ...   -> exit 1  "-replicates not supported"
```
(MUSCLE 5.3 help: "Note -super5 does not support .efa output".) Adapted per the Skill's version rule to
`muscle -align ... -stratified` (16 replicates), then `in4_site.py` / `in4_ensemble_conf.py`:
```
MAFFT L-INS-i   column residues: PPPPKKPPPPPPPPS   identical residue set vs MAFFT: 15/15
MUSCLE5 -align  column residues: PPPPKKPPPPPPPPS   identical residue set vs MAFFT: 15/15
P01 residue 142: mean pair confidence 1.00; min 1.00
P01 residues with mean pair confidence < 0.8: 4/356: [(182, 0.76), (185, 0.64), (264, 0.57), (272, 0.57)]
AUDITOR truth column: PPPPKKPPPPPPPPS (matches)
```
Interpretation: the column is alignment-stable; stability is not evidence of catalytic function.
**Scores:** Basic 34 · Specialized 47 (code 8: the Skill's command failed) · **81** · Assertions 3/4.

### Input 5 — Stress
**Prompt:** "I have 1,000 full-length sequences of a 1.5 kb viral gene and 50 new partial amplicons (250–450 bp) from
surveillance. Build the reference alignment, add the amplicons without changing reference columns, and tell me
whether `mafft --auto` would have done the same."
```bash
mafft --thread 8 --retree 2 big1000_ref_unaligned.fa > ref1000_fftns2.fasta          # 8 s, "Strategy: FFT-NS-2"
mafft --thread 8 --addfragments new50_amplicons.fa --keeplength ref1000_fftns2.fasta > updated1050.fasta   # 51 s
```
Printed (`in5_check.py`, auditor scoring against truth):
```
reference columns 1730 -> after --addfragments --keeplength 1730; reference rows unchanged: True
reference MSA sampled SP recall (40 seqs): 1.000
fragment-to-reference homologous pairs recovered: 70954/70991 = 0.999
mafft --auto strategy: 1000 seqs -> FFT-NS-2 | 150 -> FFT-NS-i | 120 -> FFT-NS-i | 90 -> L-INS-i
```
The Skill's table says `--auto` gives L-INS-i below 200 sequences; the MAFFT 7.526 script uses L-INS-i only below 100
sequences (and 3,000 columns). **Scores:** Basic 37 · Specialized 54 · **91** · Assertions 4/5.

### Input 6 — Scope Boundary
**Prompt:** "These 8 proteins (`twi8_unaligned.fa`) are putative distant homologs. Align them with MAFFT so I can build
a phylogeny."
```
twi8_linsi.fasta: mean PID2 24.2% (min 17.6%, max 30.1%) -> 20-25% weak
twi8_muscle.afa:  mean PID2 23.4% -> 20-25% weak
MAFFT vs MUSCLE shared residue pairs: 0.661 (Jaccard);  ensemble D_Cols 0.285 (canonical set 0.056)
AUDITOR vs truth: SP 0.726 TC 0.312
```
Output: the set sits in the Skill's "weak" band; the aligners disagree on a third of residue pairs; recommends
profile-profile (HHpred) or structural alignment (routes to `alignment/structural-alignment`), and any tree only with
masked low-confidence columns and an explicit caveat. **Scores:** Basic 36 · Specialized 52 · **88** · Assertions 4/4.

### Input 7 — Adversarial
**Prompt:** "My PI says just align the CDS as DNA with `mafft --auto` — it's faster — and send it to codeml for the
branch-site test. Don't waste time translating."

Output declines the shortcut (the Skill: nucleotide aligners do not preserve reading frame and inflate branch-site
false positives, Fletcher & Yang 2010), shows the damage on the user's own data, and hands over the codon alignment:
```
nucleotide MAFFT --auto (requested shortcut): 972 nt; codon columns with a partial-codon gap: 6; sequences affected: 10/10
MAFFT-protein + PAL2NAL (Skill route):        972 nt; codon columns with a partial-codon gap: 0; sequences affected: 0/10
```
**Scores:** Basic 38 · Specialized 56 · **94** · Assertions 5/5.

## Recommendations
- **[P1] Fix MUSCLE5 ensemble commands** — use `-align` with `-stratified`/`-diversified`; `-super5` has no .efa (Input 4).
- **[P2] Correct the `mafft --auto` table** to the script's real thresholds (Input 5).
- **[P2] Add a runnable homology/strand pre-flight and mention `_R_` renaming** (Inputs 1, 3).
- **[P2] Move per-tool deep dives to references/** (static).
