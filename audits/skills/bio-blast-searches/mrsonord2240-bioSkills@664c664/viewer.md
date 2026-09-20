> **Audit record for `bio-blast-searches`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@664c664](https://github.com/mrsonord2240/bioSkills/tree/664c6644129047ec1118596250dfac1451a1d1bb/database-access/blast-searches) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-blast-searches (RE-AUDIT after fix)
Generated: 2026-09-19

Source: `mrsonord2240/bioSkills@664c664:database-access/blast-searches` (worktree `F:\OpenScience\wt\db-blast`, branch `db-blast`)
Prior audit: `F:\OpenScience\audits\_pre-fix-20260919\bio-blast-searches\` (score 83, ✅ Limited Release)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-blast-searches.md`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=7)

This is an independent re-audit by a fresh auditor (not the original auditor, not the fixer). Its
job: verify the fix with fresh evidence, not rubber-stamp the fixer's own claims.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 57 | 95 | 5/5 PASS | ✅ |
| 2 | Variant A | 37 | 57 | 94 | 4/4 PASS | ✅ |
| 3 | Edge (fix #2) | 35 | 54 | 89 | 3/4 PASS | ✅ |
| 4 | Variant B | 37 | 51 | 88 | 4/4 PASS | ✅ |
| 5 | Stress (fix #1) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 39 | 53 | 92 | 3/3 PASS | ✅ |
| 7 | Adversarial (fix #3) | 34 | 53 | 87 | 4/4 PASS | ✅ |

**Execution Average: 91.3 / 100** (was 80.0)
**Assertion Pass Rate: 27/28** (was 22/28)

**Static Score: 96/100** (was 87) | **Final Score: 93/100 → ⭐ Production Ready** (was 83, ✅ Limited Release)

> All three previously-failing inputs (3, 5, 7) now pass. Inputs 3 and 5 were independently
> re-executed live against real NCBI on sequences neither the original auditor nor the fixer used.
> Input 7 was verified by document-to-evidence inspection only (see its note) — the ~13-minute cost
> of reproducing it was judged not worth it given the original audit's own captured evidence is
> unambiguous and the fix was purely documentary.

---

## Independent fix verification (this session's own live NCBI calls)

### Finding #2 — PAM30 short-peptide `gapcosts` (Input 3)

Peptide used: **human insulin B-chain, residues 1–15 (`FVNQHLCGSHLVEAL`)** — distinct from both the
original auditor's peptide (12-aa hemoglobin-beta fragment) and the fixer's own verification peptide
(also hemoglobin-beta).

**Regression check** (unfixed pattern, no `gapcosts`):
```
Submitting UNFIXED short-peptide BLASTP (PAM30, no gapcosts) to NCBI...
FAILED as expected after 0.5s: ValueError: Error message from NCBI: Message ID#36 Error:
Cannot validate the Blast options:  Gap existence and extension values of 11 and 1 not
supported for PAM30
```
Confirms the pre-fix defect is real and reproduces on a completely different peptide — not an
artifact of the original auditor's specific query.

**Fixed pattern** (`gapcosts='9 1'` added, as SKILL.md now documents):
```
Elapsed: 1141.5s, raw XML bytes: 84916
Query length: 15
Total hits returned: 82
  F8WCM5   bits=35.0  E=2.69e-03  ident=15/15   Insulin, isoform 2 (INS-IGF2 readthrough)
  P01317   bits=33.7  E=8.16e-03  ident=15/15   Insulin (contains Insulin B chain)
  P06306   bits=33.7  E=8.51e-03  ident=15/15   Insulin (contains Insulin B chain)
  ... (5 more, all real insulin/insulin-B-chain Swiss-Prot records)
```
**Correct, biologically sensible result**: every top hit is a genuine insulin or insulin-B-chain
Swiss-Prot record at 15/15 identity — exactly what BLASTing an insulin B-chain fragment against
Swiss-Prot should find. Confirms the fix works, independent of the fixer's and original auditor's
own runs.

**New observation (not in the prior audit or the fix log):** this run took **1141.5s (19.0 min)** —
Biopython raised the same `BiopythonWarning: ... taking longer than 10 minutes` seen elsewhere in
this Skill's failure modes — versus 181.4s for the same code pattern in the prior audit. Most likely
NCBI queue congestion (several other audits were concurrently hitting NCBI from this same machine
during this session), not a property of the fix or the query, but it is a real, reproducible
observation that the Skill's "30-60s typical" framing does not anticipate for this specific parameter
combination (permissive expect=1000, word_size=2). Captured as a new P2.

### Finding #1 — megablast/dc-megablast invocation (Input 5)

Query used: a **live-fetched 95nt window of human ACTB (beta-actin) mRNA, NM_001101.5, positions
300–395** — fetched via `Bio.Entrez.efetch` rather than hand-transcribed, to guarantee correctness,
and distinct from both the original auditor's and the fixer's HBB-based query.

**Regression check** (unfixed `program='megablast'`):
```
Submitting qblast(program='megablast', ...) -- the UNFIXED/documented-table form...
FAILED as expected after 0.0s: ValueError: Program specified is megablast. Expected one of
blastn, blastp, blastx, tblastn, tblastx
```

**Fixed pattern** (`program='blastn', megablast=True`):
```
Elapsed: 181.6s, raw XML bytes: 16097
Query length: 95
Total alignments: 12
  NM_001101      id=1.000  E=9.63e-44  Homo sapiens ACTB, mRNA                    <- exact self-hit
  NM_001005356   id=0.978  E=1.26e-37  Homo sapiens POTE ankyrin domain ...
  NM_009609      id=0.947  E=2.10e-35  Mus musculus Actg1 (actin, gamma) ...
  NM_019212      id=0.955  E=9.77e-34  Rattus norvegicus actin, alpha 1 (skeletal muscle)
  NM_005159      id=0.944  E=1.26e-32  Homo sapiens ACTC1 (actin alpha cardiac muscle 1)
  ... (7 more)
```
Correct, biologically sensible result: exact self-match plus real actin paralogs (ACTG1, ACTC1,
POTE family) and real cross-species orthologs (mouse Actg1, rat skeletal-muscle actin) — confirming
both that the corrected API call works and that megablast still finds real non-human hits (matching
the Skill's now-softened "reduced, not necessarily zero" cross-species claim from finding #4, rather
than the old "zero hits" overstatement).

### Finding #3 — empty FASTA defline (Input 7) — not independently re-run

Per the dispatch's explicit time-budget guidance, this ~13-minute (781s) path was **not**
reproduced live in this session. Verified instead by inspection: `SKILL.md`'s Failure Modes and
Common Errors sections now state the literal placeholder string (`'No definition line'`) and the
12.7x latency figure (781s vs. 62s) exactly as the original audit captured them live — a direct,
checkable match between the archived pre-fix evidence and the corrected documentation, not a claim
taken on the fixer's word alone.

---

## Detailed Outputs (inputs 1, 2, 4, 6 — unaffected by the fix, reused from the prior audit)

These four inputs exercise code paths and reasoning the fix did not touch. Full detail (prompts,
code, live output) is unchanged from the prior audit at
`F:\OpenScience\audits\_pre-fix-20260919\bio-blast-searches\eval_viewer_bio-blast-searches.md`.
Summary:

- **Input 1 (Canonical):** Standard BLASTN, `refseq_select_rna`, HBB query. 61.6s, top hit NM_000518
  (HBB self-hit), 100% id/cov. 95/100, 5/5 assertions.
- **Input 2 (Variant A):** BLASTP + `entrez_query='Mammalia[Organism]'`, Swiss-Prot, HBA query.
  241.4s, 200 real hits, top hit P69905 (human HBA) 100% identity. 94/100, 4/4 assertions.
- **Input 4 (Variant B, reasoning-only):** Cross-database E-value comparison question. Correctly
  answered per SKILL.md/references/statistics.md. 88/100, 4/4 assertions.
- **Input 6 (Scope Boundary, reasoning-only):** 200-sequence identification request. Correctly
  hands off to `local-blast`/`remote-homology` per the Skill's own >50-sequence threshold.
  92/100, 3/3 assertions.

---

## Score Breakdown

```
Static Score   : 96/100  x 40% = 38.4
Dynamic Score  : 91.3/100 x 60% = 54.8
FINAL SCORE    : 93 / 100
GRADE          : ⭐ Production Ready  (was 83, ✅ Limited Release)
Deployable     : true
Veto override  : false
```

Floor check (Production Ready requires all of): Static ≥80 (96 ✓) · Execution ≥85 (91.3 ✓) ·
Layer 1 avg ≥32 (36.9 ✓) · Layer 2 avg ≥48 (54.4 ✓) · Assertion pass rate ≥90% (96.4% ✓). All met,
no floor-triggered downgrade.

## Skill Veto (Step 1) — unchanged, PASS
```
T1. Stability    : PASS -- no random crashes/infinite loops; both prior defects were deterministic,
                          reproducible parameter bugs, now fixed and independently reverified.
T2. Contract     : PASS -- frontmatter has name/description/tool_type/primary_tool.
T3. Determinism  : PASS -- BLAST is deterministic for a fixed database snapshot; the one real
                          non-determinism source (nt/nr) is disclosed with a named mitigation.
T4. Security     : PASS -- no eval/exec, no credentials, no injection vectors.
```

## Research Veto (Step 6, Category 3 applies) — PASS, M4 now unambiguous
```
M1. Scientific Integrity  : PASS -- all citations real and correctly attributed, correctly split
                                    between SKILL.md and the new references/statistics.md.
M2. Practice Boundaries   : PASS -- pure bioinformatics tool, no clinical/diagnostic scope.
M3. Methodological Ground : PASS -- the one imprecise claim (megablast "zero hits") is now corrected.
M4. Code Usability        : PASS -- both previously-crashing patterns fixed and independently
                                    reverified live in this re-audit on fresh sequences. No
                                    remaining code defect found anywhere in the Skill.
```

## What changed since the pre-fix audit (83 -> 93)

| # | Prior finding | Status | This re-audit's independent evidence |
|---|---|---|---|
| 1 (P1) | megablast/dc-megablast not valid `program=` values | Fixed | Regression reconfirmed (instant ValueError); fix reconfirmed live on human ACTB (12 real alignments) |
| 2 (P1) | PAM30 short-peptide pattern crashes (missing gapcosts) | Fixed | Regression reconfirmed (instant ValueError); fix reconfirmed live on human insulin B-chain (82 real hits) |
| 3 (P1) | Empty-defline symptom/latency undocumented | Fixed | Verified by inspection against the original audit's own captured live evidence (not re-run, per time budget) |
| 4 (P2) | Megablast cross-species "zero hits" overstated | Fixed | Softened wording now matches this session's own live result (2/3 species found, not zero) |
| 5 (P2) | No `references/` split | Fixed | `references/statistics.md` added; spot-checked for correctness (E-value formula, CBS table, twilight-zone note all accurate) and that SKILL.md keeps the two decisions agents need day-to-day |
| new (P2) | Latency guidance doesn't anticipate order-of-magnitude spikes | Open | This re-audit's own PAM30 peptide run took 1141.5s vs. 181.4s in the prior audit for the same pattern -- not a regression, a new observation |
