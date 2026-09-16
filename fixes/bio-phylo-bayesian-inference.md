# bio-phylo-bayesian-inference fixes (2026-09-15)

Worktree `F:\OpenScience\external\bioSkills-wt-phylo`, branch `fix/phylogenetics`. Runtime: MrBayes 3.2.7a (Windows), R rwty 1.0.3, audit data `d12.nex`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `stoprule=yes stopval=0.01` halts before scalars are sampled | P1 | Block now `stoprule=no`; text states stoprule is ASDSF/topology-only; extend with `mcmc append=yes ngen=<new total>`; Common Errors row | ran: block with seeds, 20k gens then `append=yes ngen=40000` -> 401 samples/run, sump/sumt ok | `ngen` under append is the new total, confirmed from sample count |
| Advice without runnable commands (assertion rate) | P1 | Added `mcmc data=no ... filename=prioronly`, samples-per-step formula `ngen/(nsteps+1)/samplefreq`, `alpha=0.4`/`burninss=-1` defaults, `samplefreq` in the `ss` line | ran: data=no ("Running without data"); ss 51000/50/100 -> "10 samples within each step"; help ss for defaults | |
| RWTY `burnin=25` is trees | P2 | `burnin=round(0.25 * length(run1$trees))` + unit note | ran: analyze.rwty + makeplot.treespace on MrBayes .t files (401 trees, burnin 100) | |
| sump prints "Use the harmonic mean" | P2 | Common Errors row: ignore, use `ss` | ran: banner seen in sump output | |
| No seeds; polytomy prior not actionable | P2 | `set seed=12345 swapseed=67890;`; polytomy prior stated not available in MrBayes 3.2.7a, report as effective polytomy | ran (seeds accepted); help: `prset topologypr` options uniform/speciestree/constraints/fixed | |
| Example self-test FAIL undocumented | P2 (viewer note) | Self-test prints that the TL PSRF FAIL is intended | ran + py_compile | |

Unfixed: none. BEAST2/RevBayes commands remain names only (adding them would be new content, out of scope).

## Backlog pass — 2026-09-15

Worktree `F:\OpenScience\external\bioSkills-wt-p1`, branch `fix/backlog-p1`. Runtime: MrBayes 3.2.7a, BEAST 2.7.7 (bundled launcher.jar), Python 3.12.13 (candidate venv).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Example silently self-tests with one .p file | P2 | `examples/bayesian_convergence.py`: `--selftest` required for the self-test; one file prints an error + usage and exits 1; no args prints usage and exits 1; two files unchanged | ran: py_compile; all four invocation modes (no args, one arg, `--selftest`, two real .p files from a fresh nst=mixed run) | commit e06b806 |
| `nst=mixed` output unexplained | P2 | SKILL.md: `sump` prints a "Model probabilities above 0.050" table (`gtrsubmodel[...]` rows, written to `<file>.mstat`); report the spread, not the top model | ran: MrBayes 3.2.7a, nst=mixed on d12.nex (12 taxa, 1500bp, 30000 gen, 2 runs) — table matched exactly (4 groupings, 0.212/0.186/0.131/0.093), `d12.nex.mstat` written | commit a64e476 |
| BEAST2/RevBayes named only, no commands | P2 | Added "Minimal BEAST2 Run" subsection (`beast -seed <n> -overwrite <xml>` + BEAUti/Tracer/TreeAnnotator/LogCombiner workflow); RevBayes left without a fabricated command, with an explicit routing note (rb not installed; model is bespoke by definition of choosing RevBayes) | ran: BEAST 2.7.7 via bundled launcher on example XML `bitflip.xml`, exit 0, `-seed`+`-overwrite` both honored | commit 9a30d0d. RevBayes (`rb`) confirmed absent on this machine (checked `tools/` recursively); no command fabricated per brief's "delete the claim when absent" rule |

Unfixed: none in this slice.
