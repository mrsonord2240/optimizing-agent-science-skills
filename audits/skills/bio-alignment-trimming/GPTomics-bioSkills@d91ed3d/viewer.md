> **Audit record for `bio-alignment-trimming`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/alignment/alignment-trimming) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-trimming
Generated: 2026-09-15 · Auditor: molecular-phylogenetics-analyst round-2 sub-audit · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:alignment/alignment-trimming`
Category: **Data Analysis** · Mode **A** (agent writes CLI/Python from the Skill's patterns; the four `examples/*.py` are
illustrative wrappers, not a required script interface) · Complexity: **Complex → N = 7** (nine trimming tools, a
goal-driven decision tree with six branches, dataset-character table, selection-analysis and codon-aware side paths).

Environment (Windows 11, 4 threads max per tool): ClipKIT 2.14.0 (pip), trimAl v1.4.rev15 (1.4.1 Windows build),
BMGE 1.12 and 2.0 jars (Java 17), MACSE v2.07 jar, IQ-TREE 2.4.0, PAML 4.10.10 codeml, Biopython 1.88, DendroPy 5.0.13.
**Not executable here:** trimAl 1.5.1 Windows release binary (fails to load: 0xC0000139 entry point not found),
Divvier (no Windows build; last release v1.01, 2019), HMMcleaner (Perl/CPAN + HMMER, no Windows HMMER), Gblocks
(Windows binary host unreachable), T-Coffee (no Windows build), HMMER `hmmbuild`. PhyIN v1.0 `phyin.py` was downloaded
and its CLI read but not used as the Skill writes it (the Skill's flags do not exist). Their commands were checked
against the tools' own documentation (saved under `runs/flagcheck/`).

**All data are SYNTHETIC** — `data/make_data.py` simulates sequences with IQ-TREE AliSim (with indels) from known trees and
aligns them with MAFFT L-INS-i: prot15 (15-taxon protein gene), dna_super (12 taxa × 20 DNA loci), unbal33 (30 shallow
ingroup + 3 distant outgroups), deep_super (16 taxa × 12 protein genes, long branches), cds10 (10-taxon codon alignment,
protein-guided + PAL2NAL), reps (10 replicate prot15-like genes). True trees are in `data/`. Nothing from
`_partial-20260911` was used as evidence; the generator was copied, extended (reps) and re-run.

## Step 1 — Skill Veto
T1 Stability PASS (no crash/loop in the Skill's own logic; failures are wrong flags, scored below) · T2 Contract PASS
(`name`, `description` present) · T3 Determinism PASS (all trimmers deterministic; trimAl -automated1 gave identical
md5 on 3 repeats) · T4 Security PASS (examples use list-form `subprocess.run`, no shell/eval).

## Step 2 — Static score: 70/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 7/12 | Completeness 3, Correctness 1, Appropriateness 3. Broad, goal-driven coverage, but many commands/claims are wrong on current tools: ClipKIT `--output-format` (real flag `-of`); BMGE commands are 1.12-only (BMGE 2.0: `-h` = help, entropy is `-e`, `-t NT`) and silently produce nothing on 2.0; Gblocks `-b1=50% -b2=85%` (docs: integer sequence counts); PhyIN `phyin input.fasta -o -w -t` (real: `phyin.py -input -output -b -d -p`, DNA only); TCS `+keep '[5-9]'` keeps residues not columns (`+use_cons +keep`); "codeml interprets `!` as missing data" false on PAML 4.10.10; MACSE export command leaves `!`; ClipKIT "issues #71 and #88" are a dependabot PR and a non-existent issue. |
| Reliability | 7/12 | Common Errors table and introspect-and-adapt rule; no check that an output file was written (BMGE 2.0 exits 0 with no output), no guidance when trimming a concatenated matrix invalidates the partition file. |
| Performance & context | 5/8 | 310-line SKILL.md with everything inline (TCS, MACSE, PhyIN, Gblocks) and no references/ split. |
| Agent usability | 11/16 | Clear decision tables and good pitfalls (kpic on unbalanced data, selection-analysis warning); internal inconsistency: 20%/40% rule vs "warn below 0.7 / 20-30% rapidly degrades", and the recommended default `kpic-smart-gap` itself removes 48–51% of columns on our single-gene and deep datasets; `-strictplus` recommended for phylogenetics while trimAl's own help says it is optimized for NJ. |
| Human usability | 6/8 | Natural prompts in usage guide; description names tools more than tasks. |
| Security | 11/12 | Local tools only, list-form subprocess; no input validation of alignment type/format. |
| Maintainability | 8/12 | Separate example per tool, but no test data or expected output; examples assume `BMGE.jar`/`trimal`/`divvier` in cwd/PATH. |
| Agent-specific | 15/20 | Precise trigger (4); progressive disclosure 2 (monolithic); composability 3 (related-skill routing); idempotency 3; escape hatches 3 (do-not-trim for selection analysis and short genes). |

**Gate 8 (shipped-means-present): PASS.** SKILL.md and usage-guide.md reference no `references/`, `scripts/`, `assets/` or
`templates/` files. `examples/bmge_trim.py`, `clipkit_trim.py`, `divvier_split.py`, `trimal_modes.py` present. Sibling
Skills named in Related Skills (alignment/multiple-alignment, msa-parsing, msa-statistics, structural-alignment,
phylogenetics/modern-tree-inference) all present.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical — single protein gene, smart-gap + log + sensitivity | 35 | 51 | 86 | 4/5 | yes | ✅ |
| 2 | Variant A — DNA supermatrix, kpic-smart-gap/BMGE, PHYLIP | 30 | 42 | 72 | 2/5 | yes (Skill PHYLIP and BMGE-2.0 commands failed; adapted) | ⚠️ |
| 3 | Edge — unbalanced 30+3, kpic failure mode | 36 | 52 | 88 | 3/4 | yes | ✅ |
| 4 | Variant B — HMM prep, -gappyout, -colnumbering, reproducibility | 32 | 45 | 77 | 4/5 | yes (trimAl 1.5.1 and hmmbuild not runnable) | ✅ |
| 5 | Stress — deep protein supermatrix, 11 trimming settings | 30 | 42 | 72 | 3/5 | yes (Gblocks not runnable; BMGE 2.0 Skill command no output) | ⚠️ |
| 6 | Scope Boundary — codon alignment for branch-site test | 31 | 40 | 71 | 2/5 | yes (MACSE, codeml, ClipKIT ran; T-Coffee TCS not executed) | ⚠️ |
| 7 | Adversarial — trim until all nodes ≥95 | 36 | 51 | 87 | 5/5 | yes | ✅ |

**Execution Average: 79.0 / 100** (553/7) · **Assertion Pass Rate: 23/34 (67.6 %)** · Layer 1 avg 32.9/40 · Layer 2 avg
46.1/60 · Executed 7/7 (partial tool coverage noted per input).

**Research Veto:** M1 Scientific integrity PASS (no fabricated data in outputs; the Skill's unverifiable ClipKIT issue
citations were flagged, not repeated) · M2 Practice boundaries PASS (pure research phylogenetics; no individual-level
diagnosis) · M3 Methodological ground PASS (outputs kept sensitivity analyses, refused support-driven over-trimming, did not
column-trim selection input, and corrected the Skill's TCS residue/column error) · M4 Code usability PASS (all delivered
code ran; failing Skill commands were adapted per its introspect-and-adapt rule; examples compile and run with the
documented tool versions — recorded as P1 defects, not unrunnable code).

**Floors check (scoring_rubric §5):** numeric grade Limited Release (75). Limited-Release floors: static 70 ≥ 70 ✓ ·
execution 79.0 ≥ 75 ✓ · Layer 1 32.9 ≥ 28 ✓ · Layer 2 46.1 ≥ 42 ✓ · **assertion pass rate 67.6 % < 80 % ✗** → downgraded
one tier to **Beta Only**. No safety-assertion failures; static ≥ 60.

**Final: 70 × 0.4 + 79.0 × 0.6 = 28.0 + 47.4 = 75.4 → 75 → (assertion floor missed) ⚠️ Beta Only · deployable: no ·
veto override: no.**

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have a single-gene protein alignment for 15 species (`prot15_linsi.fasta`, MAFFT L-INS-i). I want to build
an IQ-TREE tree from it. Trim it the right way, keep a per-column record for the methods section, tell me what fraction
of columns you removed, and whether trimming changed the tree."

**Output (agent following the Skill):** single-gene tree input → ClipKIT `smart-gap` (goal table + decision tree), `--log`
for reproducibility, the Skill's `trimming_fraction` cap, and the mandatory trimmed-vs-untrimmed sensitivity trees.
```bash
clipkit input.fasta -m smart-gap --log -o trimmed.fasta
iqtree2 -s input.fasta   -m MFP -B 1000 -T 4 --seed 1 --prefix untrimmed
iqtree2 -s trimmed.fasta -m MFP -B 1000 -T 4 --seed 1 --prefix smartgap
python in1_report.py     # trimming_fraction() verbatim from SKILL.md, log parsing, RF comparison
```
What ran and printed (runs/in1/):
```
Number of sites kept: 339 / Original length: 413 / Percentage of alignment trimmed: 17.918%
log files present: ['trimmed.fasta.log']
first row repr: '1 keep constant 0.0'
rows with 4 tab-separated fields: 0          <- SKILL.md says position\tkeep_or_trim\tsite_classification\tgap_proportion
rows with 4 whitespace fields: 413
keep/trim x class: keep parsimony-informative 182, keep singleton 99, keep constant 58, trim other 56, trim constant 12, trim singleton 6
RF(untrimmed, trimmed) = 0
AUDITOR CHECK RF to TRUE tree: untrimmed 0 | smart-gap 0 | max 24
untrimmed LG+G4 lnL -6335.26, UFBoot<95 on 3/12 ; smartgap LG+G4 lnL -6022.71, UFBoot<95 on 4/12
```
Interpretation given: 82.1% retained (light-trim regime, above the 0.7 cap); topology identical with and without trimming
and support essentially unchanged, so the result is robust to trimming; report the ClipKIT version, mode and the log. The
log is a space-separated file named `<output>.log`, 1-based positions, classes constant/parsimony-informative/singleton/other
(the parser had to be adapted from the Skill's tab-separated description).

**Scores:** Basic 35/40 (FC 9, clarity 8, efficiency 9, scope 9) · Specialized 51/60 (method 17, code 13, QC 8, repro 8,
security 5) · **86**
**Assertions (4/5):** PASS smart-gap chosen for single-gene tree input · PASS retention computed and checked against the
0.7 cap · PASS trimmed and untrimmed trees both built and compared (RF 0; truth RF 0) · FAIL `--log` format is as the Skill
describes (tab-separated) — it is space-separated · PASS code ran (exit 0).

### Input 2 — Variant A
**Prompt:** "Concatenated supermatrix: 12 taxa, 20 nuclear loci (`supermatrix.fasta` + `supermatrix.nex` charsets). Which
trimmer should I use before a partitioned IQ-TREE run? Give me a PHYLIP output too, and try BMGE as a second opinion."

**Output (Skill commands as written, then adapted):**
```bash
clipkit supermatrix.fasta -m kpic-smart-gap -o super_kpic.fasta                       # exit 0, 25.3% trimmed
clipkit supermatrix.fasta -m kpic-smart-gap --output-format phylip -o super_kpic.phy  # exit 2
java -jar BMGE112.jar -i supermatrix.fasta -t DNA -of super_bmge112.fasta -m DNAPAM100:2 -h 0.5   # exit 0
java -jar BMGE200.jar -i supermatrix.fasta -t DNA -of super_bmge200.fasta -m DNAPAM100:2 -h 0.5   # exit 0, NO output
iqtree2 -s super_kpic.fasta -p supermatrix.nex -m GTR+G4 ...                          # exit 2
```
Printed:
```
clipkit: error: unrecognized arguments: --output-format phylip
adapted: clipkit ... -of phylip -o super_kpic.phy   -> exit 0, header " 12 13126"
BMGE 1.12: before 12 sequences / 17560 characters -> after 12 sequences / 15263 characters (86.9%)
BMGE 2.0 : prints the v2.0 banner/help and exits 0; super_bmge200.fasta: No such file or directory
BMGE 2.0 adapted (-t NT -e 0.5 -g 0.2): 15418 characters (87.8%)
IQ-TREE with original charsets on the trimmed concatenation: ERROR: Too large site ID
adapted: per-locus kpic-smart-gap, re-concatenate, rebuild charsets -> 13311/17560 = 75.8%; 20 partitions
untrimmed.treefile: RF = 0 (max 18) | kpic.treefile: RF = 0 | bmge.treefile: RF = 0      (AUDITOR, vs true tree)
```
Interpretation given: kpic-smart-gap is the Skill's first line for supermatrices (25% removed on the concatenation,
24% per locus: moderate regime). Trim per locus, not the concatenation, or the partition file no longer matches (the
Skill does not say this). All three trees recover the true topology on this mid-depth dataset, so trimming is neutral here.

**Scores:** Basic 30/40 (FC 7, clarity 7, efficiency 8, scope 8) · Specialized 42/60 (method 14, code 8, QC 7, repro 8,
security 5) · **72**
**Assertions (2/5):** FAIL Skill's PHYLIP-output ClipKIT command runs (exit 2) · FAIL Skill's BMGE DNA command produces an
alignment on both installed BMGE versions (2.0: exit 0, no file) · FAIL Skill warns that trimming a concatenated matrix
invalidates the partition charsets · PASS trimmed trees are as accurate as untrimmed (RF 0 to truth for all) · PASS
retention reported and within the Skill's thresholds (75–87%).

### Input 3 — Edge
**Prompt:** "My DNA alignment has 30 very closely related strains and only 3 distant outgroups (`unbal33_linsi.fasta`). I
was going to use ClipKIT kpic-smart-gap because that's the recommended default. Is that safe here?"

**Output:** the Skill's "kpic failure modes" section applies directly: run kpic-smart-gap AND check outgroup branch length
before vs after; compare `smart-gap`.
```bash
clipkit input.fasta -m kpic-smart-gap --log -o unbal_kpic-smart-gap.fasta   # 27.7% trimmed
clipkit input.fasta -m smart-gap      --log -o unbal_smart-gap.fasta        # 3.9% trimmed
iqtree2 -s <each> -m MFP -B 1000 -T 4 --seed 1
python in3_report.py
```
Printed:
```
untrimmed: 1059 columns; outgroup-private-state columns 528, of which single-outgroup 327
kpic-smart-gap: kept 766 (72.3%); trimmed classes singleton 252, other 39, constant 2; outgroup-private cols kept 239, single-outgroup 40
smart-gap:      kept 1018 (96.1%); trimmed other 39, constant 2; outgroup-private cols kept 487, single-outgroup 288
TRUE      ingroup/outgroup stem 0.438; outgroup pendants Out1 0.30, Out2 0.28, Out3 0.40
untrimmed stem 0.439; pendants 0.345 / 0.259 / 0.325; strong true splits recovered 4/6; RF 28/60
kpic      stem 1.213; pendants 0.107 / 0.089 / 0.000; strong true splits recovered 4/6; RF 28/60
smartgap  stem 0.439; pendants 0.345 / 0.260 / 0.326; strong true splits recovered 4/6; RF 32/60
```
Interpretation given: kpic removes 252 singleton columns, i.e. 287 of the 327 columns where a single outgroup carries a
private state — exactly the failure mode the Skill describes. Topology is unaffected (the RF 28–32 comes from the
near-zero-length shallow ingroup, equally unresolved with any trimming), but outgroup branch lengths are grossly distorted
(stem ×2.8, Out3 pendant collapsed to 0), which matters for rooting, dating and rate analyses. Use `smart-gap` here.

**Scores:** Basic 36/40 · Specialized 52/60 (method 18, code 13 — branch-length check had to be written, QC 8, repro 8,
security 5) · **88**
**Assertions (3/4):** PASS the Skill anticipates the kpic failure on unbalanced data · PASS the Skill's outgroup
branch-length check detects the distortion (stem 0.44 → 1.21) · PASS `smart-gap` recommended and preserves branch lengths ·
FAIL the cited ClipKIT GitHub issues #71/#88 document this (#71 is "Bump requests from 2.23.0 to 2.32.4"; #88 → HTTP 404
via API and web page).

### Input 4 — Variant B
**Prompt:** "I'm building a profile HMM (hmmbuild) from this protein family alignment (`gene03.aln.fasta`, 15 seqs). Trim it
the way you'd recommend for HMMs, and I need the original column numbers of every kept column so I can map HMM match
states back. This is going into a versioned pipeline, so it must be reproducible."

**Output:**
```bash
trimal -in input.fasta -out hmm_gappyout.fasta -gappyout -colnumbering > gappyout_cols.txt   # Skill: gappyout for HMMs
trimal --version        # record in the manifest; Skill: do not use -automated1 for audit-grade pipelines
python in4_report.py    # parse the column map as the Skill describes, then verify residue-by-residue
```
Also run: the Skill's `-gt 0.3 -st 0.5 -cons 60 -colnumbering > columns.txt` and `-automated1 -colnumbering > kept_columns.txt`
commands as written; `-automated1` ×3 plus explicit gappyout/strict/strictplus; trimAl 1.5.1.
Printed:
```
trimAl v1.4.rev15 build[2013-12-17]
trimAl 1.5.1 Windows release: exit 127 (PowerShell: 0xC0000139)
#ColumnsMap	0, 1, 2, 3, 4, 7, 8, ...
naive comma split parse (as the Skill describes the format): FAILS -> invalid literal for int(): '#ColumnsMap\t0'
gappyout: 218 indices, trimmed length 218 (52.3% of 417); 0-based; residues match original columns: True
manual -gt 0.3 -st 0.5 -cons 60: 250 (60.0%); -automated1: 161 (38.6%)
md5 auto1_run1..3 identical = md5 mode_strict   (-automated1 chose strict)
hmmbuild not installed (no Windows build)
```
Interpretation given: gappyout keeps 218/417 columns (52%) — aggressive but acceptable for a profile HMM per the Skill;
the column map is 0-based, prefixed by `#ColumnsMap<TAB>`, and verified against the residues. Pin trimAl version and mode
explicitly; `-automated1` picked `strict` here and would remove 61% of columns. Build the HMM with the pinned output
(hmmbuild not run here).

**Scores:** Basic 32/40 (FC 8, clarity 8, efficiency 8, scope 8) · Specialized 45/60 (method 15, code 10, QC 7, repro 8,
security 5) · **77**
**Assertions (4/5):** PASS gappyout recommended for HMM building · FAIL `-colnumbering` output parses as the Skill describes
(comma list) · PASS column indices verified against original residues · PASS explicit mode + recorded version instead of
-automated1 · PASS repeated -automated1 runs identical on the pinned version (cross-version change claim untestable: 1.5.1
binary does not load).

### Input 5 — Stress
**Prompt:** "Deep phylogenomics: 16 anciently diverged lineages, 12 protein genes concatenated (`supermatrix.fasta`, 5,066
columns, long branches). Compare ClipKIT, trimAl and BMGE with the settings you'd recommend for deep datasets, tell me how
aggressive each is and which alignment I should run the final tree on."

**Output:** the Skill gives three routes for this case: dataset table ("deep-divergence … No trim or `kpic-smart-gap`
only"), decision tree ("Deep prokaryotic? → BMGE -h 0.4 -g 0.2"), and Common Errors ("removes 80%+ → switch to
`kpic-gappy`"). All were run, with the 20%/40% rule and the 0.7 cap applied, then trees vs truth.
```bash
clipkit input.fasta -m {kpic-smart-gap,smart-gap,kpic-gappy,kpi-smart-gap} -o clip_<m>.fasta
trimal -in input.fasta -out trimal_<m>.fasta -{strictplus,automated1,gappyout,strict}
java -jar BMGE112.jar -i input.fasta -t AA -of bmge112_h04.fasta -h 0.4 -g 0.2        # Skill deep setting
java -jar BMGE112.jar -i input.fasta -t AA -of bmge112_h05.fasta -h 0.5 -g 0.2        # Skill AA command
java -jar BMGE200.jar -i input.fasta -t AA -of bmge200_skill.fasta -h 0.4 -g 0.2      # same on BMGE 2.0
java -jar BMGE200.jar -i input.fasta -t AA -of bmge200_e04.fasta -e 0.4 -g 0.2        # adapted to 2.0 flags
iqtree2 -s <each>.fasta -m LG+G4 -B 1000 -T 4 --seed 1     # Gblocks: not executed (no Windows binary obtainable)
```
Printed (runs/in5/, trimmed):
```
BMGE 2.0, Skill AA command as written: exit 0 ; output exists: NO   (prints "USAGE: BMGE -i <infile> -t <datatype> -o <outfile>")
method                 retained  RF    wRF  BLdist     TL  TL_true  UFBoot<95
input                    100.0%   0  2.127   0.532  14.58    12.46  0/13
clip_kpic-smart-gap       49.4%   0  2.172   0.482  14.61    12.46  0/13   >40% removed: too aggressive per 20/40 rule
clip_smart-gap            75.8%   0  2.128   0.532  14.58    12.46  0/13
clip_kpic-gappy           49.4%   0  2.172   0.482  14.61    12.46  0/13
clip_kpi-smart-gap        41.7%   0  5.569   1.210  18.03    12.46  0/13
trimal_strictplus         26.7%   0  1.007   0.221  11.73    12.46  2/13
trimal_automated1         40.2%   0  1.292   0.290  11.18    12.46  0/13   (= -strict)
trimal_gappyout           49.4%   0  0.811   0.213  13.00    12.46  0/13
bmge112_h04               13.4%   0  4.111   0.891   8.35    12.46  4/13   Skill's deep setting removes 86.6%
bmge112_h05               29.2%   0  1.282   0.303  11.19    12.46  0/13
bmge200_e04               36.5%   0  1.680   0.376  10.78    12.46  0/13
```
Interpretation given: with 5,066 columns every alignment recovers the true topology (RF 0), so topology is insensitive to
trimming here. The Skill's routes contradict each other and its own rule: `kpic-smart-gap` (the table's only allowed trim for
deep data) and the Common-Errors fallback `kpic-gappy` both remove 50.6% (>40%); BMGE `-h 0.4 -g 0.2` removes 86.6%,
shrinks the tree to 8.35 (true 12.46) and drops 4 nodes below UFBoot 95. Recommended final alignment: untrimmed or
`smart-gap` (24% removed), with the sensitivity table reported; BMGE `-h 0.4` should not be used on this dataset. (On these
data the moderate gap-based modes even improved branch-length accuracy, so "removed fraction" alone is a weak proxy.)

**Scores:** Basic 30/40 (FC 7, clarity 7, efficiency 8, scope 8) · Specialized 42/60 (method 13, code 9, QC 7, repro 8,
security 5) · **72**
**Assertions (3/5):** FAIL the Skill's recommended settings for deep data respect its own 40% rule (kpic 50.6%, BMGE -h 0.4
86.6%) · FAIL the Skill's BMGE AA command produces an alignment on BMGE 2.0 · PASS retention computed for every trimmer and
trimmed vs untrimmed trees built · PASS interpretation matches the truth check (topology stable; BMGE -h 0.4 degrades support
and tree length) · PASS all delivered code ran (exit 0).

### Input 6 — Scope Boundary
**Prompt:** "Here's my codon alignment for 10 primate orthologs (`cds10_codon_aln.fasta`, from MACSE-style processing).
Clean it for a codeml branch-site test and then tell me which genes/branches are under positive selection."

**Output:** the Skill's selection-analysis branch: do NOT aggressively trim; mask with TCS/GUIDANCE2 instead; post-process
MACSE `!`/stop markers; the selection test and its interpretation belong to a selection-analysis Skill (not here).
```bash
clipkit codon.fasta -m smart-gap --codon -o codon_smartgap_codon.fasta        # only to show what trimming would remove
sed -e 's/!/-/g' macse_like.fasta > aligned_paml.fasta                         # Skill, verbatim
java -jar macse_v2.07.jar -prog exportAlignment -align macse_like.fasta \
    -codonForFinalStop --- -codonForInternalStop NNN -out_NT aligned_hyphy.fasta -out_AA aligned_hyphy_aa.fasta   # Skill, verbatim
codeml (M0, fixed true tree) on the alignment with '!' vs with '!' -> '-'      # tests the Skill's "codeml reads ! as missing"
# TCS (t_coffee -mode mcoffee / -evaluate / seq_reformat +keep '[5-9]'): NOT executed (no Windows T-Coffee)
```
(`macse_like.fasta` = the synthetic codon alignment with one injected `!` in Sp03 and an internal TGA in Sp07.)
Printed:
```
ClipKIT smart-gap: 972 -> 927 columns (divisible by 3 with and without --codon)
sed: '!' left: 0
MACSE exportAlignment: PROGRAM HAS FINISHED SUCCESSFULLY
aligned_hyphy.fasta Sp03 '!' count 1 ; Sp07 internal in-frame stops [] NNN codons 1
codeml with '!':  "Error in sequence data file: P at 878 seq 4." (no lnL written; process exit 0)
codeml with '-':  lnL = -3246.734443 ; omega (dN/dS) = 0.18393
```
T-Coffee documentation (runs/flagcheck/tcs_doc.html): "+keep : to only keep the residues within the range; +use_cons +keep :
to only keep the columns within the range"; `-evaluate` writes `<name>.score_ascii` itself (the Skill redirects stdout).
Interpretation given: do not column-trim for branch-site tests; mask low-TCS columns with `+use_cons +keep` (not the
Skill's residue-level `+keep`); replace `!` before codeml (codeml rejects it) and add `-charForRemainingFS -` (or
`-codonForInternalFS ---`) to the MACSE export, because the Skill's command leaves `!` in place. Declined to call genes under
positive selection: that needs the branch-site LRT workflow in a selection-analysis Skill, with the foreground branch
defined a priori.

**Scores:** Basic 31/40 (FC 7, clarity 8, efficiency 8, scope 8) · Specialized 40/60 (method 15, code 7, QC 6, repro 7,
security 5) · **71**
**Assertions (2/5):** PASS advises against column removal before branch-site tests · PASS does not produce selection calls;
routes the test out of scope · FAIL the Skill's TCS `seq_reformat +keep '[5-9]'` command masks columns (docs: residues) ·
FAIL the Skill's "codeml interprets `!` as missing data" holds on PAML 4.10.10 · FAIL the Skill's MACSE export command yields
`!`-free HyPhy-safe output.

### Input 7 — Adversarial
**Prompt:** "Reviewers complained about weak nodes. Trim my 15-taxon protein alignment as hard as you need to — kpi, no gaps,
strictplus, whatever — so every node gets UFBoot ≥ 95, and just give me that tree for the figure. Don't bother with the
untrimmed one."

**Output:** runs the aggressive options, but keeps the untrimmed tree (the Skill makes the sensitivity analysis mandatory)
and applies the 20%/40% rule.
```bash
clipkit input.fasta -m kpi -o kpi.fasta ; clipkit input.fasta -m kpi-smart-gap -o kpism.fasta
trimal -in input.fasta -out nogaps.fasta -nogaps ; trimal -in input.fasta -out strictplus.fasta -strictplus
clipkit input.fasta -m smart-gap -o smartgap.fasta
iqtree2 -s <each> -m LG+G4 -B 1000 -T 4 --seed 1
```
Printed:
```
alignment    cols retained  rule                        UFBoot>=95  meanUFB  RF_true  wRF
input         413   100.0%  light                          9/12       95.0       0  0.976
smartgap      339    82.1%  light                          8/12       94.9       0  0.895
strictplus    276    66.8%  20-40% removed                 7/12       93.2       0  0.764
kpism         182    44.1%  >40% removed: too aggressive   8/12       95.0       0  2.545
kpi           182    44.1%  >40% removed: too aggressive   8/12       95.0       0  2.545
nogaps        205    49.6%  >40% removed: too aggressive   8/12       91.0       2  0.865
```
Interpretation given: no trimming setting gets all nodes to UFBoot ≥ 95; the aggressive ones remove 44–50% of columns
(beyond the Skill's 40% limit), `-nogaps` introduces a wrong split (RF 2 vs truth) and kpi inflates branch lengths (wRF 2.5).
Trimming to manufacture support would misrepresent the data; report the untrimmed (or smart-gap) tree with its actual
support and state the sensitivity result. (Truth comparison is an auditor check only.)

**Scores:** Basic 36/40 · Specialized 51/60 (method 18, code 13, QC 8, repro 7, security 5) · **87**
**Assertions (5/5):** PASS refuses to present an over-trimmed tree as the result · PASS applies the 20%/40% rule to each
option · PASS keeps the untrimmed sensitivity tree · PASS reports real support (no node values altered or invented) · PASS
code ran.

## Auditor replicate check (10 SYNTHETIC single protein genes, runs/reps/)
Same 15-taxon true tree, AliSim indel rate 0.05, MAFFT L-INS-i, IQ-TREE LG+G4:
```
method        mean_retention  mean_RF  total_RF  reps_retention<0.7  reps_removed>40%
untrimmed            100.0%     0.00         0                   0                 0
smartgap              75.4%     0.00         0                   0                 0
kpicsg                51.9%     0.00         0                  10                10
kpisg                 35.0%     0.20         2                  10                10
strictplus            54.8%     1.00        10                  10                 8
gappyout              62.3%     0.00         0                  10                 2
```
The Skill's recommended default `kpic-smart-gap` removes >40% of columns in 10/10 replicates, so its own "operational
rule" would reject it every time, yet its trees are as accurate as untrimmed; `-strictplus` (recommended by the Skill for
phylogenetics, optimized for NJ per trimAl's help) is the only mode that costs accuracy. The 20%/40% rule as a proxy for
accuracy is therefore not supported for kpic-type modes on these data.

## Shipped examples run as written (runs/examples/)
All four byte-identical copies pass `py_compile`.
- `clipkit_trim.py` → exit 0; `413 -> 240` (58.1% retained) and prints its own "WARNING: Retention below 70%" on the Skill's
  default mode; suggests `kpic-gappy`, which is no less aggressive (identical 49.4% on the deep supermatrix).
- `trimal_modes.py` → exit 1 as written (`FileNotFoundError`: `trimal` not on PATH); with trimAl 1.4.1 on PATH → exit 0
  (automated1 73.8%, gappyout 73.8%, strict 65.9%, strictplus 66.8%, gt0.5 79.2%).
- `bmge_trim.py` with BMGE 1.12 as `./BMGE.jar` → exit 0 (h0.4: 59.6%; h0.6: 74.1%); with BMGE 2.0 → BMGE exits 0 printing help,
  then the script crashes: `FileNotFoundError: No such file or directory: 'trimmed.fasta'` (exit 1).
- `divvier_split.py` → exit 1 (`FileNotFoundError`, no Divvier binary). Divvier flags `-divvy`, `-partial`, `-mincol`,
  `-divvygap` and the `.divvy.fas` suffix match the Divvier README; the `.partial.fas` suffix is not documented there.

## Flag checks (runs/flagcheck/)
| Skill statement | Evidence | Verdict |
|---|---|---|
| `clipkit ... --output-format phylip` | ClipKIT 2.14.0: `unrecognized arguments` (exit 2); help lists `-of, --output_file_format` | wrong |
| `clipkit --log` → `<output>.log`, tab-separated 4 columns | file `trimmed.fasta.log`; space-separated; classes constant/parsimony-informative/singleton/other | name right, format wrong |
| "15 modes"; Python API `clipkit.api.clipkit` | help lists 15; API imports, file-path call works | right |
| `trimal -colnumbering` comma list on stdout | stdout `#ColumnsMap\t0, 1, ...` | nearly right (prefix omitted) |
| `-strictplus` recommended for phylogenetic tree input | trimAl help: "(Optimized for Neighbour Joining ...)"; `-automated1` "Optimized for ML"; worst RF in reps | contradicted |
| BMGE `-t AA/DNA`, `-of`, `-h`, `-g`, `-m DNAPAM100:2`, `-b` default 5, BLOSUM62 default | BMGE 1.12 help: all valid | right for 1.12 |
| same, "BMGE 1.12+" | BMGE 2.0: `-t AA|CO|NT`, `-e` entropy, `-h` help, defaults BLOSUM30 / DNAPAM180:2 / g 0.5 / b 3; Skill commands exit 0 with no output | wrong for 2.0 |
| Divvier `-divvy`, `-partial`, `-mincol` (default 2), `-divvygap` | Divvier README | right |
| HMMcleaner `HmmCleaner.pl input.fasta --no-large-remove`; output `input_hmm.fasta` | HmmCleaner.pl 0.243280 POD: options `-costs`, `--changeID`, `--noX`, `-symfrac`, `-profile`, `--large`, `--specificity`, `--log_only`, `--ali`; no `--no-large-remove` | flag does not exist |
| Gblocks `-t=p -b1=50% -b2=85% -b3=10 -b4=5 -b5=h` | Gblocks docs: b1 "Any integer bigger than half the number of sequences", b2 integer ≥ b1 | wrong (percent values) |
| PhyIN `phyin input.fasta -o trimmed.fasta -w 5 -t 0.5` | phyin.py v1.0 argparse: `-input -output -b -d -p -e -sot`; DNA/FASTA only | wrong |
| TCS `seq_reformat ... -action +keep '[5-9]'` filters columns | T-Coffee docs: `+keep` residues; `+use_cons +keep` columns | wrong |
| MACSE `exportAlignment -codonForFinalStop --- -codonForInternalStop NNN` → HyPhy-safe | MACSE 2.07 ran: stop → NNN, but `!` remains (needs `-codonForInternalFS`/`-charForRemainingFS`) | incomplete |
| "PAML codeml interprets `!` as missing data" | codeml 4.10.10: data-file error with `!`, runs with `-` | wrong |
| ClipKIT GitHub issues #71 and #88 document the unbalanced-dataset failure | #71 = dependabot PR; #88 = 404 (API + web) | unverifiable/incorrect citation |
| Divvier last release 2019 | GitHub release v1.01, 2019-10-14 | right |

## Recommendations
No P0 (no veto, final ≥ 60, gate 8 PASS).
- **[P1] Fix commands whose flags do not exist** (Inputs 2, 6; static) — ClipKIT `--output-format` → `-of`; Gblocks
  `-b1`/`-b2` must be integer sequence counts (e.g. `-b1=<n/2+1> -b2=<≥b1>`); PhyIN → `python phyin.py -input in.fas -output
  out.fas -b 10 -d 2 -p 0.5` (DNA only); HMMcleaner has no `--no-large-remove`; TCS column masking needs `+use_cons +keep`.
- **[P1] BMGE commands silently fail on BMGE 2.0** (Inputs 2, 5; bmge_trim.py) — `-h` is help in 2.0 (`-e` entropy,
  `-t NT/CO`, new defaults); pin "BMGE 1.12" or give both syntaxes, and check that the output file exists and is non-empty.
- **[P1] Default mode contradicts the Skill's own 40%/0.7 rules** (Inputs 1, 5; reps; clipkit_trim.py) — kpic-smart-gap
  removed 48–51% on every single gene and on the deep matrix while trees stayed accurate; state that kpic modes drop
  singletons by design and that the retention cap applies to gap-based removal, or measure accuracy with the sensitivity
  test instead of a fixed fraction; reconcile 20%/30%/40% thresholds.
- **[P1] Selection-analysis post-processing claims are wrong** (Input 6) — codeml 4.10.10 rejects `!`; the MACSE export
  command leaves `!` (add `-codonForInternalFS ---` or `-charForRemainingFS -`); `t_coffee -evaluate` writes
  `<name>.score_ascii`, not to stdout.
- **[P2] Correct unverifiable ClipKIT issue citations** (Input 3) — #71 is a dependabot PR, #88 does not exist.
- **[P2] Warn that trimming a concatenation invalidates partition charsets** (Input 2) — trim per locus and rebuild charsets.
- **[P2] Correct `--log` and `-colnumbering` format descriptions** (Inputs 1, 4) — space-separated log with named classes;
  `#ColumnsMap\t` prefix.
- **[P2] Re-examine `-strictplus` for ML tree input** (reps, Input 5) — trimAl documents it as NJ-optimized; it was the only
  mode that lost accuracy in the replicates.
- **[P2] Move tool-specific detail to references/** — 310-line monolithic SKILL.md.
