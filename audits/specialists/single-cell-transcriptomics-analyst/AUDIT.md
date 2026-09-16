# Audit — `single-cell-transcriptomics-analyst` (2026-09-16)

Lead auditor for round 2. Fourteen Skills counted toward coverage: **nine audited in this pass**
and **five reused** from finished reports. Every report lives in `F:\OpenScience\audits\<skill-id>\`
with its code and logs in `run\` and its derived synthetic data, where any, in `data\`.

**Verdict: viable.** Gates 2, 3, 4, 7 and 8 all pass. Two of the fourteen Skills are excluded from
`spec.json` and both exclusions are stated below.

---

## Skills audited

| Skill ID | Role | Category | Mode | N | Executed | Static | Exec avg | Final | Grade (post-floor) | Veto | Top P1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `bio-workflows-scrnaseq-pipeline` | core — framing/orchestration | Data Analysis | A | 7 | 6/7 | 78 | 89.9 | **85** | ✅ Limited Release | PASS | Three of its seven ordering rules have no code anywhere |
| `bio-single-cell-preprocessing` | core — entry | Data Analysis | A | 7 | 6/7 | 83 | 86.1 | **85** | ✅ Limited Release | PASS | SoupX snippet errors on the input the Skill names |
| `bio-single-cell-doublet-detection` | core — artifact removal | Data Analysis | A | 5 | 5/5 | 84 | 86.2 | **85** | ✅ Limited Release | PASS | The Python per-sample loop silently discards its own results |
| `bio-single-cell-batch-integration` | core — multi-sample | Data Analysis | A | 7 | 7/7 | 88 | 91.0 | **90** | ✅ Limited Release | PASS | The Seurat v5 snippet aborts on its own default method |
| `bio-single-cell-clustering` | core — partition | Data Analysis | A | 5 | 5/5 | 86 | 91.6 | **89** | ✅ Limited Release | PASS | The Skill's only operational stop rule never stops |
| `bio-single-cell-cell-annotation` | core — labelling | Data Analysis | A | 5 | 5/5 | 86 | 88.4 | **87** | ✅ Limited Release | PASS | The triage screens on the one signal artifacts do not trip |
| `bio-single-cell-differential-abundance` | core — validation (composition) | Data Analysis | A | 5 | 5/5 | 87 | 88.8 | **88** | ⭐ Production Ready | PASS | The primary tool returns a false negative on the canonical use case |
| `bio-differential-expression-deseq2-basics` | core — validation (expression) | Data Analysis | A | 7 | 7/7 | 88 | 94.0 | **92** | ⭐ Production Ready | PASS | *(none — no P0 and no P1)* |
| `bio-single-cell-markers-annotation` | supporting — annotation evidence | Data Analysis | A | 5 | 5/5 | 84 | 90.0 | **88** | ⭐ Production Ready | PASS | The Python pseudobulk snippet sums normalized values, against the Skill's own rule |
| `bio-pathway-gsea` *(reused)* | supporting — interpretation | Data Analysis | A | 7 | 7/7 | 91 | 90.0 | **90** | ✅ Limited Release | PASS | `nPerm` is accepted and silently downgrades the engine |
| `bio-pathway-go-enrichment` *(reused)* | supporting — interpretation | Data Analysis | A | 5 | 5/5 | 89 | 90.0 | **90** | ⭐ Production Ready | PASS | *(P2 only)* |
| `bio-experimental-design-batch-design` *(reused)* | supporting — design | Protocol Design | A | 5 | 5/5 | 81 | 83.2 | **82** | ✅ Limited Release | PASS | SVA block fails on matrices with missing values |
| `bio-experimental-design-multiple-testing` *(reused)* | **excluded** | Data Analysis | A | 7 | 7/7 | 84 | 81.4 | **82** | ⚠️ Beta Only | PASS | Four open P1s; `deployable: false` |
| `bio-experimental-design-sample-size` *(reused)* | **excluded** | Protocol Design | A | 7 | 7/7 | 69 | 66.0 | **67** | ❌ Reject | **FAIL (M4)** | `ssizeRNA_vary` called with scalars errors on every call |

**Totals for the nine audited in this pass: 53 inputs, 51 executed (96%).** The two that did not
execute are text-only scope-boundary responses (spatial Visium for `preprocessing`; a hashed CITE-seq
pool for the workflow Skill), recorded as `executed: false` with the reason in each report.

Every JSON validates with no ERROR lines under
`audit-envs\single-cell-transcriptomics-analyst\tools\validate_report.py`. The two reused reports for
`bio-pathway-go-enrichment` and `bio-experimental-design-batch-design` emit one `meta.source wrong
prefix` line each, because they were audited against the **fork** (`mrsonord2240/bioSkills@575ab946`)
after a fix pass rather than against the upstream base commit. That is correct for those reports and
is not a defect; see *Provenance* below.

---

## Skills read and not chosen

All read from `single-cell/`, `differential-expression/`, `pathway-analysis/`, `experimental-design/`
and `workflows/scrnaseq-pipeline`. One line each.

| Skill | Why not chosen |
|---|---|
| `single-cell/data-io` | Genuinely useful (10x raw-vs-filtered, h5ad/Seurat/SCE conversion) but purely plumbing; the workflow Skill and `preprocessing` already state the raw-vs-filtered commitment, which is the only decision in it that changes a result. Closest call of the twenty-one. |
| `single-cell/hashing-demultiplexing` | Only applies to multiplexed pools; the workflow Skill names it as a precondition and the candidate's scope starts from per-sample count matrices. Strong candidate if the bundle grows. |
| `single-cell/multimodal-integration` | CITE-seq and multiome joint analysis; `scglue` has no Windows build and the candidate's scope is RNA-only. |
| `single-cell/scatac-analysis` | scATAC/multiome, admitted by `CANDIDATES.md` only "if the Skill is strong"; ArchR is Unix-only and SnapATAC2 will not build here, so half its routes are untestable in this environment. |
| `single-cell/trajectory-inference` | Continuous-process analysis sits past the candidate's stated endpoint (annotated cells → DE and abundance); CellRank could not be installed without downgrading the shared venv. |
| `single-cell/cnv-inference` | Tumour malignant-cell calling, out of the PBMC/immune scope; `infercnv` cannot load here at all (needs JAGS 4). |
| `single-cell/cell-communication` | Ligand–receptor inference is a separate downstream question; LIANA and CellPhoneDB both downgrade shared-venv packages and CellChat is GitHub-only R. |
| `single-cell/metabolite-communication` | Explicitly out of scope; MEBOCOST is not installable here. |
| `single-cell/lineage-tracing` | CRISPR-scar and barcode lineage reconstruction, a different assay entirely; Cassiopeia has no Windows wheels. |
| `single-cell/perturb-seq` | CRISPR screens belong to the `crispr-screen-analyst` candidate, and `sceptre` requires R ≥ 4.5. |
| `differential-expression/edger-basics` | A second bulk DE engine covering the same step as `deseq2-basics`, which scored 92. Adding it duplicates the central validation step rather than extending coverage. |
| `differential-expression/de-results` | Strong content, but its whole subject (padj=NA causes, IHW, TREAT, GSEA input prep) is also in `deseq2-basics`, which was audited on exactly those points and passed them. |
| `differential-expression/de-visualization` | Figure production; no decision in it changes a result, and gate 4 asks for coverage, not breadth. |
| `differential-expression/batch-correction` | Bulk-specific (ComBat/SVA/RUVSeq); the single-cell equivalent is `batch-integration`, which is in the bundle, and the design-side case is covered by `experimental-design/batch-design`. |
| `differential-expression/timeseries-de` | Time-course designs are outside the candidate's two-condition scope; `ImpulseDE2` is gone from Bioconductor. |
| `pathway-analysis/kegg-pathways` | A third interpretation Skill after GSEA and GO ORA; KEGG adds a licensing and organism-code surface for no new decision. |
| `pathway-analysis/reactome-pathways` | Same reason — a fourth gene-set source, not a new step. |
| `pathway-analysis/wikipathways` | Same reason, and the weakest-curated of the three sources. |
| `pathway-analysis/enrichment-visualization` | Figure production downstream of GSEA/GO; no result-changing decision. |
| `experimental-design/power-analysis` | Overlaps `sample-size`, which failed its Research Veto on exactly this material; auditing the neighbouring Skill was not worth a slot before that fix lands. |
| `experimental-design/randomization-blocking` | Design-stage material adjacent to `batch-design`, which is already in the bundle as the supporting design Skill. |

---

## Verdict against the gates

### Gate 2 — every bundled Skill is audited and deployable

**PASS for the twelve Skills in `spec.json`.** Each has a `skill-auditor` report, no veto fired,
`deployable: true`, no open P0 recommendation, and a final score ≥ 75. The lowest score in the bundle
is 82 (`bio-experimental-design-batch-design`, supporting) and the lowest core score is 85.

Two Skills are **excluded**:

- **`bio-experimental-design-sample-size` (67, ❌ Reject, Research Veto M4 FAIL).** Its
  `ssizeRNA_vary` call errors on every invocation and its worked example returns NA/NaN as its
  headline answers. It cannot be bundled until a fix pass lands and a fresh audit clears the veto.
- **`bio-experimental-design-multiple-testing` (82, ⚠️ Beta Only, `deployable: false`).** Four open
  P1s; gate 2 requires `deployable: true`, which it does not have. The FDR material the Specialist
  actually needs is carried inside `deseq2-basics` (independent filtering, IHW, TREAT — all three
  verified working in this audit) and `bio-pathway-gsea`.

### Gate 3 — core workflow Skills are Production Ready

**PASS on score.** All eight Skills marked `core` score ≥ 85: 92, 90, 89, 88, 87, 85, 85, 85.

**Read this with the grades.** Five of the eight carry a post-floor grade of ✅ Limited Release rather
than ⭐ Production Ready. In every one of those five the *only* floor missed is the assertion-pass
rate (89.3%, 85%, 85%, 80%, and — for the workflow Skill — the static floor at 78 against 80). The
gate is written on `final.score`, and on `final.score` all eight clear it. I am flagging the
distinction rather than burying it, because the pattern behind those assertion failures is consistent
and is the single most important finding of this audit: **the reasoning in these Skills is excellent
and the prescribed code is not always executable as printed.**

Eight separate snippets failed or misbehaved when run verbatim:

| Skill | What did not work as printed |
|---|---|
| `preprocessing` | SoupX `load10X → autoEstCont` aborts on a standard Cell Ranger delivery ("Clustering information must be supplied") |
| `preprocessing` | `seurat_v3` HVG with `batch_key` raises a singular-loess `ValueError` on a shallow batch |
| `doublet-detection` | The Scrublet per-sample loop scores a **view**; the parent object ends with no doublet columns and no error |
| `doublet-detection` | `examples/doubletfinder.R` passes `reuse.pANN = FALSE` and dies with "cannot xtfrm data frames" |
| `doublet-detection` | `scDblFinder(samples=)` is not reproducible under `set.seed`: 22.7% of doublet calls moved between identically seeded runs |
| `batch-integration` | `IntegrateLayers(method = RPCAIntegration)` aborts on `future.globals.maxSize` on a 6,000-cell object |
| `markers-annotation` | `sc.get.aggregate(..., func='sum')` sums log-normalized values, violating the same document's "aggregate RAW counts" rule |
| `cell-annotation` | The four-way triage screens on low annotation confidence, which had **0/4 sensitivity** on labelled artifact clusters |

Every one is a one-line fix. None is a design error. If a fix pass lands them, at least four of the
five Limited Release core Skills would clear the 90% assertion floor and become Production Ready.

### Gate 4 — end-to-end coverage

**PASS.** Eight core Skills covering all three required areas:

- **Framing / design** — `bio-workflows-scrnaseq-pipeline` (85, core) owns the made-once commitments,
  the seven cross-cutting ordering rules and the hand-offs, supported by
  `bio-experimental-design-batch-design` (82, supporting) for the batch/condition layout.
- **Central operation** — `preprocessing` → `doublet-detection` → `batch-integration` → `clustering`
  → `cell-annotation`, with `markers-annotation` as supporting evidence. This chain was run end to
  end on eight simulated Cell Ranger samples and reached **0.998 accuracy / ARI 0.996** against
  ground-truth cell types.
- **Validation / reporting** — `deseq2-basics` (92) for replicate-aware pseudobulk DE and
  `differential-abundance` (88) for simplex-aware composition testing, with `gsea` and
  `go-enrichment` for interpretation. Run on the annotated object from the chain above, these
  recovered exactly the injected biology: 20 DE genes at **precision 1.000** in the one cell type
  that changed, **zero** calls in the other seven, and NK cells as the sole abundance shift.

No planning Skill stands in for an execution Skill: the framing Skill is a workflow orchestrator with
its own executable paths, not a protocol-design Skill, and both validation Skills are executors.

### Gate 7 — research scope

**PASS.** All twelve bundled Skills are Category 3 (Data Analysis) or Category 2 (Protocol Design)
and operate on count matrices and sample sheets. No output in 53 inputs diagnosed, prescribed for or
triaged an individual; the M2 dimension is PASS in every report. Two inputs deliberately invited
over-claiming (a "novel transitional cell type" from a doublet-enriched cluster; a "new PBMC subset"
from a high-resolution split) and both were refused with measurements.

### Gate 8 — shipped means present

**PASS, with nothing missing.** None of the twelve bundled `SKILL.md` or `usage-guide.md` files
points at a `references/`, `scripts/`, `assets/` or `templates/` file — these Skills carry their
method in the body and ship `examples/` only. Every shipped example file exists; all Python examples
compile under `py_compile` and all R examples parse. No `known_missing` entry is needed and no P0 was
raised on this gate.

One runtime caveat, recorded because it is adjacent: `examples/doubletfinder.R` **exists and parses**
but aborts at line 36. That is a correctness P1 inside `bio-single-cell-doublet-detection`, not a
gate-8 failure.

---

## Provenance

The five candidate folders in `F:\OpenScience\external\mrsonord2240__bioSkills\` were verified
byte-identical to `F:\OpenScience\external\GPTomics__bioSkills\` for `single-cell/`,
`differential-expression/`, `pathway-analysis/`, `experimental-design/` and
`workflows/scrnaseq-pipeline` (`diff -rq`, all five clean). `spec.json` therefore names the upstream
base commit `GPTomics/bioSkills@d91ed3d5` and its clone path, and every report this pass emitted
records `meta.source = "GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:<folder>/<skill>"`.

Two reused reports do not: `bio-pathway-go-enrichment` and `bio-experimental-design-batch-design`
cite `mrsonord2240/bioSkills@575ab946989a7029d235eb0ab711e47b08edbcb0`, because both were audited
after a fix pass on the fork. **If a release ships those two Skills it must ship the fixed bytes and
record the fork route in `skills/bioSkills/UPSTREAM.json` per THRESHOLD gate 6 (round 2), not the
base commit above.** A build that mixes the two routes will fail gate 6. If any of the eight P1 fixes
listed under gate 3 lands, the whole `upstream` block moves to the export commit in the same way.

---

## Recommendations to whoever writes the Specialist

1. **Lead with the ordering, not the tools.** The single strongest measurement in this audit is that
   clustering the same object on a raw PCA gave ARI 0.648 against ground truth and on the Harmony
   embedding gave 0.996. The workflow Skill's seven ordering rules are what make this bundle work;
   the system prompt should carry them, not a tool list.
2. **State the two cross-condition questions as separate obligations.** Pseudobulk DE answered
   "which genes changed" at precision 1.000 and said nothing about composition; differential
   abundance answered "which populations shifted" and said nothing about expression. Each alone
   reports half the biology. The Skills say this; the Specialist should require it.
3. **Carry the pseudoreplication refusal explicitly.** On a deliberately null contrast, cell-level
   testing produced 78 false positives with a smallest adjusted p of 2×10⁻¹³ while pseudobulk
   produced zero. This is the error researchers will ask the Specialist to make, in those words.
4. **Do not promise sample-size or power planning.** Both `experimental-design` Skills that cover it
   are excluded, and `sample-size` failed its Research Veto. The Specialist should decline cohort
   sizing and hand it off rather than improvising from `batch-design`.
5. **Expect the hand-offs to dangle.** `bio-workflows-scrnaseq-pipeline` names 19 Related Skills and
   five `depends_on` entries; `deseq2-basics` names 13. Several — `single-cell/data-io`,
   `single-cell/hashing-demultiplexing`, `single-cell/trajectory-inference`, `de-results`,
   `expression-matrix/*` — exist upstream but are **not in this bundle**. Either add `data-io` and
   `hashing-demultiplexing` (the two most likely to be needed) or have the system prompt say what is
   out of scope so the Specialist does not point at Skills it does not have.
