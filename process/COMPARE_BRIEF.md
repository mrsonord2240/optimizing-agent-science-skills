# Brief: compare two Skills that look alike, by running both (2026-09-21)

You are the **comparer** for ONE pair (or trio) of Skills whose titles suggest they overlap. Earlier
comparisons were made by reading files. This one is by execution: what does each Skill actually let a
researcher do? You score nothing and you have no stake in either side. Your dispatch names the Skills,
where each lives, the env and its `TOOLS.md`.

## Two facts

- **Skill ID is the SKILL.md frontmatter `name`, not the folder name.**
- **Upstream provenance.** Our Skills come from `GPTomics/bioSkills` at `d91ed3d` (MIT), read-only clone
  `F:\OpenScience\external\GPTomics__bioSkills`. The other side is Open Science's marketplace
  (`aipoch/medical-research-skills`, pinned commit `d924410`); the exact bytes are already copied to
  `F:\OpenScience\comparisons\_theirs\<id>\`. Ours are on the shelf,
  `F:\optimized-scientific-skills\skills\<id>\` (audited, fixed and re-audited). Read all of them
  in full; never write inside any of these folders.

## What to do

1. Claim the pair: `mkdir F:\OpenScience\comparisons\<pair-id>`. Stop if it fails.
2. Read both sides completely (`SKILL.md`, `references/`, `scripts/`, `examples/`). Write down, before
   running anything, what each side says it does and for whom.
3. Write 2-3 realistic requests a researcher would send with either Skill loaded, on one shared dataset
   (small synthetic, or public; say which and why it is fair to both). Run **each request through each
   Skill's own instructions and scripts**, as an agent that loaded that Skill would. If a Skill ships a
   script, run the script; if it ships prose, do what the prose says. Give both sides the same effort.
4. Run the code. **Judge by output, never by exit code**: assert on a count, a value against known
   truth (plant an effect and see whether it is recovered), or a file that exists and parses. Record
   `executed: true|false` and why, per request per side.
5. Note what each side does that the other cannot: runnable code vs guidance, statistical guardrails
   (background sets, multiple testing, assumption checks, leakage), failure modes it warns about,
   and any output that is silently wrong. Where one side is better, say so plainly, including when it
   is the other party's Skill.
6. Verdict per pair: **duplicate** (either would serve any request the other would), **partial**
   (overlap, each does something the other does not), or **distinct** (different jobs). Then which to
   use for what. Support it with at least one concrete demonstrated difference in output.

## Rules

- This is a comparison, not an audit: no score, no grade, no P0/P1 list. Report defects you hit, one
  line each, because they explain the verdict.
- Env: read the env's `TOOLS.md` first. R only through the env's `r.sh` (bare `Rscript` exits 0 and
  prints nothing). Linux-only tools run in WSL `science` (`process/TOOLING_BRIEF.md`). Install missing
  libraries **outside** `F:\OpenScience\comparisons\`, without changing any existing package's version,
  under the env's `install.lock`.
- Save every script you ran as a file under `F:\OpenScience\comparisons\<pair-id>\run\`. Nothing that
  only existed in a tool call is evidence.
- Never write in `F:\OpenScience\external\`, `F:\OpenScience\audits\`, or the shelf. Never kill a
  process by image name; kill the PID you started. Python on Windows needs `F:\...` paths, not `/f/...`.
  Edit with Write/Edit or Python `encoding='utf-8'`. No paid or authenticated services.
- Do not spawn sub-agents.

## Deliverable

`F:\OpenScience\comparisons\<pair-id>\COMPARISON.md`, at most one page of prose plus tables:
what each side claims; the requests and the shared data; a table of request x side with
executed, key output, and what was asserted; what only one side can do; the verdict and when to prefer
which; defects hit. Put every number you quote next to the file that produced it.

## Final message (at most 100 words)

Verdict, the single clearest demonstrated difference, executed k/N per side, anything blocked.
