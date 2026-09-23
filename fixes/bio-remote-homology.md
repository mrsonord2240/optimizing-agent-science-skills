# Fix log: bio-remote-homology (database-access/remote-homology)

2026-09-19. Fixer for the audit's 83/100, Limited Release verdict. Branch
`fix/db-remote-homology` on staging `main` (`mrsonord2240/bioSkills`), commit `1d0172a`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `examples/pfam_annotation.sh` awk line labels hmmscan's query-accession/qlen ($5,$6) as full_evalue/full_score | P1 | Changed indices to $7,$8 (real full_evalue/full_score); fixed the misleading column comment above it | ran — hmmscan --cut_ga on cached PF00069.hmm vs P17612.fasta (audit-envs fixture); broken awk gave `-`/`351`, fixed awk gave `1.4e-79`/`253.2`, matching the audit's ground truth | SKILL.md's own awk line was already correct; the shipped script just didn't match it |
| Documented `foldseek --version` setup-verification command fails on every Foldseek subcommand (`Invalid Command`, exit 1) | P1 | Replaced in SKILL.md's "Required Setup" with `foldseek 2>&1 | grep -i "^foldseek Version"`, which reads the version from the no-arg banner | ran — installed Foldseek 10.941cd33 in the audit env's WSL/bioconda seat; new command exits 0 and prints `foldseek Version: 10.941cd33`; old command re-confirmed failing for comparison | usage-guide.md's duplicate copy of this line was removed under the redundancy pass rather than fixed in place (see below) |
| No escape hatch for a user demanding unqualified certainty, dropping statistics | P2 | Added one sentence to SKILL.md's intro: answer with the real E-value/score/probability inline instead of refusing or dropping it | docs — no code to run; matches the Skill's own worked examples, which always report a statistic | |
| No shipped toy fixture; every exercise needs the full ~1.7 GB Pfam-A.hmm | P2 | Bundled `examples/data/PF00069.hmm` (one Pfam family, 123 KB, CC0) + `examples/data/P17612.fasta` (478 B, CC BY 4.0) — same public files the audit env already cached from InterPro/UniProt — and added `examples/pfam_annotation_toy.sh` | ran end-to-end in the audit env's WSL/bioconda seat: hmmpress + hmmscan --cut_ga recovers the true hit, E=1.4e-79/score=253.2; `bash -n` clean | Deliberately did not bundle Foldseek/MMseqs2/DIAMOND/HH-suite toy fixtures — those need multi-GB prebuilt DBs per TOOLS.md, not cheap |

## Redundancy pass (mandatory every fix, not itself an audit finding)

`usage-guide.md` carried full "Prerequisites", "Tips", and "What the Agent Will Do" sections that
mostly restated `SKILL.md`. Deleted all three; migrated the handful of facts that existed only
there into the matching `SKILL.md` section rather than dropping them:

- twilight-zone range (20-35% identity) -> folded into `SKILL.md`'s opening paragraph (previously
  only gave the ~35% floor).
- ">50 sequences -> default to MMseqs2/DIAMOND over BLAST" -> folded into the same paragraph.
- "HHsearch is gold standard for PDB70; prefer Foldseek for AlphaFoldDB coverage" -> folded into
  the HHblits/HHsearch section.
- Foldseek multimer mode (`easy-multimersearch`/`easy-multimercluster`) -> added to the Foldseek
  section (was in neither file before).
- Everything else in those three sections (ProstT5 bridge, MMseqs2 `easy-cluster` at scale,
  PSI-BLAST non-determinism/PSSM reuse, DIAMOND `--frameshift`, "fold similarity != homology") was
  a verbatim or near-verbatim restatement of existing `SKILL.md` content and was deleted outright.

`usage-guide.md` now holds only Overview, Quick Start, Example Prompts, and Related Skills.

## Left unfixed

Nothing from the audit's P1/P2 list. Not attempted: toy fixtures for Foldseek/MMseqs2/DIAMOND/
HH-suite (multi-GB prebuilt DBs, not cheap — TOOLS.md already documents smaller self-search
smoke tests for those instead).

---

## 2026-09-21 (P2 batch)

Fixer for the two open P2s of the 92/100 re-audit, plus the length/redundancy pass. Branch
`fix/database-access-remote-homology` on staging `main` (431aa55), commit `482fd24`. Env:
`database-access` (WSL `science`/`bio`: HMMER 3.4, MMseqs2 18.8cc5c, DIAMOND 2.2.6, Foldseek
10.941cd33, BLAST+ 2.17.0+). SKILL.md 370 -> 296 lines, so no split was needed.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `pfam_annotation.sh` prints nothing on a zero-hit query | P2 | Both `pfam_annotation.sh` and `pfam_annotation_toy.sh` print "No Pfam-A domains found above the gathering threshold." and exit 0. The audit's suggested `[ ! -s query.domtbl ]` would never fire (domtbl always has `#` header lines), so the check is `! grep -qv '^#' query.domtbl` | ran: P17612 vs PF00069 still `1.4e-79 / 253.2`; poly-Q/poly-G query prints the message, exit 0, in both scripts | |
| PSI-BLAST-only / HHsearch-only example scripts missing | P2 | not changed | | see Left unfixed |
| (found while running) MMseqs2 default `-s` stated as 4.0 | none (correction) | Default is 5.7 for `easy-search`/`search`; SKILL.md text and the failure mode corrected, `-s 5.7 is a middle ground` dropped, real 0-hit/`-s 7.5` numbers added | ran + help: `mmseqs easy-search -h` says `[5.700]`; default and explicit `-s 5.7` gave 0 hits on P17612 vs the 300-seq Swiss-Prot sample, `-s 7.5` gave Q197B6 (E=1.37e-13) | Contradicted the audit's own run (Input 2: "implicit 5.7") |
| (found while running) `hmmscan (-gathering)` | none (correction) | `-gathering` -> `--cut_ga` | help: `hmmscan -h` | |
| (found while running) `hmmsearch iter-3.hmm` after jackhmmer | none (correction) | Uses the highest-numbered `iter-*.hmm` (jackhmmer converged at round 2 on the audit pair, so `iter-3.hmm` did not exist) | ran: `hmmsearch iter-2.hmm` hits Q197B6 (E=8.6e-62) | |
| (found while running) DIAMOND `--more-sensitive` implied enough for remote homology | none (correction) | Failure-mode line now says default and `--more-sensitive` both returned 0 hits on the 25%-identity pair, only `--ultra-sensitive` recovered it | ran: DIAMOND 2.2.6 on the same pair (0 / 0 / 2 hits, Q197B6 E=5.39e-12) | Same finding as TOOLS.md note 2 |
| (found while running) `iterative_profile.sh` fails as SKILL.md invokes it | none (correction) | `psiblast -db` got a FASTA path and died: script now runs `makeblastdb` first; `grep -c` on zero jackhmmer hits aborted under `set -e`: `|| true` | ran: on the Swiss-Prot sample psiblast, jackhmmer and MMseqs2 all find Q197B6, exit 0 | |
| (found while running) `foldseek_search.sh` re-downloads AFDB every run | none (correction) | Guard `[ ! -d afdb_sp ]` (never true, `foldseek databases` writes files) -> `[ ! -f afdb_sp.dbtype ]` | ran: 1ATP self-DB as `afdb_sp`, structure path completes with no download, self-hit prob 1.000, TM 1.000 | Observed by the script starting a real AFDB download; that process was killed by PID |
| PSI-BLAST failure-mode trigger said "5+ iterations", body said 4+ drift | none (correction) | Trigger reworded to "past 3 rounds, or to convergence" | docs (internal consistency) | |

### Left unfixed

- **PSI-BLAST-only and HHsearch-only `examples/` scripts** (P2 #1): new content, not a correction.
  The audit's own carry-over note calls it optional. The PSI-BLAST leg (with PSSM output) already ships
  in `iterative_profile.sh`, and both tools have runnable inline blocks in SKILL.md (PSI-BLAST incl.
  `-in_pssm` reuse; HHblits + HHsearch). A verified HHsearch script needs UniRef30 and PDB70 (tens of
  GB, not on disk and not built by the tooling pass); only the flags were checked (`hhblits -h`,
  `hhsearch -h`).
- **ProstT5 branch of `foldseek_search.sh`** (`foldseek databases ProstT5` then `--prostt5-model`) was
  not run: it downloads multi-GB weights. Its `[ ! -d prostt5 ]` guard is unverified for the same
  reason.
- **Step 4b (scripts/)**: no complete runnable block of ~15+ lines is left inline. The Foldseek,
  iterative-profile and Pfam recipes were already `examples/` scripts and their inline copies were
  deleted (below); the remaining inline blocks (PSI-BLAST 12 lines, HHsearch 7, jackhmmer, MMseqs2,
  DIAMOND) are short. No `scripts/` directory created.

### Redundancy pass: deleted passage -> new home

`usage-guide.md` was already deduplicated on 2026-09-19 (skipped). This pass collapsed repetition
inside SKILL.md. Verified by grep that each command survives in its new home.

| deleted (SKILL.md, before) | now lives in |
|---|---|
| "Foldseek search against AlphaFoldDB" code block (`foldseek databases Alphafold/Swiss-Prot`, `easy-search --format-output ...`) | `examples/foldseek_search.sh`; SKILL.md "Foldseek search" pointer keeps the field list, TM-score note, `prob > 0.9`; the `easy-search` commands stay in "Foldseek: the 2024 revolution" |
| "Sequence-only Foldseek via ProstT5" block | "Foldseek: the 2024 revolution" access mode 2 (same two commands), `foldseek_search.sh` sequence branch, "Foldseek without ProstT5" failure mode |
| "MMseqs2 sensitive iterative search" block (createdb/createindex/search --num-iterations 3 -s 7.5/convertalis) | "MMseqs2" section (`easy-search ... -s 7.5 --num-iterations 3`, iterative bullet) and `examples/iterative_profile.sh` |
| "Pfam domain annotation (canonical)" block (hmmpress, hmmscan --cut_ga, awk filter) | "HMMER 3" section block (hmmpress + `hmmscan --cut_ga --domtblout`), `examples/pfam_annotation.sh` (awk columns) and the toy script |
| "DIAMOND ultra-sensitive on a metagenome" block | "DIAMOND" section (makedb + blastp block; `--ultra-sensitive` in table and default-choice line) |
| Common-errors rows: PSI-BLAST implausible hits, MMseqs2 all unrelated, DIAMOND misses BLAST hits, Foldseek structurally unrelated | the four matching Failure-modes sections (unchanged); the table keeps its two unique rows (HHblits prefilter, jackhmmer ConvergenceError) |

---

## 2026-09-22 (final-pass Phase 1)

Continued from `482fd24` on `fix/database-access-remote-homology`. Full runnable-block walk used the
cached P17612 / 300-sequence Swiss-Prot public fixture and the 1ATP Foldseek fixture. Phase-1
checkpoint: `F:\OpenScience\audits\_final_pass\bio-remote-homology\CHECKPOINT.md`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Iterative HMMER block passes `--chkhmm iter.hmm` but then glob-selects `iter-*.hmm`; HMMER actually writes `iter.hmm-<round>.hmm`, so the documented `hmmsearch` cannot receive a checkpoint | P1 | Changed the checkpoint prefix to `iter`, matching the existing `iter-*.hmm` selector | ran — HMMER 3.4 wrote `iter-2.hmm` for P17612 vs cached Swiss-Prot; the exact downstream `hmmsearch` recovered Q197B6, E=8.6e-62 | The old spelling was a real shell/glob mismatch, not an early-convergence edge case |
| Sequence-only `foldseek_search.sh` treats the ProstT5 cache as a directory, but `foldseek databases` writes a file-prefix database | P2 | Changed cache guard from `prostt5/` to `prostt5.dbtype` | ran + syntax — all shipped shells pass `bash -n`; structurally equivalent cached `afdb_sp.dbtype` guard skipped download and 1ATP self-search returned probability/TM-scores/lDDT 1.000 | ProstT5 weights were not downloaded; see Left unfixed |

### Left unfixed / checkpointed

- Full `pfam_annotation.sh` against current Pfam-A: needs approval for the ~1.7 GB compressed Pfam-A download. The same `hmmscan --cut_ga` command and bundled toy script ran and returned Pkinase E=1.4e-79 / score 253.2.
- Default Foldseek AlphaFoldDB Swiss-Prot and sequence-only ProstT5: each requires multi-GB artifacts. The structural script ran end-to-end against a cached 1ATP Foldseek DB, but Sam is away and no >1 GB download was started.
- Exact HHblits/HHsearch against UniRef30/PDB70: needs tens-of-GB profile databases. `hhsearch` itself ran against a one-entry local profile DB and returned the expected self-hit (Prob=100.00, E=3.3e-215); production DB execution remains gated by those artifacts.
