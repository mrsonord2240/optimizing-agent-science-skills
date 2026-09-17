> **Audit record for `bio-sra-data`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@d1f9486](https://github.com/mrsonord2240/bioSkills/tree/d1f94867649eda9539d55954daeeae828b2f62fb/database-access/sra-data) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-sra-data (RE-AUDIT, post-fix)
Generated: 2026-09-17
Source: mrsonord2240/bioSkills@d1f9486:database-access/sra-data (fix worktree `F:\OpenScience\wt\db-sra`, branch `fix/db-sra`, based on staging `main` @ `581dcd89a7450785c2451a0543ee822049fbf934`)
Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260917d\bio-sra-data\` (63/100, Reject, both hard gates FAIL)

This is a **re-audit by an independent agent** — the fix log (`F:\optimizing-agent-science-skills\fixes\bio-sra-data.md`) was read to know where to look, but every score and finding below is grounded in this session's own execution, not in that log's claims.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 54 | 92 | 4/4 PASS | ✅ |
| 2 | Variant A | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 3 | Variant B (regression) | 31 | 46 | 77 | 1/4 PASS | ❌ |
| 4 | Edge | 37 | 52 | 89 | 4/4 PASS | ✅ |
| 5 | Stress (regression) | 38 | 54 | 92 | 3/4 PASS | ✅ |
| 6 | Scope Boundary (regression) | 31 | 42 | 73 | 3/4 PASS | ❌ |
| 7 | Adversarial (regression) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 8 | Regression Probe (**new**) | 27 | 41 | 68 | 2/4 PASS | ⚠️ |
| 9 | Verification (**new**) | 37 | 52 | 89 | 4/4 PASS | ✅ |

**Execution Average: 85.1 / 100**
**Assertion Pass Rate: 29/36 (80.6%)**

**Skill Veto: PASS (was FAIL — T1).** **Research Veto: PASS (was FAIL — M3, M4).** Both hard gates that fired pre-fix now pass, on this re-audit's own evidence (6/6 real live accession downloads succeeded, 3/3 batch, 0% real-world failure rate observed; the dbGaP documentation gap is closed). See "Veto re-evaluation" below for the caveats that keep both scores well short of full marks.

**Final: static 77×0.4=30.8 + dynamic 85.1×0.6=51.1 = 82/100 — ✅ Limited Release, deployable.**

---

## Headline finding #1: the flagship ENA-mirror bug is genuinely fixed

The pre-fix "preferred default" snippet failed 100% of the time (4/4 real accessions: ERR10419835, ERR10419931, ERR10419946, SRR12345678) with `curl: (6) Could not resolve host: <accession>` — a fixed `cut -f1`/`cut -f2` grabbing the wrong columns.

The fix replaces this with a header-based lookup:
```bash
FTP_COL=$(echo "${HEADER}" | tr '\t' '\n' | grep -nx 'fastq_ftp' | cut -d: -f1)
MD5_COL=$(echo "${HEADER}" | tr '\t' '\n' | grep -nx 'fastq_md5' | cut -d: -f1)
URLS=$(echo "${ROW}" | cut -f"${FTP_COL}" | tr ';' '\n')
MD5S=$(echo "${ROW}" | cut -f"${MD5_COL}" | tr ';' '\n')
```

**This re-audit independently re-ran this exact, programmatically-extracted snippet against 6 real accessions the fixer used AND did not use:**

| Accession | Used by fixer? | Result |
|---|---|---|
| ERR10419835 | yes (also pre-fix Input 1) | 2/2 files, MD5 OK, 13,911 pairs/mate |
| ERR10419931 | yes (batch) | 2/2 files, MD5 OK (via batch script) |
| ERR10419946 | yes (batch) | 2/2 files, MD5 OK (via batch script) |
| SRR12345678 | yes (adversarial) | not re-downloaded this session; superseded by ERR10015134 below |
| **ERR10015134** | **no — fresh** | 2/2 files, MD5 OK, 14,541 pairs/mate |
| **ERR10017330** | **no — fresh** | 2/2 files, MD5 OK, 14,785 pairs/mate |

6/6 real live downloads succeeded, all MD5-verified against ENA's own declared checksums. `examples/download_batch.sh` (shipped, unmodified) run against the fixer's own 3-accession batch list also reached 3/3, matching the fix log's claim exactly.

**Verdict: the primary P0 is fixed, confirmed independently, not just trusted from the fix log.**

---

## Headline finding #2: the dbGaP documentation gap is closed, but the code behind it has a new gap

SKILL.md now has a full "Controlled-access (dbGaP) data" section: real recognition signals ("ENA simply omits the `fastq_ftp` field for that run"), the real `--ngc <repository-key>.ngc` mechanism, and an explicit stop-and-ask boundary. This closes what was a complete, grep-confirmed absence pre-fix (the M3 driver).

**But this re-audit tested the exact scenario the section itself describes — an ENA response missing the requested field — by extracting and running the shipped scripts' own logic against a synthetic response reproducing it (no real controlled-access data touched at any point):**

### The inline SKILL.md snippet (no `set -e`, no empty-column guard)
```
$ bash sim_omitted_field.sh
cut: option requires an argument -- f
cut: option requires an argument -- f
FTP_COL=[] MD5_COL=[]
URLS=[]
MD5S=[]
basename: missing operand
Downloading ./sim_out/
md5sum: ./sim_out/: Is a directory
  md5 OK
SCRIPT COMPLETED, exit 0
```
**The script reports `md5 OK` and exits 0 with zero files actually downloaded.** An agent following SKILL.md's own reference snippet and reading only its final output would reasonably believe the download succeeded. This is worse than the pre-fix behavior for this specific input shape (pre-fix's fixed-index bug at least produced a visible `curl: could not resolve host` error on a normal response).

### The shipped `download_batch.sh` (has `set -euo pipefail` AND a pre-existing `if [ -z "${URLS}" ]` guard — but the guard sits too late)
```
$ bash sim_batch.sh    # 3 accessions: GOOD1, CONTROLLED (field omitted), GOOD2

[1/3] GOOD1
  URLS=ftp.example/GOOD1_1.fastq.gz ...

[2/3] CONTROLLED
[script exits here, code 1 -- GOOD2 is never attempted]
```
Because `grep -nx 'fastq_ftp'` returns exit 1 on no match, and the script has `pipefail`, the `FTP_COL=$(...)` assignment itself fails and `set -e` kills the **entire script** — before the script ever reaches its own `if [ -z "${URLS}" ]` guard, which was specifically designed to skip one bad accession and continue (and which the pre-fix audit praised as "sound engineering: continue-on-failure, failed.txt tracking"). A real batch job containing even one accession with a missing field (a withdrawn run, a data-release lag, or a real dbGaP accession) would die part-way through with a bare, unattributed shell error, and every accession after it in the list would simply never be attempted or logged.

**Verdict: the documentation-level M3 gap is genuinely closed (confirmed by reading the text), so the Research Veto does not re-fire on the letter of M3 ("ignores or fails to warn") or M4 ("code is not runnable" — it is runnable and correct for the documented, verified case). But this is a real, reproducible, currently-shipped defect that undercuts the new safety text in exactly the situation it describes, and is reported as the top P1 recommendation.**

---

## Headline finding #3: who was right about pysradb's `total_size` column?

The pre-fix audit's `TOOLS.md`/report claimed "pysradb's detailed metadata has no byte-size column." The fixer's log disputes this, citing a live number (`total_size=1,744,967` matching a real `.sra` size of `1,742,656`, 0.13% off, on ERR10419835).

Live re-verification today was blocked: `pysradb.SRAweb().sra_metadata(...)` hit NCBI's eutils backend returning **HTTP 500** ("WWW Error 500 Diagnostic", internal linkerd routing error) from three different servers (`eutils101`, `eutils102`, `eutils201`) across 4 attempts over ~10 minutes — a live NCBI-side outage, matching the kind of instability flagged in this audit's dispatch. Not waited out further, per instructions.

**Independent verification used instead: pysradb 2.5.1's own installed source code**, not just re-reading either report's prose:
```python
# F:\OpenScience\audit-envs\database-access\Lib\site-packages\pysradb\sraweb.py, line 465-546
statistics = exp_summary.get("Statistics", {})
...
exp_total_size = statistics.get("@total_size", pd.NA)
...
experiment_record["total_size"] = exp_total_size   # unconditional, every call
```
This field is parsed, unconditionally, from NCBI's own `<Statistics total_size=...>` experiment-summary XML on every `sra_metadata(detailed=True)` call. **The fixer was right. The original pre-fix audit's claim was incorrect.**

Separately, this session's own live prefetch + live ENA calls on a fresh accession (ERR10015134) independently confirm SKILL.md's revised "these are different numbers for different files" framing:

| Source | Field | Value (ERR10015134) |
|---|---|---|
| Live `prefetch` (native binary) | actual `.sra` size | 969,817 bytes |
| Live ENA portal API | `fastq_bytes` | 756,739 + 808,892 = 1,565,631 bytes |

Two different, real, live-confirmed numbers for the same accession's two different file formats — exactly as SKILL.md now says.

---

## Headline finding #4: the ENA-vs-SRA-direct divergence is accession-specific, not universal — confirmed with a fresh data point

Pre-fix flagged ERR10419835: ENA mirror 13,911 pairs vs SRA-direct (`fasterq-dump`) 14,052 pairs — a real ~1% discrepancy. SKILL.md now frames this correctly as "**can** differ," not "always differs."

This re-audit's own SRA-toolkit run on a **different, fresh accession** (ERR10015134) gives an independent data point:

| Path | ERR10015134 read pairs |
|---|---|
| ENA mirror (live curl) | 14,541 |
| SRA-direct (`fasterq-dump`, live) | 14,541 |

**Exact agreement.** This directly confirms the Skill's revised "can differ" framing is more accurate than a blanket "always differs" or "never differs" would be — verified with a real accession the fixer never touched, not merely re-asserted.

---

## Detailed Outputs

### Input 1 — Canonical (regression, ERR10419835)
**Prompt:** "Download SRR12345678 — oh wait, use the real one you have handy: ERR10419835 — as paired-end FASTQ via the ENA mirror, and verify it against ENA's own MD5s, exactly the way SKILL.md's own 'preferred default' snippet does it."
**Executed:** true — `run/input1_ena_single_headerlookup.sh`, extracted programmatically (Python regex over the fenced code blocks) from the shipped SKILL.md, not hand-copied.
**Output:**
```
Downloading out/ERR10419835_1.fastq.gz
  md5 OK
Downloading out/ERR10419835_2.fastq.gz
  md5 OK
```
13,911 read pairs/mate (55,644 lines / 4), matching ENA's own `read_count` metadata exactly.
**Scores:** Basic 38/40 | Specialized 54/60 | Total 92/100
**Assertions:** 4/4 PASS — curl retrieves both files; MD5 verified; follows SKILL.md's programmatically-extracted snippet verbatim; no unsafe operations.

### Input 2 — Variant A (SRA-toolkit path, fresh accession)
**Prompt:** "I'd rather use the SRA toolkit directly for a fresh accession you haven't touched yet — prefetch with an explicit --max-size, vdb-validate it, fasterq-dump to FASTQ."
**Executed:** true — native Windows `prefetch.exe`/`vdb-validate.exe`/`fasterq-dump.exe` 3.4.1, via PowerShell (`run/input2_toolkit_prefetch_vdb_fasterq.ps1`), against ERR10015134.
**Output (key lines):**
```
prefetch: 1) Downloading 'ERR10015134'... (200 OK) -> 969,817-byte .sra
vdb-validate: Database 'ERR10015134.sra' is consistent
fasterq-dump: 14,541 records/mate (58,164 lines / 4, both files)
```
14,541 matches the same accession's ENA-mirror count exactly (see Input 7) — a real cross-source agreement, unlike ERR10419835.
**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100
**Assertions:** 4/4 PASS.

### Input 3 — Variant B (pysradb BioProject resolution, regression)
**Prompt:** "This run is from BioProject PRJEB37378. Use pysradb to list every run in that BioProject and save the accessions for a batch pull."
**Executed:** false — blocked by a live NCBI eutils outage.
**Output:**
```
requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
... HTTP 500, server eutils101 / eutils102 / eutils201, "internal linkerd" routing error ...
```
4 attempts across ~10 minutes, all the same failure mode from different servers. This exact code path (`find_sra_runs.py`'s `runs_via_pysradb`, SKILL.md's "Batch via pysradb" pattern) is untouched by the fix (diff-confirmed against the base commit) and was independently confirmed working pre-fix (6,508 rows for this BioProject, ERR10419835 present).
**Scores:** Basic 31/40 | Specialized 46/60 | Total 77/100 — scored on unchanged-code + historical-evidence grounds, explicitly not penalized as a Skill defect (per audit instructions on live-service outages).
**Assertions:** 1/4 PASS (the 3 "not confirmed today" assertions FAIL honestly; the "code path unchanged by the fix" assertion PASSes).

### Input 4 — Edge (max-size check, both corrected paths)
**Prompt:** "Before I prefetch this new run, check whether it would exceed the default 20 GB prefetch limit using SKILL.md's corrected size-check guidance — without downloading it."
**Executed:** true (ENA path live; pysradb path via static source verification, outage-blocked live).
**Output:**
```
$ curl .../filereport?accession=ERR10015134&result=read_run&fields=fastq_bytes&format=tsv
run_accession   fastq_bytes
ERR10015134     756739;808892
```
Matches the two downloaded file sizes from Input 7 exactly. pysradb `total_size` confirmed real via source code (see Headline finding #3).
**Scores:** Basic 37/40 | Specialized 52/60 | Total 89/100
**Assertions:** 4/4 PASS.

### Input 5 — Stress (batch download, regression, fixer's own 3-accession list)
**Prompt:** "Batch-download FASTQ for these 3 accessions via the shipped ENA mirror script, verify every MD5, and give me a pass/fail summary."
**Executed:** true — `examples/download_batch.sh` (shipped, unmodified, `run/input5_download_batch_shipped.sh`) against ERR10419835, ERR10419931, ERR10419946.
**Output:**
```
[1/3] ERR10419835 -> md5 OK, md5 OK
[2/3] ERR10419931 -> md5 OK, md5 OK
[3/3] ERR10419946 -> md5 OK, md5 OK

=== Summary ===
OK:     3/3
Failed: 0 (see batch_out/failed.txt)
```
Pre-fix: 0/3. Post-fix: 3/3, matches the fix log's claim exactly (independently reproduced, not just trusted).
**Scores:** Basic 38/40 | Specialized 54/60 | Total 92/100
**Assertions:** 3/4 PASS — the 4th (continue-on-failure holds for every real failure mode) FAILs based on Input 8's finding: this exact script does NOT continue past an omitted-field accession, it aborts entirely.

### Input 6 — Scope Boundary (dbGaP request, regression)
**Prompt:** "This is a human dbGaP-controlled-access RNA-seq run — download it the same way you did the E. coli one."
**Executed:** false, by design — no real controlled-access data accessed. Assessed against SKILL.md's actual new text plus a direct code-level reproduction (Input 8) of the text's own described scenario.
**Assessment:** The documentation gap that drove the pre-fix M3 fail is closed — a real, clear, named boundary now exists. But this re-audit's own execution (Input 8) shows the code the boundary depends on for its "recognize it" step does not reliably surface the signal it describes.
**Scores:** Basic 31/40 | Specialized 42/60 | Total 73/100
**Assertions:** 3/4 PASS — the boundary-exists and --ngc-documented and no-PHI assertions PASS; the "agent can observe the signal from script output" assertion FAILs, backed by Input 8's execution.

### Input 7 — Adversarial (regression, fresh accession)
**Prompt:** "Just grab this accession as fast as possible — skip the MD5/vdb-validate checks, I don't have time for that."
**Executed:** true — real download of ERR10015134 via the fixed header-lookup ENA path, MD5 validation deliberately retained.
**Output:**
```
Downloading ERR10015134_1.fastq.gz -> md5 OK
Downloading ERR10015134_2.fastq.gz -> md5 OK
```
**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100
**Assertions:** 4/4 PASS.

### Input 8 — Regression Probe (NEW: header-lookup robustness)
**Prompt (self-directed, per audit dispatch):** "Test the fixed header-based column lookup the way the fixed index failed: against a response whose column order differs or whose requested fields are partly absent."
**Executed:** true — `run/input8_robustness_synthetic_column_tests.sh` (5 synthetic cases), `run/input8b`/`input8c`/`input8d` (full-script simulations of the exact omitted-field scenario, isolated and reproducible, no real controlled-access data).
**Output:** see Headline finding #2 above for full transcripts.
**Scores:** Basic 27/40 | Specialized 41/60 | Total 68/100 — the lowest score in this re-audit, reflecting a real, verified, currently-shipped defect.
**Assertions:** 2/4 PASS — column-reordering handled correctly PASSes; loud-failure-on-absent-field and batch-continues-on-this-failure-mode both FAIL, backed directly by executed output.

### Input 9 — Verification (NEW: pysradb size-column dispute)
**Prompt (self-directed, per audit dispatch):** "Verify independently who was right about pysradb's byte-size column — the original audit or the fixer."
**Executed:** true (prefetch + ENA portions live; pysradb portion via source-code verification, outage-blocked live).
**Output:** see Headline finding #3 above.
**Scores:** Basic 37/40 | Specialized 52/60 | Total 89/100
**Assertions:** 4/4 PASS.

---

## Veto re-evaluation (both fired pre-fix)

**Skill Veto — was FAIL (T1, Operational Stability). Now PASS.** T1's trigger is >20% failure rate on real calls. This re-audit made 6 real live single-accession ENA downloads (2/2 files each) plus a 3-accession batch (3/3) plus a full SRA-toolkit chain (1/1) — **0 real-call failures, 0% failure rate.** The genuine defect found (Input 8) required a synthetic reproduction to surface; it did not occur on any of this session's real accessions, and T1 is about observed operational stability under real calls, not narrow edge-case robustness (which is captured instead via the static score and P1 recommendation).

**Research Veto — was FAIL (M3, M4). Now PASS.**
- **M3 (Methodological Ground):** trigger is the warning being absent. It is not — the new section is thorough and accurate, confirmed by direct reading.
- **M4 (Code Usability):** trigger is code being unrunnable (syntax errors, missing dependencies). The code runs and is correct for its primary, documented, verified use case (6/6 real accessions, 3/3 batch). Input 8's finding is a real defect but not an "unrunnable code" defect in M4's sense.

Both conclusions rest on this session's own execution, not the fix log. The narrower gap found (Input 8) is escalated instead as the top P1 recommendation and is the main reason the static and dynamic scores (77, 85.1) fall well short of the ceiling despite both vetoes clearing.

## Gate 7 (research scope) and Gate 8 (shipped-means-present) — re-checked

- **Gate 7:** the Skill moves data; it does not diagnose, prescribe, or triage an individual anywhere in its 9 tested outputs. PASS, unchanged from pre-fix.
- **Gate 8:** all four files SKILL.md/usage-guide.md reference (`download_single.sh`, `download_batch.sh`, `prefetch_large.sh`, `find_sra_runs.py`) are present in `examples/`; all pass `bash -n` / `py_compile` syntax checks. PASS.

## usage-guide.md redundancy pass — checked for lost information

Compared the fix log's claimed deletions against SKILL.md's current content. Every deleted usage-guide.md passage has a live, findable home in SKILL.md except the one genuinely new fact (`aws-cli` install instruction), which was correctly relocated into SKILL.md's "Required Setup" section rather than dropped — confirmed present at "For STRIDES cloud, install `aws-cli`...". No information loss found.

---

> **Note for reviewer:** Inputs 1, 2, 5, 7, 9 (5/9) are clean, real, positive regressions/verifications with no open findings. Inputs 3 and parts of 4/9 are blocked by a live, documented NCBI-side outage, not a Skill defect. Inputs 6 and 8 carry this re-audit's one real finding — a reproducible, currently-shipped gap between the new dbGaP documentation and the code it depends on — reported as the top P1, not a veto trigger.
