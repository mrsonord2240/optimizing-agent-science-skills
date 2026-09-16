# `mass-spec-proteomics-analyst` — audit record (2026-09-15)

**Verdict: VIABLE.** Every bundled Skill is deployable, every core Skill clears 85 and every
supporting Skill clears 75. No veto gate fired anywhere and no P0 is open.

This replaces the 2026-09-15 afternoon record, which read NOT VIABLE. Five fix passes and three
re-audit rounds happened between the two; the earlier text is superseded, not amended.

Upstream for this release: `optimizing-agent-science-skills@567cab000f3728427c4c8a18e36d2f794a9def7d`
under `skills/bioSkills/` (MIT). That export is the fork
`mrsonord2240/bioSkills@a62c7097f37cde2f1d44763ac22c3f5c6d5350bb`, which carries audit-evidenced
fixes to `GPTomics/bioSkills@d91ed3d5`. Upstream was archived on 2026-08-15 and accepts no pull
requests, so the fork is the maintained line rather than a staging area.

---

## Audited Skills

| Skill ID | Role | Category | Mode | N | Executed | Static | Exec avg | Final | Grade | Veto | Top open P1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `bio-proteomics-data-import` | core — entry | Data Analysis | A | 8 | 8/8 | 84 | 86.0 | **85.2** | ✅ Limited Release | PASS | No TMT route; the no-LFQ error names columns a TMT table does not have |
| `bio-proteomics-dia-analysis` | core — DIA identification | Data Analysis | A | 7 | 7/7 | 85 | 87.0 | **86.2** | ✅ Limited Release | PASS | DIA-NN 2.6.1 rejects the headline predicted-library command as "incorrect settings" |
| `bio-proteomics-peptide-identification` | core — DDA identification | Data Analysis | A | 10 | 10/10 | 91 | 89.9 | **90** | ⭐ Production Ready | PASS | none |
| `bio-proteomics-protein-inference` | core — inference | Data Analysis | A | 7 | 7/7 | 89 | 88.6 | **88.8** | ⭐ Production Ready | PASS | The new Percolator picked-protein route emits a flat list, not groups |
| `bio-proteomics-quantification` | core — quantification | Data Analysis | A | 11 | 10/11 | 90 | 88.7 | **89** | ⭐ Production Ready | PASS | none |
| `bio-proteomics-differential-abundance` | core — terminal step | Data Analysis | A | 11 | 10/11 | 90 | 88.5 | **89** | ⭐ Production Ready | PASS | Input 9's inflated-FDR explanation is wrong (see below); the guard itself is sound |
| `bio-proteomics-proteomics-qc` | core — validation/reporting | Data Analysis | A | 8 | 8/8 | 87 | 88.8 | **88.1** | ⭐ Production Ready | PASS | Degenerate-design caveats are `print()`-only, so a caller cannot trap them |
| `bio-proteomics-ptm-analysis` | supporting — PTM branch | Data Analysis | A | 6 | 6/6 | 85 | 87.3 | **86.4** | ⭐ Production Ready | PASS | Documents `channel.1…N`, but MaxQuant is 0-indexed, so its own annotation is rejected |
| `bio-pathway-go-enrichment` | supporting — interpretation | Data Analysis | A | 5 | 5/5 | 89 | 90.0 | **90** | ⭐ Production Ready | PASS | none |
| `bio-experimental-design-batch-design` | supporting — framing/design | Protocol Design | A | 5 | 5/5 | 81 | 83.2 | **82** | ✅ Limited Release | PASS | SVA block fails on matrices with missing values |
| `bio-workflows-proteomics-pipeline` | supporting — orchestration | Data Analysis | A | 8 | 7/8 | 86 | 88.9 | **87.7** | ⭐ Production Ready | PASS | `treat()`'s fold-change floor silently zeroes a dose series' intermediate level |

Eleven Skills, 86 test inputs, 83 executed (97%). `dia-analysis` and `data-import` carry a
`grade_note`: both map to Production Ready on raw score but were held at Limited Release by the
rubric's ≥90% assertion floor.

## Where these scores came from

Every Skill was re-audited against the fixed tree by an agent that did not write the fix, per
`process/AUDIT_BRIEF.md`. Each re-audit re-ran the pre-fix inputs as regression tests and added at
least two new inputs of the auditor's own, so no score measures only the defects a fixer was told
about. That requirement earned its keep: `protein-inference`'s dead `percolator --protein` flag and
`proteomics-qc`'s unseeded PCA were both found by inputs nobody asked for.

Movement across the day:

| Skill | Start | End |
| --- | --- | --- |
| `peptide-identification` | 79, not deployable | 90 |
| `workflows-proteomics-pipeline` | 67, not deployable | 87.7 |
| `dia-analysis` | 77 | 86.2 |
| `data-import` | 78 | 85.2 |
| `differential-abundance` | 82 | 89 |
| `quantification` | 84 | 89 |
| `ptm-analysis` | 83 | 86.4 |
| `proteomics-qc` | 86 | 88.1 |
| `protein-inference` | 85 → 83 | 88.8 |

`protein-inference` is the instructive one. It *fell* below the core floor mid-way, not through
regression but because Percolator was installed after its first audit and made a previously
untestable claim testable — the Skill's Fido row named `percolator --protein`, a flag 3.09.0
rejects outright. The generalisable lesson, recorded in the process notes: install a candidate's
full tool inventory before the first audit, not during.

## Known-wrong explanation, retained deliberately

`bio-proteomics-differential-abundance` ships a guard against inflated FDR in blocked designs. The
guard is correct and was verified in four configurations — realized FDR 12.0% → 4.8% on the donor
data, and without it `eBayes` fails outright. **The explanation originally attached to it was
refuted.** A fixer attributed the inflation to a −0.18 log2 offset from per-run median
normalization; a later auditor reproduced the numbers but showed the mechanism is wrong — injecting
a uniform −0.20 offset alone produces 0 false positives, and real normalization also halves the null
SE (0.206 → 0.116). Neither half suffices. This is filed as an explanation-only P1. Do not repeat
the original account.

## Skills read but not chosen

- `bio-proteomics-spectral-libraries` — overlaps `dia-analysis`'s library handling without adding a
  distinct step; SpectraST coverage is partial with TPP absent.
- `bio-pathway-gsea` — a ranked-list method where this workflow terminates in a tested contrast;
  `go-enrichment` covers the interpretation step the Specialist actually routes to.
- `bio-experimental-design-sample-size` and `bio-experimental-design-multiple-testing` — useful but
  general; `batch-design` is the one whose failure mode (confounded batches) this workflow can
  actually check for.
- `bio-proteomics-crosslinking`, `bio-proteomics-top-down` — out of the bottom-up scope declared in
  `process/CANDIDATES.md`.

## Verdict against the gates

- **Gate 2 — every bundled Skill audited and deployable.** Pass. Eleven reports against this exact
  tree, `deployable: true` throughout, no veto, no open P0, lowest score 82 against a 75 floor.
- **Gate 3 — core Skills Production Ready.** Pass. All seven core Skills score ≥ 85: 90, 89, 89,
  88.8, 88.1, 86.2, 85.2. The two at the margin are the ones to watch on any future change.
- **Gate 4 — end-to-end coverage.** Pass. Framing (`batch-design`), the central operation as two
  real acquisition routes (`peptide-identification` for DDA, `dia-analysis` for DIA, both with
  executable searches rather than prose), and validation and reporting (`proteomics-qc`,
  `differential-abundance`). No planning Skill stands in for an execution Skill.
- **Gate 7 — research scope.** Pass. Bottom-up proteomics of experimental cohorts. Nothing
  diagnoses, prescribes or triages an individual, and the summary states research use explicitly.
- **Gate 8 — shipped means present.** Pass. Every `references/`, `scripts/` and `examples/` file the
  bundled SKILL.md files point at exists in the pinned tree, including the three examples added
  during the fix passes (`dda_search.sh`, `separate_search_fdr.py`, `msqrob2_peptide_level.R`).

## For the author of the system prompt

Route around these explicitly; each is an open P1 or a confirmed environmental trap:

- **Philosopher's silent successes.** `philosopher peptideprophet` and `philosopher filter` both
  **exit 0 and produce nothing** on this machine — header-only tables, `read in no data`, zero
  result elements. `proteinprophet` by contrast fails loudly. Check output, never exit code.
  Percolator is the rescoring path.
- **TPP is absent and will stay absent** — its installer aborts because the local VC++ runtime is
  newer than the one it bundles. Never make a TPP-only binary a required step.
- **Registration-gated and unavailable:** MSFragger, MaxQuant, Spectronaut, PEAKS, Skyline. Their
  *output tables* are supported; their binaries are not.
- `ptm-analysis`'s `channel.1…N` annotation versus MaxQuant's 0-indexed channels.
- `data-import`'s missing TMT route, and its misleading no-LFQ error for TMT inputs.
- `dia-analysis`'s headline predicted-library command, which DIA-NN 2.6.1 rejects.
- `pipeline`'s `treat()` floor on dose series with an intermediate level.

Reports live in `F:\OpenScience\audits\<skill-id>\`; per-Skill fix logs in
`optimizing-agent-science-skills/fixes/<skill-id>.md`.
