# Handoff: bio-workflows-crispr-screen-pipeline / prepare-scientific-skill-tooling (delta)

- Updated: 2026-10-04
- Lane: 1
- Status: ready-for-phase
- Owner leaving: tooling worker (delta after fix-001)
- Next role: reaudit-scientific-skill

## Source identity

- Working tree: F:\OpenScience\wt\recut-crispr-pipeline\skills\bio-workflows-crispr-screen-pipeline (branch recut/crispr-screen-pipeline, base f162b3a; candidate bytes uncommitted, untouched by this phase)
- Candidate identity: 6654a4f7d596c13a76b5b68b0346c9f521335f10e4d4a38ae7b58e2f3067d6dc. The orchestrator made one edit after the tooling delta, to the defect that delta reported: `routes/chronos.md` read the NEGv1 gene column as `.Gene` (the staged file's header is `GENE`); it now reads the first column, `.iloc[:, 0]`. Unexecuted: the re-auditor runs the chronos snippet as shipped against the standard NEGv1 file. Before that edit: 4db139576e8d5f48cb118db1f2cacd2eef87ca596d63fd25ae5dc711aa94c9a7 (skill_preflight --offline --shape PASS, 19 files; warn: no Skill-root LICENSE, F-11 deferred)
- Fix ledger and evidence: F:\OpenScience\fix-evidence\recut-crispr-pipeline\fix-001\ (F-10 and F-11 deferred-with-rationale)

## Tooling

- TOOLS.md: F:\optimizing-agent-science-skills\audits\skills\bio-workflows-crispr-screen-pipeline\tooling\TOOLS.md (Delta section at the end)
- Cases: ...\tooling\routing-cases.json (11 cases, rework below)
- Environment fingerprint: unchanged from the full pass (TOOLS.md table); no environment rebuilt
- Delta evidence: F:\OpenScience\fix-evidence\recut-crispr-pipeline\tooling-delta-001\
- Ecosystem: F:\OpenScience\audit-envs\crispr-screen-analyst\ ; new inputs registered in public-data\README.md

## Delta results

- chronos route snippet, verbatim, clean dir: exit 0, 2m03s, 5 x 4,502, 0 NaN, ribosomal mean -2.66 to -2.94
- jacks route command, clean dir: exit 0, 21 s, 4,502 x 5, RPL/RPS mean -1.04 to -1.83
- qc.py: HAP1 still FAIL by construction; the no-plasmid WARNING prints
- New route defect for the next fix: routes/chronos.md reads NEGv1.txt with `.Gene`; the BAGEL NEGv1.txt header is `GENE` (AttributeError on the standard file). Not blocking a re-audit of the fix.

## Routing cases changed

- rra: data rra-qcpass (simulated QC-passing, real HAP1 guide ids/fold changes), allow_before qc, bagel2
- cn-correction: data cn-correction-qcpass (simulated, KY library ids), allow_before qc
- mle and jacks: allow_before qc, cn-correction
- Check: rra PASS 3/3, cn-correction PASS 2/3 (tooling-delta-001\routing). mle/jacks allow_before not rerun: the confirming run hit HTTP 402 (OpenRouter out of credit; routing-b is void). fix-001 had mle 2/3 and jacks 3/3 with the same values

## Blockers and deferred

- F-10 real drug-screen data for drugz: deferred (no small public counts table staged; drugz case uses relabelled HAP1 columns)
- Simulated inputs: rra-qcpass, cn-correction-qcpass (said in TOOLS.md)
- No heavy-optional surface

## Worktree safety

- Run-owned: tooling-delta-001, derived\crispr-pipeline\{rra-qcpass,cn-correction-qcpass,make_inputs_qcpass.py,chronos\NEGv1.txt}, TOOLS.md, routing-cases.json, this handoff
- Untouched: candidate bytes, test/validate.bats (user-owned), old rra and cn-correction case dirs
- No commits or pushes

## Transition assertion

- Next-phase prerequisites met: yes (route to reaudit-scientific-skill)
