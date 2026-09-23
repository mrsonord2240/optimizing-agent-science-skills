> **Audit record for `bio-crispr-screens-crispresso-editing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@205c857](https://github.com/mrsonord2240/bioSkills/tree/205c8574b66f30fb04cb2fdbd0464f6d37a70920/crispr-screens/crispresso-editing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-crispresso-editing

Generated: 2026-09-23  
Source: `mrsonord2240/bioSkills@205c8574b66f30fb04cb2fdbd0464f6d37a70920:crispr-screens/crispresso-editing`  
Final-pass exception: `auditor_independent: false` — `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Summary

| Input | Type | Executed | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical Cas9 | No | 31 | 48 | 79 | 3/4 | Partial |
| 2 | CBE | No | 31 | 48 | 79 | 3/4 | Partial |
| 3 | Wrong locus | No | 30 | 46 | 76 | 3/4 | Partial |
| 4 | Pooled | No | 31 | 48 | 79 | 3/4 | Partial |
| 5 | Batch + compare | No | 31 | 47 | 78 | 3/4 | Partial |
| 6 | Parser | Yes | 38 | 56 | 94 | 4/4 | Completed |
| 7 | WGS | No | 30 | 46 | 76 | 3/4 | Partial |
| 8 | Ambiguous BE | No | 31 | 47 | 78 | 4/4 | Partial |
| 9 | Shipped shell example | Yes | 37 | 55 | 92 | 4/4 | Completed |
| 10 | ABE | No | 31 | 48 | 79 | 3/4 | Partial |
| 11 | Prime editor | No | 31 | 48 | 79 | 3/4 | Partial |

Execution average: **80.8 / 100**. Assertion pass rate: **36/44**.

## Fresh evidence

The exact checked source is clean (`HEAD` and branch were verified before the audit). The old audit bundle was preserved at `F:\OpenScience\audits\_pre-fix-20260923\bio-crispr-screens-crispresso-editing\` before this bundle was created.

Freshly passed:

- `scripts/parse_crispresso.py --selftest` → `selftest OK`.
- `python -m py_compile scripts/parse_crispresso.py` → exit 0.
- `bash -n examples/crispresso_analysis.sh` → exit 0.
- Docker daemon probe → `29.7.2`.

Freshly blocked, and not scored as successful execution:

- `run/run_dynamic.ps1` created `audit_crispresso_input1_cas9_*`, but `docker cp` into that created container hung before `CRISPResso` started. The audit process was stopped and that exact `created` container was removed.
- `run/docker_start_probe.ps1` separately attempted `CRISPResso --version`; after 45 seconds the process it started was stopped. Its container was still `created`, then removed. See `run/docker_start_probe_status.txt` and `run/docker_start_probe_container_state.txt`.

The saved suite includes fresh Cas9, CBE, wrong-locus, pooled, batch, positional-compare, parser, WGS, default-BE, shipped-script, ABE, and prime-editor checks. `run/validate_dynamic.py` is intentionally not claimed to have passed because its container-dependent prerequisites were unavailable.

## Detailed checks

### 1. Canonical Cas9

Prompt: quantify Cas9 indels from the FANC amplicon and report mapping plus edited fraction. The command includes FASTQ, amplicon, guide, and named output. The parser’s fresh self-test confirms the expected 250-input / 235-aligned / 94.0% schema. Quality filtering is disclosed as result-changing. Live output was blocked by Docker.

### 2. CBE

Prompt: report target conversion, bystanders, and indels from a CBE amplicon. The command explicitly requests `C -> T`, base-editor output, and a 10-base window. The reference directs users to the per-position table and separately describes target/bystander interpretation. Docker prevented output production.

### 3. Wrong locus

Prompt: distinguish a complete wrong-locus failure from a low-alignment run. The suite intentionally pairs FANC reads with HEK3 sequence and expects failure. Documentation correctly says no percentage should be invented when no output exists. Docker prevented the new expected failure observation.

### 4. Pooled amplicons

Prompt: quantify the two-amplicon pilot pool. The suite explicitly overrides the silent-NA 1000-read default with `--min_reads_to_use_region 100`; the guide requires inspection for `NA` rows. Docker prevented output production.

### 5. Batch and compare

Prompt: process untreated/Cas9 samples then compare output folders. Batch headers, aggregate output layout, and positional `CRISPRessoCompare` syntax are documented. Docker prevented the batch and comparison runs.

### 6. Parser

Prompt: parse a CRISPResso output directory. This was executed: `--selftest` passed the 94.0% mapping and 26.38297872 Modified% assertions, and `py_compile` passed.

### 7. WGS

Prompt: quantify suspected off-target regions from a small BAM. The audit freshly staged BAM, index, upstream small-genome reference, and region table. The guide uses `--bam_file` and explains WGS `NA` rows. Docker prevented execution.

### 8. Ambiguous BE

Prompt: analyze a base editor without declaring CBE or ABE. The decision tree warns that absent conversion flags assume CBE and can misclassify ABE; direction-specific reference commands are available. Docker prevented the default-behavior run.

### 9. Shipped shell example

Prompt: validate the repository’s executable example. `bash -n` was freshly run successfully. The script uses `set -e`, named configuration variables, and positional `CRISPRessoCompare` folders. End-to-end placeholder FASTQ execution needs Docker.

### 10. ABE

Prompt: quantify A-to-G editing in a widened window. The stored command includes `--base_editor_output`, `A`, `G`, window size 10, and center -10; interpretation requires the per-position table. Docker prevented output production.

### 11. Prime editor

Prompt: quantify an intended HEK3 prime edit and scaffold incorporation. The fresh staged synthetic input and command include spacer, extension, and scaffold parameters. The documentation distinguishes intended, scaffold, indel, and unmodified outcomes. Docker prevented the run.

## Gates and decision

- Skill Veto: **PASS** — frontmatter, structure, determinism, and security passed.
- Research Veto: **PASS** — no scientific fabrication, medical diagnosis, methodological redline, or unusable shipped code was found.
- Final score: **84/100 — Limited Release**.
- Deployable: **false**. This is an evidence hold, not a source-code veto: nine core container-dependent checks have no fresh checked outputs.

## Required next action

Restore Docker’s container-start path, then run `run/run_dynamic.ps1`. It must reach `run/validation.json` successfully and produce checked CRISPResso outputs before this report can become deployable.
