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
