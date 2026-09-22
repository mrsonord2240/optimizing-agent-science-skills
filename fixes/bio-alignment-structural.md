# bio-alignment-structural (alignment/structural-alignment) - fix log

## 2026-09-20 - fix/al-struct (worktree `F:\OpenScience\wt\al-struct`, from staging main 130efd1)

Audit: first audit 73, Beta Only, not deployable, no veto/P0 (`F:\OpenScience\audits\bio-alignment-structural\`).
Tools (WSL `science`, env `alignment`): Foldseek 10.941cd33, Foldmason 4.dd3c235, TM-align 20240303 (compiled
from USalign source), US-align 20241108, TMscore (same build), DaliLite v5, MUSTANG 3.2.3, PyMOL 3.1.0,
T-Coffee 12.00.7, Biopython 1.88, Python 3.12.14. Scratch data: real PDB entries only (RCSB, AFDB v6 model
AF-P02185-F1) plus the three degenerate synthetic PDBs from the audit's `data/synthetic/`.
Every changed `.py` passed `py_compile`; every shipped example was rerun from a clean copy.

### Findings

| finding | pri | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| Foldmason example not reproducible (no `--refine-seed`) | P1 | SKILL command and `foldmason_msa.py` pass `--refine-seed 42`; SKILL states default `--refine-iters` is 0 (deterministic), unseeded refinement is random, results are only comparable with a seed | ran: two unseeded `--refine-iters 100` runs -> 2 different md5; two `--refine-seed 42` runs -> identical md5 (`dff2bd88...`); `--refine-iters 0` x2 identical; example rerun twice from clean copy gives the same md5 | audit's 74% aligned-pair overlap figure is quoted from the audit run |
| Foldseek-Multimer commands wrong or lossy | P1 | `easy-multimersearch` no longer shows `--multimer-tm-threshold`; `easy-multimercluster` takes one directory (file list / glob clusters only the last file, exit 0); `Foldseek-MM-TM` = `--alignment-type 1`; `_report` file and its 9 columns documented; complex TM filtered on report columns 5-6 | ran: search 1IRD vs dir of 7 complexes -> `s1_report` 17 rows (qTM 0.981 / tTM 0.492 for 1A3N A,B); `--multimer-tm-threshold` on search rejected (help lists it only under easy-multimercluster); cluster on directory -> 7 rows, glob of 7 files -> 1 row (`2LHB`), 3 files -> 1 row (`1IRD`); `--alignment-type 1` search ran | second method: US-align `-mm 1 -ter 0` 0.977 / 0.494 on the same pair |
| `-mm 4 -byresi 0` remedy wrong | P1 | replaced by: `-mm 1 -ter 0` already handles unequal stoichiometry, report both normalisations; `-mm 4` is MSTA and unsuitable | ran: US-align `-mm 1 -ter 0` 1IRD vs 1A3N -> 0.9769 / 0.4943, RMSD 0.94, Lali 286; `USalign -h` text for `-mm 4` ("MSTA ... consensus alignment") | I did not add `-mm 2`: one run gave a single row I could not interpret |
| `per_column_lddt` returns None | P1 | SKILL snippet and example use `report['scores']` with a length assert, `-1` = no LDDT; example prints scored-column count | ran: JSON keys `entries, scores, tree, statistics`; `.get('per_column_lddt')` -> None; `len(scores)` 486 == `len(entries[0]['aa'])` 486 (11 files, seed 42); 113 columns are -1 | |
| Superimposer example silently mis-pairs (Ca2+ counted as CA) | P1 | example rewritten: CA of standard residues of model 0 (`id[0]==' '`), paired by (chain, resseq, icode); refuses when < half the shorter chain pairs or > 20% of paired residue names differ; SKILL inline block fixed | ran: original example on 1CLL/1CFD -> 13.378 A (148 "CA"); fixed example -> 10.829 A over 144 pairs; independent numpy Kabsch on the same pairing -> 144 pairs, 10.829 A. 1A6M/1MBN -> 0.483 A / 151 pairs (Kabsch 0.483, TM-align 0.48). 1MBN vs 1A3N (co-chain, not co-numbered) -> ValueError (116/141 names differ); 1MBN vs 1ATP (no shared chain id) -> ValueError | |
| `--alignment-type 1` breaks E-value filter; `max_seqs` cap hides count | P1 | `confident_hits()` filters alnTM > 0.5 (and E < 1e-3 only for type 2); example warns when rows == cap; SKILL table row and `--max-seqs` note | ran: 11-file DB (18 chains), 1MBN query: type 2 -> 13 confident; type 1 -> old filter 0 hits, new filter 13 (min E among them 0.83); `max_seqs=10` prints the cap warning | Foldseek default `--max-seqs` is 1000 (help) |
| `tm_align()` crashes on degenerate input | P1 | `RuntimeError` naming the tool's message when no data row returns | ran: one_residue -> `Sequence is too short <3!`; ligand_only -> `Cannot parse file ... Chain number 0`; both exit 0 with no row, both now raise | US-align segfaults on the one-residue file (noted in SKILL) |
| "Larger TM" headline metric inflates short-chain scores; `>0.8` labelled homologous; `<60` caveat absent in code | P2 | SKILL and example report both TM-scores, fold call uses `min(TM1,TM2)`; `interpret_tmscore(tm, length)` guards < 60 residues; `>0.8` -> "very similar topology (not proof of homology)"; unsupported "~3-5% by chance" sentence dropped; Xu-Zhang p-value stated as not computable with these tools | ran: 136 pairs of real PDB entries (86 different-fold): `max` -> 3 false same-fold calls (1PGA vs 1ATP 0.505, 1HCK 0.544, 2ITZ 0.538); `min` -> 0. 10-residue helix scored 0.846 (max), example prints the short-chain guard | `min` misses conformationally shifted homologs (1CFD/1CLL 0.414, 1PGA/1UBQ 0.421); SKILL says `max` answers containment only |
| usage-guide installs broken `tmalign`; `-o` wording; Expresso/3D-Coffee need a working command | P2 | install line now in SKILL (`usalign`, build TM-align from US-align source, never bioconda `tmalign`); `-o` documented as a prefix that appends `.pdb`; example `output_prefix`; `PDB100` -> `PDB`; T-Coffee/Expresso/3D-Coffee claim deleted (see below) | ran: `TMalign -o sup` -> `sup.pdb`+`.pml`; `-o sup.pdb` -> `sup.pdb.pdb`; `foldseek databases` list has no `PDB100`; example rerun asserts `superposed.pdb` exists | 3D-Coffee: 5 attempts (per-chain PDB templates with/without `.pdb`, absolute path, `-pdb_type d`, 60-250 s) - T-Coffee 12.00.7 either retries retired RCSB/wwPDB endpoints (timeout) or logs "Could Not Fill _P_ template" and falls back to `proba_pair`; no working command exists here |
| GDT-TS and DALI have no runnable path | P2 | DALI: DaliLite block (`import.pl`, `dali.pl`, result file trap); GDT-TS: `TMscore model native -seq` with the residue-number trap; MUSTANG table row got its command | ran: DaliLite 1MBN vs 1A3N-A Z 20.3, rmsd 1.6, lali 141, 26% id; 1ATP-E vs 1HCK-A Z 24.1; 1MBN vs 1ATP empty. TMscore AF-P02185 model vs 1MBN: default GDT-TS 0.5082 / TM 0.593, `-seq` GDT-TS 0.9853 / TM 0.9804 / RMSD 0.705 (TM-align gives 0.9804, 0.71). MUSTANG 3 myoglobins -> 3-row `.afasta` | `TMscore` was not in the Skill before; added because the GDT-TS row already claimed the criterion |
| Foldmason summary counts chains as structures | P2 | example prints "11 files -> 18 chain rows"; SKILL says rows are chains named `<file>_<chain>` | ran: 11 files -> 18 rows x 486 columns | |

Also fixed while there (not audit findings): `foldseek --version` / `foldmason --version` are rejected ->
`foldseek version`, `foldmason version` (ran); Common Errors table rows replaced with ones reproduced by the
audit's logs (TM-align exits 0 without a row, wrong DB path message, 0-row Foldseek, Bio `Fixed and moving atom
lists differ in size` reproduced here, `-L`, Foldmason `structuremsa died` on one structure); `-a T` cannot be
combined with `-outfmt 2` (ran); version banner "checked on" lines.

### Missing referenced executables (FIX_BRIEF)

| named tool | choice | why |
| --- | --- | --- |
| DALI | wrote it (DaliLite block) | installed, public download, ran |
| GDT-TS | wrote it (`TMscore -seq`) | installed, ran |
| MUSTANG | wrote it (one command in the table row) | installed, ran |
| CE | pointed at PyMOL `cealign` | already in the Skill, runs headless |
| T-Coffee Expresso / 3D-Coffee | deleted | Expresso needs a BLAST server; 3D-Coffee cannot resolve templates offline in T-Coffee 12.00.7 (see above) |
| PROMALS3D, mTM-align | deleted | web servers |
| FATCAT | deleted | no CLI in any example, not installed |
| ChimeraX `matchmaker` | deleted | licence-gated download, not installed |
| TM-Vec, vcMSA, DEDAL, pLM-BLAST (and `fair-esm` install) | deleted | GPU and multi-GB weights, out of the tooling scope |

SKILL.md keeps one sentence ("Not covered, because no runnable path could be verified ...") so an agent does
not try them.

### Deleted passages and where the content lives

| deleted | now |
| --- | --- |
| usage-guide "Prerequisites" (conda line, downloads, `foldseek databases` for AFDB/`PDB100`, pip, pLM installs) | SKILL "Install" (corrected: no bioconda `tmalign`, `PDB` not `PDB100`); pLM installs deleted with the pLM claim |
| usage-guide "Quick Start" (4 prompts, all repeated in Example Prompts) | Example Prompts |
| usage-guide "What the Agent Will Do" (6 steps) | SKILL "When to Use", "Decision Tree by Goal", metric tables |
| usage-guide "Tips" (10 bullets) | each bullet already in SKILL (normalisation and RMSD in "Pairwise Structural Alignment Tool Selection", US-align/Foldseek-Multimer in the multimer section, DALI Z bands in the metric table, 3Di speedup in "Structural Search at Scale", predict-first in AlphaFold Integration / Decision Tree); the two facts found only there ("TM < 0.2 is random, not weak homology", "`align` for closer matches") were added to the TM-score table row and the PyMOL sentence |
| usage-guide prompts for PROMALS3D, T-Coffee Expresso, "improve my MSA with AlphaFold predictions", TM-Vec, pLM aligners | deleted with the claims above; "Twilight-Fold Homology" DALI prompt added |
| usage-guide overview mentions of PROMALS3D, T-Coffee Expresso, pLM aligners | deleted |
| SKILL "Hybrid Sequence-Structure Approaches" (T-Coffee Expresso, 3D-Coffee, PROMALS3D bullets, two `t_coffee` commands) | deleted; one "Not covered" sentence in the structural-MSA section; AlphaFold Integration step 4 now names Foldmason only |
| SKILL "pLM-Based Sequence Aligners" (table, "accuracy ceiling" paragraph) | deleted; row removed from the "< 15%" row and the Decision Tree |
| SKILL table rows for 3D-Coffee/Expresso, mTM-align, PROMALS3D, FATCAT | deleted (see Not-covered sentence) |
| SKILL ChimeraX bullet, command and sentence | deleted |
| SKILL threshold sentence "TM > 0.5 same fold ... < 0.2 random" inside the normalisation paragraph | kept once, in the "Metric / Threshold" table |
| SKILL "Pair RMSD with the atom count" and "-a T for the symmetrised average" repeats in the caveats paragraph | kept once in the normalisation paragraph |

Disagreement between copies: usage-guide named `PDB100` and bioconda `tmalign`; the runs support neither
(`foldseek databases` list, `libgfortran.so.3` failure), so SKILL's corrected form is the only copy.

### Findings left unfixed

- No Xu & Zhang 2010 p-value is computed: no shipped tool prints one and I could not verify the formula, so the
  SKILL says so instead of giving a number.
- T-Coffee Expresso/3D-Coffee are deleted, not repaired (see above): they need T-Coffee 13+ or network services
  that are not available here.
- Foldseek-Multimer literature claims (">99% chain-pairing match", "10-100x", "10^3-10^4x") and the DALI
  Foldseek-vs-DALI comparison table are unchanged and not checked by any run.
- ChimeraX and the pLM aligners were never executed (removed).
- Examples still hard-code placeholder file names (`reference.pdb`, `query.pdb`, `/path/to/afdb`); not a listed
  finding, left as is.

## 2026-09-21 - fix/alignment-structural-alignment (worktree `F:\OpenScience\wt\alignment-structural-alignment`, from staging main 431aa55)

Second pass, Sam's Production Ready batch: audit `eval_report_bio-alignment-structural_result.json` (4 P2, audited at
upstream d91ed3d). Commits `e33c5f3` (fix), `5388004` (split), `17418eb` (scripts/). Env `alignment`: WSL Foldseek
10.941cd33, Foldmason 4.dd3c235, TM-align 20240303, US-align 20241108, Biopython 1.88 (Windows venv for the
Superimposer runs, WSL env python for the rest). The audit's `data\` folder is gone, so runs use
`audit-envs\alignment\public-data\structures` (real PDB entries: 1MBN, 1A6M, 1A3N, 1ATP, 1HCK, ...).

### Findings

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| Inline Superimposer block has no name check; MSE/modified residues undocumented | P2 | inline block deleted (duplicated `examples/biopython_superimposer.py`, see scripts/ below); SKILL points at the example and states both refusals, and that HETATM MSE/modified residues are skipped by `id[0]==' '` (missing, not mis-paired); example docstring says the same, `__main__` reads paths from argv. Before that deletion the inline block got the residue-name check and was run | ran: inline block 1MBN/1A6M 0.483 A over 151 pairs, 1MBN/1A3N asserted (116/141 names differ), 1ATP/1HCK asserted (no shared key); example gives the same, refuses 1MBN/1A3N | did not accept `H_MSE` (audit's optional suggestion): would pair MSE to MET by key and the name check would then flag every one; the 1-4% figure is the audit's, not re-measured |
| Foldseek-Multimer 10-100x pairwise, >99% and PDB100/AFDB-Multimer claims unverified | P2 | table row, section intro and decision guide reworded: scale-only citation (3-4 orders of magnitude at database scale), no gain expected for one pair, the audit's measured 1.7x-5.8x on 62 small oligomers, prefilter reported 22 of 62 targets; PDB100/AFDB-Multimer dropped, target is a folder or a `createdb` of PDB entries, placeholder `afdb_multimer_or_pdb_dir` -> `complexes_dir/`; usage-guide prompt no longer names AFDB-Multimer | help: `foldseek databases` (10.941cd33) lists Alphafold/*, ESMAtlas30, PDB, CATH50, BFMD, BFVD, ProstT5 and no multimer or PDB100 entry | the 1.7x/5.8x timings are the audit's (one run), labelled as such; I did not re-time them |
| Foldmason unseeded variance figures set-specific | P2 | "74% shared / 88% homologous" replaced by "depends on the set: from under 1% to about 40% of aligned pairs differing" | ran: 3 unseeded `--refine-iters 100` runs on 12 real structures, pair-set overlap 0.80-0.88 of the union (12-20% differ), consistent with the range | range endpoints are the audit's (0.6% / 44%); my 12-structure set falls inside |
| Housekeeping: description "Predict"; Hamamsy 2024 reference; example placeholder names; foldseek_search prints parameter table; no references/ split | P2 | description now "Score and superpose"; Hamamsy reference deleted (its pLM section is gone); all four examples take paths from argv; `foldseek_search.py` passes `-v 1`; split done (below) | ran: `foldseek_search.py` on a 12-entry DB, type 2 (5 rows shown, no parameter table) and type 1 (15 confident of 17 rows); `tm_align_pairwise.py 1A3N 1MBN` TM 0.836/0.900, RMSD 1.56, 141 aligned; `foldmason_msa.py` on 3 files -> 3 rows x 153 cols, 153/153 columns scored; `foldseek -v 1` output byte-identical to default (`cmp`); all `py_compile` | |

### Split (own commit `5388004`)

SKILL.md 332 -> 286 lines (270 after the scripts/ commit). Verbatim moves; every non-blank old line is found in
SKILL.md + references/ except the 3 decision-tree rows that gained a pointer; fences balanced; moved bash fences
pass `bash -n`, the Foldmason python fence parses.

| moved | to |
| --- | --- |
| "Foldseek-Multimer for Database-Scale Complex Search" body (mode table, commands, `_report` columns, decision guide, reporting convention) | `references/foldseek-multimer.md` (SKILL keeps a 3-line summary) |
| "Local DALI with DaliLite v5" paragraph, `import.pl`/`dali.pl` block, result-file trap, checked Z-scores | `references/dalilite.md` (SKILL keeps one pointer sentence) |
| "Foldmason easy-msa" (command, seeding paragraph, per-column LDDT JSON snippet, `-1` note) | `references/foldmason.md` (SKILL keeps the command, the seed rule, the `scores` key) |

### scripts/ (own commit `17418eb`)

| old location | disposition |
| --- | --- |
| SKILL.md Bio.PDB.Superimposer inline block (21 lines) | duplicates `examples/biopython_superimposer.py`: deleted, SKILL points at the example (invocation + `superpose_ca` import). Ran as invoked: 1MBN/1A6M 0.483 A over 151 pairs; 1MBN/1A3N refuses |
| every other block (TMalign/USalign/TMscore/foldseek/foldmason/pymol commands, DaliLite 5-liner, Foldmason 5-line JSON reader) | 1-6 line commands or short fragments: left inline. No `scripts/` directory created |

### Redundancy

Already done 2026-09-20 (usage-guide is overview, prompts, related Skills). This pass added no repeated fact: the
Multimer speed evidence lives once in `references/foldseek-multimer.md`, the table row only cites the scale.

### Left unfixed

- Foldseek-Multimer ">99% chain-pairing match" is removed, not verified: I could not source it, so it is gone rather than kept.
- The audit's optional `H_MSE` acceptance in the Superimposer (see finding 1).
- Foldseek's "Removing temporary files" line still prints under `-v 1` (one line); no flag found to silence it.
