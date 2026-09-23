# Brief: compare two Skills that look alike, by running both (2026-09-21)

Read `COMMON.md` first. You are the **comparer** for ONE pair (or trio) of Skills whose titles suggest
they overlap: what does each actually let a researcher do? You score nothing and have no stake in either
side. Your dispatch names the Skills, where each lives, the env and its `TOOLS.md`.

## The two sides

- **Ours:** the shelf, `F:\optimized-scientific-skills\skills\<id>\` (audited, fixed, re-audited).
- **Theirs:** Open Science's marketplace (`aipoch/medical-research-skills@d924410`), copied to
  `F:\OpenScience\comparisons\_theirs\<id>\`.

Read both completely (`SKILL.md`, `references/`, `scripts/`, `examples/`). Write in neither.

## What to do

1. Claim: `mkdir F:\OpenScience\comparisons\<pair-id>`. Stop if it fails.
2. Before running anything, write down what each side says it does and for whom.
3. Write 2-3 realistic requests on one shared dataset (small synthetic, or public; say which and why it is
   fair to both). Run **each request through each Skill's own instructions and scripts**, as an agent that
   loaded it would: run a shipped script; do what prose says. Give both sides the same effort.
4. Assert on output (plant an effect and see whether it is recovered). Record `executed: true|false` and
   why, per request per side. Install missing libraries outside `comparisons\`.
5. Note what each side does that the other cannot: runnable code vs guidance, statistical guardrails
   (background sets, multiple testing, assumption checks, leakage), failure modes it warns about, output
   that is silently wrong. Where the other party's Skill is better, say so plainly.
6. Verdict: **duplicate** (either serves any request the other would), **partial** (each does something
   the other does not) or **distinct** (different jobs), then which to use for what, backed by at least
   one demonstrated difference in output.

No score, grade or P0/P1 list. Report defects you hit, one line each, because they explain the verdict.
Scripts go under `F:\OpenScience\comparisons\<pair-id>\run\`.

## Deliverable

`F:\OpenScience\comparisons\<pair-id>\COMPARISON.md`, at most one page plus tables: what each side claims;
the requests and data; a table of request × side with executed, key output and what was asserted; what
only one side can do; the verdict; defects hit. Every number quoted sits next to the file that produced it.

## Final message (≤ 100 words)

Verdict, the clearest demonstrated difference, executed k/N per side, anything blocked.
