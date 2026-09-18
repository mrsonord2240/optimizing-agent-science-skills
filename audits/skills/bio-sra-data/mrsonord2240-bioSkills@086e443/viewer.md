> **Audit record for `bio-sra-data`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@086e443](https://github.com/mrsonord2240/bioSkills/tree/086e4439c0b8b7c13d5892ccc51492b9a0828e70/database-access/sra-data) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-18 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-sra-data (RE-AUDIT, second fix round, post-fix)
Generated: 2026-09-18
Source: mrsonord2240/bioSkills@086e443:database-access/sra-data (fork worktree `F:\OpenScience\wt\db-sra2`, branch `fix/db-sra2`, based on staging `main` @ `1f07281`)
Pre-fix report (this round): `F:\OpenScience\audits\_pre-fix-20260918b\bio-sra-data\` (82/100, Limited Release, deployable, no open P0, two open P1s)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-sra-data.md` (2026-09-18 section, second fix round) — read to know where to look; every score and finding below is grounded in this session's own execution, independent of both the fixer and the two prior re-auditors.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 54 | 92 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 38 | 54 | 92 | 4/4 PASS | ✅ |
| 3 | Edge (NEW) | 37 | 53 | 90 | 4/4 PASS | ✅ |
| 4 | Stress — THE CRUX (NEW) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 5 | Variant B (NEW) | 37 | 53 | 90 | 4/4 PASS | ✅ |
| 6 | Adversarial (NEW) | 33 | 47 | 80 | 3/4 PASS | ⚠️ |
| 7 | Verification (NEW) | 36 | 52 | 88 | 4/4 PASS | ✅ |

**Execution Average: 89.3 / 100**
**Assertion Pass Rate: 27/28 (96.4%)**

**Skill Veto: PASS.** **Research Veto: PASS** (applicable — Data Analysis category). Both P1s from the pre-fix report are closed on this session's own evidence.

**Final: static 84×0.4=33.6 + dynamic 89.3×0.6=53.6 = 87/100 — ⭐ Production Ready, deployable.**

---

## The two P1s under test

From `_pre-fix-20260918b`:

1. **ENA-mirror header-based column lookup had no guard for a genuinely-absent requested field.** The inline SKILL.md snippet silently printed a false "md5 OK" with zero files downloaded; `download_batch.sh` aborted the *entire* batch on one bad accession because `set -euo pipefail` plus `grep -nx`'s non-match exit status fired before the script's own continue-on-failure guard was ever reached.
2. **The dbGaP boundary section was advisory text only** — no shipped script actually surfaced the recognition signal it described (an ENA response omitting `fastq_ftp`).

The fix (commit `086e443`) adds, in both the SKILL.md inline snippet and `download_batch.sh`, right after `FTP_COL=$(...) || true` / `MD5_COL=$(...) || true`:

```bash
if [ -z "${FTP_COL}" ] || [ -z "${MD5_COL}" ]; then
    echo "fastq_ftp not found in ENA response for ${SRR} -- may indicate controlled-access (dbGaP) data, see SKILL.md 'Controlled-access (dbGaP) data' section" >&2
    exit 1   # (or `continue` in the batch script)
fi
```

---

## Headline finding: the mixed-batch crux holds — and generalizes

This re-audit built its **own** fixtures rather than reusing the fixer's: `CONTROLLEDTEST1` is derived from **ERR10419972's own real, live-fetched ENA TSV shape** (a different real accession than the fixer's fixture) with `fastq_ftp` stripped.

**Input 4 (the crux):** a 3-accession batch — real accession `ERR10419969` (good), `CONTROLLEDTEST1` (bad, synthetic), real accession `ERR10419972` (good) — run through the shipped, unmodified `examples/download_batch.sh`:

```
[1/3] ERR10419969
  Downloading ERR10419969_1.fastq.gz
  md5 OK
  Downloading ERR10419969_2.fastq.gz
  md5 OK

[2/3] CONTROLLEDTEST1
  fastq_ftp not found in ENA response for CONTROLLEDTEST1 -- may indicate controlled-access (dbGaP) data, see SKILL.md 'Controlled-access (dbGaP) data' section

[3/3] ERR10419972
  Downloading ERR10419972_1.fastq.gz
  md5 OK
  Downloading ERR10419972_2.fastq.gz
  md5 OK

=== Summary ===
OK:     2/3
Failed: 1 (see failed.txt)
```

Both good accessions' MD5s match ENA's declared checksums exactly:
```
608d6aefcedebbd0bd38a65924d62fc7  ERR10419969_1.fastq.gz
0d28299dc9684e3e9b38b8d5e0568883  ERR10419969_2.fastq.gz
0976d39fb1c22e0c8005bb85dc743895  ERR10419972_1.fastq.gz
a8cf684044728c175d7ae8f27198249a  ERR10419972_2.fastq.gz
```

**Input 5** repeats this with the bad accession moved to position 1 and to position 3 — identical outcome both times (`OK: 2/3`, same MD5s). **The fix is position-independent, not just correct for the one arrangement the fixer tested.**

This was independently reproduced twice: once fully interactively, and again via a from-scratch consolidated driver script (`run/run_all_inputs.sh`) built after the interactive session — both runs produced byte-identical MD5s for every downloaded file.

---

## New inputs beyond the fixer's own verification

**Input 3 (Edge):** the single-accession case with the independently-built `CONTROLLEDTEST1` fixture, via the inline SKILL.md snippet (extracted programmatically with a Python regex, not hand-copied):
```
$ bash extracted_inline_snippet.sh CONTROLLEDTEST1 out/
fastq_ftp not found in ENA response for CONTROLLEDTEST1 -- may indicate controlled-access (dbGaP) data, see SKILL.md 'Controlled-access (dbGaP) data' section
exit=1
(output dir empty — zero files written)
```
Confirms the false-positive "md5 OK" defect is gone: the script now fails loudly, names the accession, and points at the right section, with no files silently left behind.

**Input 6 (Adversarial) — new defect found:** the mirror-image fixture `CONTROLLEDTEST2` (fastq_ftp *present*, fastq_md5 genuinely *absent*):
```
$ bash extracted_inline_snippet.sh CONTROLLEDTEST2 out/
fastq_ftp not found in ENA response for CONTROLLEDTEST2 -- may indicate controlled-access (dbGaP) data, see SKILL.md 'Controlled-access (dbGaP) data' section
exit=1
```
The **safety property holds** (guard fires, exit 1, zero files) — but the message is **factually wrong**: it says "fastq_ftp not found" when fastq_ftp was present and fastq_md5 was the actually-missing column. This is a real, reproducible message-accuracy defect the fixer's own single-fixture verification would not have caught (their fixture only ever stripped fastq_ftp). Reported as the top (and only) new recommendation, P2 — it does not weaken the guard's core safety behavior, so it does not re-fire M3/M4.

**Input 7 (Verification):** a completely empty/malformed ENA response (`EMPTYRESP1`, no header row and no data row at all) — harsher than a well-formed TSV missing one column:
```
Inline snippet: exit=1, output dir empty.
Batch (mixed with 2 real accessions): OK 2/3, both real accessions' files present and MD5-verified,
only EMPTYRESP1 skipped and logged to failed.txt.
```
The same `-z` guard on `FTP_COL`/`MD5_COL` generalizes correctly to this harsher input shape — no new failure mode (e.g. a bare, unattributed shell error) was found.

---

## Regression check: no happy-path breakage

**Input 1:** inline snippet, real accession `ERR10419835` (used previously by the fixer and prior re-auditors) — 2/2 files, MD5-verified, unaffected by the new guard.

**Input 2:** shipped `download_batch.sh`, all-good 3-accession batch (`ERR10419835`, `ERR10419931`, `ERR10419946`, the fixer's own list) — `OK: 3/3`, all 6 files MD5-verified. The guard does not produce any false positive on well-formed responses.

---

## Detailed Outputs

### Input 1 — Canonical (regression)
**Setup:** Inline SKILL.md "Single SRR via ENA mirror" snippet, extracted programmatically, against `ERR10419835`.
**Executed:** true — `run/full_transcript_inputs1-4.txt`.
**Scores:** Basic 38/40 | Specialized 54/60 | Total 92/100. Assertions 4/4 PASS.

### Input 2 — Variant A (regression)
**Setup:** Shipped `download_batch.sh`, unmodified, 3 real accessions.
**Executed:** true — `run/full_transcript_inputs1-4.txt`.
**Scores:** Basic 38/40 | Specialized 54/60 | Total 92/100. Assertions 4/4 PASS.

### Input 3 — Edge (NEW)
**Setup:** Independent `CONTROLLEDTEST1` fixture (from ERR10419972's real TSV shape), inline snippet.
**Executed:** true — `run/full_transcript_inputs1-4.txt`.
**Scores:** Basic 37/40 | Specialized 53/60 | Total 90/100. Assertions 4/4 PASS.

### Input 4 — Stress, THE CRUX (NEW)
**Setup:** Mixed 3-accession batch, real+bad(middle)+real, shipped `download_batch.sh`.
**Executed:** true, twice (interactive + consolidated driver, identical MD5s) — `run/full_transcript_inputs1-4.txt`.
**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100. Assertions 4/4 PASS.

### Input 5 — Variant B (NEW)
**Setup:** Same mixed batch, bad accession moved to position 1, then position 3.
**Executed:** true — `run/interactive_transcript_inputs5-7.txt` (position 1 also reproduced by the consolidated driver before it was stopped on an unrelated network stall; see note in that file).
**Scores:** Basic 37/40 | Specialized 53/60 | Total 90/100. Assertions 4/4 PASS.

### Input 6 — Adversarial (NEW) — defect found
**Setup:** Reverse-omission fixture `CONTROLLEDTEST2` (fastq_md5 missing, fastq_ftp present), inline snippet.
**Executed:** true — `run/interactive_transcript_inputs5-7.txt`.
**Scores:** Basic 33/40 | Specialized 47/60 | Total 80/100. Assertions 3/4 PASS — the "message accurately names the missing field" assertion FAILs (hardcoded "fastq_ftp not found" wording).

### Input 7 — Verification (NEW)
**Setup:** Completely empty/malformed ENA response (`EMPTYRESP1`), inline snippet + batch (mixed with 2 real accessions).
**Executed:** true — `run/interactive_transcript_inputs5-7.txt`.
**Scores:** Basic 36/40 | Specialized 52/60 | Total 88/100. Assertions 4/4 PASS.

---

## Veto re-evaluation

**Skill Veto: PASS.** No crashes, no infinite loops, no unresolvable dependency issues across 7 executed inputs; every failure mode tested (missing fastq_ftp, missing fastq_md5, empty response, at any batch position) is handled deliberately by the guard, not by an uncontrolled crash.

**Research Veto: PASS.**
- **Scientific integrity:** no fabricated data anywhere in this session's outputs.
- **Practice boundaries:** no diagnostic/prescriptive content.
- **Methodological ground (M3):** the dbGaP section remains present and accurate, and — new this round — the code now genuinely surfaces the signal it describes, closing the pre-fix report's second P1.
- **Code usability (M4):** all shipped scripts pass `bash -n` (this session re-confirmed `download_batch.sh`, the extracted inline snippet, `download_single.sh`, `prefetch_large.sh`) and `py_compile` (`find_sra_runs.py`); the flagship code path is correct and verified across 7 real/synthetic scenarios, well beyond the fixer's own single-fixture test.

## Gate 7 / Gate 8 — re-checked

- **Gate 7 (research scope):** the Skill moves data; it does not diagnose, prescribe, or triage an individual anywhere in this session's outputs. PASS.
- **Gate 8 (shipped-means-present):** all four files SKILL.md/usage-guide.md reference (`download_single.sh`, `download_batch.sh`, `prefetch_large.sh`, `find_sra_runs.py`) are present in `examples/` at commit `086e443` and pass syntax checks. PASS.

## Housekeeping notes

- No writes were made inside `F:\OpenScience\external\` or the fork worktree at any point — the Skill was copied into this auditor's own scratch area and into `run/skill-copy/` before any execution; `git status --porcelain` on the worktree was re-checked clean after this audit.
- The consolidated driver script (`run/run_all_inputs.sh`) was stopped mid-way through re-confirming Input 5 after a single real ENA download stalled on the network for over a minute (confirmed via a persistent, unchanging `curl` PID) — an unrelated, already-multiply-verified code path, not a Skill defect. Every input this report scores was already independently confirmed via direct interactive execution beforehand; see `run/interactive_transcript_inputs5-7.txt` for the full record and the stall note.

> **Note for reviewer:** 6/7 inputs are clean, real, positive confirmations of both fixed P1s, including the crux mixed-batch case at all three accession positions. Input 6 carries this re-audit's one new finding — a cosmetic message-accuracy defect — reported as a single P2, not a veto trigger.
