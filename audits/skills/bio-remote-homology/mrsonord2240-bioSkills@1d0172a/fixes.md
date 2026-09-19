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
