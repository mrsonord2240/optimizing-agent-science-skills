> **Audit record for `bio-local-blast`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@e3ae050](https://github.com/mrsonord2240/bioSkills/tree/e3ae050e9b0c4bef22129953132c11e80ded18e8/database-access/local-blast) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-local-blast (RE-AUDIT, post-fix)
Generated: 2026-09-17

Source: `mrsonord2240/bioSkills@e3ae050:database-access/local-blast` (fix worktree `F:\OpenScience\wt\db-blast\`, branch `fix/db-blast`, based on staging `main` `581dcd89a7450785c2451a0543ee822049fbf934`)
Category: Data Analysis | Execution Mode: D (Hybrid — SKILL.md instructions + bundled scripts) | Complexity: Complex (N=9: 7 regression re-runs of the pre-fix inputs + 2 new)
All test data is synthetic (`F:\OpenScience\audits\bio-local-blast\data\`, copied from the pre-fix archive); scripts saved under `run\`.

Pre-fix baseline: `F:\OpenScience\audits\_pre-fix-20260917d\bio-local-blast\` — 87/100, Limited Release, deployable, **one open P0** (taxonomy filter silently no-ops without `taxdb.tar.gz`).

**Every claim below was independently executed by this re-auditor. The fix log (`fixes/bio-local-blast.md`) was read to know where to look, but nothing in it was accepted as evidence — a fresh `taxdb.tar.gz` was downloaded rather than reusing anything from the fixer's own run (nothing was cached on disk).**

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 38 | 56 | 94 | 3/3 PASS | ✅ |
| 3 | Variant B — **the P0** (regression) | 37 | 56 | 93 | 4/4 PASS | ✅ |
| 4 | Edge (regression) | 38 | 56 | 94 | 3/3 PASS | ✅ |
| 5 | Stress — RBH+extraction (regression) | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 6 | Scope Boundary (regression) | 39 | 55 | 94 | 4/4 PASS | ✅ |
| 7 | Adversarial — CRLF (regression) | 38 | 55 | 93 | 3/4 PASS | ✅ |
| 8 | Adversarial — **NEW, v4 taxid_map** | 28 | 46 | 74 | 1/4 PASS | ⚠️ |
| 9 | Variant B — **NEW, dedup verification** | 40 | 57 | 97 | 4/4 PASS | ✅ |

**Execution Average: 92.1 / 100**
**Assertion Pass Rate: 31/35 (88.6%)**

**Skill Veto (Step 1):** PASS on all of T1–T4.
**Research Veto (Step 6, Category 3 applicable):** PASS on all of M1–M4.

**Final Score = 95 (static) × 0.4 + 92.1 (execution avg) × 0.6 = 38.0 + 55.3 = 93.3 → 93**
Numeric score of 93 would map to Production Ready, but the assertion pass rate (88.6%) is below the
90% Production-Ready floor (`scoring_rubric.md` §5) — driven by Input 8's new finding and Input 7's
unreproduced (and not a Skill defect) `max_target_seqs` bias. Per the floor rule ("downgrade by
exactly one grade tier"), the final grade is **Limited Release (✅)**, not Production Ready. No
safety-assertion failed on 2+ outputs, so the Beta-Only-cap rule does not apply. `deployable: true`.

> **Note for reviewer:** Input 8 (⚠️) is the one new finding in this re-audit — a real, narrower
> inaccuracy the fix itself introduced. Everything the fix was actually tasked with (the P0, both
> P1s, both P2s) is confirmed fixed by independent execution below.

---

## P0 regression — Input 3 (the headline result)

**Prompt:** "Build a v5 protein DB with per-sequence taxids (-taxid_map) and run a taxonomy-filtered
blastp restricted to the human taxid (9606) using -taxids, so fly-tagged sequences are excluded
even if they'd otherwise be a hit."

Built exactly per SKILL.md: `makeblastdb -blastdb_version 5 -parse_seqids -hash_index -taxid_map
taxid_map.tsv`. `blastdbcmd -info` confirms `BLASTDB Version: 5`.

**Unfiltered search (baseline):**
```
Warning: [blastp] Taxonomy name lookup from taxid requires installation of taxdb database ...
TQ_HUMANLIKE  REF002  9606  N/A  3.82e-109  296
TQ_FLYLIKE    REF007  7227  N/A  2.28e-95   261
(2 rows)
```

**`-taxidlist human_only.txt` (9606) WITHOUT `taxdb.tar.gz` present — reproduces the P0 exactly:**
```
The -taxids command line option requires additional data files. ...
TQ_HUMANLIKE  REF002  9606  N/A  3.82e-109  296
TQ_FLYLIKE    REF007  7227  N/A  2.28e-95   261      <-- NOT excluded
exit code: 0
(2 rows -- byte-identical to unfiltered)
```

**Fetched `taxdb.tar.gz` via SKILL.md's own exact command** (`curl -O
https://ftp.ncbi.nlm.nih.gov/blast/db/taxdb.tar.gz`, 65,374,825 bytes, independently downloaded —
not reused from the fixer's run), extracted, retried:
```
TQ_HUMANLIKE  REF002  9606  Homo sapiens  1.44e-109  296
(1 row -- TQ_FLYLIKE correctly excluded, sscinames now resolves)
```
`taxonomy4blast.sqlite3` (98,504,704 bytes) confirmed auto-fetched during the retry.

**Verdict: the P0 is genuinely gone.** SKILL.md no longer claims v5 is self-sufficient; it now gives
the exact fetch command and a row-count-based detection method, and both were independently verified
to produce the documented before/after behavior. Full log: `run/out_input3.log`.

---

## New finding — Input 8 (v4 + `-taxid_map`)

**Prompt (self-generated):** Build a **v4**-format DB with `-taxid_map` and check the fix's own new
table claim: "Per-sequence taxid at build time (`-taxid_map`): v4 No | v5 Yes."

```
makeblastdb -blastdb_version 4 -parse_seqids -taxid_map taxid_map.tsv -out v4_taxid_db
  -> exit 0, no warning, DB built ("BLASTDB Version: 4")

blastdbcmd -db v4_taxid_db -entry REF002 -outfmt "%a %T"  -> REF002 9606
blastdbcmd -db v4_taxid_db -entry REF007 -outfmt "%a %T"  -> REF007 7227
```
Both match `taxid_map.tsv` exactly. **The table's "v4: No" for per-sequence taxid at build time is
false** — v4 stores and returns it fine via `blastdbcmd`/`staxids`.

Separately, with `taxdb.tar.gz` + `taxonomy4blast.sqlite3` copied in and `-taxidlist` attempted on
the same v4 DB:
```
BLAST Database error: Taxonomy filtering is not supported in v4 BLAST dbs
exit code: 2
```
This is a **hard, loud failure** — a third failure mode, distinct from both the v5-without-taxdb
silent no-op (exit 0) and what SKILL.md currently documents. Full log: `run/out_input8.log`.

---

## Verification — Input 5 (RBH → blastdbcmd chaining, the P2 fix)

Following SKILL.md's new 4-line addition verbatim (`cut -f1 rbh.tsv` → B accessions, `cut -f2` → A
accessions, extract from the matching DB) succeeded on the **first try** — 6/6 and 6/6 accessions
extracted, 0 errors. The pre-fix auditor's own run needed a self-correction here; that ambiguity is
now closed. Independently confirmed the column direction: `blastdbcmd -db A_db -entry B1` →
`Entry not found`, proving column 1 is genuinely a B accession. Full log: `run/out_input5.log`.

## Verification — Input 6 (Practice boundaries, the P1 fix)

Same real blastp result as pre-fix (`REF003, 96.104% identity, E=7.74e-116, bitscore 313`). The
refusal to diagnose/prescribe now explicitly follows SKILL.md's new "Practice boundaries" section
("local BLAST reports sequence similarity, not diagnosis... route diagnostic or treatment questions
to a clinical genetics service") rather than being incidental to baseline agent judgment — the one
assertion that FAILed pre-fix now PASSes. Full log: `run/out_input6.log`.

## Verification — Input 7 (CRLF, the other P2 fix)

Isolated the claim on a single content-identical row rather than a whole-file diff (the pre-fix
audit's whole-file diff conflated CRLF with intentional row dedup): `head -1` of the raw `blastp
-out` file, byte-inspected via Python `repr()`, ends `...295\r\n`; the same row piped through
SKILL.md's own documented `sort | awk '!seen[$1]++'` pattern ends `...295\n` — `awk` on this
toolchain strips the trailing CR. `diff` on the two flags them as different before normalizing;
`tr -d '\r'` on both sides makes them byte-identical (`diff` exit 0). The fix's new Common-errors row
is correct and necessary. Full log: `run/out_input7.log`.

## Verification — Input 9 (dedup pass, no content lost)

`import Bio.Blast.Applications` → `ModuleNotFoundError` on the installed biopython 1.88, consistent
with SKILL.md's moved claim ("deprecated and removed in BioPython 1.85"). All 5 section headings
`usage-guide.md`'s Tips-replacement pointer names (`Database format: v5 vs v4`, `Soft vs hard
masking`, `Output format reference`, `Thread scaling`, `Practice boundaries`) exist verbatim in
SKILL.md; all 4 `examples/` files exist; the "run `update_blastdb.pl` pulls overnight" fact moved by
the dedup pass is present in the Prebuilt-databases section. Full log: `run/out_input9.log`.

---

## Regression sanity — Inputs 1, 2, 4 (untouched by the fix)

Byte-for-byte identical results to the pre-fix run (same hits, same pident/evalue/bitscore). These
sections of SKILL.md were not touched by the fix; included for completeness per the re-audit brief.
Full logs: `run/out_input1.log`, `run/out_input2.log`, `run/out_input4.log`.

---

## Bundled scripts re-verified

- `examples/blast_wrapper.py` — byte-identical to the pre-fix version (fix log: "left alone"). Every
  function (`make_blast_db`, `run_blast`, `parse_tabular`, `top_by_bitscore_per_query`, `filter_hits`,
  `require`) re-run against real BLAST+ output, same results as pre-fix. `run/test_blast_wrapper.py`,
  log `run/out_wrapper_test.log`.
- `examples/create_database.sh` — the fixed file (its echo text no longer claims v5 needs no
  companion file). Ran end-to-end, both DBs built correctly. `run/work/create_db_test/`, log
  `run/out_create_database.log`.
- `examples/reciprocal_best.sh` — unchanged; its own awk pattern matches SKILL.md's documented column
  mapping, confirmed in Input 5.

## Code extraction method

All 12 fenced code blocks were extracted programmatically from the shipped `SKILL.md`
(`run/extract_skill_blocks.py`, output `run/skill_blocks.json` / `run/skill_blocks_dump.txt`) rather
than hand-copied, so the inputs above test the document itself.

## No external clone pollution

`find F:/OpenScience/external/mrsonord2240__bioSkills -name __pycache__` returned nothing, and
`git status --porcelain` on the clone's `database-access/local-blast` path is clean. Nothing was
written inside the fix worktree (`F:\OpenScience\wt\db-blast\`) either — it was read-only for this
re-audit.
