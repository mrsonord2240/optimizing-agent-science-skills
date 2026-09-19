> **Audit record for `bio-ncbi-datasets-cli`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@bac15cc](https://github.com/mrsonord2240/bioSkills/tree/bac15ccbda059dfec158576ae61cf7249a673cdb/database-access/ncbi-datasets-cli) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-ncbi-datasets-cli (RE-AUDIT)

Generated: 2026-09-19
Re-audit of: `F:\OpenScience\audits\_pre-fix-20260919\bio-ncbi-datasets-cli\` (73, Beta Only, not deployable)
Fix under review: `F:\optimizing-agent-science-skills\fixes\bio-ncbi-datasets-cli.md`
Source: `mrsonord2240/bioSkills@bac15cc:database-access/ncbi-datasets-cli`
Worktree: `F:\OpenScience\wt\db-ndc`, branch `fix/db-ncbi-datasets`
Environment: `F:\OpenScience\audit-envs\database-access\` — NCBI Datasets CLI 18.37.0 (native Windows binaries), live public NCBI access; WSL `science`/`bio` for the `aria2c` leg only.

**This is an independent re-audit.** I did not write the fix and treated the fix log as a claim,
not evidence — every one of its 6 findings was re-run from scratch, and I ran 3 new inputs beyond
the fixer's own test cases.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 37 | 54 | 91 | 4/4 PASS | ✅ |
| 3 | Edge (regression) | 36 | 53 | 89 | 4/4 PASS | ✅ |
| 4 | Variant B (regression) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 5 | Stress (regression, new species) | 37 | 54 | 91 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (regression) | 39 | 54 | 93 | 3/3 PASS | ✅ |
| 7 | Adversarial (regression) | 36 | 52 | 88 | 3/3 PASS | ✅ |
| 8 | Variant C — ortholog generalization (NEW) | 38 | 55 | 93 | 3/3 PASS | ✅ |
| 9 | Scope Boundary — virus workflow (NEW) | 33 | 47 | 80 | 3/4 | ⚠️ |
| 10 | Adversarial — rehydrate verification probe (NEW) | 22 | 30 | 52 | 1/4 | ❌ |

**Execution Average: 86.3 / 100**
**Assertion Pass Rate: 33/37**
**Static Score: 90/100 (was 74/100 pre-fix)**
**Final Score: 87.8/100 — ⭐ Production Ready (was 73, ⚠️ Beta Only, pre-fix)**

> Reviewer note: check ⚠️/❌ rows first. Input 10 found a genuinely new, previously-undetected
> defect — read it before landing.

## Detailed Outputs

### Input 1 — Canonical (regression): phiX174 download + dataformat

**Command:**
```bash
datasets download genome accession GCF_000819615.1 \
  --include genome,gff3,protein,cds,seq-report --filename phix.zip --no-progressbar
dataformat tsv genome --inputfile phix/ncbi_dataset/data/assembly_data_report.jsonl \
  --fields accession,organism-name,assminfo-level,assmstats-scaffold-n50,assmstats-contig-n50,assmstats-total-sequence-len
```
**Output:** Organism "Escherichia phage phiX174", 11 CDS, one correct TSV row
(`GCF_000819615.1 | Escherichia phage phiX174 | Complete Genome | 5386 | 5386 | 5386`). No field
errors — the pre-fix run's #1 failure mode is gone.

Also cross-checked a *different* `--fields` combination than the fixer's own test — the
"Filter assemblies by quality and date" pattern (`assminfo-release-date`):
```
datasets summary genome taxon "Salmonella enterica" --assembly-level chromosome,complete \
  --released-after 2024-01-01 --as-json-lines | dataformat tsv genome \
  --fields accession,organism-name,assminfo-level,assmstats-scaffold-n50,assminfo-release-date
```
1,764 real rows, real dates ≥ 2024-01-01.

**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:** 4/4 PASS (all field lists resolve, correct data, second independent field
combination also clean).

---

### Input 2 — Variant A (regression): BRCA1 gene metadata across Mammalia

**Command:** `bash examples/gene_metadata.sh` (unmodified, default args BRCA1/Mammalia)
**Output:** 272-row TSV (271 real mammal species + header) — human, mouse, rat, dog, cow, macaque,
chimp, opossum, pig. Exactly reproduces the fixer's own claimed result.

**Scores:** Basic: 37/40 | Specialized: 54/60 | Total: 91/100
**Assertions:** 4/4 PASS.

---

### Input 3 — Edge (regression): dehydrated discovery + rehydrate, single accession

fetch.txt confirmed still 3 tab-separated columns on 18.37.0 (`<url>`, `"0"` placeholder,
`<path>`) — SKILL.md and `bulk_dehydrated.sh` now correctly describe 3, not 2. Clean-directory
`datasets rehydrate` recovers the real file. Reverted the awk fix locally (`$2` instead of `$3`)
to confirm the script's own sanity check correctly fires and exits before any download.

**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:** 4/4 PASS. *(See Input 10 — this input's happy path does not surface the
rehydrate-verification gap found there.)*

---

### Input 4 — Variant B (regression): NCBI ortholog set, `--ortholog all`

```
datasets summary gene symbol BRCA1 --taxon human --ortholog all --as-json-lines
```
558 real ortholog records, exact match to the fix log's claim. Bare `--ortholog` (no value) still
fails with the same misleading "taxonomy name '--as-json-lines' is not exact" error — but SKILL.md
no longer presents that broken form as the happy path; it's documented as a Common error instead.

**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:** 4/4 PASS.

---

### Input 5 — Stress (regression, fresh species): bulk dehydrated pull

The fixer verified the awk `$2`→`$3` fix on Deinococcus radiodurans and GCF_000819615.1 only. Ran
the identical mechanism on two unrelated genera the fixer never touched:

- **Mycoplasma genitalium** (`--reference --annotated --assembly-source RefSeq`): 1 genome, 3
  files queued, 3 columns, correct `out=` paths, zero `out=0` lines, `datasets rehydrate` →
  "Completed 3 of 3", real FASTA/GFF/protein content confirmed against `dataset_catalog.json`'s
  own recorded byte sizes.
- **Buchnera aphidicola**: same mechanism, same clean result on the awk transform.

**Scores:** Basic: 37/40 | Specialized: 54/60 | Total: 91/100
**Assertions:** 4/4 PASS.

---

### Input 6 — Scope Boundary (regression): SRA reads

`datasets download --help` still lists only `gene, genome, taxonomy, virus` — no SRA subcommand.
Unchanged from pre-fix; correctly out of scope per SKILL.md's own table.

**Scores:** Basic: 39/40 | Specialized: 54/60 | Total: 93/100
**Assertions:** 3/3 PASS.

---

### Input 7 — Adversarial (regression): nonexistent / malformed accessions

`GCF_999999999.1` → `{"total_count": 0}`, exit 0 (unchanged CLI behavior — this is inherent to the
CLI, not something the Skill can fix). `NOT_AN_ACCESSION` → clear error, exit 1. The pre-fix P2 is
closed: SKILL.md's Common errors table now has a row for the silent-zero-count case.

**Scores:** Basic: 36/40 | Specialized: 52/60 | Total: 88/100
**Assertions:** 3/3 PASS.

---

### Input 8 — Variant C (NEW): ortholog generalization beyond BRCA1

The fixer verified `--ortholog` only on BRCA1/Mammalia. Tested a second human gene and the other
clade SKILL.md claims coverage for:

- `gene_metadata.sh TP53 Mammalia` → 272 rows (271 real mammal TP53/Trp53/Tp53 orthologs: human,
  mouse, rat, dog, pig, cattle, macaque, cat, rabbit, horse, ...).
- `datasets summary gene symbol white --taxon "Drosophila melanogaster" --ortholog Insecta` → 150+
  real insect species (Drosophila, Anopheles gambiae, Bombyx mori, Aedes aegypti, Tribolium
  castaneum, mosquitoes, moths, beetles, ...) for the eye-pigment transporter gene "white", which
  has no human ortholog — this deliberately exercises a gene/clade combination where the default
  `--taxon human` would return nothing, confirming `--taxon <species> --ortholog <clade>` is the
  correct general pattern, not just a BRCA1-specific coincidence.

**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:** 3/3 PASS.

---

### Input 9 — Scope Boundary (NEW): virus genome download

`datasets download virus genome taxon "SARS-CoV-2" --refseq` — named in SKILL.md's scope table but
never exercised by the original 7-input audit or the fix. Works correctly: 5-file zip
(`genomic.fna` 30,428 bytes — consistent with the real ~29.9 kb SARS-CoV-2 genome, plus
`data_report.jsonl`, `dataset_catalog.json`, `md5sum.txt`, `README.md`).

**Gap found:** SKILL.md's "Code patterns" section has worked examples for genome/gene/orthologs
but nothing for virus — an agent following the doc has only the one-line scope-table mention to
go on, no `--include` guidance, no `dataformat virus-genome --fields` example.

**Scores:** Basic: 33/40 | Specialized: 47/60 | Total: 80/100
**Assertions:** 3/4 PASS — 1 FAIL ("SKILL.md provides a complete, testable code pattern for virus
workflows"). **P2 recommendation filed.**

---

### Input 10 — Adversarial (NEW): does `datasets rehydrate` actually verify anything?

**This is the most important finding of the re-audit.** SKILL.md's "Checksum verification
(automatic)" section says: *"Rehydrate workflows also verify. If a file fails checksum, Datasets
retries up to 3 times then errors."* `bulk_dehydrated.sh`'s own Step 3 comment says: *"datasets
rehydrate validates checksums of all files."*

**Test 1 — real network failure.** Ran the fixed `bulk_dehydrated.sh` pipeline end-to-end
(`datasets download --dehydrated` → fixed awk transform → `aria2c` via WSL `science`/`bio` →
`datasets rehydrate` as "Step 3: verify"). The `aria2c` leg hit a live NCBI bot-block
(`misuse.ncbi.nlm.nih.gov/error/abuse.shtml`) and silently wrote the abuse-page HTML (3,876 bytes,
identical size for all 3 files) into the correct target paths with `aria2c` reporting "Download
complete" for each — this part matches the fixer's own note about a WSL-side bot-block being a
known, separate issue. But then running `datasets rehydrate --directory .` as documented — the
Skill's own recommended verification step — reported **"All 3 files already rehydrated"** and left
the HTML garbage in place. No error, no retry, no re-download.

**Test 2 — isolated, no network involved.** To rule out this being a fluke of the bot-block
specifically, manually replaced a genuinely-correct, previously-rehydrated `genomic.gff` (real
size 373,156 bytes, exactly as recorded in the tool's own `dataset_catalog.json`) with a 50-byte
placeholder string, then re-ran `datasets rehydrate --directory .`. Identical result: **"All 3
files already rehydrated,"** file left at 50 bytes.

```
$ python -c "... print catalog uncompressedLengthBytes ..."
GCF_040556925.1/genomic.gff 373156
$ echo "THIS IS NOT REAL GFF DATA - CORRUPTED FOR TESTING" > .../genomic.gff
$ ls -la .../genomic.gff
-rw-r--r-- 1 User 197121 50 ... genomic.gff
$ datasets rehydrate --directory myco_dehy/ --max-workers 4
All 3 files already rehydrated
$ cat .../genomic.gff
THIS IS NOT REAL GFF DATA - CORRUPTED FOR TESTING
```

`datasets rehydrate` appears to check only whether a file exists at the expected relative path —
not its size (despite recording the correct expected size in its own catalog) and not a checksum.
This directly contradicts the documented safety net for exactly the compound
dehydrate→aria2c→rehydrate pattern SKILL.md recommends for HPC/cloud bulk pulls (1000+ genomes),
where partial/corrupted transfers are the realistic failure mode the "verify" step exists to catch.

Note this is **not** a regression from the fix under review — the awk `$2`→`$3` fix is correct and
verified (Inputs 3/5); this is a pre-existing property of `datasets rehydrate` itself that neither
the original audit nor the fix pass happened to exercise, because both only ran rehydrate against
clean, never-touched directories.

**Scores:** Basic: 22/40 | Specialized: 30/60 | Total: 52/100
**Assertions:** 1/4 PASS. **P1 recommendation filed** — does not veto (no fabrication, no harm; the
simple/clean-state paths remain safe and verified), but is a real, reproducible integrity gap in
the documented safety net for the Skill's recommended bulk workflow.

## Redundancy Pass Check (usage-guide.md)

Confirmed: `usage-guide.md` (58 lines) holds only Overview, Quick Start, Example Prompts, Related
Skills — the claimed Prerequisites/8-step "What the Agent Will Do"/Tips sections are gone. Diffed
every fact those sections held against SKILL.md's Installation, Version Compatibility, scope table,
Subcommand taxonomy, Key parameters, `--dehydrated` section, and Failure modes/Common errors: every
fact is present, correct, and stated exactly once. The stale `--taxon --ortholog` bare-flag claim
and stale genome `--fields` list that were duplicated inside `usage-guide.md`'s own Example Prompts
text are also fixed there (not just in SKILL.md).

## Veto Gates

- **Skill Veto (structural):** PASS — unchanged, no stability/contract/determinism/security issues.
- **Research Veto:** PASS — all 4 dimensions pass; Code Usability now PASS on both axes (CLI works,
  and all 3 shipped example scripts now also run unmodified and produce correct output, unlike
  pre-fix where only the CLI half of that claim held).

## Landing Decision

Final score 87.8 ≥ 85, deployable, no open P0, no veto → **PASSES.** Proceeding to merge, promote,
and file the Input 10 finding as a P1 recommendation for a future fix + re-audit round (per this
project's auditor/fixer/re-auditor separation — not fixed in this pass).
