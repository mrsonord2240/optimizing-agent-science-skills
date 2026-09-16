# Audit — `cheminformatics-hit-triage-analyst` (2026-09-16)

Ten Skills audited, all from `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a`,
read from `F:\OpenScience\external\mrsonord2240__bioSkills\{chemoinformatics,machine-learning}\`
(verified byte-identical to that upstream commit by the tooling pass; nothing under
`F:\OpenScience\external\` was written to during this audit).

**Verdict: viable.** All ten Skills are deployable, no veto gate fired anywhere, no P0
recommendation is open, and every Skill marked `core` scores ≥ 85. Gates 2, 3, 4, 7 and 8 all pass.

Reports: `F:\OpenScience\audits\<skill-id>\eval_report_<skill-id>_result.json` and
`eval_viewer_<skill-id>.md`; code and logs in each `run\`.

---

## Audited Skills

| Skill ID | Role in the workflow | Core | Category | Mode | N | Executed | Static | Exec avg | Final | Grade | Veto | Top open P1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `bio-molecular-io` | Ingestion — load and convert without silent loss | – | 3 Data Analysis | A | 7 | 7/7 | 94 | 89.6 | **91** | ✅ Limited Release | none | *(P2 only)* Open Babel snippet writes InChI, unsupported in the pinned build |
| `bio-molecular-standardization` | Framing — standardise, deduplicate, register | ✔ | 3 | A | 5 | 5/5 | 91 | 89.4 | **90** | ✅ LR | none | ChEMBL parent route returns an unstripped organic salt, undocumented |
| `bio-substructure-search` | Central — PAINS/BRENK alerts, SMARTS screening | ✔ | 3 | A | 7 | 7/7 | 87 | 89.3 | **88** | ✅ LR | none | Ester SMARTS `[!H]` silently misses every `-O-CH<` ester |
| `bio-molecular-descriptors` | Central — fingerprints and physchem panel | ✔ | 3 | A | 7 | 7/7 | 85 | 87.3 | **86** | ✅ LR | none | 3D convergence guard rejects valid ensembles for ordinary flexible drugs |
| `bio-similarity-searching` | Central — similarity, clustering, activity cliffs | ✔ | 3 | A | 7 | 7/7 | 92 | 89.3 | **90** | ✅ LR | none | "Tanimoto = 1.0" failure mode has the wrong cause and a fix that does not work |
| `bio-scaffold-analysis` | Central — series, R-groups, MMPA, chemotype splits | ✔ | 3 | D | 7 | 7/7 | 91 | 86.9 | **88** | ✅ LR | none | MMPA recipe omits `loadprops`; shipped splitter always yields an all-singleton test set |
| `bio-qsar-modeling` | Central + validation — QSAR with the AD gate | ✔ | 3 | D | 7 | 7/7 | 90 | 87.1 | **88** | ✅ LR | none | chemprop predict block crashes against a model trained by its own training block |
| `bio-admet-prediction` | Central — ADMET liability and prioritisation | ✔ | 3 | A | 7 | 6/7 | 88 | 85.3 | **86** | ✅ LR | none | No executable ADMET prediction route ships with the Skill |
| `bio-machine-learning-model-validation` | Validation — honest performance estimation | ✔ | 3 | A | 7 | 7/7 | 95 | 91.3 | **93** | ✅ LR | none | *(P2 only)* leakage taxonomy ordering implies a severity ranking it does not have |
| `bio-machine-learning-prediction-explanation` | Reporting — what the model keys on | – | 3 | A | 5 | 5/5 | 92 | 86.8 | **89** | ✅ LR | none | Conditional-SHAP "credit to an unused feature" claim does not reproduce |

**66 of 67 inputs were executed against real code.** The single non-executed input is
`bio-admet-prediction` input 2 (the ADMETlab 3.0 route), recorded `executed: false` because the
Skill deliberately ships no API route for its own declared `primary_tool`; static evidence was
collected instead and the Research Veto M4 dimension was assessed on it.

**Why every grade is Limited Release rather than Production Ready.** Every one of the ten Skills
lands in the 85–100 numeric band. Every one also misses the assertion-pass-rate floor in
`scoring_rubric.md` §5 (≥ 90 % for ⭐), which forces a one-tier downgrade. Rates ran 77–87 %.
Not one of the failed assertions was a safety or scope failure; the pattern across all ten is the
same and worth stating plainly: **these Skills are stronger at method and judgement than at
keeping their own worked examples and version claims current.** Gate 3's operative test is the
score, and all eight core Skills clear 85, so the downgrades do not block the candidate. They do
say what a fix pass should target.

Score floors held everywhere else: static ≥ 80 on all ten (range 85–95), execution average ≥ 85
on all ten (range 85.3–91.3), Layer 1 average ≥ 32 and Layer 2 average ≥ 48 on all ten.

---

## Verdict against the gates I own

**Gate 2 — every bundled Skill is audited and deployable.** Pass. Ten `skill-auditor` reports,
no veto gate fired, `deployable: true` on all ten, no open P0 recommendation anywhere, and final
scores of 86–93 against a ≥ 75 requirement. Every report carries per-input `executed` and
`execution_note` fields and `meta.executed_inputs`.

**Gate 3 — core workflow Skills are Production Ready.** Pass on the operative test. All eight
Skills marked `core` score ≥ 85 (86, 86, 88, 88, 89, 90, 90, 93). See the note above on why the
grade label is Limited Release in every case.

**Gate 4 — end-to-end coverage.** Pass, with eight core Skills across all three legs:

- *Framing / data preparation*: `bio-molecular-standardization` (core), supported by
  `bio-molecular-io`. Input 4 of the standardization audit measured what this leg is worth —
  cross-registry join recovery rose from 43.7 % to 97.3 % on a ground-truth test.
- *The domain's central operation*: `bio-substructure-search`, `bio-molecular-descriptors`,
  `bio-similarity-searching`, `bio-scaffold-analysis`, `bio-qsar-modeling` and
  `bio-admet-prediction` — alerts, featurisation, clustering, series analysis, prediction and
  prioritisation. All core, all executed on real ChEMBL hERG data.
- *Validation / reporting*: `bio-qsar-modeling`'s applicability-domain gate (core) and
  `bio-machine-learning-model-validation` (core), with
  `bio-machine-learning-prediction-explanation` for interpretation. No planning Skill stands in
  for an execution Skill: every one of the ten generates and runs code.

**Gate 7 — research scope.** Pass, and this candidate is unusually well defended here. The one
Skill that could plausibly stray — `bio-admet-prediction` — was pushed with a "is this safe to
dose?" input and refused structurally rather than by disclaimer: a single model probability is
explicitly not a kill signal in either direction, ICH S7B/E14 is named as the governing guidance
rather than the model output, in vitro patch-clamp is required for a clinical candidate even when
the model is reassuring, and a universal safe/unsafe IC50 cutoff is explicitly declined. Across
its 299 lines the word "patient" appears once, in a cross-reference; "prescribe" appears zero
times. Nothing in any of the ten Skills diagnoses, prescribes for or triages an individual.

**Gate 8 — shipped means present.** Pass. Every `references/`, `scripts/`, `assets/` or
`templates/` path referenced by any bundled `SKILL.md` or `usage-guide.md` exists. All ten Skills
follow the same layout — `SKILL.md`, `usage-guide.md`, `examples/` — and reference exactly the
example files they ship: eleven example files across ten Skills, every one present, every one
byte-compiling, and every one either executed in full during this audit or exercised through the
identical snippet in `SKILL.md`. No `known_missing` entry is needed.

*Two adjacent problems that are not gate-8 failures and should not be confused with one.*
`bio-admet-prediction` ships every file it names, but its declared `primary_tool` (ADMETlab 3.0)
has no request code at all — a missing route, not a missing file. `bio-molecular-descriptors`
pins `map4 1.1+` in Version Compatibility and cites its PyPI page; PyPI serves no version of that
package. Both are recorded as P1 recommendations in their reports.

---

## The three findings that matter most for the Specialist

1. **The seams between sections are where these Skills break, not the sections themselves.**
   Three of the four hardest defects are hand-offs. `bio-qsar-modeling`'s chemprop training block
   is entirely correct and its prediction block crashes against a model that block produced
   (`RuntimeError: mat1 and mat2 shapes cannot be multiplied (64x300 and 517x300)` — the
   featurizer flag is not repeated). The same Skill recommends a scaffold split in one section and
   conformal prediction in another without noting that the first breaks the exchangeability the
   second needs; measured coverage undershot at every level (0.851 / 0.916 / 0.706 against
   0.90 / 0.95 / 0.80). `bio-scaffold-analysis`'s MMPA recipe omits `mmpdb loadprops`, so the
   documented command sequence returns `--property 'pIC50' is not present in the database`.

2. **Several failure modes name the right symptom and the wrong cause, and one prescribes a fix
   that does not work.** `bio-similarity-searching` attributes Tanimoto-1.0 collisions to hash
   collisions and tells the reader to disambiguate with an unhashed sparse fingerprint; all 141
   such pairs in a 3,224-compound library are stereoisomers whose sparse fingerprints are
   identical too (the real cause is `includeChirality=False`). `bio-machine-learning-prediction-explanation`
   states three times that conditional TreeSHAP gives nonzero credit to a feature the model never
   uses; on a depth-1 tree the 0.9995-correlated twin of the only split feature got exactly
   0.0000 — and the Skill's own shipped example asserts only the weaker, correct claim.
   `bio-molecular-descriptors`'s 3D ensemble guard treats MMFF status 1 ("more iterations
   required") as a failure and throws away a usable ensemble for any flexible drug: 19 of 20
   conformers for atenolol, 20 of 20 for verapamil.

3. **Where these Skills are careful, they are genuinely excellent, and it is measurable.** All
   seven RDKit filter-catalog sizes are exact. The Butina claim that a 0.4 cutoff guarantees
   member-to-centroid but not pairwise similarity is right on both halves (0 centroid violations;
   1,292 of 3,080 non-centroid pairs below 0.6). The MDL aromaticity description reproduces atom
   for atom, including the fused-system exception. All three of `model-validation`'s scikit-learn
   drift predictions are exact on 1.9.1, and its central claim is demonstrable: selecting features
   outside the CV fold on 200×5,000 pure noise gives CV AUC **0.904** against 0.547 inside a
   Pipeline. `qsar-modeling`'s MAPIE version bound is load-bearing — the snippet runs verbatim
   under 0.8.6 and raises `ImportError` under 1.5. And `admet-prediction`'s central hERG rule is
   quantitatively correct: against 300 measured ChEMBL IC50 values, an 18.1 % false-kill rate at
   the 0.5 threshold it warns about, still 12.7 % at 0.9.

---

## Skills read and not chosen

All 26 Skills in `chemoinformatics/` and `machine-learning/` were read (frontmatter and
description for every one; full text for the ten audited plus the two scope-boundary Skills
below).

**Out of candidate scope by the CANDIDATES.md boundary — the Specialist must stay distinct from the published `synthesis-route-optimizer`:**

- `bio-retrosynthesis` — this is the boundary: AiZynthFinder/ASKCOS multi-step route planning and
  route scoring, which is what `synthesis-route-optimizer` exists to do. Excluded on scope, not
  on quality; no tooling was installed for it.
- `bio-reaction-enumeration` — the other half of that boundary: reaction-SMARTS library
  enumeration and forward transformation. Its MMPA and R-group content overlaps
  `bio-scaffold-analysis`, which was audited instead and covers the triage-side need.

**Structure-based and 3D — a different workflow (docking and pose work), and largely unrunnable here:**

- `bio-virtual-screening` — docking campaigns; its primary Python route (`from vina import Vina`)
  cannot be built on Windows, and docking is a distinct workflow from compound-set triage.
- `bio-ml-docking-rescoring` — DiffDock/Boltz/Chai, all GPU-first with multi-GB weights; nothing
  runnable exists in this environment.
- `bio-pose-validation` — PoseBusters pose QC; only meaningful downstream of docking.
- `bio-shape-similarity` — 3D shape overlays; a scaffold-hopping adjunct, and the 2D route in
  `bio-similarity-searching` covers the triage need.
- `bio-pharmacophore-modeling` — 3D pharmacophore search; its primary hosted tool (Pharmit) is a
  web service the Skill itself says to verify before automating.
- `bio-conformer-generation` — 3D ensemble generation; needed by the 3D Skills above, and its
  CREST route has no Windows build.

**Design rather than triage:**

- `bio-generative-design` — de novo molecule generation; REINVENT 4 is a CUDA-pinned source
  install and MolMIM needs an NGC account, so nothing here is runnable, and generation is a
  different job from triaging an existing set.
- `bio-covalent-design`, `bio-protac-degraders` — modality-specific design skills whose hosted
  tools (DOCKovalent, PRosettaC) are submission-form web services.
- `bio-free-energy-calculations` — alchemical RBFE/ABFE; conda-forge and GPU-only, list-only by
  the tooling pass, and far downstream of hit triage.

**Machine-learning Skills that are genuinely omics-specific:**

- `bio-machine-learning-atlas-mapping` — single-cell reference mapping; no chemistry content.
- `bio-machine-learning-omics-classifiers` — classifier training on expression/methylation
  matrices; `bio-qsar-modeling` is the in-domain equivalent and was audited instead.
- `bio-machine-learning-biomarker-discovery` — Boruta/mRMR/LASSO feature selection framed
  entirely around gene signatures and replication cohorts; the two ML Skills that were chosen
  (`model-validation`, `prediction-explanation`) are representation-agnostic and applied to ECFP4
  fingerprints unchanged, which this one does not.
- `bio-machine-learning-survival-analysis` — time-to-event clinical modelling; out of scope and
  the nearest to the gate-7 boundary of the six.

---

## Provenance and environment notes for the builder

- Every report records `"source": "GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:<folder>/<skill>"`.
  Files were read from the `mrsonord2240__bioSkills` clone, which the tooling pass verified
  byte-identical to that upstream commit. No Skill audited here was modified, so under
  THRESHOLD gate 6 each should stay byte-identical to the upstream base commit unless a fix pass
  changes it — in which case that Skill needs a `fixes/<skill-id>.md` log and a re-audit by a
  different agent.
- Execution used `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\` throughout:
  the shared venv for most work, plus `tools\chemprop-venv` (chemprop 2.3.1), `tools\mapie08-venv`
  (mapie 0.8.6 — required to run the qsar conformal snippet as written), `tools\mhfp-venv`
  (numpy 1.26, required because `mhfp` overflows under numpy 2), and `tools\admet-ai-venv`
  (offline ADMET predictions). Real data throughout: ChEMBL hERG CHEMBL240, 3,966 rows /
  3,224 distinct compounds, CC BY-SA 3.0.
- One synthetic dataset was created, for the cross-registry join test in the standardization
  audit: `F:\OpenScience\audits\bio-molecular-standardization\data\inhouse_registry_synthetic.csv`,
  documented as synthetic in the README beside it with the script and seed that built it.
- **One self-reported breach of the read-only rule, corrected.**
  `bio-admet-prediction/run/input2_admetlab_static.py` originally imported `predict_admet.py`
  directly from the clone, which caused Python to create
  `chemoinformatics/admet-prediction/examples/__pycache__/`. It was deleted, the script was
  changed to import from a local copy inside `run/`, and the input was re-run with byte-identical
  output. Verified afterwards: 85 files under `chemoinformatics/` and `machine-learning/`, none
  modified on 2026-09-16, no `__pycache__` or `.pyc` anywhere in either folder, and
  `git status --porcelain` clean for both. Separately, pre-existing `__pycache__` directories
  exist under *other* folders of the same clone (for example
  `alignment/alignment-trimming/examples/`); those are not from this audit and were left alone,
  but the builder should know they are there before checking byte-identity.
- Two environment limits are recorded in reports rather than charged against a Skill: `mhfp`
  raises `OverflowError` under numpy 2 (upstream bug, affects the MHFP6 routes in
  `molecular-descriptors` and `similarity-searching`), and the installed `openbabel-wheel` build
  has no InChI format compiled in (affects one line of `molecular-io`).
