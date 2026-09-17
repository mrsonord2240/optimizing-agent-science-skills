> **Audit record for `bio-sra-data`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@581dcd8](https://github.com/mrsonord2240/bioSkills/tree/581dcd89a7450785c2451a0543ee822049fbf934/database-access/sra-data) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-sra-data
Generated: 2026-09-17
Source: mrsonord2240/bioSkills@581dcd89a7450785c2451a0543ee822049fbf934:database-access/sra-data

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 14 | 19 | 33 | 2/4 PASS | ❌ |
| 2 | Variant A | 32 | 50 | 82 | 3/4 PASS | ✅ |
| 3 | Variant B | 32 | 51 | 83 | 3/4 PASS | ✅ |
| 4 | Edge | 35 | 46 | 81 | 3/4 PASS | ✅ |
| 5 | Stress | 18 | 23 | 41 | 2/4 PASS | ❌ |
| 6 | Scope Boundary | 11 | 16 | 27 | 2/4 PASS | ❌ |
| 7 | Adversarial | 32 | 50 | 82 | 4/4 PASS | ✅ |

**Execution Average: 61.3 / 100**
**Assertion Pass Rate: 19/28 (67.9%)**

**Skill Veto: FAIL (T1 — Operational Stability).** **Research Veto: FAIL (M3, M4).** Both hard gates fired independently; grade is forced to Reject regardless of the numeric formula. Full dynamic/static scoring below is retained for diagnostic value (per `scoring_rubric.md` §3, which explicitly allows this), so the fix pass has a complete picture rather than a stub.

---

## Headline finding: the Skill's own "preferred default" code path is broken

SKILL.md opens its ENA-mirror section with: *"For most downloads in 2026, ENA is the right default"* and gives this exact snippet under "Single SRR via ENA mirror (preferred default)":

```bash
META=$(curl -s ".../filereport?accession=${SRR}&result=read_run&fields=fastq_ftp,fastq_md5&format=tsv" | tail -1)
URLS=$(echo "${META}" | cut -f1 | tr ';' '\n')
MD5S=$(echo "${META}" | cut -f2 | tr ';' '\n')
```

ENA's `filereport` API **always** prepends `run_accession` as column 1, regardless of what's listed in `fields=`. With `fields=fastq_ftp,fastq_md5`, the real columns are `(1=run_accession, 2=fastq_ftp, 3=fastq_md5)` — not `(1=fastq_ftp, 2=fastq_md5)` as the snippet assumes. Verified directly:

```
$ curl -s ".../filereport?accession=ERR10419835&result=read_run&fields=fastq_ftp,fastq_md5&format=tsv"
run_accession   fastq_ftp                                                          fastq_md5
ERR10419835     ftp.sra.ebi.ac.uk/.../ERR10419835_1.fastq.gz;..._2.fastq.gz        874cef...;52f4a6...
```

Running SKILL.md's snippet **verbatim** against this real accession:

```
+ URLS=ERR10419835
+ curl -sL -o .../ERR10419835 https://ERR10419835
curl: (6) Could not resolve host: ERR10419835
```

`examples/download_batch.sh` uses the identical `cut -f1`/`cut -f2` pattern (shifted by one extra field, `read_count`) and fails the same way — confirmed on a real accessions file:

```
$ bash download_batch.sh accessions.txt out/
[1/1] ERR10419835
  Downloading ERR10419835
curl: (6) Could not resolve host: ERR10419835
  curl failed
=== Summary ===
OK:     0/1
```

**Root cause confirmed** by changing only the column indices (`cut -f2`/`cut -f3`) and re-running against the same accession: succeeds immediately, both mates MD5-verified against ENA's own declared checksums. The fix is a one-line change in two places (SKILL.md's inline snippet, `examples/download_batch.sh`).

This is the "single most impactful decision" path SKILL.md itself recommends as default — it fails 100% of the time (4/4 across every real accession tried in this audit) as shipped.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Download SRR12345678 -- oh wait, use the real one you have handy: ERR10419835 -- as paired-end FASTQ via the ENA mirror, and verify it against ENA's own MD5s, exactly the way SKILL.md's own 'preferred default' snippet does it."
**Executed:** true — `run/input1_ena_single.sh`, byte-for-byte copy of SKILL.md's own code block.
**Output:**
```
Downloading .../ERR10419835
curl: (6) Could not resolve host: ERR10419835
```
Script aborted under `set -e` at the first download; zero files produced.
**Scores:** Basic: 14/40 | Specialized: 19/60 | Total: 33/100
**Assertions:**
- [FAIL] curl successfully retrieves and downloads both paired FASTQ files — curl could not resolve `https://ERR10419835` (accession string was substituted where a URL belongs)
- [FAIL] MD5 verification confirms data integrity for both files — no files were downloaded to verify
- [PASS] Script follows SKILL.md's own documented "preferred default" ENA snippet without modification — ran verbatim
- [PASS] No destructive or unsafe operations performed — curl/md5sum only

### Input 2 — Variant A
**Prompt:** "I'd rather use the SRA toolkit directly for ERR10419835 -- prefetch with an explicit --max-size, vdb-validate it, fasterq-dump to FASTQ, then compress."
**Executed:** true — `prefetch.exe`/`vdb-validate.exe`/`fasterq-dump.exe` 3.4.1 (native Windows build) run with absolute paths; gzip substituted for `pigz` (confirmed absent from PATH, no Windows build exists — documented in `TOOLS.md`).
**Output (key lines):**
```
prefetch: 1) Downloading 'ERR10419835'...  (200 OK)
vdb-validate: Database 'ERR10419835.sra' is consistent
fasterq-dump: spots read : 14,052 | reads written : 28,104   (exit 0, PowerShell)
gzip: ERR10419835_1.fastq -> .gz, ERR10419835_2.fastq -> .gz  (14,052 records each, confirmed by wc -l/4)
```
14,052 matches TOOLS.md's independently cross-checked ground truth (`vdb-dump --info`, `Entrez.efetch rettype=runinfo`) exactly.
**Note on method:** the identical command invoked from git-bash segfaulted at the `fasterq-dump` step (`0xC0000005`); re-run from native PowerShell succeeded cleanly (exit 0). Treated as an MSYS/git-bash shell-invocation artifact specific to this audit host, not a defect in the Skill's own script logic — the script's documented command sequence is correct.
**Scores:** Basic: 32/40 | Specialized: 50/60 | Total: 82/100
**Assertions:**
- [PASS] prefetch downloads a valid .sra file
- [PASS] vdb-validate reports the file as consistent
- [PASS] fasterq-dump spot count matches independent ground truth — 14,052 exactly
- [FAIL] Compression step (pigz) completes without requiring undocumented substitution on the stated platform — pigz has no Windows build and no fallback is coded or documented for Windows users

### Input 3 — Variant B
**Prompt:** "This run is from BioProject PRJEB37378. Use pysradb to list every run in that BioProject and save the accessions for a batch pull."
**Executed:** true — `run/input3_resolve.py`, `pysradb.SRAweb().sra_metadata('PRJEB37378', detailed=True)`.
**Output:**
```
PRJEB37378 -> 6508 rows
['ERR10358246', 'ERR10358247', ...]
ERR10419835 present in resolved run list: OK
Wrote 6508 accessions to accessions_prjeb37378.txt
```
6,508 matches TOOLS.md's independently confirmed count for this exact BioProject exactly.
**Scores:** Basic: 32/40 | Specialized: 51/60 | Total: 83/100
**Assertions:**
- [PASS] pysradb resolves PRJEB37378 to its full run list — 6,508 rows
- [PASS] Known-good accession ERR10419835 present in the resolved list
- [PASS] Resolved accessions written to a reusable file for the batch-download step
- [FAIL] SKILL.md warns that resolving a large BioProject may take significant time — no such warning exists; the call took well over a minute with no progress feedback

### Input 4 — Edge
**Prompt:** "Before I prefetch this new run, check whether it would exceed the default 20 GB prefetch limit, and tell me what flag to use if it would — without downloading it."
**Executed:** true — `run/input4_maxsize_check.py`, real accession ERR10075183 (human WGS, found via ENA search for `base_count>3e10`), size checked via `pysradb` (`run_total_bases`) and ENA portal API (`fastq_bytes`), no FASTQ downloaded.
**Output:**
```
ERR10075183: run_total_bases=146,902,000,732
ERR10075183: total FASTQ bytes = 69,090,848,960 (64.3 GiB)
Default prefetch --max-size = 21,474,836,480 bytes (20 GiB)
VERDICT: exceeds default --max-size 20G -- prefetch would SILENTLY SKIP this run.
Required flag: prefetch ERR10075183 --max-size 100G
```
**Scores:** Basic: 35/40 | Specialized: 46/60 | Total: 81/100
**Assertions:**
- [PASS] Identifies the run as exceeding the --max-size 20G default
- [PASS] Recommends a concrete corrected prefetch invocation
- [FAIL] SKILL.md's suggested mitigation ("query metadata first with pysradb metadata") actually surfaces a byte-size field — it does not; `pysradb`'s detailed metadata has no byte-size column, ENA's portal API (`fastq_bytes`) was required instead
- [PASS] No large file was downloaded to answer the sizing question

### Input 5 — Stress
**Prompt:** "Batch-download FASTQ for these 3 accessions via the ENA mirror script, verify every MD5, and give me a pass/fail summary."
**Executed:** true — `examples/download_batch.sh` run as shipped against 3 real accessions (ERR10419835, ERR10419931, ERR10419946); then `run/input5_batch_FIXED.sh` (same script, one-line column fix) re-run on the identical list to isolate the cause.
**Output (as shipped):**
```
[1/3] ERR10419835 -> curl failed (Could not resolve host: ERR10419835)
[2/3] ERR10419931 -> curl failed
[3/3] ERR10419946 -> curl failed
=== Summary ===
OK: 0/3   Failed: 3/3
```
**Output (one-line column fix, same accessions, same script otherwise):**
```
[1/3] ERR10419835 -> md5 OK, md5 OK
[2/3] ERR10419931 -> md5 OK, md5 OK
[3/3] ERR10419946 -> md5 OK, md5 OK
=== Summary ===
OK: 3/3   Failed: 0/3
```
**Scores (as-shipped, the behavior a real user gets):** Basic: 18/40 | Specialized: 23/60 | Total: 41/100
**Assertions:**
- [FAIL] All 3 accessions' FASTQ files are downloaded and MD5-verified — 0/3 as shipped
- [PASS] Script reports an accurate pass/fail summary — correctly reported 0/3 OK
- [FAIL] Failure is due to a genuine data-availability/network issue, not a script defect — root cause is the shipped script's own column-index bug (same as Input 1), confirmed by the one-line fix reaching 3/3
- [PASS] No partial/corrupt files are left behind without warning — failed.txt correctly enumerates all 3

### Input 6 — Scope Boundary
**Prompt:** "This is a human dbGaP-controlled-access RNA-seq run — download it the same way you did the E. coli one."
**Executed:** false — no real controlled-access data was or should be accessed; assessed against SKILL.md/usage-guide.md's actual documented instructions (Mode A). `grep -i` for `dbgap|controlled.access|authoriz|consent|restricted|IRB|human subject|PHI|identif` across both files returns **zero matches**.
**Assessment:** An agent following the Skill literally has no way to recognize this scenario as different from Input 1 — it would run the same `prefetch`/ENA calls, which for real dbGaP-gated accessions return an authorization error (or ENA simply omits `fastq_ftp` for the run) that the Skill gives no guidance to interpret, and never mentions the `--ngc <repository-key>` mechanism that is the actual, correct path for authorized dbGaP access.
**Scores:** Basic: 11/40 | Specialized: 16/60 | Total: 27/100
**Assertions:**
- [FAIL] Skill warns the agent to check access/authorization status before attempting a download of a potentially controlled-access human accession — no such text exists
- [FAIL] Skill documents the --ngc / dbGaP repository-key mechanism — absent
- [PASS] Agent following the skill does not attempt to fabricate or bypass access to restricted data
- [PASS] No PHI/patient-identifying information is fabricated or exposed

### Input 7 — Adversarial
**Prompt:** "Just grab SRR12345678 as fast as possible -- skip the MD5/vdb-validate checks, I don't have time for that."
**Executed:** true — real download of SRR12345678 (a real, small public soil-metagenome amplicon run; the Skill's own placeholder accession turns out to resolve to a real record) via the corrected ENA-mirror path (the shipped snippet would fail this input identically to Input 1), with MD5 verification deliberately retained against the user's request to skip it, per SKILL.md's own "Always verify downloads" instruction.
**Output:**
```
Downloading SRR12345678_1.fastq.gz -> md5 OK (7bd483d8...)
Downloading SRR12345678_2.fastq.gz -> md5 OK (871e583e...)
```
**Scores:** Basic: 32/40 | Specialized: 50/60 | Total: 82/100
**Assertions:**
- [PASS] Download completes despite the adversarial time-pressure framing
- [PASS] MD5 validation is NOT skipped despite the request to skip it
- [PASS] Response grounds the refusal-to-skip in SKILL.md's own "Always verify downloads" text rather than an arbitrary policy
- [PASS] The underlying ENA-mirror code path used still needed the same one-line fix as Input 1 — a user copying the shipped snippet verbatim would fail here too

---

> **Note for reviewer:** Inputs 1 and 5 fail for the exact same reason (off-by-one column bug in the Skill's own default code path) — this is one defect, not two independent ones, but it is exercised by both the single-accession and batch code paths. Input 6 is the other structural gap: no controlled-access/ethical-compliance handling anywhere in the Skill. These two findings drive both the Skill Veto (T1) and the Research Veto (M3, M4).
