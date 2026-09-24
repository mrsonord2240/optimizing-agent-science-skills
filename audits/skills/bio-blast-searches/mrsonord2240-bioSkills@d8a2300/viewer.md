> **Audit record for `bio-blast-searches`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@d8a2300](https://github.com/mrsonord2240/bioSkills/tree/d8a2300a9a90869eccd13a5867d22d00709c6e6c/database-access/blast-searches) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-blast-searches

## Canonical final summary

**Final:** 93/100 — ⭐ Production Ready; deployable: true.

**Result: 93/100 — Production Ready — deployable**

- Source: `mrsonord2240/bioSkills@d8a2300a9a90869eccd13a5867d22d00709c6e6c:database-access/blast-searches`
- Environment: `F:\OpenScience\audit-envs\database-access` (Biopython 1.88)
- `auditor_independent: false`; final pass: fixed and audited under one brief, see CHECKPOINT.md.

## Fresh execution summary

| # | Input | Executed evidence | Score | Assertions | Status |
|---:|---|---|---:|---:|---|
| 1 | Live HBB RID lifecycle | One confirmed RID `B8T2VYTW014` / RTOE 2; retained `WAITING` records then `READY`; fetch and parse exited 0. | 96 | 4/4 | ✅ |
| 2 | Fresh XML `basic_blast.py` parsing | Current `top_n_by_bitscore` ran on fetched XML; `NM_000518` ranked first. | 94 | 3/3 | ✅ |
| 3 | Fresh XML `save_and_parse.py` parsing | Current `parse_hits` ran on fetched XML; 33 hits, first q=1–92 and s=51–142. | 91 | 3/3 | ✅ |
| 4 | PAM30 short-peptide contract | Retained contract regression passed; `word_size=2`, `gapcosts='9 1'`, and permissive settings were checked. | 93 | 3/3 | ✅ |
| 5 | Megablast and queue recovery | Retained contract regression passed; same confirmed RID progressed from queue `WAITING` to `READY`. | 91 | 3/3 | ✅ |
| 6 | Batch route and comparison metric | Exact pinned documentation inspection checked local/scalable routing and cross-database bit-score guidance; no remote call needed. | 93 | 3/3 | ✅ |
| 7 | Defline guard and RID resubmission discipline | Defline-less FASTA exited 1; watcher only used `status`/`fetch` for the confirmed RID. | 91 | 3/3 | ✅ |

Dynamic average: **92.7/100**. Assertion pass rate: **22/22**.

## RID lifecycle and parsed output

`blast_rid_source_copy.py` was byte-identical to the pinned `scripts/blast_rid.py` (SHA-256 `0234D9524BEF39E4509EB1C54D95B4C362B64818E8EA940F3A8D030CB070E9C1`). `rid_submit_summary.json` recorded one confirmed client submission: `RID=B8T2VYTW014`, RTOE 2. Retained status summaries show the same RID in `WAITING` state, and `rid_watcher_terminal.json` records `READY`, fetch exit 0, and parser exit 0.

Fresh `rid_fetch.xml` parsed as query length 92 against `refseq_select_rna`, with 33 alignments. Its top hit was `NM_000518.5` (HBB): 167.196 bits, E=5.8643e-41, identity 1.0, coverage 1.0. `replacement_regressions.py` then executed the current `examples/basic_blast.py` and `examples/save_and_parse.py` parsing functions against that XML and reproduced these facts.

## Duplicate-submission scope

The RID client submitted once and the watcher never resubmitted: it invokes only `status` and `fetch` for `B8T2VYTW014`. A separate bounded synchronous Biopython `qblast` process was stopped after 300 seconds without output; its server-side submission state is unknown. The evidence therefore supports RID-client resubmission discipline, not a global claim that no server-side duplicate job could have existed.

## Vetoes and score

Structural veto: PASS (stability, contract, determinism, security). Research veto: PASS (scientific integrity, practice boundaries, methodological ground, code usability).

Static: `94 × 0.4 = 37.6`. Dynamic: `92.7 × 0.6 = 55.6`. Weighted final: `93.2`, rounded to **93/100 — Production Ready, deployable**. No P0/P1 is open; P2 remains to add a bounded live audit harness.

Evidence: `run/phase2_closure_20260923_1430/{integrity.json,rid_submit_summary.json,rid_status_summary_4.json,rid_status_summary_24.json,rid_watcher_progress.jsonl,rid_watcher_terminal.json,rid_fetch.xml,rid_fetch_parse.json,replacement_regressions.json,contract_regressions.json,no_defline.log,qblast_bounded_summary.json}`.
auditor_independent: false
