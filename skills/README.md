# Context-aware Skill candidates

Router-shaped recuts kept here while the shape is under test. They are not on the
optimized shelf and are not released. The shelf is where they are meant to end up
once the shape is proven (Sam, 2026-10-04).

A `ca-` prefix means "context aware": `SKILL.md` is a short route table, each
`routes/<task>.md` leads with its command, and `scripts/` holds one entry point per
route. The rules are in `.claude/skills/normalize-scientific-skill/SKILL.md`.

| Skill | Recut of | State |
|---|---|---|
| `ca-bio-workflows-crispr-screen-pipeline` | `bio-workflows-crispr-screen-pipeline` | Through the full relay; candidate-ready in `audits/skills/bio-workflows-crispr-screen-pipeline/candidate@e609525649bd-reaudit-delta-001` (final 89). Only the frontmatter `name` differs from the audited bytes. |
| `ca-bio-differential-expression-deseq2-basics` | `bio-differential-expression-deseq2-basics` | Not audited. Eval: pseudobulk task 5 of 5 with a cheap model (old layout 2 of 5); routing check 7 of 7 routes. Eleven older reference files only lightly cleaned. |
| `ca-bio-proteomics-differential-abundance` | `bio-proteomics-differential-abundance` | Not audited. Eval: 5 of 5 (old layout 2 of 5). DEqMS, proDA, msqrob2 and MSstats scripts and `shrink=ashr` never executed. No routing cases. |
| `ca-bio-machine-learning-model-validation` | `bio-machine-learning-model-validation` | Not audited. Eval: 3 of 5 (old layout 2 of 5); routing check 9 of 9 routes. Known defects: the decision-curve route needs a predictions file nothing produces; one route overstates that leave-one-out cannot give an AUC. |

`shelf-pointer-edits.patch` holds two one-line edits to shelf Skills
(`bio-workflows-scrnaseq-pipeline`, `bio-single-cell-markers-annotation`) that point
at the DESeq2 recut's pseudobulk route. Apply them only when that recut reaches the
shelf.
