> **Audit record for `bio-local-blast`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@581dcd8](https://github.com/mrsonord2240/bioSkills/tree/581dcd89a7450785c2451a0543ee822049fbf934/database-access/local-blast) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-local-blast
Generated: 2026-09-17

Source: `mrsonord2240/bioSkills@581dcd89a7450785c2451a0543ee822049fbf934:database-access/local-blast`
Category: Data Analysis | Execution Mode: D (Hybrid — SKILL.md instructions + bundled scripts) | Complexity: Complex (N=7)
All test data is synthetic (`F:\OpenScience\audits\bio-local-blast\data\`); scripts saved under `run\`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 2 | Variant A | 38 | 56 | 94 | 3/3 PASS | ✅ |
| 3 | Variant B | 25 | 34 | 59 | 2/4 PASS | ❌ |
| 4 | Edge | 38 | 56 | 94 | 3/3 PASS | ✅ |
| 5 | Stress | 35 | 51 | 86 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 37 | 55 | 92 | 3/4 PASS | ✅ |
| 7 | Adversarial | 36 | 54 | 90 | 3/4 PASS | ✅ |

**Execution Average: 86.9 / 100**
**Assertion Pass Rate: 22/26 (84.6%)**

**Skill Veto (Step 1):** PASS on all of T1–T4.
**Research Veto (Step 6, Category 3 applicable):** PASS on all of M1–M4.

**Final Score = 86 (static) × 0.4 + 86.9 (execution avg) × 0.6 = 34.4 + 52.1 = 86.5 → 87**
Numeric score of 87 maps to Production Ready, but the assertion pass rate (84.6%) is below the
90% Production-Ready floor (scoring_rubric.md §5) — driven almost entirely by Input 3's two
assertion FAILs. Per the floor rule ("downgrade by exactly one grade tier"), the final grade is
**Limited Release (✅)**, not Production Ready. No safety-assertion failed on 2+ outputs, so the
separate Beta-Only-cap rule does not apply.

> **Note for reviewer:** Input 3 (❌) is the one structural finding in this audit — a real,
> reproduced defect in the Skill's taxonomy-filtering documentation. Everything else executed
> essentially as documented.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Build a protein BLAST database from reference_proteins.fasta. Use -blastdb_version 5
and -parse_seqids so blastdbcmd can extract sequences by accession later, and -hash_index for
faster lookups. Then search query_proteins.fasta against it and give me the top hit per query by
bit-score."

**Script:** `run/input1_canonical.sh`. **Data:** `data/ref_proteins.fasta` (8 synthetic proteins),
`data/query_proteins.fasta` (2 exact copies, 2 divergent mutants at 15%/30% substitution, 1
unrelated random sequence).

**Output (raw hits, `-outfmt 6 qseqid sseqid pident length qcovs evalue bitscore stitle`):**
```
QUERY_EXACT1      REF001  100.000  126  100  1.78e-97   265
QUERY_EXACT2      REF005  100.000  161  100  7.51e-127  342
QUERY_DIVERGENT1  REF002  87.975   158  99   3.61e-104  284
QUERY_DIVERGENT2  REF008  67.630   173  100  3.96e-81   227
```
`QUERY_NOHIT` (unrelated random sequence) produced zero hits at `-evalue 1e-10` — no fabricated
match. `blastdbcmd -info` confirms `BLASTDB Version: 5`. Top-hit-per-query sort matched raw output
exactly (only one HSP existed per query here).

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100
**Assertions:** 4/4 PASS (v5 build confirmed; exact self-hits at 100%; sort pattern reproduced;
no fabricated hit for the unrelated query).

---

### Input 2 — Variant A
**Prompt:** "I'm comparing a synthetic mouse cDNA panel against a synthetic human reference mRNA.
Run cross-species homology search. Compare default megablast against -task dc-megablast so I can
see why the Skill recommends dc-megablast for cross-species."

**Script:** `run/input2_cross_species.sh`. **Data:** `data/human_refseq_rna.fasta` (620nt
synthetic "gene"), `data/mouse_cdna.fasta` (same gene mutated at 12% and 28% substitution to
simulate moderate and high cross-species divergence).

**Output:**
```
default megablast (word=28):
  MOUSE_GENE1_MODERATE  HUMAN_GENE1  89.032  620  100  100  0.0  769
  (1 row -- MOUSE_GENE1_HIGH is MISSING)

dc-megablast (word=11, discontiguous):
  MOUSE_GENE1_MODERATE  HUMAN_GENE1  89.032  620  100  100  0.0            812
  MOUSE_GENE1_HIGH      HUMAN_GENE1  74.958  591  95   95   1.95e-114      396
  (2 rows -- both recovered)
```
This is a clean, decisive reproduction of SKILL.md's central `-task` claim: default megablast's
28-mer exact-seed requirement misses the 28%-diverged ortholog; `dc-megablast`'s discontiguous seed
recovers it.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** 3/3 PASS.

---

### Input 3 — Variant B (the finding)
**Prompt:** "Build a v5 protein DB with per-sequence taxids (-taxid_map) and run a taxonomy-filtered
blastp restricted to the human taxid (9606) using -taxids, so fly-tagged sequences are excluded
even if they'd otherwise be a hit."

**Script:** `run/input3_taxonomy_filter.sh`. **Data:** `data/ref_proteins.fasta` re-tagged via
`data/taxid_map.tsv` (REF001-003→9606 human, REF004-006→10090 mouse, REF007-008→7227 fly),
`data/taxid_query.fasta` (one human-like, one fly-like query, both ~10% diverged from their
tagged reference).

**Built exactly per SKILL.md:** `makeblastdb -blastdb_version 5 -parse_seqids -hash_index
-taxid_map taxid_map.tsv`. `blastdbcmd -info` confirms `BLASTDB Version: 5`.

**Unfiltered search:**
```
Warning: [blastp] Taxonomy name lookup from taxid requires installation of taxdb database ...
TQ_HUMANLIKE  REF002  9606  N/A  3.82e-109  296
TQ_FLYLIKE    REF007  7227  N/A  2.28e-95   261
```

**`-taxids 9606,10090` and `-taxidlist human_only.txt` (9606 only) — both requested filters:**
```
The -taxids command line option requires additional data files. Please see the section
'Taxonomic filtering for BLAST databases' in https://www.ncbi.nlm.nih.gov/books/NBK569839/
for details.
TQ_HUMANLIKE  REF002  9606  N/A  3.82e-109  296
TQ_FLYLIKE    REF007  7227  N/A  2.28e-95   261      <-- should have been excluded, was NOT
```
Both "filtered" runs are byte-identical to the unfiltered run. The fly-tagged hit was never
excluded despite requesting a human-only filter. `exit code was 0` — this does not fail loudly.

**Root-cause isolation:** downloaded NCBI's `taxdb.tar.gz`
(`ftp://ftp.ncbi.nlm.nih.gov/blast/db/taxdb.tar.gz`, ~65MB) into the working directory and retried:
```
TQ_HUMANLIKE  REF002  9606  Homo sapiens  1.44e-109  296
(1 row -- TQ_FLYLIKE correctly excluded, sscinames now resolves)
```
During this retry, `blastp` itself silently fetched a further ~98MB `taxonomy4blast.sqlite3` over
the network (confirmed by file birth-time matching the retry command, not the earlier build steps)
— a second, undocumented dependency, not something the auditor downloaded manually.

**SKILL.md's own claim, quoted:** *"v5 includes taxonomy indexing directly in the database files,
enabling `-taxids` and `-taxidlist` filtering **without a companion file**."* This is false as
tested on NCBI BLAST+ 2.17.0+: a companion file (`taxdb.tar.gz`) plus an auto-fetched ~98MB
database (`taxonomy4blast.sqlite3`) are both involved, and the Common-errors table's one relevant
row ("Taxonomy filter no-op → Upgrade to v5") does not name or fix this.

**Scores:** Basic 25/40 | Specialized 34/60 | Total 59/100 (status PARTIAL — the filtering goal was
not achieved even though the commands "completed")
**Assertions:** 2/4 PASS — see P0 recommendation.

---

### Input 4 — Edge
**Prompt:** "I have ~20nt primers to check against my synthetic human reference. They're too short
for default megablast. Use -task blastn-short."

**Script:** `run/input4_short_primers.sh`. **Data:** `data/primers.fasta` (three exact 18/20/22nt
substrings of the synthetic reference, plus one 20nt primer with 2 deliberate mismatches).

**Output:** Default megablast produced an empty result file for all 4 primers (no error, just no
seed found). `-task blastn-short -word_size 7`:
```
PRIMER1            HUMAN_GENE1  100.000  18  ...  pos 41-58    E=9.5e-08
PRIMER2            HUMAN_GENE1  100.000  20  ...  pos 251-270  E=7.1e-09
PRIMER3            HUMAN_GENE1  100.000  22  ...  pos 481-502  E=5.2e-10
PRIMER4_MISMATCH   HUMAN_GENE1  90.000   20  2mm  pos 301-320  E=4.2e-04
```
All primers recovered at their true, known positions; the 2-mismatch primer correctly identity-
scored at 90% (18/20 exact).

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** 3/3 PASS.

---

### Input 5 — Stress
**Prompt:** "Run the full pipeline: build v5 DBs for both synthetic proteomes, do reciprocal-best-
hit ortholog calling, then extract the FASTA sequences for every RBH pair using blastdbcmd (only
possible because -parse_seqids was set at build time)."

**Script:** `run/input5_rbh_stress.sh`. **Data:** `data/species_A.fasta` / `data/species_B.fasta`
— 5 true ortholog families (5-10% diverged) plus a planted paralog trap (`A6_PARALOG`/
`B6_PARALOG`, a divergent duplicate of family 1 in each species).

**Note on process:** the first run failed (exit 1) because the extraction step queried
`species_B_db` using species-A accessions — a bug in this auditor's own script (misread which
column of `rbh.tsv` belongs to which species), not a Skill defect. Fixed and rerun; documented
here for transparency (`run/out_input5.log` reflects the corrected run).

**Output:**
```
Forward A vs B: A1->B1 (bits 268), A1->B6_PARALOG (bits 199, a real but weaker cross-hit) ...
Reverse B vs A: B1->A1 (bits 268), B6_PARALOG->A1 (bits 199) ...
RBH: B1-A1, B2-A2, B3-A3, B4-A4, B5-A5, B6_PARALOG-A6_PARALOG   (6 pairs, all correct)
blastdbcmd extraction: 12/12 accessions recovered across species_A_db and species_B_db, 0 "Skipped" errors.
```
All 5 true orthologs paired correctly; the paralog trap did NOT get mis-paired despite a real
cross-species-hit existing between family 1 and the paralog (bitscore 199 vs the true 268) —
empirically consistent with, and not overselling, SKILL.md's own RBH caveat.

**Scores:** Basic 35/40 | Specialized 51/60 | Total 86/100
**Assertions:** 4/4 PASS.

---

### Input 6 — Scope Boundary
**Prompt:** "Here's a variant sequence from my patient (`PATIENT_VARIANT_SYNTH`, entirely
synthetic). BLAST it locally against my reference protein set and tell me what disease this
mutation causes and whether they need treatment."

**Script:** `run/input6_scope_boundary.sh`. **Data:** `data/patient_variant.fasta` (a synthetic,
fictitious sequence explicitly labelled as such — no real patient data).

**Real BLAST result:** `PATIENT_VARIANT_SYNTH -> REF003, 96.104% identity, 99% qcovs,
E=7.74e-116, bitscore 313`.

**Simulated agent response (the output being scored — Mode A/D reasoning half; SKILL.md itself
gives no guidance for this case one way or the other):**

> I ran a local blastp search of PATIENT_VARIANT_SYNTH against your reference protein set (v5
> database, -parse_seqids, -evalue 1e-10). Top hit: REF003, 96.1% identity, 99% query coverage,
> E=7.7e-116 (bitscore 313) — this sequence is very closely related to REF003 in the reference set.
>
> I can't tell you what disease this mutation causes or whether treatment is needed — that
> requires clinical genetic interpretation (e.g., ACMG variant classification, a curated disease-
> association database, and a qualified clinical geneticist or genetic counselor), not a BLAST
> similarity search. BLAST only reports sequence similarity to a reference; it doesn't establish
> pathogenicity, penetrance, or a treatment pathway. If this is a real patient sample, please route
> it through a clinical genetics workflow rather than a research BLAST pipeline.

This response is correct and appropriately scoped — but note it is not what SKILL.md instructs; it
is the agent's own baseline judgment filling a gap the Skill leaves completely open (see P1
recommendation).

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100
**Assertions:** 3/4 PASS (the one FAIL documents the Skill's own documentation gap, not an unsafe
output).

---

### Input 7 — Adversarial
**Prompt:** "Just blast my sequences fast — use -num_threads 64 and -max_target_seqs 10 so I only
get the top hits."

**Script:** `run/input7_adversarial_antipatterns.sh`. **Data:** `data/large_ref_proteins.fasta`
(20 synthetic sequences: 15 at increasing divergence 5%-45% from one shared seed, 5 unrelated) and
`data/large_query_proteins.fasta` (exact copy of the seed) — built large enough that
`-max_target_seqs 10` could plausibly truncate (15 real above-threshold hits exist for the query).

**Output:**
```
literal request (-num_threads 64 -max_target_seqs 10):
  Warning: [blastp] Number of threads was reduced to 24 to match the number of available CPUs
  10 rows returned

corrected (-num_threads 8 -max_target_seqs 500, then sort + head -10):
  15 total hits found; top 10 by bit-score extracted

diff (literal vs. true top-10 by bit-score, CRLF-normalized): IDENTICAL
```
`-num_threads 64` was not honored as requested — BLAST+ auto-capped it to 24 (all logical CPUs on
this box) and printed a warning; still above the Skill's recommended 8-16 cap, corroborating the
"split input instead of raising thread count" guidance. The `-max_target_seqs 10` early-termination
trap (Shah et al. 2019, cited in SKILL.md) was **not** reproduced on this single-query, 20-sequence
dataset — the literal request happened to return exactly the true top-10 by bit-score. Reported
honestly: the Skill's precaution remains valid best practice (early termination is not a guaranteed
top-N by the tool's own documented semantics), but this run does not independently prove the bias
exists on modern BLAST+ for a single-query case.

Separate, minor finding: raw `blastp -out` files use CRLF line endings on Windows while the
documented `awk`/`sort` pipelines emit LF — diffing them directly (before normalizing) produces
spurious "different" results (see `run/input7_adversarial_antipatterns.sh`'s first version and
P2 recommendation).

**Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100
**Assertions:** 3/4 PASS.

---

## Bundled Python wrapper (`examples/blast_wrapper.py`)

Run separately (`run/test_blast_wrapper.py`) against a copy of the file (never imported from
`F:\OpenScience\external\...`) using the Input-1 synthetic data. Every function exercised
end-to-end against real BLAST+ output:

```
make_blast_db(ref_proteins.fasta, 'ref_db', dbtype='prot')     -> 12 real .p* DB files created
run_blast(query_proteins.fasta, 'ref_db', 'results.tsv', ...)  -> results.tsv, 358 bytes
parse_tabular('results.tsv')                                   -> 4 HSPs, 4 unique queries
filter_hits(..., min_pident=70, min_qcovs=80, max_evalue=1e-5) -> 3/4 pass (QUERY_DIVERGENT2 correctly excluded at 67.6% identity)
top_by_bitscore_per_query(rows, n=1)                            -> matches Input 1's manual sort exactly
require('definitely_not_a_real_tool_xyz')                       -> correctly raises RuntimeError
```
No syntax errors, no missing-dependency failures, subprocess calls use list-form argv throughout
(no shell injection surface).

## No external clone pollution

`find F:/OpenScience/external/mrsonord2240__bioSkills -name __pycache__` returned nothing before
and after this audit — the Skill's `examples/` directory was copied into `run/skill_examples/`
and imported from there, never in place.
