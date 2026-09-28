# Tooling record: bio-clinical-biostatistics-adaptive-designs

- Mode: `full`
- Phase: `prepare-scientific-skill-tooling`
- Prepared: 2026-09-28 UTC
- Candidate: `F:\OpenScience\wt\opt10-adaptive-designs\skills\bio-clinical-biostatistics-adaptive-designs`
- Candidate identity: `sha256-manifest-v1:73116b86978447d18f14945b236561b0685796da68f1a993420352c3c6953546`
- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:clinical-biostatistics/adaptive-designs`
- Origin subtree: `85188936f8fee497db8c92c095bcbd0a888e376e`
- Worktree / branch / HEAD: `F:\OpenScience\wt\opt10-adaptive-designs` / `optimize/ten-20260928-lane1-adaptive-designs` / `0bc0b31fc52742dbec1034f698103434cc9460c3`
- Scope boundary: tooling records only; candidate bytes were not changed and no audit score was assigned.

## Runtime boundary

Scientific commands ran as unprivileged user `sci` in WSL distro `science`, Ubuntu
26.04, through `tools/wsl_isolated_exec.sh`. The wrapper creates a private mount
namespace, removes `/mnt/f` from that namespace, unsets `WSL_INTEROP`, verifies
that `/mnt/openscience` remains mounted, and then executes the requested command.
`evidence/execution-boundary.tsv` records the resulting boundary. The environment
prefix is `.../conda-env`; its exact conda transaction is
`environment-explicit.lock`. The lock passed an offline micromamba dry-run
(`evidence/rebuild-dry-run.exit-code` is `0`).

Pinned runtime: R 4.4.3; rpact 4.4.0; gsDesign 3.11.0; gsDesign2 1.2.0;
simtrial 1.1.0; adaptr 1.5.0; BOIN 2.7.2; dfcrm source 0.2-2.1
(`packageVersion` 0.2.2.1); RBesT source 1.12-0 (`packageVersion` 1.12.0);
rstan 2.32.6; RcppParallel 5.1.9. `evidence/r-package-versions.tsv`,
`evidence/r-session-info.txt`, and `evidence/api-signatures.txt` are authoritative.
RcppParallel is intentionally pinned to 5.1.9: 6.2.1 produced an rstan/TBB ABI
load failure during preparation; this is environment history, not a candidate defect.

## Rebuild and invoke

From PowerShell, enter the isolated boundary with this command shape:

```powershell
wsl.exe -d science -- bash -lc "/mnt/openscience/audit-envs/bio-clinical-biostatistics-adaptive-designs/tools/wsl_isolated_exec.sh <command>"
```

Inside that boundary, an exact conda-only rebuild at a fresh prefix is:

```bash
export MAMBA_ROOT_PREFIX=/mnt/openscience/audit-envs/bio-clinical-biostatistics-adaptive-designs/mamba-root
/home/sci/.local/bin/micromamba create -y -p /mnt/openscience/audit-envs/bio-clinical-biostatistics-adaptive-designs/conda-env-rebuild \
  -f /mnt/openscience/audit-envs/bio-clinical-biostatistics-adaptive-designs/environment-explicit.lock
bash /mnt/openscience/audit-envs/bio-clinical-biostatistics-adaptive-designs/tools/install_cran_sources.sh \
  /mnt/openscience/audit-envs/bio-clinical-biostatistics-adaptive-designs/conda-env-rebuild \
  /mnt/openscience/audit-envs/bio-clinical-biostatistics-adaptive-designs/evidence/rebuild-cran-install.log
```

The second step installs retained, hash-recorded CRAN source archives and
deliberately skips `trialr`/`escalation`; see the bounded classification below.
The primary execution entry points are:

```bash
bash /mnt/openscience/audit-envs/bio-clinical-biostatistics-adaptive-designs/tools/run_candidate_surfaces.sh
bash /mnt/openscience/audit-envs/bio-clinical-biostatistics-adaptive-designs/tools/run_valid_smoke.sh
```

## Surface inventory and execution classification

| Surface | Runtime / fixture | Invocation and evidence | Classification |
|---|---|---|---|
| Candidate section 1: O'Brien-Fleming/Lan-DeMets `gsDesign()` | gsDesign 3.11.0; exact candidate constants | section runner; `section-01.json`, log and PDF | `PASS`; object printed and plot device completed |
| Candidate section 2: survival `gsSurv()` | gsDesign 3.11.0; exact candidate hazards/follow-up | section runner; `section-02.json`, log | `PASS` |
| Candidate section 3: blinded variance SSR | rpact 4.4.0; exact candidate SD 12/14 | section runner; `section-03.json` | `ERROR`; `getDesignGroupSequential(kMax=1,typeOfDesign='asUser')` requires `userAlphaSpending` before either sample-size call |
| Candidate section 4: inverse-normal promising-zone scaffold | rpact 4.4.0; exact candidate spending | section runner; `section-04.json`, log | `PASS`; design and sample size constructed |
| Candidate section 5: BOIN boundaries and 1,000-trial OC | BOIN 2.7.2; exact candidate six-dose fixture | section runner; `section-05.json`, log | `PASS`; selection percentages 0.7/7.8/29.5/37.6/20.0/4.4, expected N 26.961 |
| Candidate section 6: CRM 1,000-trial OC | dfcrm 0.2-2.1; exact candidate fixture | section runner; `section-06.json`, log | `ERROR` after simulation; six-value `PI` and five-value `prior` produce recycling warning and malformed object whose print method errors |
| Candidate section 7: enrichment | comments only | `section-07.json`; source section | `DOCUMENTED_ONLY`; no executable candidate analysis |
| Candidate section 8: MAP/EXNEX-shaped example | RBesT 1.12-0; exact three-study fixture | section runner; `section-08.json`, log | `ERROR` after successful `gMAP`; `ess(map_prior)` reports `Unknown density` because current API requires a mixture fit such as `automixfit(map_prior)` |
| Candidate section 9: I-SPY-style graduation | comments only | `section-09.json`; source section | `DOCUMENTED_ONLY`; custom Stan/JAGS or licensed FACTS implementation is not supplied |
| Candidate section 10: RAR/time trend | comments only | `section-10.json`; source section | `DOCUMENTED_ONLY`; allocation and analysis scaffold only |
| Full shipped script | exact candidate file, clean working directory | `evidence/full-script.log`, `.exit-code` | `ERROR` (exit 1); sections 1-2 run, then section 3 stops the script |
| Valid OBF and survival API | gsDesign 3.11.0 | valid smoke result 1 | `PASS`; boundary, crossing probability, events and N asserted |
| Valid fixed-analysis SSR, inverse-normal and Fisher designs | rpact 4.4.0 | valid smoke result 2 | `PASS`; larger SD increased N; inverse-normal and Fisher objects asserted. Fixed `kMax=1` warns that `asUser` is ignored |
| Deterministic BOIN OC | BOIN 2.7.2; seed 20260928, 300 trials | valid smoke result 3 | `PASS`; boundary and selection-total assertions |
| Deterministic CRM | dfcrm 0.2-2.1; shape-matched six-dose fixture, seed 20260928, 100 sims | valid smoke result 4 | `PASS`; valid object fields asserted |
| Bounded RBesT MAP mixture | RBesT 1.12-0; seed 20260928, 2 chains, 2,400 iterations | valid smoke result 5 | `PASS`; `gMAP -> automixfit -> ess`, ESS 44.3593 |
| Non-proportional-hazards design | gsDesign2 1.2.0 | valid smoke result 6 | `PASS`; four analysis rows asserted |
| Fixed-N survival simulation | simtrial 1.1.0; seed 20260928, 20 simulations | valid smoke result 7 | `PASS`; 100 result rows and schema asserted |
| Three-arm RAR engine | adaptr 1.5.0; base seed 20260928, 20 reps | valid smoke result 8 | `PASS`; reproducible `trial_results` asserted; this proves engine availability, not the candidate's conceptual RAR design |
| Invalid-input contracts | gsDesign/rpact/BOIN/dfcrm | valid smoke result 9 | `PASS`; nonmonotone timing, missing spending, invalid BOIN target and CRM shape failure asserted |
| Reference snippets: OBF, blinded SSR, inverse-normal, Fisher, CRP narrative | gsDesign/rpact APIs | candidate sections, API signatures and valid smoke | `AVAILABLE`; snippets were not promoted to candidate fixes |
| Enrichment and selection guidance | rpact exports include enrichment simulation; adaptr engine available | API signatures / valid smoke | `DOCUMENTED_ONLY` in candidate; no closed-test enrichment implementation supplied |
| Platform/graduation and Project Optimus dose comparison | no candidate implementation | source references and sections 9-10 | `DOCUMENTED_ONLY` |
| `trialr` 0.1.6 / `escalation` 0.2.3 alternatives | exact CRAN sources retained | `optional-package-classification.md`; `cran-install.log` 34097-34110 | `UNAVAILABLE_BOUNDED`; not candidate-invoked; install ceiling reached after missing `MASS` stopped trialr, so dependent escalation was not attempted |
| East/EastHorizon, ADDPLAN, FACTS | commercial/licensed external software | candidate documentation only | `RESTRICTED_DOCUMENTED_ONLY`; no license, binaries or user authorization supplied, and no bypass was attempted |
| Dated FDA/ICH sources | public authoritative HTTP endpoints | `check_regulatory_sources.sh`; `regulatory-access.tsv` | `ACCESSIBLE_NOT_ADJUDICATED`; 9/9 returned HTTP 200 on 2026-09-28; tooling did not decide current regulatory status or correct candidate text |

`evidence/valid-api-smoke.json` is the structured source for the nine passing
valid/boundary/invalid-input checks. Section JSON files carry status, elapsed
time, warnings and exact errors separately from potentially long transcripts.
Exploratory API probes remain in `probe_remaining.*` and `probe_adaptr.*`; they
are auxiliary evidence, not additional pass criteria.

## Inherited defects exposed for audit

- `TOOL-ADAPT-001` (P1): candidate section 3 omits required user alpha spending
  for rpact 4.4.0; the inherited full script stops here.
- `TOOL-ADAPT-002` (P1): candidate section 6 gives dfcrm different true-rate
  and skeleton lengths; 1,000 simulations complete but printing the malformed
  result fails.
- `TOOL-ADAPT-003` (P1): candidate section 8 passes a `gMAP` object directly to
  `ess`; the model fit succeeds but the current RBesT density contract does not.
- `TOOL-ADAPT-004` (P2): the valid fixed-analysis rpact analogue warns that
  `typeOfDesign='asUser'` is ignored at `kMax=1`; audit must assess the intended
  scientific design, not merely make the call constructible.
- `TOOL-ADAPT-005` (P2): regulatory pages were access-checked only. The audit
  must verify every dated status and quantitative claim against current source
  content before accepting or revising it.

These are execution observations for the independent audit. No candidate bytes
were repaired, and no accept/reject conclusion is encoded here.

## Provenance, caches, and retained inputs

- `data/cran-sources.tsv` lists exact public CRAN URLs; all ten archives remain
  in `sources/`, and `evidence/cran-source-fetch.tsv` records byte counts,
  SHA-256 digests and fetch times. Package bodies are durable local inputs.
- `data/regulatory-sources.tsv` lists official FDA/ICH endpoints. The checker
  discards response bodies; only status, content type, byte count, final URL,
  timestamp and access classification are retained.
- Candidate fixtures are embedded constants in `adaptive_designs.R`; independent
  deterministic fixtures and seeds live in `tools/smoke_valid_apis.R`.
- Generated evidence and plots live only below this tooling root. Candidate
  identity was recomputed after all runs and remains exact; see
  `evidence/candidate-manifest-current.tsv` and `evidence/worktree-safety.txt`.
- `environment-fingerprint.json` binds the candidate manifest, conda lock,
  package inventory, session, execution boundary, dry-run, and retained sources.
  `evidence/artifact-hashes.tsv` binds the final tooling record and key evidence.

## Exact blockers and rerun ownership

- If the auditor decides `trialr`/`escalation` must be executed, the user or
  auditor must authorize extending the bounded environment. Add a compatible
  `MASS` and all remaining declared dependencies, install retained trialr first,
  then retained escalation, and record a new lock/fingerprint. Their absence is
  not represented as evidence that their documented methods work or fail.
- East/EastHorizon, ADDPLAN and FACTS require legitimate licensed access and an
  authorized environment supplied by the user. Until then they remain
  restricted documented-only surfaces.
- No other tooling blocker remains. The prepared record is ready for the
  independent initial `audit-scientific-skill` phase.
