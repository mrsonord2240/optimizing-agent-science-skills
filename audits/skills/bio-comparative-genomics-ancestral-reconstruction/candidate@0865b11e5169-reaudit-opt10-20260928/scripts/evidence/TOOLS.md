# Tooling record: bio-comparative-genomics-ancestral-reconstruction

- Mode: `delta` (after fix; baseline full inventory retained below for unchanged surfaces)
- Phase: `prepare-scientific-skill-tooling`
- Prepared: 2026-09-29 UTC (2026-09-28 America/Los_Angeles)
- Candidate: `F:\OpenScience\wt\opt10-ancestral-reconstruction\skills\bio-comparative-genomics-ancestral-reconstruction`
- Candidate identity: `sha256-manifest-v1:0865b11e5169758a84e241ca9ab4e59ecf855add0b46c6a38153808788a85871` (16 files; 1,535-byte ordinal manifest; independently reproduced before/after delta)
- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:comparative-genomics/ancestral-reconstruction`; subtree `9f7e2256c6b8246e58387a268006a675df9fd866`
- Boundary: tooling and evidence only. Candidate bytes were read-only during this delta; no audit score, further repair, or product change was made. Delta evidence root: `F:\OpenScience\audits\bio-comparative-genomics-ancestral-reconstruction\tooling-delta-opt10-20260928\`.

## Runtime boundary and reproducibility

Scientific commands ran as unprivileged user `sci` in WSL distro `science`, Ubuntu
26.04.1, through `tools/wsl_isolated_exec.sh`. The wrapper creates a private mount
namespace, removes `/mnt/f`, unsets `WSL_INTEROP`, verifies `/mnt/openscience`, and
then runs the command. The delta run independently confirmed `sci`, unset
`WSL_INTEROP`, and absent `/mnt/f` in `tooling-delta-opt10-20260928/evidence/execution-boundary.log`.

The conda prefix is `conda-env`. `environment-explicit.lock` is a 171-package
`@EXPLICIT` transaction lock (SHA-256
`216277a7a3841fb84bd731034fbfe09ca28a7514289e9bc15c8a8d92e6f4856c`); an
offline clean-prefix dry-run passed (`evidence/rebuild-dry-run.exit-code` = `0`).
Pinned core versions are Python 3.12.14, Biopython 1.88, pandas 3.0.6, PAML
4.10.10, IQ-TREE 2.4.0, MAFFT 7.526, FastTree 2.2.0, OpenJDK 21.0.10, R
4.4.3, ape 5.8-1, phytools 2.5-2, geiger 2.0.12, phangorn 2.12.1, and
data.table 1.17.8. Source-installed packages used here are corHMM 2.8, OUwie
3.0.3, and bayou 2.3.2; exact direct archives and hashes are in
`evidence/source-artifacts.tsv`, while the complete installed R inventory is
`evidence/r-installed-packages.tsv`. The base environment lock and package
fingerprint were unchanged; delta environment details and candidate binding are
in `F:\OpenScience\audits\bio-comparative-genomics-ancestral-reconstruction\tooling-delta-opt10-20260928\environment-fingerprint.json` (SHA-256 `022bf7e8720d84223d3d6f02d242b74ade72107b76bb88bd3df3321f706c7a2f`).

From PowerShell, execute within the boundary with:

```powershell
wsl.exe -d science -- bash -lc "/mnt/openscience/audit-envs/bio-comparative-genomics-ancestral-reconstruction/tools/wsl_isolated_exec.sh <command>"
```

Primary reruns are `tools/run_post_sequence_checks.sh`,
`tools/run_paml_surfaces.py`, `tools/run_r_surfaces.sh`, and
`tools/run_grasp_current.sh`. `environment-fingerprint.json` binds the candidate,
lock, versions, public input, sources, and key results; its SHA-256 is
`da8b3ef12894f2f41730e89ef09335bfefb7905a8e40963546a76dcee5f6aa08`.

## Public input and fixture contracts

The bounded real input is eight UniProtKB cytochrome-c proteins: P99999,
P62897, P62898, P62894, P00004, P00030, P00011, and P00044. Exact REST URLs,
HTTP status, response bytes, response SHA-256, taxon role, and fetch time are in
`data/public-cytochrome-c-accessions.tsv` and `evidence/public-input-fetch.tsv`.
MAFFT produced a 110-column alignment; FastTree produced a nonnegative-branch
tree, then Biopython rooted it on the declared P00044 outgroup. Inputs and cache
are `data/cytochrome-c-aligned.fasta`, `data/cytochrome-c-rooted.nwk`, and
`cache/cytochrome-c-raw.fasta`; validation is in
`evidence/public-input-summary.txt`. R fixtures use deterministic seed 20260928
and explicit matching taxon names. Parser fixtures separately exercise malformed
schemas and boundary probabilities.

## Current delta surface coverage

The complete table below remains the full-inventory baseline for unaffected
surfaces. This delta supersedes its statuses for the changed surfaces below.

| Changed surface | Runtime and invocation | Meaningful evidence | Current status |
|---|---|---|---|
| Shared PAML `rst` parser and `codeml_asr.py` posterior parser | Python 3.12.14; retained PAML 4.10.10 provider and extracted current protein `rst` outputs | `tooling-delta-opt10-20260928/evidence/python-delta-results.json`; each output parses 7 nodes × 110 sites, 770 probability records | `PASS_REAL_PROTEIN`; no real codon `rst` fixture was prepared, so codon execution is not claimed |
| Empty reconstruction summary | Same Python runtime; empty probability data | same JSON; `status=no_data`, complete zero-count/null-metric shape, summary completes without exception | `PASS_NO_DATA` |
| IQ-TREE state parser | IQ-TREE 2.4.0 real `.state` table and malformed schema fixtures | same JSON; real table has 110 rows/node and 20 posterior columns; missing columns, empty rows, bad sums, and wrong argmax each reject | `PASS_STRICT_VALIDATION` |
| GRASP CLI and candidate wrapper | Official 21-Mar-2024 JAR, Java 21.0.10; `-a/-n/-o/-j/-t --save-as FASTA TREE ASR` | `grasp-help.log`, `grasp-validation.txt`, `grasp-outputs.tsv`, and `grasp-candidate-wrapper.log`; 7 ancestors × 110 columns, 8 tree tips, parseable ASR JSON | `PASS_CURRENT_CLI_AND_ARTIFACTS` |
| Seeded stochastic mapping and taxon reconciliation | R 4.4.3; phytools 2.5.2; corHMM 2.8; `--seed=20260928`; 30-tip fixture, 1,000 maps | `r-delta-results.json` and `r-delta.log`; ARD, seed, taxa/states reported; missing `b6` rejected with reconciliation guidance; omitted seed separately rejects in `seed-required.log` | `PASS`; GitHub corHMM 2.10.5 remains untested and unsupported |
| Continuous BM and OU branches | geiger 2.0.12, phytools 2.5.2, OUwie 3.0.3; 35-tip BM and 24-tip single-regime OU fixtures | `r-delta-results.json`; BM: 34 estimates and `fastAnc 95% confidence intervals`; OU: fitted object with `knowledge=TRUE`, 29 exploratory points, no uncertainty | `PASS_WITH_EXPLICIT_LIMITS`; OU is exploratory-only and has no uncertainty |
| OUwie single-regime diagnostic handling | OUwie 3.0.3 default identifiability check then bounded `check.identify=FALSE` control | `edge-case-results.json`; default emits `missing value where TRUE/FALSE needed`; bounded fit plus fitted-object reconstruction returns 29 points | `DIAGNOSTIC_LIMIT_RETAINED`; candidate validates setup and finite AICc before this exploratory route |
| Transformed-model winners | Controlled AIC winner for EB, lambda, kappa, and delta | `edge-case-results.json`; each winner stops before using original-tree `fastAnc`/`contMap` output | `PASS_STOPPED` |

Delta rerun scripts are `evidence/test_delta_python.py`, `evidence/test_delta_r.R`,
`evidence/test_delta_edge_cases.R`, and `evidence/run_grasp_delta.sh` under the
delta evidence root. No changed environment package was installed. The old full
table below describes initial-candidate baseline results and is not current for
rows explicitly superseded above.

## Complete shipped-surface coverage

| Shipped surface | Runtime / invocation | Meaningful evidence | Status |
|---|---|---|---|
| `scripts/ancestral_reconstruction.py` demo | Python 3.12.14, exact file | `python-surfaces.json`; simulated three-node result and confidence bins | `PASS_SIMULATED`; demonstration only, not a real reconstruction |
| Provider PAML control writer | PAML 4.10.10 on public protein/tree fixture | `paml-surfaces.json`; `paml-provider/rst` and `mlc` | `PASS_WRITER`; PAML exit 0 and produced seven-node reconstruction |
| Provider `parse_rst_ancestors` / `extract_site_probabilities` | same real `rst` | both return zero records while `rst` contains 110 sites and seven nodes | `FAIL_CURRENT_OUTPUT` |
| `scripts/codeml_asr.py` control writer | PAML 4.10.10 on same input | `paml-extracted/rst` and `mlc` | `PASS_WRITER`; PAML exit 0 |
| `codeml_asr.py` posterior parser / confidence summary | same real `rst`; documented-shape control | real output returns zero nodes; control shape parses two nodes | `FAIL_CURRENT_OUTPUT`; parser expects nonexistent per-node blocks |
| `scripts/iqtree_ancestral.sh` | exact shell with IQ-TREE 2.4.0, public alignment, declared outgroup | exit 0; `asr_iqtree.state`; 660 rows, 6 nodes, 110 sites, 20 posterior columns; sums within 3e-5 | `PASS` |
| IQ-TREE outgroup contract | same alignment, absent outgroup | `iqtree-bad-outgroup.log`, exit 2, no accepted reconstruction | `PASS_NEGATIVE` |
| `scripts/iqtree_state.py` | actual IQ-TREE table plus valid and missing-probability fixtures | real rows/states/max posterior validate; missing `p_*` columns are accepted as NaN | `PASS_REAL`; `WEAK_INVALID_SCHEMA` |
| `scripts/stochastic_mapping.R` | R 4.4.3, phytools 2.5-2, corHMM 2.8, 30 tips | exact script: ARD selected, 1,000 maps, 59 summary rows, 29 corHMM marginal node rows | `PASS` on installed interface |
| Stochastic taxon mismatch | six-tip tree, one missing trait row | `r-surfaces.log`; rejected with subscript-out-of-bounds | `PASS_NEGATIVE`, but error is not diagnostic |
| `scripts/continuous_trait_asr.R` BM branch | 35-tip BM fixture; geiger 2.0.12 / phytools 2.5-2 | all six AICs finite; BM best (53.33056), lambda 0.9999267, K 0.9607117; 34 ancestors | `PASS` |
| Continuous OU branch as written | OUwie 3.0.3 current API probe | `ouwie-probe.log`; candidate fit fails on single-regime check; `OUwie.anc(fit,data=df)` rejects unused `data` | `FAIL_CURRENT_INTERFACE` |
| Current OUwie control | fitted OU1 object on an ultrametric fixture | `OUwie.anc(fit, knowledge=TRUE)` completes | `PASS_CONTROL`; establishes candidate/API issue |
| `scripts/grasp_asr.sh` without provider | exact shell | exit 127 (`grasp` unavailable by default) | `UNAVAILABLE_DEFAULT` |
| Official GRASP CLI control | official 21-Mar-2024 JAR, Java 21; current `-a/-n/-o/-j/-t` API | exit 0; 7 ancestor sequences x 110 columns, 8-tip tree, valid ASR JSON | `PASS_CONTROL` |
| Exact GRASP shell against official CLI | documented wrapper shim to same JAR | exit 5; current CLI rejects candidate's first `-aln` option | `FAIL_CURRENT_INTERFACE`; later `-tree`, `--inference`, and output names also differ from current help |

`evidence/python-surfaces.json` (SHA-256
`b864d501f4d05df3fa451335259aeea0fe517e02a5001923fc87e77d65ac342b`),
`evidence/paml-surfaces.json` (`e986040147829b83d2d7211bccf529c2035a629a1778f0f90cdf469665c83c8c`),
`evidence/r-surfaces.log` (`186fce21d0d4be93b9ba29b20c8a9afb2e3a383b055f5a74ed3242da5b1a4402`),
and `evidence/grasp-current-validation.txt` are the compact execution sources.

## Findings exposed for independent audit

- `TOOL-ASR-001` (material): both advertised PAML parsing routes are incompatible
  with real PAML 4.10.10 `rst`. PAML emits one site-by-node probability matrix;
  the scripts expect per-node probability blocks or `node #` sequence blocks and
  silently return empty results.
- `TOOL-ASR-002` (material): the GRASP command/output contract is stale. The
  official 2024 CLI uses `-a/--aln`, `-n/--nwk`, `-o/--output-folder`, `-j`, and
  `-t`; the candidate uses rejected options and promises filenames not emitted by
  the current tool.
- `TOOL-ASR-003` (material when OU wins): the OU branch uses stale OUwie calls.
  Current `OUwie.anc` accepts a fitted OUwie object and no `data=` argument;
  reconstruction also explicitly requires `knowledge=TRUE` after reading its
  documentation.
- `TOOL-ASR-004`: the provider empty-probability path returns a short
  `quality=unknown` object that its own summarizer dereferences as full metrics,
  raising `KeyError: total_sites`.
- `TOOL-ASR-005`: `iqtree_state.py` does not reject absent posterior columns;
  pandas produces NaN `max_post` values.
- `TOOL-ASR-006`: the version matrix says corHMM 2.9+, while current CRAN supplied
  2.8. The official GitHub `master` inspected on 2026-09-28 is 2.10.5 at commit
  `3ae10b22cfb519245b75777342812a0023ac0d43`; it adds RTMB and was not substituted
  into this bounded environment. The exact candidate call passes on 2.8, but that
  is not proof for the advertised 2.9+ range.

These are tooling observations, not an audit score or repair decision.

## Conditional and documented-only inventory

| Advertised surface | Classification / exact rerun ownership |
|---|---|
| FastML 3.11+, RevBayes 1.2.4+, MrBayes, BEAST2, PhyloBayes-MPI, BayesTraits V4.1 | `DOCUMENTED_ONLY`; no shipped invocation, model, prior, or expected artifact. Auditor may provision a separate environment only if judging those claims requires execution. BayesTraits is an external binary distribution; use the provider's legitimate download terms. |
| RPANDA | `UNAVAILABLE_CURRENT_CRAN`; current R 4.4 CRAN index did not offer `RPANDA`. No shipped RPANDA code. |
| HiSSE / FiSSE, RERconverge | `DOCUMENTED_ONLY_UNINSTALLED`; no shipped calls. Do not infer interface validity from prose. |
| ALE / GeneRax DTL, Dollo/phangorn | DTL tools are `DOCUMENTED_ONLY`; phangorn 2.12.1 is installed but no candidate Dollo script is supplied. |
| STRIDE, MAD, PREQUAL, HmmCleaner, PRANK, MACSE | `DOCUMENTED_ONLY_PREPROCESSING`; no packaged command, input contract, or output parser. |
| BAli-Phy, PhyloAcc, CSUBST, OrthoFinder, BUSCO | `DOCUMENTED_ONLY_RELATED`; outside shipped ASR execution surfaces. |
| GRASP web service | `WEB_ONLY_OPTIONAL`; the primary site timed out during this run. The official downloadable CLI was used instead, without bypassing access controls. |
| ete4 | `DOCUMENTED_INSTALL_ONLY`; not imported by any shipped file and not needed by executed surfaces. |

No remote authentication, commercial license, GPU, or large dataset is required
to reproduce the executed core surfaces. Conditional methods above remain honest
documentation classifications, not implicit pass results.

## Worktree safety and next role

The before/current manifests are byte-identical at the incoming identity. Python
imports initially created three run-owned `.pyc` files; they were moved out of
the candidate to `evidence/candidate-generated-pycache`, harnesses now disable
bytecode writes, and the final 15-file manifest is exact. Product status remains
only the normalized untracked Skill tree; no product commit, push, publication,
release, PR, or Marketplace action occurred.

The environment is ready for a fresh `audit-scientific-skill` worker. That worker
should independently reproduce the material failures, adjudicate the scientific
claims/thresholds and current-provider citations, and decide severity. It must
not treat successful valid controls as repairing the exact shipped scripts.
