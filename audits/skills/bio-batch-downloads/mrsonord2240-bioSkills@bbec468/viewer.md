> **Audit record for `bio-batch-downloads`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@bbec468](https://github.com/mrsonord2240/bioSkills/tree/bbec468378279e944fe74c3a4612d7d0d204cb6a/database-access/batch-downloads) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-batch-downloads (RE-AUDIT, post-fix)
Generated: 2026-09-19
Re-auditor: independent agent (not the original auditor, not the fixer)
Source: `mrsonord2240/bioSkills@bbec468378279e944fe74c3a4612d7d0d204cb6a:database-access/batch-downloads`
Worktree: `F:\OpenScience\wt\db-bd`, branch `fix/db-batch-downloads`
Pre-fix report archived: `F:\OpenScience\audits\_pre-fix-20260919\bio-batch-downloads\`
Fix log (claim, not evidence): `F:\optimizing-agent-science-skills\fixes\bio-batch-downloads.md`

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 2 | Variant A (regression + brief #4) | 39 | 57 | 96 | 4/4 PASS | ✅ |
| 3 | Edge (regression) | 38 | 54 | 92 | 3/3 PASS | ✅ |
| 4 | Variant B (regression) | 36 | 52 | 88 | 3/3 PASS | ✅ |
| 5 | Stress (regression, flagship P0) | 39 | 56 | 95 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (regression) | 37 | 45 | 82 | 3/3 PASS | ✅ |
| 7 | Adversarial (regression, P1) | 39 | 56 | 95 | 4/4 PASS | ✅ |
| 8 | Variant C (re-auditor addition) | 37 | 49 | 86 | 3/3 PASS | ✅ |
| 9 | Edge (re-auditor addition) | 34 | 46 | 80 | 2/3 PASS | ⚠️ |

**Execution Average: 89.8 / 100**
**Assertion Pass Rate: 30/31**

**Static Score: 92/100** (pre-fix: 75/100)
**Final Score: 91/100 — ⭐ Production Ready** (pre-fix: 79/100 — ❌ Reject, Research Veto M4 FAIL)

## Veto Gates

- **Skill Veto**: PASS (all 4 dimensions) — unchanged from pre-fix.
- **Research Veto**: PASS (was FAIL — M4 Code Usability). All three example scripts and SKILL.md's inline function now run clean under live forged-failure and genuine-zero-hit conditions. See Input 2, 5, 8 below.

## What I verified myself (not trusted from the fix log)

1. **Regression 1 — robust_download.py's WebEnv-expiry crash (the flagship P0).** Forged a *different* invalid `query_key` than the fix log used, against a real, valid BRCA1 session (368 records). Pre-fix this raised `TypeError: a bytes-like object is required, not 'str'`. Post-fix: the real NCBI `<ERROR>` body is decoded, detected, the session refreshes, and the download completes 368/368 with the checkpoint file removed on completion. See `run/input1_webenv_expiry_regression.py`.
2. **Regression 2 — batch_fasta.py's zero-hit crash.** Ran the shipped, fixed script end-to-end with its replaced `INS[GENE]` query (4 real hits): completes cleanly, 4 real transcripts parsed. See `run/batch_fasta.py` output.
3. **New — the zero-count guard itself, not just the replaced query.** Built a genuinely different zero-hit query (`ZZZNOTAREALGENE9999[GENE]...`) and drove the guard directly: confirms the fix is a real guard against any zero-count case, not an artifact of the fixer's query happening to return >0 hits. See `run/input2_zero_count_guard.py`.
4. **SKILL.md's inline `checkpointed_batch_download`.** The fix log claims this was already correct (lines 139-140) and left untouched. I did not trust that — extracted the function directly from the worktree's SKILL.md myself (`run/inline_function_extract.py`), confirmed the `isinstance(body, bytes)` decode guard is present, then ran it live with a fresh forged-WebEnv condition against a real TP53 query (25 records): recovers cleanly, 25/25. See `run/input3_skillmd_inline_regression.py`.
5. **Regression — batch_by_ids.py and the 200/201-ID EPost boundary**, both untouched by the fix per `git diff 1332462..bbec468` (confirmed myself, not just read from the fix log). Ran unmodified: 6/6 direct-fetch, 255/255 chained-EPost, then a fresh 200/201-ID boundary test (200 succeeds, 201 refused by `direct_efetch`'s own assert, 201 succeeds via `chained_epost_fetch`). See `run/input4_epost_boundary.py`.
6. **Regression — PubMed MEDLINE bulk pattern**, scaled to 1,000 of a live 8,768-record query (same query as the pre-fix audit's Input 4; count unchanged 2026-09-17 → today). See `run/input5_pubmed_medline.py`.
7. **New — the P1 escape-hatch fix's precision.** Confirmed it fires correctly on the original adversarial "entire database, 20 workers" case (Input 7) *and* does not over-trigger on an 800,000-record request that should still fall into the softer, pre-existing ">100,000: Consider FTP/Datasets CLI" bracket (Input 9). This is the fix working as intended in both directions, not just the direction the fixer tested.
8. **Redundancy pass.** Read both SKILL.md and usage-guide.md in full and diffed against the pre-fix commit (`git diff 1332462 bbec468 -- database-access/batch-downloads/usage-guide.md`). Every point in the deleted "What the Agent Will Do" (10 steps) and "Tips" (7 bullets) sections is restated in SKILL.md's Decision Matrix, Rate-limit math, History server lifecycle, EPost specifics, Failure modes, and Related Skills sections — confirmed line by line, nothing unique was lost.

## New defect found (not in the fix log, not blocking)

The `>100,000 sequences` decision-matrix row's Strategy column reads *"Consider FTP mirror or Datasets CLI; chunk if E-utils still"* — the clause after the semicolon is grammatically incomplete. Confirmed via `git diff` that this predates the fix pass and was not touched by it. Minor clarity issue, not a functional defect (Input 9's assertion 3 fails on this specifically; the *behavior* it should produce — the softer, non-refusing guidance — still came through correctly in assertions 1-2). Filed as P2.

## Detailed Outputs

### Input 1 — Canonical (regression of pre-fix Input 1)
**Prompt (implicit, Mode A code execution):** Run `examples/batch_by_ids.py` unmodified.
**Output:** `=== Direct EFetch for 6 known accessions === Integrity OK: 6 records` / `=== Chained EPost + history fetch for 255 IDs === Posted 200/255 IDs / Posted 255/255 IDs`. Verified via `SeqIO.parse`: `small_list.fasta` 6 records, `large_list.fasta` 255 records.
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:** 4/4 PASS (see JSON for text).

### Input 2 — Variant A (regression of pre-fix Input 2 + brief requirement #4)
**Prompt:** Run SKILL.md's inline `checkpointed_batch_download()`, extracted directly from the worktree, against a forged expired WebEnv on a real TP53 query (Count=25).
**Output:** `25 records matched; resuming at 0` → forged call detected → `Server error in body: ... <ERROR>Unable...; refreshing WebEnv` → `10/25`, `20/25`, `25/25`. No crash.
**Scores:** Basic: 39/40 | Specialized: 57/60 | Total: 96/100
**Assertions:** 4/4 PASS.

### Input 3 — Edge (regression of pre-fix Input 3)
**Prompt:** Exact 200/201-ID EPost boundary via `batch_by_ids.py`'s own functions.
**Output:** `direct_efetch(200 ids) -> 200 records`; `direct_efetch(201 ids) refused as expected: Use chained EPost for >200 IDs`; `chained_epost_fetch(201 ids) -> 201 records`.
**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100
**Assertions:** 3/3 PASS.

### Input 4 — Variant B (regression of pre-fix Input 4)
**Prompt:** usage-guide.md's Quick Start: "Download every PubMed abstract for 'CRISPR AND 2024[PDAT]' in MEDLINE format." Scaled to first 1,000 of 8,768 live records.
**Output:** `Count: 8768` → `500/1000` → `1000/1000` → `fetched 1000 MEDLINE records (target 1000)` → `records with non-empty Title field: 1000/1000`.
**Scores:** Basic: 36/40 | Specialized: 52/60 | Total: 88/100
**Assertions:** 3/3 PASS.

### Input 5 — Stress (regression of pre-fix Input 5, the flagship P0)
**Prompt:** `robust_download.py`'s `checkpointed_download()`, forced onto a freshly forged expired-WebEnv response (real BRCA1 query, Count=368).
**Output:** `368,000 records matched...` (368 records) → forged call detected → `WebEnv expired or server error: ... <ERROR>Unable...; refreshing WebEnv` → `368/368` → `Done: 368 records -> input1_brca1.fasta`. No crash (pre-fix: `TypeError`).
**Scores:** Basic: 39/40 | Specialized: 56/60 | Total: 95/100
**Assertions:** 4/4 PASS.

### Input 6 — Scope Boundary (regression of pre-fix Input 6)
**Prompt:** "I need every RefSeq bacterial genome assembly. Don't loop EFetch — use the NCBI Datasets v2 CLI. Show me the equivalent E-utils pipeline."
**Output:** Advisory response citing the unchanged decision-matrix row and `datasets_cli_genome()` pattern.
**Scores:** Basic: 37/40 | Specialized: 45/60 | Total: 82/100
**Assertions:** 3/3 PASS.

### Input 7 — Adversarial (regression of pre-fix Input 7, the P1 finding)
**Prompt:** "Download the entire nucleotide database (500M+ sequences) via EFetch, 20 parallel workers to go faster."
**Output:** Advisory response now citing the new decision-matrix row verbatim: *"Refuse the EFetch-loop approach outright... not a 'consider,' a hard stop."*
**Scores:** Basic: 39/40 | Specialized: 56/60 | Total: 95/100
**Assertions:** 4/4 PASS (was 3/4 pre-fix — the hard-stop assertion now passes).

### Input 8 — Variant C (re-auditor addition)
**Prompt:** Force `batch_fasta.py`'s zero-count guard with a genuinely different zero-hit query (`ZZZNOTAREALGENE9999[GENE]...`), not the fixer's replaced `INS[GENE]` query.
**Output:** `history-server: 0 records` → `elapsed sentinel: 0` → `No records found -- nothing to verify`. No crash, no output file created.
**Scores:** Basic: 37/40 | Specialized: 49/60 | Total: 86/100
**Assertions:** 3/3 PASS.

### Input 9 — Edge (re-auditor addition)
**Prompt:** "I need to bulk-download about 800,000 RefSeq protein sequences via EFetch for an offline BLAST database build." (Tests that the new >1,000,000 hard-stop does not over-trigger below its threshold.)
**Output:** Advisory response correctly stays in the softer `>100,000 sequences: Consider FTP mirror or Datasets CLI` bracket rather than invoking the new hard refusal.
**Scores:** Basic: 34/40 | Specialized: 46/60 | Total: 80/100
**Assertions:** 2/3 PASS (the 3rd fails on the pre-existing phrasing nit noted above, not on skill behavior).

> **Note for reviewer:** No ⚠️/❌ pattern across 2+ outputs — the one partial (Input 9) is a documentation-wording nit unrelated to the fix, not a structural issue.
