# Skill catalog and overlap measurement across the source pool (2026-09-17)

Written for: Sam, choosing the working list for hybrid multi-repository Specialists.

Source pool is `skill_lists.md` (13 repos) plus four more already cloned under
`F:\OpenScience\external`. Data: `catalog.json` (every Skill) and `similarity.json` (every measured
pair). Rebuild with the scripts named at the end.

## Headline

**2,235 Skills cataloged → 2,079 distinct after removing duplicates.** The pool is far less redundant
than the raw collision count suggested: only 156 of 2,235 files are redundant copies.

The dangerous number is different. **495 pairs share a declared `name` while being completely
different Skills** — median content similarity 0.03. Those collide on install while doing unrelated
jobs.

## Corpora

Four repos were excluded before cataloging, each for a verified reason:

| excluded | why |
| --- | --- |
| `GPTomics/bioSkills` | superseded by our fork `mrsonord2240/bioSkills`, same 562 Skills plus audit-evidenced fixes |
| `K-Dense-AI/scientific-agent-skills` | byte-identical to `K-Dense-AI/claude-scientific-skills` — same 164 paths, same content |
| `InternScience/Awesome-Scientific-Skills` | submodule aggregator of ~30 other repos, not a corpus; includes several we already clone separately |
| `Agnuxo1/PaperClaw` | contains no `SKILL.md` |

So `skill_lists.md`'s 13 entries are **11 distinct corpora**.

| repo | skills | unique | shared | licence | in list |
| --- | ---: | ---: | ---: | --- | :-: |
| aipoch/medical-research-skills | 605 | 593 | 12 | MIT | yes |
| mrsonord2240/bioSkills (our fork) | 562 | 562 | 0 | MIT | yes |
| jaechang-hits/scicraft | 208 | 208 | 0 | **CC-BY** | yes |
| InternScience/scp | 207 | 207 | 0 | MIT | – |
| LeonChaoX/qinyan-academic-skills | 187 | 142 | 45 | MIT | yes |
| K-Dense-AI/claude-scientific-skills | 164 | 110 | 54 | MIT | yes |
| K-Dense-AI/claude-scientific-writer | 78 | **9** | 69 | MIT | yes |
| NVIDIA-BioNeMo/bionemo-agent-toolkit | 62 | 62 | 0 | Apache-2.0 | yes |
| HaoxuanLiTHUAI/cognitive-and-neuroscience | 50 | 50 | 0 | MIT | yes |
| google-deepmind/science-skills | 40 | 40 | 0 | Apache-2.0 | yes |
| HughYau/AcademicForge | 33 | 32 | 1 | MIT | yes |
| Weizhena/Deep-Research-skills | 20 | 20 | 0 | MIT | – |
| yorkeccak/scientific-skills | 13 | 13 | 0 | MIT | – |
| HughYau/neuroforge-skills | 5 | 5 | 0 | **MIT per README, LICENSE file absent** | yes |
| Intelligent-Internet/II-Commons-Skills | 1 | 1 | 0 | Apache-2.0 | – |

## How overlap was measured

Three passes, cheapest first, and **no conclusion rests on a single metric**:

1. **Identical bytes** — sha256 over `SKILL.md`. 62 sets covering 152 files.
2. **Name collision** — same frontmatter `name`, different bytes. 168 names.
3. **Near-duplicate by description** — word-shingle Jaccard over name + description, bucketed so this
   stays linear rather than 2.5M pairwise comparisons. 322 candidate pairs at ≥ 0.30.

Every candidate pair from 2 and 3 was then measured on **body text with frontmatter stripped**, using
`SequenceMatcher.ratio()` **and** a word-level Jaccard as an independent second measure.

> A correction worth recording. The first pass used `difflib.quick_ratio()`, which is a
> bag-of-characters **upper bound** that ignores word order. It reported a median 0.87 between
> `claude-scientific-skills` and `qinyan-academic-skills` and led to a wrong conclusion — that the pool
> was one lineage republished. The true `ratio()` for those same pairs is **0.03**. They share Skill
> *names*, not text. Do not use `quick_ratio` for this.

## Results — 665 pairs measured

| band | pairs | what it means | action |
| --- | ---: | --- | --- |
| ≥ 0.80 near-identical | 117 | genuinely the same Skill text | pick one |
| 0.45–0.80 substantial | 53 | real overlap, different emphasis | judgement call per pair |
| < 0.45 name-only | 495 | same name, unrelated Skill | **must be namespaced** |

**Real duplication is concentrated in one cluster**, the K-Dense / qinyan family:

- `claude-scientific-skills` ↔ `claude-scientific-writer` — 69 near-identical. The writer repo has only
  **9 Skills unique to it** out of 78; it is close to a subset.
- `claude-scientific-skills` ↔ `qinyan-academic-skills` — 32 near-identical, 20 substantial.
- `qinyan-academic-skills` ↔ `medical-research-skills` — 12 near-identical, 12 substantial.

Every other corpus — bioSkills, scicraft, scp, bionemo, science-skills, the neuroscience sets — has
**zero** content overlap with anything else in the pool.

## The naming problem, and the corpus that already solved it

495 name-only collisions means names like `literature-review` (5 repos), `scientific-visualization`,
`hypothesis-generation` and `exploratory-data-analysis` (4 repos each) are declared independently by
different authors for different Skills. Installing two of them conflicts by ID while the Skills do
unrelated work.

**bioSkills is the exception: 2 of 562 Skills are involved in any name collision at all**, because
every ID carries a `bio-` prefix. Those two collide with `medical-research-skills` at 0.03–0.05
similarity — name-only, as everywhere else.

That makes the rule for the hybrid model concrete: **namespace every Skill ID by source corpus on
intake**, the way bioSkills already does. Without it, a multi-repo Specialist has a 495-pair minefield;
with it, the problem disappears and only the 117 genuine duplicates need a decision.

## Working list

**2,079 distinct Skills.** Reductions available before any quality judgement:

- Drop `claude-scientific-writer` except its 9 unique Skills, or treat it as the canonical source for
  the 69 it shares and drop those from `claude-scientific-skills`. One of the two, not both.
- Resolve the 106 duplicate clusters (262 Skills) by picking a canonical source per cluster.
- Decide the two licence questions below.

Both remaining licence items need a decision before anything from those sources ships:

- **`scicraft` is CC-BY** (208 Skills), not MIT. Attribution obligations differ from the rest of the pool.
- **`neuroforge-skills` states MIT in its README and links to a `LICENSE` file that is not in the
  repository.** Five Skills; cheapest answer is to skip it.

Apache-2.0 (`science-skills`, `bionemo-agent-toolkit`, `II-Commons-Skills`) is redistributable but
requires NOTICE preservation, which `build_specialist.py`'s `THIRD_PARTY_NOTICES` does not currently
handle.

## What this does not tell you

Overlap is measured on text, not on behaviour. Two Skills at 0.03 similarity can still answer the same
request, and the 2026-09-17 bioSkills-vs-published cross-reference (`REPORT.md`) found exactly that —
`gsea` and `bio-pathway-gsea` are textually unalike and functionally competing. Text similarity finds
copies; it does not find functional duplicates. Those need reading, and that is what `REPORT.md` did
for 98 Skills.

Nothing here is a quality judgement either. Of the 2,079, only the bioSkills subset has audit reports.

## Rebuild

`crossref/scripts/catalog.py` writes `crossref/data/catalog.json`; `crossref/scripts/similarity.py` writes `crossref/data/similarity.json`
from it. Both read the clones under `F:\OpenScience\external` and take a couple of minutes.
