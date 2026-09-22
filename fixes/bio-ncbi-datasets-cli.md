# Fix log: bio-ncbi-datasets-cli

2026-09-19 — fixer pass on `fix/db-ncbi-datasets` (worktree `F:\OpenScience\wt\db-ndc`),
commit `bac15cc`, base `mrsonord2240/bioSkills@339f73e`.
Source audit: `F:\OpenScience\audits\bio-ncbi-datasets-cli\` (73/100, Beta Only, not deployable, no veto).
All verification ran live against NCBI Datasets CLI 18.37.0 (`datasets.exe`/`dataformat.exe`,
`F:\OpenScience\audit-envs\database-access\tools\ncbi-datasets-cli\`) and the public NCBI Datasets API.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| "Gene metadata across species" pattern (SKILL.md's flagship example, `gene_metadata.sh`'s own default): `--taxon Mammalia` on `summary gene symbol` errors outright -- `--taxon` is single-species only | P1 | Reworked the pattern and script to use `--ortholog <taxon\|all>` instead -- confirmed via live `--help` that `--ortholog` accepts any taxonomic rank (not just `all`), and this is the CLI's only real cross-species mechanism (limited to vertebrates/insects) | ran | `datasets summary gene symbol BRCA1 --ortholog Mammalia --as-json-lines \| dataformat tsv gene --fields gene-id,symbol,tax-name,description,chromosomes` returns 272 real rows (human, mouse, rat, dog, cow, macaque, chimp, opossum, pig, ...). Ran the fixed `gene_metadata.sh` end-to-end with its own new defaults (BRCA1, Mammalia) -- correct output, no crash. |
| `dataformat --fields` names stale across every shipped code block (genome and gene) | P1 | `assembly-level`->`assminfo-level`, `scaffold-n50`->`assmstats-scaffold-n50`, `contig-n50`->`assmstats-contig-n50`, `total-sequence-length`->`assmstats-total-sequence-len`, `taxname`->`tax-name`, `submission-date`->`assminfo-release-date`. `nomenclature-authority-symbol` dropped entirely -- no replacement field exists. Updated SKILL.md (4 code blocks), `download_genome.sh`, and a stale field list embedded in usage-guide.md's example prompt text | ran + help | Corrected fields verified against `dataformat tsv genome --help` / `dataformat tsv gene --help`'s live field catalogs, then run for real: phiX174 (GCF_000819615.1) assembly stats, Salmonella enterica release-date query (3 real rows with dates), BRCA1 ortholog TSV. |
| `bulk_dehydrated.sh`'s aria2c awk transform silently corrupts every downloaded filename | P1 | `fetch.txt` is 3 tab-separated columns (`<url>`, a `"0"` placeholder, `<path>`) on 18.37.0, not the 2 the script assumed. Changed the awk field index from `$2` to `$3`; added a sanity check that exits with an error if any generated line still reads `out=0` | ran | Real dehydrated download of GCF_000819615.1 and of Deinococcus radiodurans (3 files): fixed awk produces real paths (e.g. `out=data/GCF_020546685.1/protein.faa`), sanity check passes (no `out=0` lines), `datasets rehydrate` recovers the same files at those exact paths, and `aria2c` (WSL `science`/`bio`) accepted the fixed input file and queued the correct filenames -- the byte transfer itself was interrupted by an NCBI-side bot-block / WSL network flakiness unrelated to the column-index fix (the signed `fetch_h` URLs and the CLI's own `datasets rehydrate` path, which uses the same fetch.txt, worked cleanly). |
| `--ortholog` bare-flag syntax is broken with a misleading error | P1 | `--ortholog` now requires an explicit value (`--ortholog strings`); a bare `--ortholog --as-json-lines` gets `--as-json-lines` consumed as the taxon argument and fails with unrelated taxonomic suggestions. Changed every call site (SKILL.md's "Find orthologs" pattern, usage-guide.md's ortholog prompt) to `--ortholog all` or `--ortholog <taxon>` | ran + help | Confirmed via `datasets summary gene symbol --help` (`--ortholog strings`) and by running the corrected `--ortholog all` form -- 558 real ortholog rows, matching the audit's own smoke test. |
| Nonexistent accessions fail silently, undocumented | P2 | Added a Common errors row: `{"total_count": 0}`, exit 0 -> accession doesn't exist/withdrawn/superseded; check record count, not just exit code | help | Matches the audit's live-verified behavior (`datasets summary genome accession GCF_999999999.1` -> exit 0, `{"total_count": 0}`); not independently re-run (no new information to verify beyond the audit's own finding). |
| `dataformat version` prints the literal string "undefined" | P2 | Documented in Version Compatibility: use `dataformat --help`'s banner or confirm the build shipped alongside a known-good `datasets` binary, not `dataformat version` | ran | `dataformat.exe version` reproduced: exit 0, stdout exactly `undefined`. |
| (Found during verification, not in the audit's 7 inputs) Python wrapper's `g.get('assemblyStats', {}).get('contigN50')` uses camelCase keys that don't exist on 18.37.0's JSON output | not audited (cheap, in-scope "wrong field name" defect) | Changed to `g.get('assembly_stats', {}).get('contig_n50')` | ran | `datasets summary genome taxon "Escherichia coli" --reference --as-json-lines` inspected directly: real keys are snake_case (`assembly_stats.contig_n50`), no `assemblyStats`/`contigN50` anywhere in the record. |
| Internal contradiction: CLI version drift failure mode and multiple code-block labels still said "v16+"/"16.0+" after the field/flag fixes, contradicting the new Version Compatibility note (checked on 18.37.0) | not audited (internal contradiction, in scope) | Updated all version labels to 18.37.0 / checked 2026-09-19; reworded the "CLI version drift" failure mode to point at live `--help` re-verification instead of a hardcoded version pin, so it doesn't go stale on the next release | inspection | `grep`-confirmed no remaining "16.0+"/"v16+" pins in SKILL.md. |
| Mandatory redundancy pass | -- | Deleted usage-guide.md's Prerequisites (duplicated SKILL.md's Installation), "What the Agent Will Do" 8-step list (duplicated the scope table / subcommand taxonomy / dehydrated section / key parameters, all already in SKILL.md), and Tips (8 bullets, all restating SKILL.md content, one item was itself a now-wrong "pin to v16+" claim). usage-guide.md now holds only Overview, Quick Start, Example Prompts, Related Skills. Also fixed the same stale `--taxon --ortholog` bare-flag claim and stale genome `--fields` list that were duplicated inside its Example Prompts text (not just in SKILL.md) | inspection + ran | Every fact usage-guide.md lost is present, corrected, in SKILL.md's Installation, Version Compatibility, What's in scope, Subcommand taxonomy, Key parameters, When to use --dehydrated, and Failure modes / Common errors sections. |

## Unfixed

None. All 4 P1s and both P2s from the audit's `recommendations[]` were fixed, plus two additional
defects (Python wrapper field names, stale version pins) found and fixed during verification because
they were cheap and directly tied to the same version-drift root cause.

## Environment

Verification used the audit env's native Windows `datasets.exe`/`dataformat.exe` 18.37.0
(`F:\OpenScience\audit-envs\database-access\tools\ncbi-datasets-cli\`) and, for the `aria2c` leg of
`bulk_dehydrated.sh`, the WSL `science` distro's `bio` env (`aria2 1.37.0`, already present as a
transitive dependency from an earlier pass -- not installed or changed here). No packages were
installed or version-changed in any shared env. Temporary verification files written under the
shared `tools\ncbi-datasets-cli\` directory (a scratch TSV and a throwaway `fix-verify\` folder) were
deleted after use; nothing left behind there beyond the pre-existing `datasets.exe`/`dataformat.exe`.

---

## 2026-09-21 -- second fixer pass

Worktree `F:\OpenScience\wt\ncbi-datasets-cli`, branch `fix/ncbi-datasets-cli`, from staging `main`.
Source audit: latest report for `bio-ncbi-datasets-cli` (87.8, Production Ready, deployable; 1 P1, 1 P2).
Verified live with `datasets`/`dataformat` 18.37.0 (native Windows), `aria2 1.37.0` (WSL `science`/`bio`),
Python 3 for the size check. No shared env changed; scratch dir under the tools folder deleted after use.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| `datasets rehydrate` does not verify files already on disk; SKILL.md ("Rehydrate workflows also verify... retries up to 3 times") and `bulk_dehydrated.sh` Step 3 comment claimed it does | P1 | Rewrote SKILL.md "Checksum verification" (was "(automatic)"): `download` validates the zip checksum (per `--fast-zip-validation` help); `rehydrate` is presence-only; added a size-check snippet against `dataset_catalog.json` `uncompressedLengthBytes`. `bulk_dehydrated.sh` Step 3 now size-checks, deletes mismatches, rehydrates again, and exits 1 if still wrong. Dropped the unverified "retries up to 3 times" claim and the "MD5 mismatch retried" Common-errors row (replaced by two rows: zip validation failure, and the "already rehydrated" trap). Description: "automatic checksum verification" -> "download-time zip checksum validation". Same claim softened in `download_genome.sh` comments and usage-guide (3 places) | ran | Reproduced: overwrote a rehydrated .fna with 4 bytes -> rehydrate "All 1 files already rehydrated", file untouched; deleting it -> rehydrate restores 5510 bytes. Full `bulk_dehydrated.sh` run (Mycoplasma genitalium) with real WSL aria2c: NCBI bot-block wrote 3.9 KB HTML over 3 files, step 3 detected all 3, deleted, rehydrated, re-check passed (rc 0, sizes 587407/373156/219385). |
| Virus download has no code pattern | P2 | Added "Virus genomes" pattern (summary + `dataformat tsv virus-genome` + download with `--include`, filters, default package contents) | ran | `summary virus genome taxon "Zika virus" --refseq` -> 2 RefSeq genomes; download with `--include genome,cds,protein` produced genomic.fna/cds.fna/protein.faa/data_report.jsonl; `annotation` include yields annotation_report.jsonl; `virus-genome` field names checked against `--help`. |
| (found while testing) aria2c `--dir` was `.../ncbi_dataset/data/` in `bulk_dehydrated.sh` and SKILL.md, but fetch.txt column 3 already begins with `data/` | not audited | `--dir` -> `.../ncbi_dataset/`; files were landing in `data/data/`. The 2026-09-19 fix never completed an aria2c transfer, so this was unseen | ran | Real aria2c placed files at `ncbi_dataset/data/<acc>/...` after the change. |
| (found while testing) SKILL.md's bulk pattern passed raw `fetch.txt` to `aria2c --input-file`; it is 3 tab columns, not aria2c input format | not audited | Added the awk conversion (already in the script) to the SKILL.md pattern and to the dehydrated step 3 prose | ran | Same awk as the script, exercised by the run above. |

Redundancy: no new duplication; the size check appears once in SKILL.md (Checksum verification) and the
script is the runnable copy, per the shipped-examples exemption.

Unfixed: none. Notes: the size check relies on `python3`; `--gzip` rehydrate was not tested against it.

---

## 2026-09-21 (structure)

Worktree `F:\OpenScience\wt\ncbi-datasets-cli`, branch `fix/ncbi-datasets-cli`, on top of `a7bc8e2`.
Structure only; no behaviour or claim changed.

**Split** (commit `cc48c31`): `SKILL.md` 397 -> 276 lines (253 after the scripts commit). Verbatim moves,
no non-blank line lost (the only differing lines are the four scope-table / `--dehydrated` lines that gained
a pointer); every moved bash fence passes `bash -n`, python fences compile.

| Moved | To |
| --- | --- |
| "When to use --dehydrated", "Checksum verification", "Bulk download all reference bacterial genomes" | `references/dehydrated-bulk.md` |
| "Gene metadata across species", "Find orthologs for a gene" | `references/gene-orthologs.md` |
| "Virus genomes" | `references/virus-genomes.md` |

"Reference Files" index added before "Code patterns", with pointers from the Gene, Ortholog and Virus scope-table
rows and from the `--dehydrated` paragraph. Blank runs inside the file were collapsed to single blanks (the
old python block lost its PEP8 double blanks; the script restores them).

**Scripts** (second commit):

| Old location | Now | How run |
| --- | --- | --- |
| SKILL.md "Python wrapper" (33 lines) | `scripts/datasets_wrapper.py` (functions verbatim, argparse `main`) | `--taxon "Escherichia coli" --accession GCF_000819615.1`, datasets 18.37.0: 2 reference assemblies with contig N50, download zip asserted to hold a 5386 bp NC_001422 genome and `protein.faa` |
| references/dehydrated-bulk.md bulk-bacteria block (26 lines) | deleted; points at `examples/bulk_dehydrated.sh` (duplicate) | Ran the example as now invoked (`<taxon> <zip> <dest> <threads>`, Mycoplasma genitalium, WSL aria2c 1.37.0 via a path shim): rc 0, NCBI blocked the aria2c transfer again, step 3 caught 3 bad files and rehydrated, sizes 587407/373156/219385 match `dataset_catalog.json`, genome 587 kb |

Stayed inline: the 10-line size-check python heredoc (under the 15-line bar, and the example already
carries the runnable copy); the single-genome download block (11 lines, mirrors `examples/download_genome.sh`);
the filter-assemblies and ortholog pipelines (short one-liners, `gene_metadata.sh` covers the gene case).
Scratch dir under `tools\ncbi-datasets-cli\` deleted after use; nothing installed.
