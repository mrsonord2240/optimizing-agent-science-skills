# Brief: author one round-2 OpenScience Specialist

You are completing ONE candidate Specialist package for the OpenScience Specialist Marketplace
(Protocol v1). An auditor has already chosen and graded the Skills. Your job is the part that needs
judgment: reading the bundled Skills, writing the system prompt and metadata, building, and saying
honestly how the result could be better.

## Where things are

- Threshold every Specialist must meet: `F:\optimizing-agent-science-skills\process\THRESHOLD.md`
  (read first). Round 2 differs in two ways, both already handled by the builder: Skills come from
  the repository, commit and `prefix` pinned in `spec.json`'s `upstream` block — for fixed Skills
  that is `optimizing-agent-science-skills` at the export commit, under `skills/bioSkills/` — and
  gate 6 checks bytes against that commit; and audit reports live in
  `F:\OpenScience\audits\<skill-id>\`.
- Why every candidate uses bioSkills only:
  `F:\optimizing-agent-science-skills\process\CANDIDATES.md`. Your candidate's scope and
  boundaries are its row there.
- Your spec: `F:\OpenScience\specialist-src\<id>\spec.json` and the auditor's
  `F:\OpenScience\specialist-src\<id>\AUDIT.md`. Do not change the `upstream` block, Skill `id`s
  or `source`s.
- Audit evidence per Skill: `F:\OpenScience\audits\<skill-id>\eval_report_*_result.json` and
  `eval_viewer_<skill-id>.md` (what the auditor ran, what executed, the P1/P2 findings).
- Bundled Skills: under the `upstream` `path` (plus `prefix`) your `spec.json` pins — fixed Skills
  at `F:\optimizing-agent-science-skills\skills\bioSkills\<source>\`, unmodified ones at
  `F:\OpenScience\external\GPTomics__bioSkills\<source>\` (`SKILL.md`, `usage-guide.md`,
  `examples/`). Read-only.
- Builder: `python F:\OpenScience\specialist-src\build_specialist.py <id>` → writes
  `F:\OpenScience\specialists\<id>\...`. It enforces the threshold and fails loudly.
- Clean marketplace worktree with dependencies installed: `F:\osa` (read-only for you).
  - Protocol: `protocol/README.md`; authoring guide `specialists/README.md`.
  - Exemplar system prompts (read at least one fully before writing):
    `specialists/pharmacometrics-pkpd-designer/versions/1.0.0/package/specialist.json` (the
    structure you must follow) and `specialists/auto-research-specialist/versions/1.0.1/package/specialist.json`
    (routing discipline). The round-1 prompts in `F:\OpenScience\specialist-src\*\system_prompt.md`
    show the same structure applied to biomedical workflows.

## Steps

1. **Read every bundled Skill's `SKILL.md` and `usage-guide.md`, and its audit viewer.** Note its
   trigger, inputs, boundary, which tools and versions it assumes, and whether its code actually
   ran in the audit. If a Skill turns out not to fit, remove it from `spec.json` and say why. You
   may not add a Skill that has no audit report meeting THRESHOLD.md (core ≥ 85, supporting ≥ 75,
   no veto, no P0). You may flip a `core` flag only with a stated reason.
2. **Fill `spec.json`**: `display_name`; `summary` (one sentence, ≤ 300 chars, in the style of the
   published summaries, e.g. "Designs unit-safe, uncertainty-aware ... without issuing
   patient-specific prescriptions."); per Skill a Title Case `display_name` and a one-sentence
   `description` (≤ 170 chars) accurate to its SKILL.md. Connectors only from the published
   vocabulary: pubmed literature clinical-trials biorxiv genes genomes expression
   protein-annotation structures rna regulation biomart clinical-genomics human-genetics
   drug-regulatory cancer-models research-resources chembl chemistry molecule zinc omics-archives
   variants cellguide. Leave `required: false`.
3. **Write `F:\OpenScience\specialist-src\<id>\system_prompt.md`** using EXACTLY the section
   structure of the pharmacometrics exemplar:
   `# <Display Name>` / `## Identity` / `## Open Science runtime contract` / `## Packaged Skill routing`
   / `## Connector policy` / `## Domain operating principles` / `## Mindset And First Principles` /
   `## How You Frame A Problem` / `## How You Work` / `## Rigor And Critical Thinking` /
   `## Troubleshooting Playbook` / `## Definition Of Done` / `## Open Science domain gates` /
   `## Required delivery` / `## Final release check`.
   - Copy the **Open Science runtime contract** section verbatim from the exemplar.
   - **Skill routing**: every bundled Skill ID with a precise trigger, grouped by workflow stage.
     bioSkills Skills are mostly code-pattern guides: the agent writes and runs code by following
     them. Say so, and say that nothing counts as executed until the code has run in the user's
     environment and produced output. Name the handoff order between Skills. Where two Skills
     overlap, say which wins for which input. Where the audit found a defect or a tool that could
     not run, route around it explicitly. Keep the exemplar's closing paragraph about resolving
     supporting files relative to each Skill folder.
   - **Domain operating principles** through **Definition Of Done**: write as a senior practitioner
     of this field — specific methods, named failure modes, reflexive questions. No generic filler.
   - **Open Science domain gates**: the concrete, checkable ways work in THIS field goes wrong
     (e.g. pseudoreplication, FDR at the wrong level, compositional artefacts, long-branch
     attraction). Each gate is a rule the agent can verify, not an aspiration. Research scope only:
     no diagnosis, prescription, or individual patient triage.
   - Tool and database versions, reference releases, and guideline versions: do not assert from
     memory unless certain; instruct recording the version actually used.
   - Target 14,000–22,000 characters.
4. **Build**: run the builder until it passes. Then build the release twice and confirm identical
   artifact SHA-256:
   ```
   cd F:/osa && npm run build:release --silent -- --specialist-id <id> --version 1.0.0 --version-directory F:/OpenScience/specialists/<id>/versions/1.0.0 --output F:/OpenScience/builds/<id>-a
   (repeat with F:/OpenScience/builds/<id>-b)
   ```
   Do NOT copy anything into `F:\osa` and do not run `npm run validate`; central validation runs
   after all agents finish.
5. **Write `F:\OpenScience\specialist-src\<id>\improvements.md`**: prioritized, actionable bullets —
   missing workflow steps and what Skill would fill each; bundled Skills whose audit P1s matter
   here; bioSkills or other listed-repo Skills that would add value once audited (name them);
   system-prompt limits; connector gaps; the evaluation this Specialist itself still needs. Short
   bullets, no preamble. Start with a dated heading `# Improvements — <display name> (2026-09-11)`.
6. If, after reading the Skills, you conclude the candidate genuinely fails THRESHOLD.md, do not
   build. Write `not-viable.md` in the same folder stating which gate fails and exactly what is
   needed to make it viable.

## Where a finished Specialist goes (2026-09-15)

**Our own marketplace: `mrsonord2240/openscience-specialists`.** Not yours to do — Sam or the
session lead lands it — but know the destination so you do not aim at the wrong one.

The package is committed to `main` there (`specialists/<id>/`, same layout as the existing ones),
then released by dispatching the **Publish Specialist** workflow with `specialist_id=<id>`. Signing
happens in CI; there is no local key and you should never look for one.

**Do not open a pull request against `aipoch/openscience-specialist-marketplace`.** The first ten
Specialists were contributed there deliberately, and the same ten seeded our own marketplace. From
round two on we publish only to ours. `F:\osa` is a clone of the fork of that upstream repo; it is
the protocol reference and the release builder, **not** a publishing target.

## Rules

- Never edit anything under `F:\OpenScience\external`, `F:\OpenScience\skills`,
  `F:\OpenScience\audits`, or `build_specialist.py` (report builder bugs in your final message).
  Touch only your own `<id>` folders.
- On Windows: edit files with the Write/Edit tools or Python with `encoding='utf-8'`; never
  round-trip text through PowerShell `Get-Content`/`Out-File`. Prefix Python with
  `PYTHONIOENCODING=utf-8` in Bash.
- Do not invent facts about a Skill — cite what its SKILL.md says.

## Final message (≤ 200 words)

Built or not-viable; skill count (and any removed, with reason); both artifact SHA-256 values and
whether they match; prompt length; the top three improvements; any builder issue.
