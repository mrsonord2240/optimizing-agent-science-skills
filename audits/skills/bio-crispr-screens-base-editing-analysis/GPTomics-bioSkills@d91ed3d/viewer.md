> **Audit record for `bio-crispr-screens-base-editing-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/crispr-screens/base-editing-analysis) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-base-editing-analysis
Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:crispr-screens/base-editing-analysis`
(Identical byte-for-byte to the `mrsonord2240/bioSkills` fork copy — diffed, no changes; this is not a fixed-Skill re-audit.)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical — CBE library design (find_be_spacers) | 16 | 20 | 36 | 2/4 | ❌ |
| 2 | Variant A — editing-efficiency filtering | 10 | 15 | 25 | 2/4 | ❌ |
| 3 | Edge — ABE7.10 zero-bystander search | 24 | 32 | 56 | 3/4 | ⚠️ |
| 4 | Variant B — bystander deconvolution | 18 | 30 | 48 | 2/4 | ❌ |
| 5 | Stress — hit-calling aggregation | 12 | 18 | 30 | 2/4 | ❌ |
| 6 | Scope Boundary — BE-Hive prediction | 24 | 34 | 58 | 2/4 | ⚠️ |
| 7 | Adversarial — Cas9-contamination diagnostic | 32 | 44 | 76 | 4/4 | ✅ |

**Execution Average: 47.0 / 100**
**Assertion Pass Rate: 17/28**

**Static Score: 65/100 → Static Weighted 26.0**
**Dynamic Weighted: 28.2**
**FINAL SCORE: 54/100 — ❌ Reject**
**Research Veto: FAIL (M4 Code Usability)** — `deployable: false`, `veto_override: true`

## Method note

No genuine base-editing amplicon FASTQ exists in CRISPResso2's published test set (only Cas9-nuclease
samples — see `public-data/editing/README.md`). Per the audit brief, a synthetic CBE amplicon was built
(`run/make_synthetic_be_fastq.py`) with a 20nt protospacer containing a target C at spacer position 5 and
a bystander C at spacer position 7 (both inside the canonical BE4/CBE editing window, positions 4–8), and
200 single-end reads split into four planted populations: 40% unmodified, 30% target-only, 20%
target+bystander, 10% bystander-only. This gives ground truth of 50.00% target editing and 30.00%
bystander editing. Data lives in `data/synthetic_cbe.fastq` and `data/ground_truth.txt`.

CRISPResso2 2.3.4 (Docker `pinellolab/crispresso2:latest`) was run against this FASTQ with
`--base_editor_output --conversion_nuc_from C --conversion_nuc_to T --quantification_window_size 10
--quantification_window_center -10`, exactly the flags in the Skill's own bundled example
(`examples/base_editing_analysis.sh`). Output: `CRISPResso_quantification_of_editing_frequency.txt`
reports Modified% = 60.0% (= 60% "any edit" = target-only + target+bystander + bystander-only, matching
plant exactly: (60+40+20)/200 = 60%). All four of the Skill's bundled Python functions
(`find_be_spacers`, `filter_by_editing_efficiency`, `deconvolute_bystander`, `aggregate_variant_scores`)
were copied verbatim from SKILL.md and run against this real CRISPResso2 output and a real MAGeCK
`sgrna_summary.txt` (reused from the sibling `bio-crispr-screens-mageck-analysis` audit's own verified
real-data run).

**Docker note:** the bind-mount to this candidate's shared `audit-envs\crispr-screen-analyst` tree was
found hung (Docker Desktop's Hyper-V file-sharing grant had gone stale — even the pre-existing
`crispresso2-tests` folder used successfully by the tooling pass no longer mounted). Confirmed via a
minimal `alpine ls /DATA` reproduction before touching anything shared. Took the candidate's install
lock, killed the two hung `docker run` client processes, ran `docker desktop restart`, confirmed all
pre-existing containers (penpot stack, litellm-proxy) recovered automatically, verified the mount worked
again, then released the lock. No package versions were touched.

## Detailed Outputs

### Input 1 — Canonical: CBE library design (`find_be_spacers`, BE4max)

**Prompt:** "Design a CBE saturation library tiling BRCA1 RING domain (amino acids 1-100). 10-15 sgRNAs
per amino acid where at least one C in the editing window (positions 4-8) hits the target codon.
Annotate each sgRNA with predicted target + bystander variants."

**Code run** (`run/test_find_be_spacers.py`, `find_be_spacers` copied verbatim from SKILL.md):
```python
def find_be_spacers(cds_sequence, cds_protein_start, target_aa, target_base='C', editor='BE4max'):
    window_by_editor = {'BE3': (4, 8), 'BE4max': (4, 8), 'eA3A-BE3': (5, 7),
                         'ABE7.10': (4, 7), 'ABE8.20': (4, 8), 'ABE8e': (4, 8), 'evoCDA-BE': (1, 9)}
    ...
    for strand, seq in [('+', cds_sequence), ('-', str(Seq(cds_sequence).reverse_complement()))]:
        for pam_match in pam_pattern.finditer(seq):
            ...
            genomic_pos = spacer_start + i - 1
            if target_codon_start <= genomic_pos < target_codon_end:
                target_position_in_spacer.append(i)
```

**Output:** Completed, 21 candidates for target_aa=40 on a synthetic 300nt CDS (100 codons, seeded).
One candidate flagged on-target: `{'spacer': 'CCATCGGCATATCAAGAAAT', 'strand': '-', 'spacer_start': 110,
'target_positions': [8], 'bystander_positions': [5]}`.

**Independent verification (bug found):**
```
genomic_pos (as computed by the code, in reverse-complement index space): 117
Codon window compared against (forward CDS coords): [117, 120)
Is genomic_pos in [117,120)? -> True    <- this is what the code checks and accepts

TRUE forward-CDS index this base actually occupies: 182   (= len(cds)-1-genomic_pos)
cds[182]: G   (not part of codon 40 at all)
Is true_forward_index in the real target codon [117,120)? -> False
```
For strand `'-'`, `seq` is the reverse complement of the CDS, so `genomic_pos` lives in reverse-complement
index space. The code never converts it back to forward-CDS coordinates before comparing against
`target_codon_start`/`target_codon_end` (always forward-strand). The one on-target call this run produced
is confirmed wrong — the real edited base is 65nt from the intended codon. No exception, no warning: a
silently wrong result.

**Scores:** Basic: 16/40 | Specialized: 20/60 | Total: 36/100
**Assertions:**
- [PASS] find_be_spacers scans both strands for candidate NGG-adjacent spacers
- [FAIL] On-target hits reported by the function are genuinely within the intended codon — confirmed false for the one hit found
- [FAIL] No silent, unflagged coordinate error for reverse-strand candidates — confirmed present
- [PASS] Function completes without raising an exception on a realistic synthetic CDS

---

### Input 2 — Variant A: editing-efficiency filtering (`filter_by_editing_efficiency`)

**Prompt:** "Run CRISPResso2 on my pilot timepoint samples. Compute target editing % per sgRNA. Keep
sgRNAs >30% target editing for the primary screen."

**Code run** (`run/test_filter_by_editing_efficiency.py`):
```python
df = pd.read_csv(quant_file, sep='\t')
target_row = df[df['Position'] == target_pos]     # <- crashes here
original_pct = target_row[target_base].values[0]
```

**Real file structure** (`Quantification_window_nucleotide_percentage_table.txt` from this audit's
synthetic CRISPResso2 run):
```
Columns: ['Unnamed: 0', 'T', 'G', 'A', 'T.1', 'C', 'A.1', 'C.1', 'G.1', 'T.2', ...]
Row labels (first column): ['A', 'C', 'G', 'T', 'N', '-']
```
The real file is the **transpose** of what the function assumes: rows are nucleotide identities, columns
are per-window-position reference bases (duplicated names, pandas-suffixed `.1`, `.2`, ...). There is no
`'Position'` column anywhere.

**Output:**
```
CRASHED: KeyError: 'Position'
```
This is the same defect class (assumed-vs-real CRISPResso2 file schema mismatch) already flagged as a P0
in the sibling `bio-crispr-screens-crispresso-editing` audit — confirmed to recur here, in a different
function, exactly as the brief warned.

**Scores:** Basic: 10/40 | Specialized: 15/60 | Total: 25/100
**Assertions:**
- [FAIL] filter_by_editing_efficiency runs without error against real CRISPResso2 output
- [FAIL] The function's assumed table orientation matches the real file
- [PASS] The editing-efficiency threshold convention (>=30%/>=50%) is methodologically sound
- [PASS] Failure is a loud exception rather than a silently wrong number

---

### Input 3 — Edge: ABE7.10 zero-bystander search (`find_be_spacers`, target_base='A')

**Prompt:** "I need to install MLH1 c.677A>G as a single intended variant. Find ABE7.10 sgRNAs that
place A at position 5 with no bystanders. If none exists, list candidates sorted by bystander_count and
recommend prime editor as alternative."

**Output:** Completed, 20 candidates on the same synthetic CDS (target_aa=60, target_base='A',
editor='ABE7.10'). Zero candidates with both an on-target hit and n_bystanders==0 — consistent with the
Skill's documented fallback. `window_by_editor['ABE7.10'] = (4, 7)`, an exact match to SKILL.md's table.
The reverse-strand coordinate bug from Input 1 is still present in this code path (it happened not to
surface here only because no on-target hit was found in this run).

**Scores:** Basic: 24/40 | Specialized: 32/60 | Total: 56/100
**Assertions:**
- [PASS] Function completes without error for editor='ABE7.10', target_base='A'
- [PASS] Output supports the Skill's documented recommend-PE fallback when no zero-bystander candidate exists
- [FAIL] Target/bystander classification is coordinate-correct for reverse-strand candidates
- [PASS] ABE7.10's window (4,7) in the code matches the Skill's own stated table

---

### Input 4 — Variant B: bystander deconvolution (`deconvolute_bystander`)

**Prompt:** "From CRISPResso2 allele tables, separate reads by edit pattern: target only,
target+bystander_1, target+bystander_2. Compute per-pattern fitness contribution."

**Code run** (`run/test_deconvolute_bystander.py`):
```python
alleles = pd.read_csv(allele_table_path, sep='\t', compression='zip')
...
return alleles.groupby([...])['Reference_pct'].sum().reset_index()   # <- crashes here
```

**Real file** (`Alleles_frequency_table.zip`): columns are
`['Aligned_Sequence', 'Reference_Sequence', 'Reference_Name', 'Read_Status', 'n_deleted', 'n_inserted',
'n_mutated', '#Reads', '%Reads']` — no `Reference_pct` column.

**Output:**
```
CRASHED: KeyError: 'Column not found: Reference_pct'
```
Patched only the column name to `'%Reads'` and re-ran:
```
   target_edited  bystander_69_edited  %Reads
0          False                False    40.0
1          False                 True    10.0
2           True                False    30.0
3           True                 True    20.0
```
Exact match to the planted ground truth (unmodified 40%, bystander-only 10%, target-only 30%,
target+bystander 20%). The position-indexing logic itself is correct; only the column name is wrong.

**Scores:** Basic: 18/40 | Specialized: 30/60 | Total: 48/100
**Assertions:**
- [FAIL] deconvolute_bystander runs without error against a real allele table
- [FAIL] The read-fraction column name matches the real CRISPResso2 output
- [PASS] Once corrected, the partition matches the planted ground truth exactly
- [PASS] The str-indexing logic for detecting an edit at a given position is sound

---

### Input 5 — Stress: hit-calling aggregation (`aggregate_variant_scores`)

**Prompt:** "Apply MAGeCK MLE to the BE screen counts. Aggregate per-sgRNA LFC to per-variant scores."

**Code run:**
```python
df = mageck_sgrna_summary.merge(variant_annotation_df, on='sgRNA')   # <- crashes here
```

**Real MAGeCK output** (reused from the sibling `bio-crispr-screens-mageck-analysis` audit's own
verified real-data run, `input1_canonical.sgrna_summary.txt`): columns
`['sgrna', 'Gene', 'control_count', 'treatment_count', ..., 'LFC', ...]` — lowercase `sgrna`.

**Output:**
```
CRASHED: KeyError: 'sgRNA'
```
Corrected to merge on `'sgrna'`: the groupby/aggregation (mean/std/count of LFC per `target_variant`,
target-only vs mixed split) then produces the expected shape with no further issues.

**Scores:** Basic: 12/40 | Specialized: 18/60 | Total: 30/100
**Assertions:**
- [FAIL] aggregate_variant_scores merges cleanly against real MAGeCK output
- [FAIL] The sgRNA-identifier column name matches real MAGeCK output
- [PASS] The aggregation logic itself is sound
- [PASS] No fabricated per-variant fitness values are produced

---

### Input 6 — Scope Boundary: BE-Hive editing-efficiency prediction

**Prompt:** "Predict editing efficiency and bystander outcomes for my designed CBE guide using BE-Hive."

The Skill's *entire* guidance on BE-Hive: *"Python: BE-Hive (Arbab 2020) for editing-efficiency
prediction; clone maxwshen/be_predict_bystander and import via sys.path."* No code, no mention of its
50nt-substrate convention.

**First attempt** (naively following BE-Hive's README arithmetic literally: "positions -19 to 30"
implies 19nt of upstream context) produced a substrate where BE-Hive's own diagnostic field disagreed
with the intended spacer:
```
Assumed protospacer sequence: GATCACGTAGCATGCACGTT     <- BE-Hive's own read-back
Intended protospacer:         TGATCACGTAGCATGCACGT     <- what was actually meant
```
A 1-nucleotide frame shift: BE-Hive's actual internal convention needs 20nt of upstream context (position
1 of the spacer maps to substrate index 20, not 19), which is *not* obvious from the README's stated
"-19 to 30" numbering alone.

**Corrected run** (`run/behive_predict_test.py`):
```
Model successfully initialized. Settings: celltype: mES, base_editor: BE4
=== stats ===
  Total predicted probability: 0.9795
  Assumed protospacer sequence: TGATCACGTAGCATGCACGT   <- now matches intended spacer exactly
=== pred_df (top rows) ===
  columns include C4, C6 (BE-Hive's own 1-indexed editable-C positions)
```
BE-Hive's `C4` and `C6` columns correspond exactly to this audit's planted target (spacer position 5) and
bystander (spacer position 7) once BE-Hive's own internal numbering (offset by one from a naive reading of
its README) is reconciled — confirmed by direct index arithmetic. The tool itself works and gives a
correct answer; the risk is entirely in the Skill's total silence on how to correctly interface with it.

**Scores:** Basic: 24/40 | Specialized: 34/60 | Total: 58/100
**Assertions:**
- [FAIL] An agent can construct a valid BE-Hive input from the Skill's own guidance alone
- [PASS] BE-Hive prediction runs to completion using the maintainers' documented API
- [PASS] Predicted output correctly reflects the true editable C positions in the designed guide
- [FAIL] Skill warns that BE-Hive's internal position numbering can differ from its own PAM-distal 1-8 convention

---

### Input 7 — Adversarial: Cas9-contamination diagnostic

**Prompt:** "My BE sample has 70% editing but 25% indels — diagnose: is this Cas9 contamination?"

**Real data used:** `CRISPResso_quantification_of_editing_frequency.txt` for `FANC.Cas9.fastq` (cached
from the sibling `bio-crispr-screens-crispresso-editing` audit's own verified real-data run) —
Insertions=8, Deletions=49, Substitutions=7. This sample is independently known to be genuinely
Cas9-nuclease-edited (not BE), so it is real ground truth for this diagnostic.

**Applying the Skill's stated threshold:** substitution-vs-indel ratio = 7 / (8+49) = **0.12**, well under
the Skill's own `<3` "Cas9-like" cutoff — correctly classifies this real sample as Cas9 contamination /
wrong chemistry, matching its true known origin.

**Scores:** Basic: 32/40 | Specialized: 44/60 | Total: 76/100
**Assertions:**
- [PASS] The ratio threshold correctly classifies a real, independently-known Cas9-edited sample as Cas9-like
- [PASS] Diagnostic reasoning does not fabricate a root cause
- [PASS] Skill gives an actionable fix (verify vector, confirm cell line, pilot first)
- [PASS] No claim that this ratio is computed by any of the Skill's bundled Python functions

---

## Research Veto

| Dimension | Result |
|---|---|
| M1 Scientific Integrity | PASS |
| M2 Practice Boundaries | PASS |
| M3 Methodological Ground | PASS |
| M4 Code Usability | **FAIL** — 3 of 4 bundled functions crash on real CRISPResso2/MAGeCK output (KeyError on wrong assumed schema/column name in every case); the 4th silently misattributes reverse-strand target/bystander calls. |

## Note for reviewer

All four ❌/⚠️ rows trace to the same root pattern: every one of the Skill's bundled Python functions
was written against an *assumed* file schema (from CRISPResso2, MAGeCK) that does not match the real
tool's real output, and none of the four appears to have been run against real data before shipping. This
is a structural authoring gap, not four unrelated bugs — worth fixing as one pass (add a schema-assertion
line to each function and re-verify against one real run of each upstream tool) rather than four separate
patches.
