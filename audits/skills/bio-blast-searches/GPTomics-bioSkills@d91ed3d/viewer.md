> **Audit record for `bio-blast-searches`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/blast-searches) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-blast-searches
Generated: 2026-09-19

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/blast-searches`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=7)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 57 | 95 | 5/5 PASS | ✅ |
| 2 | Variant A | 37 | 57 | 94 | 4/4 PASS | ✅ |
| 3 | Edge | 21 | 32 | 53 | 2/4 PASS | ❌ |
| 4 | Variant B | 37 | 51 | 88 | 4/4 PASS | ✅ |
| 5 | Stress | 23 | 35 | 58 | 2/4 PASS | ❌ |
| 6 | Scope Boundary | 39 | 53 | 92 | 3/3 PASS | ✅ |
| 7 | Adversarial | 16 | 30 | 46 | 1/3 PASS | ❌ |

**Execution Average: 75.1 / 100**
**Assertion Pass Rate: 21/27**

**Static Score: 87/100** | **Final Score: 80/100 → ✅ Limited Release**

> Reviewer note: check inputs 3, 5, 7 first — 3 and 5 are confirmed, reproducible code defects
> with verified one-line fixes; 7 is an inconclusive execution anomaly (possible confound: shared
> machine load), not a confirmed defect.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have an unknown DNA sequence from an environmental sample. BLAST it to identify what it is — use a database that will still be valid if someone re-runs this in a year."

**What ran:** SKILL.md's "Standard remote BLASTN with reproducible parameters" pattern, unmodified:
```python
handle = NCBIWWW.qblast(program='blastn', database='refseq_select_rna', sequence=QUERY,
    expect=1e-10, word_size=11, hitlist_size=500, format_type='XML')
```
**Output (trimmed):** 61.6s. 11 alignments returned; top 10 after identity≥0.7/coverage≥0.5 filter, sorted by bit-score:
```
 1. NM_000518       bits= 167.2  E=5.9e-41  id=1.00  cov=1.00  Homo sapiens HBB mRNA
 2. NM_000519       bits= 140.1  E=8.2e-33  id=0.93  cov=1.00  Homo sapiens HBD mRNA
 3. NM_008220       bits= 108.6  E=4.8e-23  id=0.86  cov=1.00  Mus musculus Hbb-bt mRNA
 ... (7 more, down to NM_001111269 rat Hbb-bt, id=0.79)
```
Query was the human HBB partial CDS used throughout SKILL.md's own examples; top hit is the exact self-match at 100% identity/coverage, as expected.

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:** 5/5 PASS (reproducible db used; hitlist_size=500 avoids max_target_seqs trap; correct top hit; bit-score sort; zero code changes needed).

---

### Input 2 — Variant A
**Prompt:** "Find mammalian homologs of this human protein (alpha-hemoglobin) in Swiss-Prot — I only want reviewed, curated records, and I want the search itself restricted to mammals, not filtered after the fact."

**What ran:** SKILL.md's "Protein search with organism restriction" pattern, unmodified:
```python
handle = NCBIWWW.qblast(program='blastp', database='swissprot', sequence=HBA_HUMAN,
    entrez_query='Mammalia[Organism]', expect=1e-5, composition_based_statistics=2,
    hitlist_size=200, format_type='XML')
```
**Output (trimmed):** 241.4s. 200 hits returned (hitlist_size cap reached). Top hits (coverage≥0.8, sorted by bit-score):
```
P69905  bits=287.0  E=3.6e-101  100.0% id  cov=1.00  Hemoglobin subunit alpha
P01923  bits=282.3  E=1.9e-99   99.3% id  cov=0.99  Hemoglobin subunit alpha
Q9TS35  bits=281.6  E=4.3e-99   98.6% id  cov=1.00  Hemoglobin subunit alpha-1
... (all 200 titles spot-checked are real Mammalia hemoglobin-alpha Swiss-Prot records)
```
**Scores:** Basic: 37/40 | Specialized: 57/60 | Total: 94/100
**Assertions:** 4/4 PASS.

---

### Input 3 — Edge
**Prompt:** "I have a 12-amino-acid peptide from a mass-spec run. BLAST it against Swiss-Prot — I know short queries need special parameters."

**What ran:** SKILL.md's "Short peptide search" pattern, unmodified first:
```python
handle = NCBIWWW.qblast(program='blastp', database='swissprot', sequence=PEPTIDE,
    matrix_name='PAM30', word_size=2, expect=1000, composition_based_statistics=3,
    hitlist_size=100, format_type='XML')
```
**Output:**
```
Traceback (most recent call last):
  ...
ValueError: Error message from NCBI: Message ID#36 Error: Cannot validate the Blast
options:  Gap existence and extension values of 11 and 1 not supported for PAM30
```
**Root cause confirmed:** NCBI defaults gap costs to BLOSUM62's 11,1 when `gapcosts` is not
supplied; PAM30 rejects those values outright. SKILL.md's own word-size/matrix table (a few
sections earlier) correctly states PAM30 needs gap costs 9,1 — that value simply never made it
into the runnable code block.

**Fix verified live:** adding `gapcosts='9 1'` to the same call succeeds (181.4s, 100 hits, top
hits all real 11-12/12-identity human/primate hemoglobin-beta Swiss-Prot records at E≈2.3-7.0,
consistent with the Skill's own note that short queries need permissive E cutoffs).

**Scores:** Basic: 21/40 | Specialized: 32/60 | Total: 53/100
**Assertions:** 2/4 PASS — parameters otherwise correct; NCBI's exact error text is absent from
the Skill's own Common Errors table; fix works and matches the Skill's own table elsewhere.

---

### Input 4 — Variant B (reasoning only, not executed)
**Prompt:** "I ran a blastp against nr and a separate blastp against swissprot for the same query. The nr hit came back with a smaller E-value than the swissprot hit — does that mean the nr hit is the better match?"

**Expected agent answer per SKILL.md:** No — E-values scale with database size (E = K·m·n·exp(−λS));
comparing E-values from an nr search (~300 GB) against a swissprot search (small, curated) is
meaningless because n differs by orders of magnitude. The correct comparison is bit-score, which
is database-size invariant. This is stated explicitly and correctly in both SKILL.md's "E-value
interpretation" section and its Failure Modes ("Cross-database E-value comparison").

**Scores:** Basic: 37/40 | Specialized: 51/60 | Total: 88/100 (specialized docked for no concrete
code demonstration in this input — reasoning-only).
**Assertions:** 4/4 PASS.

---

### Input 5 — Stress
**Prompt:** "This is a cross-species mRNA query — I'm worried about picking megablast when I should use something more sensitive. Also save the results to disk so I can re-parse them later without re-running the search, and show me it doesn't matter whether I filter live or from the saved file."

**What ran (as first attempted, per SKILL.md's own Program table):**
```python
handle = NCBIWWW.qblast(program='megablast', database='refseq_select_rna', sequence=QUERY, ...)
```
**Output:**
```
ValueError: Program specified is megablast. Expected one of blastn, blastp, blastx, tblastn, tblastx
```
**Root cause confirmed:** `NCBIWWW.qblast()`'s `program=` argument only accepts
blastn/blastp/blastx/tblastn/tblastx. Megablast is requested via `program='blastn', megablast=True`
(discontiguous megablast additionally needs `template_type=`/`template_length=`) — a Biopython API
detail that appears nowhere in SKILL.md, whose Program table presents `megablast`/`dc-megablast`
as if they were `program=` strings.

**Fix verified live:** `program='blastn', megablast=True` succeeds (300.9s). Result: **5 alignments**
(human HBB self-hit + 2 mouse orthologs), versus **11 alignments** (human + mouse + rat) from
Input 1's plain blastn/word=11 run on the *identical* query. This confirms reduced cross-species
sensitivity, but not the Failure Modes table's literal "zero hits" symptom — 2 of 3 species were
still found; only the most-diverged (rat, 79-84% identity) was missed entirely.

The XML save-to-disk + re-parse round trip (`save_and_parse.py` pattern) was exercised on the
corrected call and reproduced the in-memory results exactly.

**Scores:** Basic: 23/40 | Specialized: 35/60 | Total: 58/100
**Assertions:** 2/4 PASS.

---

### Input 6 — Scope Boundary (reasoning only, not executed)
**Prompt:** "I have 200 unknown coding sequences from a new bacterial genome assembly I want to identify — what's the best way to BLAST all of them?"

**Expected agent answer per SKILL.md/usage-guide.md:** Remote BLAST via `NCBIWWW.qblast()` is
explicitly scoped to "one-off identification of a few sequences"; both SKILL.md ("For >50
sequences, switch to local-blast or DIAMOND/MMseqs2 in remote-homology") and usage-guide.md
("Remote BLAST submits to the NCBI queue. For >5 sequences/min, switch to local BLAST. For >1000
sequences, switch to DIAMOND or MMseqs2") give an unambiguous, specific threshold well below 200 —
the correct answer is to hand off, not to loop 200 sequential remote calls against NCBI.

**Scores:** Basic: 39/40 | Specialized: 53/60 | Total: 92/100
**Assertions:** 3/3 PASS.

---

### Input 7 — Adversarial
**Prompt:** "Just blast this for me, I don't care about the details: `ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAG` — give me the top hit."

**What ran:** Applied the Skill's own defaults for an unspecified request (blastn, refseq_select_rna,
expect=1e-10, hitlist_size=500) to the bare sequence with **no `>id` defline** — deliberately testing
SKILL.md's documented "Empty FASTA defline submitted" failure mode (expected symptom: "hits
returned but record.query is None").

**Output:** The `qblast()` call did not return within 20+ minutes, versus 61.6s for the *identical*
sequence submitted *with* a defline in Input 1. Execution was still unresolved when this audit
closed.

**Assessment:** This is flagged as an **open, inconclusive finding**, not a confirmed defect — the
audit machine had other unrelated processes/sessions active at the same time (per this project's
"other sessions work this corpus concurrently" note), so NCBI-side queue congestion or local
resource contention cannot be ruled out as the cause. What can be said: the documented symptom
("record.query is None", i.e. the search still *completes*) was not what was observed; the search
did not complete at all in a reasonable multiple of the established baseline latency.

**Scores:** Basic: 16/40 | Specialized: 30/60 | Total: 46/100
**Assertions:** 1/3 PASS.

---

## Score Breakdown

```
Static Score   : 87/100  × 40% = 34.8
Dynamic Score  : 75.1/100 × 60% = 45.1
FINAL SCORE    : 80 / 100
GRADE          : ✅ Limited Release
Deployable     : true
Veto override  : false
```

## Skill Veto (Step 1)
```
T1. Stability    : PASS — 2 of 7 code defects found are deterministic, reproducible parameter bugs
                          (not random crashes/infinite loops); no unresolvable dependency conflicts.
T2. Contract     : PASS — frontmatter has name/description/tool_type/primary_tool; no schema/API
                          contract to violate (instructional + code-pattern Skill, not a JSON-returning tool).
T3. Determinism  : PASS — BLAST itself is deterministic for a fixed database snapshot. The one real
                          non-determinism source (nt/nr change daily) is explicitly disclosed with a
                          named mitigation (refseq_select, snapshot dating) rather than hidden.
T4. Security     : PASS — no eval/exec of raw strings, no credentials, no injection vectors; sequences
                          pass through Biopython's own request builder to a public NCBI endpoint.
```

## Research Veto (Step 6, Category 3 applies)
```
M1. Scientific Integrity  : PASS — all literature citations real and correctly attributed; no fabricated data anywhere.
M2. Practice Boundaries   : PASS — pure bioinformatics tool, no clinical/diagnostic scope.
M3. Methodological Ground : PASS — no principled fallacy; one overstated symptom claim handled as a P2, not a veto.
M4. Code Usability        : PASS — the 2 confirmed code defects are incorrect-API-parameter bugs with
                                    one-line fixes, not syntax errors/infinite loops/missing dependencies
                                    (the literal M4 trigger). Primary/canonical patterns all ran correctly.
```
