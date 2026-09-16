# Specialist viability threshold (2026-09-10; gate 6 rewritten for round 2 on 2026-09-15)

A candidate Specialist is built only when every gate below passes. `build_specialist.py` enforces
gates 2, 3, 6, 8 and 9 mechanically; gate 1 is the marketplace tooling; gates 4, 5 and 7 are
design review.

Derived from the Marketplace Protocol v1 and its validator
(`aipoch/openscience-specialist-marketplace`), the ten published releases, the Open Science App's
package import rules (`aipoch/open-science`, `resources/specialists/template/v1/README.txt`), and
the `skill-auditor` grading rubric shipped with the skills
(`skills/skill-auditor/references/scoring_rubric.md`).

1. **Protocol-valid.** `npm run validate` passes and `npm run build:release` produces identical
   ZIP bytes on two builds of unchanged input.
2. **Every bundled Skill is audited and deployable.** It has a `skill-auditor` report, no veto
   gate fired, `deployable: true`, no open P0 recommendation, and a final score ≥ 75 (Limited
   Release or better). **Which score:** all 131 eval reports in the `scientific` collection were
   overwritten by an upstream "polish" pass with a templated test section (inputs labelled
   "Test case N for <skill>", generic assertions, 104 reports sharing the identical input totals
   81/86/91/90/83/88/87) and claim 86–92, while the `POLISH_CHANGELOG.md` written by the same pass
   records 75–79. For those Skills the changelog number is used. The other 148 reports (all 141
   `medical` ones plus 7 unpolished `scientific` ones) carry per-skill inputs and findings and are
   used as reported. The 183 `*_audit_result_v2.json` files
   are not counted: all score ≥ 85, their "test inputs" are sentences lifted from the Skill's own
   description, and their notes say "the archived evaluation / legacy review accepted" — they are
   backfilled summaries, not audits.
3. **Core workflow Skills are Production Ready.** Each Skill marked `core` scores ≥ 85. A Specialist
   whose central step (the thing it exists to do) has only unaudited or sub-85 Skills fails.
4. **End-to-end coverage.** At least three core Skills, covering framing/design, the domain's
   central operation, and validation or reporting. A planning Skill may never stand in for an
   execution Skill in the system prompt.
5. **Distinct scope.** The Specialist routes a workflow that no published Specialist already
   routes. Sharing individual Skills with `auto-research-specialist` is allowed; duplicating its
   purpose is not.
6. **Provenance and references.** Skill files are byte-identical to the commit the release names
   as its source (audit reports excluded), or to the published Marketplace bytes under gate 9.
   Which commit that is depends on the round:

   - **Round 1 — AIPOCH, unmodified upstream.** Byte-identical to the public upstream commit
     `aipoch/medical-research-skills@f5ef65b9`. Nothing is edited.
   - **Round 2 — bioSkills, modified (2026-09-15).** Byte-identical to
     `optimizing-agent-science-skills@<commit>:skills/bioSkills/<folder>/<skill>/`, where
     `<commit>` is the exact commit recorded in the candidate's `spec.json` `upstream` block.
     These Skills *are* edited, so the audit trail replaces "nothing is edited": the modification
     route — upstream base commit → fork branch and commit → this repository's export — must be
     recorded in `skills/bioSkills/UPSTREAM.json` (today: base
     `GPTomics/bioSkills@d91ed3d5`, fixes exported from `mrsonord2240/bioSkills@d1b8fdce`, MIT),
     and a release may cite no other route. Every changed file needs a fix log in
     `fixes/<skill-id>.md` and a post-fix audit report that meets gates 2 and 3, written by an
     agent that did not make the fix. A Skill no audit found a defect in stays byte-identical to
     the upstream base commit.

   In both rounds a Skill's ID is its SKILL.md frontmatter `name`, and the only permitted
   packaging change is omitting a test fixture that breaks a marketplace ZIP limit (10 MiB per
   file), recorded with a reason (`exclude` in `spec.json`). Every Connector ID is one already
   used by a published release. Every bundled Python and R script parses under the Open Science
   runtime's own interpreters.
7. **Research scope.** The workflow is research, not patient care. Anything that would diagnose,
   prescribe or triage an individual fails the skill-auditor Practice Boundaries redline by design.
8. **Shipped means present.** Every `references/`, `scripts/`, `assets/` or `templates/` file a
   bundled `SKILL.md` points at exists. An audit score is not evidence of this: 17 of the 136
   Skills considered for bundling score 87–96 yet reference files that were never shipped, in
   several cases the script the SKILL.md names as its primary implementation. A missing peripheral
   helper (a dependency installer, a schematic generator, one supplementary reference when the
   SKILL.md body carries the method) may be accepted with a recorded reason (`known_missing` in
   `spec.json`); a missing primary script or an entirely missing reference set drops the Skill.
9. **No Skill conflicts.** The App refuses to install a Skill whose ID is already installed with
   different content ("Skill conflict"). A Skill ID that a published Specialist already ships is
   packaged with the published bytes (content digest verified); an ID published as a *different*
   Skill is dropped or renamed.
