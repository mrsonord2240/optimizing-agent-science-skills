# Handoff: bio-splicing-quantification / prepare-scientific-skill-tooling (delta), then reaudit-scientific-skill

- Updated: 2026-10-03
- Lane: 2
- Status: ready-for-phase
- Owner leaving: fix worker (lane 2, run-fix-1)
- Next role: prepare-scientific-skill-tooling (delta mode, per fix contract for tooling impact `changed`); then reaudit-scientific-skill. The brief asked for reaudit directly: nothing in the environment changed, so the orchestrator may skip the delta if it judges a coverage-map refresh unnecessary.

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:alternative-splicing/splicing-quantification
- Working tree: F:\OpenScience\wt\norm-bio-splicing-quantification\skills\bio-splicing-quantification (untracked/uncommitted by design)
- Branch/worktree: normalize/bio-splicing-quantification, started at 29f5446
- Candidate tree hash: 0c0354add99bca532a1c7168b94a08a1923249a1a7adfddd7f7e9997953355bf (files=5, bytes=42079); `skill_preflight` PASS offline and online (one expected no-Skill-root-LICENSE warning)
- Previous identity audited: 1e34dbd9664e (audit F:\optimizing-agent-science-skills\audits\skills\bio-splicing-quantification\candidate@1e34dbd9664e-run-initial-1, 64, Reject, veto M4)

## Completed this phase

- All eleven findings dispositioned; fix log with per-finding evidence: F:\OpenScience\audits\bio-splicing-quantification\run-fix-1\FIX-LOG.md
- Changed files: SKILL.md, usage-guide.md, scripts/quantify_splicing.py, references/failure-modes-and-errors.md, references/intron-retention-and-microexons.md
- Executed against real output: parser on all five rMATS event types (JC and JCEC), hand-computed planted means, SKILL.md snippet verbatim, SUPPA2 writer/filter on planted and chrX, regtools+leafcutter with and without XS, IRFinder reference rebuild + SE and PE runs

## Open findings and blockers

| ID | Severity | State | Evidence | Disposition |
|---|---|---|---|---|
| SQ-01..SQ-05 | P1 | fixed | run-fix-1\evidence\10..13 logs | veto M4 cause cleared |
| SQ-06..SQ-10 | P2 | fixed | run-fix-1\FIX-LOG.md | see log |
| SQ-11 | P2 | fixed (BAM list, leafcutter source); LICENSE not-a-defect | FIX-LOG.md | shelf siblings carry no Skill-root LICENSE; `license: MIT` frontmatter plus repo evidence |

No blockers. Not executed by design: MAJIQ V3/VOILA (restricted-access licence), VAST-TOOLS (6.7 GB VASTDB), Shiba, MicroExonator, S-IRFindeR, iREAD, IRFinder-S 2.0 (all labelled in the Skill).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-splicing-quantification\TOOLS.md (sha256 48cde79a...; environments unchanged, fingerprint 20c07bbb...)
- Run evidence: F:\OpenScience\audits\bio-splicing-quantification\run-fix-1\ (scripts\, evidence\, out\ local raw)
- Restricted-access items: MAJIQ V3 (unchanged)
- Tooling impact: changed (runnable surfaces: coverage rows 2 inline snippet, 3 parse_rmats_output, 5 filter_reliable_events, 8 IRFinder invocation, new write_suppa_tpm; no dependency, version, dataset or environment change). Also: staged wrapper tools\bin\IRFinder cannot run BuildRefFromSTARRef because tools\bin\STAR drops the /dev/fd handle ("could not open readFilesIn=/dev/fd/63"); worked around in run-fix-1\scripts\13_irfinder.sh with as-core bin first on PATH. Do not rerun smoke_irfinder.sh.

## Worktree safety

- Run-owned changes: the five Skill files above; run-fix-1\; this handoff
- Pre-existing/user-owned changes: records test/validate.bats (untracked), shelf .vscode/ (untracked); untouched
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
