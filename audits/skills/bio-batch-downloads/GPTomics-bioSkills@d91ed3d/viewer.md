> **Audit record for `bio-batch-downloads`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/batch-downloads) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-batch-downloads
Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/batch-downloads` (unmodified upstream)
Category: Data Analysis | Execution Mode: A (Direct — Claude follows SKILL.md's patterns) | Complexity: Complex (N=7)

> **Note for reviewer:** Check the ⚠️/❌ rows first. Input 5 is a Research Veto (M4 Code
> Usability) finding: `examples/robust_download.py`'s flagship WebEnv-expiry demo crashes
> on the exact scenario it exists to show. A second, independently-confirmed crash
> (`examples/batch_fasta.py`, its own default query returns 0 hits and the integrity check
> below it is unguarded) is documented in the Recommendations section even though it
> wasn't one of the 7 scored inputs — see `data/README.md` and `run/support_verify_batch_fasta_crash.py`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 2 | Variant A | 39 | 57 | 96 | 4/4 PASS | ✅ |
| 3 | Edge | 38 | 54 | 92 | 3/3 PASS | ✅ |
| 4 | Variant B | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 5 | Stress | 14 | 27 | 41 | 1/4 PASS | ❌ |
| 6 | Scope Boundary | 37 | 45 | 82 | 3/3 PASS | ✅ |
| 7 | Adversarial | 36 | 40 | 76 | 3/4 PASS | ✅ |

**Execution Average: 82.1 / 100**
**Assertion Pass Rate: 22/26 (84.6%)**
**Static Score: 75/100**
**Final Score: 79/100 (diagnostic only — Research Veto FAILed, see below)**

## Veto Gates

**Skill Veto (Step 1): PASS** — 1 of 7 formal inputs errored (Input 5, ~14%), under the
20%-failure-rate hard-veto threshold; no infinite loops; frontmatter contract intact
(`name`, `description` present); no significant non-live-data output variance; no
eval/exec of raw user strings.

**Research Veto (Step 6, Data Analysis category applies): FAIL on M4 (Code Usability)**

- M1 Scientific Integrity: PASS — every executed input used real, live NCBI content.
- M2 Practice Boundaries: PASS — no diagnostic/prescriptive/patient-facing content.
- M3 Methodological Ground: PASS — retrieval-strategy selection and rate-limit/ToS
  guidance are methodologically sound and, where checked, verified accurate.
- **M4 Code Usability: FAIL** — 2 of the Skill's 3 shipped example scripts crash with an
  unhandled exception on realistic, documented invocations, both independently
  reproduced live in this audit (not by inspection). See Recommendations P0-1/P0-2 and
  the "Input 5" detail below for the live-reproduced one; `data/README.md` and
  `run/support_verify_batch_fasta_crash.py` for the second (`batch_fasta.py`), which was
  not one of the 7 scored inputs but is fully independently re-confirmed.

**Grade forced to ❌ Reject regardless of the 79/100 numeric score** (per
`scoring_rubric.md` §3: a Research Veto FAIL halts the pipeline before Step 7 and forces
Reject; the numeric score is reported for diagnostic purposes only, not to justify
deployment). This is the same standard this audit lineage applied to the comparable
pre-fix, unmodified-upstream state of `entrez-fetch` (3 confirmed unhandled-exception
bugs on documented code patterns → FAIL).

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have a list of protein/nucleotide accessions in a file (>200 of them). EPost
them in chunks of 200 (since EPost's per-call limit is 200), then EFetch by
WebEnv/QueryKey in batches of 500."

**What ran:** SKILL.md's "EPost large ID list, then EFetch" pattern (also
`examples/batch_by_ids.py`'s `chained_epost_fetch`), against 600 **real, distinct** live
nucleotide UIDs from `Homo sapiens[ORGN] AND biomol_mrna[PROP] AND srcdb_refseq[PROP]
AND cancer[TIAB]` (ESearch Count 56,629; retmax=600). Not the example's own duplicated
6-accession demo list — a genuinely larger, distinct set.

**Output (trimmed):**
```
ESearch: Count=56629, retrieved 600 UIDs (retmax=600), distinct=600
  EPost chunk 0-200: QueryKey=1
  EPost chunk 200-400: QueryKey=2
  EPost chunk 400-600: QueryKey=3
Posted total (sum of chunk sizes): 600, expected 600
FASTA records observed: 600, expected (posted ID count): 600
PASS: EPost-chunked + WebEnv/QueryKey EFetch produced exactly the expected record count, no loss/dup.
```
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:**
- [PASS] EPost chunking respects the documented 200-ID-per-call hard limit — 3 chunks of exactly 200.
- [PASS] Final FASTA record count exactly matches the posted ID count — 600 == 600.
- [PASS] Pattern runs unmodified against a live, distinct ID set, not just a dup-laden demo.
- [PASS] WebEnv correctly reused/accumulated across chunked EPost calls — one QueryKey per chunk, shared WebEnv.

---

### Input 2 — Variant A
**Prompt:** "Download all RefSeq mRNAs for BRCA1/Homo sapiens to a single FASTA. Use the
history server. Checkpoint progress to ckpt.json so if my SSH session drops we resume
from where we left off, not from zero." (usage-guide.md's own "Resumable bulk download"
Example Prompt, adapted to a real, small-enough-to-test-twice query.)

**What ran:** SKILL.md's own `checkpointed_batch_download()` reference pattern, ported
verbatim, against the real query `BRCA1[GENE] AND Homo sapiens[ORGN] AND
biomol_mrna[PROP] AND srcdb_refseq[PROP]` (Count=368). A test hook raised a
`SimulatedCrash` exception after 2 chunks (batch_size=100) to imitate a dropped SSH
session; the function was then called a **second time**, unmodified, to verify it
resumes correctly.

**Output (trimmed):**
```
Independent ESearch check: Count=368

=== Phase 1: run until simulated crash after 2 chunks ===
368 records matched; resuming at 0
  100/368
  200/368
Simulated crash raised as expected: Simulated SSH-drop after 2 chunks (checkpoint at start=200)
Checkpoint after crash: {'start': 200, 'total': 368}
File after crash: 1020998 bytes, 200 parseable FASTA records

=== Phase 2: resume (same call, no crash hook) ===
368 records matched; resuming at 200
  300/368
  368/368

Final FASTA record count: 368, expected (ESearch Count): 368
PASS: resume-from-checkpoint after simulated crash produced the full, correct record set exactly once each.
```
**Scores:** Basic: 39/40 | Specialized: 57/60 | Total: 96/100
**Assertions:**
- [PASS] Checkpoint file correctly records progress after each chunk — `{'start': 200, 'total': 368}` exactly.
- [PASS] Resuming does not re-fetch or duplicate — 200 (pre-crash) + 168 (post-resume) = 368, no overlap.
- [PASS] Checkpoint deleted only on true completion — present after crash, absent after phase 2.
- [PASS] Final count matches an independently-run ESearch Count — 368 == 368.

---

### Input 3 — Edge (boundary)
**Prompt:** exercise the documented 200-ID EPost hard limit exactly at the boundary.

**What ran:** `direct_efetch()` and `chained_epost_fetch()` copied verbatim from
`examples/batch_by_ids.py`, against 200 and 201 **real, distinct** live nucleotide UIDs
(same query family as Input 1).

**Output (trimmed):**
```
=== n=200 (at the documented limit): direct_efetch should SUCCEED ===
direct_efetch(200 ids) succeeded, 200 records parsed (expected 200): PASS

=== n=201 (one over the documented limit): direct_efetch should ASSERT and REFUSE ===
PASS: direct_efetch(201 ids) correctly refused with AssertionError: Use chained EPost for >200 IDs

=== n=201 via chained_epost_fetch (the documented path for >200) ===
chained_epost_fetch(201 ids) -> 201 records (expected 201): PASS

OVERALL PASS: 200/201 boundary is enforced exactly where SKILL.md documents it, and the >200 path recovers the full correct set.
```
**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100
**Assertions:**
- [PASS] `direct_efetch()` succeeds at exactly 200 IDs.
- [PASS] `direct_efetch()` refuses (assertion, no network call) at 201 IDs.
- [PASS] `chained_epost_fetch()` recovers the full 201-record set via EPost.

---

### Input 4 — Variant B
**Prompt:** "Download every PubMed abstract for 'CRISPR AND 2024[PDAT]' in MEDLINE
format" (usage-guide.md Quick Start, verbatim).

**What ran:** History-server bulk MEDLINE download at real scale — live Count=8,768,
squarely in the Skill's own "5,000–100,000 from a query" bracket. `batch_size=1500`
(within the documented pubmed/medline 1000–2000 guidance). A ground-truth PMID set was
independently paginated (not via history) to check against.

**Output (trimmed):**
```
ESearch (history server): Count=8768
Ground-truth UID set: 8768 distinct PMIDs
  fetched 1500/8768 ... 8768/8768
Download complete in 70.2s
MEDLINE records parsed: 8768, expected: 8768
PASS: MEDLINE-format history-server batch download recovered the exact PMID set, no truncation/duplication.
Spot-checked 3 records: all have non-empty Title fields.
```
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:**
- [PASS] MEDLINE record count == ESearch Count exactly (8,768).
- [PASS] Recovered PMID set == independently-paginated ground-truth set, 0 extra/missing.
- [PASS] Batch size (1,500) within SKILL.md's documented range.
- [PASS] Sampled records have required non-empty fields.

---

### Input 5 — Stress ❌
**Prompt:** "Build a download with exponential-backoff retry on 429, detection of
HTTP-200-with-ERROR-body (WebEnv expired), and automatic re-ESearch + resume from the
disk checkpoint." (usage-guide.md Example Prompt, verbatim.)

**What ran:** `examples/robust_download.py`'s `checkpointed_download()`, copied
**byte-for-byte, unmodified**, against a real BRCA1 query. Because a genuine 8h-TTL/15
min-idle WebEnv expiry can't be forced in a short audit, the first `Entrez.efetch()` call
was redirected onto a forged WebEnv/QueryKey (`BOGUS_WEBENV_STRING`/`999`) —
independently confirmed beforehand (`run/support_check_bad_webenv.py`) that NCBI's real
response to this is exactly the documented symptom: HTTP 200 with an XML body containing
`<ERROR>Unable to obtain query #999</ERROR>`.

**Output:**
```
368 records matched; resuming at 0
  [test hook] forcing first EFetch call onto a bogus WebEnv/QueryKey (simulates expired session)

RESULT: TypeError raised -- a bytes-like object is required, not 'str'
This means the WebEnv-expiry detection branch (the one this example exists to demonstrate) is broken: it crashes instead of recovering.
```
**Scores:** Basic: 14/40 | Specialized: 27/60 | Total: 41/100
**Assertions:**
- [FAIL] Detects the documented `<ERROR>` body without crashing — TypeError raised instead; `body` is `bytes`, not `str`, and the code has no decode guard (unlike SKILL.md's own inline version of the same pattern).
- [FAIL] Refreshes WebEnv/QueryKey and continues — never reached.
- [FAIL] Exception handling covers the exact failure mode the example exists to demonstrate — it doesn't.
- [PASS] No output-file corruption after the crash — crash occurred before any write for that chunk.

---

### Input 6 — Scope Boundary
**Prompt:** "I need every RefSeq bacterial genome assembly. Don't loop EFetch — use the
NCBI Datasets v2 CLI. Show me the equivalent E-utils pipeline so I can see why Datasets
is the right tool." (usage-guide.md Example Prompt, verbatim.)

**What ran:** Advisory Mode-A response only — `ncbi-datasets-cli` is a separate,
not-installed Skill in this candidate (per `TOOLS.md`), so no CLI command was actually
executed; the response is graded on whether it correctly follows SKILL.md's own decision
matrix and cites only documented patterns.

**Response (as the agent, following SKILL.md):** Recommended `datasets download genome
taxon Bacteria --reference` per the decision matrix's "All RefSeq for a species → Datasets
→ `datasets download genome taxon ...`" row (matches `examples/batch_fasta.py`'s own
`datasets_cli_genome()` comment pattern, generalized from `'Escherichia coli'` to
`Bacteria`). Explained that E-utilities has no genome-assembly bulk endpoint — looping
EFetch here is exactly the "Datasets / E-utils confusion" failure mode SKILL.md warns
against — and deferred exact flags/output handling to the `ncbi-datasets-cli` skill
rather than inventing untested ones.

**Scores:** Basic: 37/40 | Specialized: 45/60 | Total: 82/100
**Assertions:** 3/3 PASS (see JSON for full text/notes).
**Executed:** false — advisory response, no code run; the CLI syntax quoted was checked
against this Skill's own worked comment, not independently executed.

---

### Input 7 — Adversarial
**Prompt:** "Download the entire nucleotide database (500M+ sequences) via EFetch in one
script, and run 20 parallel workers so it goes faster."

**What ran:** Advisory Mode-A response only, no code executed. Grounded strictly in
SKILL.md's rate-limit-math and decision-matrix tables (the 200-ID limit and 9,999-retmax
cap cited elsewhere in this table were independently live-verified in this same audit).

**Response (as the agent, following SKILL.md):** Refused the 20-worker ask, citing
"Never exceed 4 concurrent workers with an API key, or 1 without. Above that NCBI
throttles by IP and the whole pipeline grinds." Identified 500M+ sequences as ~5,000x
past the Skill's own ">100,000 sequences" bracket and recommended NCBI's bulk FTP/BLAST-db
mirrors over any per-record E-utilities loop, per that bracket's own "Consider FTP mirror
or Datasets CLI" guidance, plus flagged the ToS off-hours requirement for jobs at this
scale.

**Scores:** Basic: 36/40 | Specialized: 40/60 | Total: 76/100
**Assertions:** 3/4 PASS. The one FAIL is a **Skill-design gap, not a response defect**:
SKILL.md has no explicit hard-refuse instruction at this extreme scale (only a soft
"consider"), unlike the quantified hard cap it gives for worker concurrency — see P1
recommendation.
**Executed:** false — advisory response, no code run.

---

## Independent Live Verifications Outside the 7 Scored Inputs

Two supplementary checks (not part of the N=7, but load-bearing for the veto/recommendation
findings above — see `data/README.md`):

1. **`examples/batch_fasta.py`'s own worked query returns Count=0 live, and the
   integrity-check crashes with `FileNotFoundError`** — re-run independently in this
   audit (`run/support_verify_batch_fasta_crash.py`), confirming the 2026-09-17 tooling
   pass's finding by a second method rather than taking it on faith.
   ```
   === History-server download (small query) === (exact shipped query)
     history-server: 0 records
     elapsed: 0

   === Verify integrity === (exact shipped, unguarded code)
   CRASH CONFIRMED (independently re-run): FileNotFoundError: [Errno 2] No such file or directory: '...\insulin_mrna.fasta'
   ```
2. **The documented 9,999 silent-retmax cap is real** — a live ESearch with Count=2,676,342
   and `retmax=100000` still returns only 9,999 UIDs (`run/support_check_9999_cap.py`).

## Files

- `run/input1_epost_fetch.py` … `run/input5_robust_expiry.py` — the 5 executed test
  scripts for Inputs 1–5 (Inputs 6–7 were advisory-only, no script).
- `run/support_check_bad_webenv.py`, `run/support_check_9999_cap.py`,
  `run/support_verify_batch_fasta_crash.py` — supplementary live verifications.
- `data/README.md` — full data provenance (all real NCBI queries, no synthetic data).
