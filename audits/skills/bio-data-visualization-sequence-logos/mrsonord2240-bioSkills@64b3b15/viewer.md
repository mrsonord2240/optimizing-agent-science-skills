> **Audit record for `bio-data-visualization-sequence-logos`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/sequence-logos) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-data-visualization-sequence-logos`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@64b3b15](https://github.com/mrsonord2240/bioSkills/tree/64b3b150c9b989c102f7ee69e0bb07c16842d894/data-visualization/sequence-logos) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval viewer: bio-data-visualization-sequence-logos

Source: `mrsonord2240/bioSkills@64b3b150c9b989c102f7ee69e0bb07c16842d894:data-visualization/sequence-logos` (unmodified upstream GPTomics/bioSkills).
Evaluated 2026-09-20, first audit, category Data Analysis, mode A, complexity Complex, N = 7 inputs, 7/7 executed.

**Final: 69, Beta Only, deployable = false, no veto, 1 open P0.** Static 71 (x0.4 = 28.4), execution average 67.6 (x0.6 = 40.6), assertions 21/35.

Environment: R 4.4.3 via `r.sh` (ggseqlogo 0.2.2, ggplot2 4.0.3); Windows venv (logomaker 0.8.7, pandas 3.0.6, numpy 2.5.3, matplotlib 3.11.2, weblogo 3.9.0); WSL `science` env `dv-cli` (WebLogo 3.7.12, Ghostscript 10.08, pdftoppm). All data are synthetic (seeded, `run/gen_data.py`) except the real JASPAR MA0106.3 TP53 PFM from `public-data`. Planted 10-position motif: pos 1 all A, 2 C 94%, 3 uniform, 4 G/T 50:50, 5 T 85%, 6 G 70%, 7 uniform, 8 A 70%, 9 all C, 10 A/G 40:40; n = 5, 20, 200, 2000 (DNA and RNA), a 500-sequence GC-rich set (bg .18/.32/.32/.18, planted G, C, A at positions 1, 2, 9), a 200-sequence protein 15-mer (S at 8, K/R at 5, LIVM at 9).

Ground truth: independent IC in numpy/base R: `log2(K) - H`, small-sample term `(K-1)/(2 ln2 n)`, relative entropy `sum p log2(p/q)` for a background `q`. Judged on numbers read from the figures' own data (`p$layers[[1]]$data`, `logo.df`, WebLogo `logodata`) and by opening the PNG/PDFs.

## Headline findings

1. **P0: `ggseqlogo(..., bg_freq = ...)` does nothing.** SKILL.md (twice), usage-guide.md and the shipped example use it; ggseqlogo 0.2.2 has no such argument (ggplot2 prints `Ignoring unknown parameters: bg_freq`), heights are byte-identical with and without it (max diff 0), and the example titles the uncorrected figure "human bg". A fully conserved C column should read 2.252 bits vs a human background and reads 2.000.
2. Logomaker `background=` and WebLogo `--composition` do work (relative entropy matches the independent value: 1.644/1.644/2.474 for the planted GC-rich columns).
3. Three tools, three small-sample treatments: one fully conserved n=5 column = 1.567 bits (ggseqlogo sequences, Schneider e_n), 0.553 (Logomaker default pseudocount=1), 1.136 (WebLogo default Dirichlet prior), 2.000 (ggseqlogo counts matrix, no correction). The Skill names Schneider 1986 as the standard and never says which route applies it.
4. The Skill states the uniform-background bias backwards: a fully conserved G in a GC-poor genome (q_G = 0.21) reads 2.000 uniform vs 2.252 corrected (uniform under-estimates); a fully conserved A (q_A = 0.29) 2.000 vs 1.786 (over-estimates).
5. Logomaker SKILL block: `fig, ax = plt.subplots(...)` is never passed as `ax=`, so a blank figure stays open and figsize is ignored (opened: blank axes); its all-A 10-count column reads 0.911 bits because `transform_matrix` defaults to `pseudocount=1`.
6. Shipped example cannot run as shipped (`aligned_motif.fa` missing, `ctcf_seqs`, `rest_seqs`, `gata1_seqs` undefined).

## Inputs

| # | Type | What | Basic /40 | Special /60 | Total | Assertions |
|---|---|---|---|---|---|---|
| 1 | Canonical | ggseqlogo blocks + planted motif n=5/20/200/2000 + JASPAR + probability | 32 | 48 | 80 | 4/5 |
| 2 | Variant A | Logomaker blocks, IC, background, alphabets | 27 | 40 | 67 | 3/5 |
| 3 | Variant B | WebLogo CLI (WSL) + Windows pip weblogo | 32 | 47 | 79 | 4/5 |
| 4 | Edge | small-sample correction across the three tools | 26 | 36 | 62 | 3/5 |
| 5 | Edge | RNA / protein / custom scheme / malformed input | 30 | 44 | 74 | 3/5 |
| 6 | Adversarial | GC-rich background request across tools | 20 | 29 | 49 | 2/5 |
| 7 | Stress | shipped example end-to-end | 26 | 36 | 62 | 2/5 |

### 1. ggseqlogo (`run/i1_ggseqlogo.R`, `logs/i1_ggseqlogo.out`)

SKILL.md block 1 run verbatim (`seqs_a`/`seqs_b` undefined in the Skill: substituted). Key printed output:

```
ASSERT block1 seqs n=5: column tops == independent IC with e_n     PASS gg=1.567,0.845,1.567,1.567,1.567,0 ind=1.567,0.845,1.567,1.567,1.567,0
ASSERT block1 PWM (prob): column tops == 2 - H (no small-sample term) PASS gg=0.6432,0.6432,0.2781
bg_freq build/print warnings: Ignoring unknown parameters: `bg_freq`
ASSERT bg_freq=human_bg changes heights vs no bg_freq   FAIL max |diff| = 0
ASSERT bg_freq is a formal argument of ggseqlogo()/geom_logo()   FAIL
planted fully-C pos 9: uniform IC = 2  human-bg IC = 2.252
n=5    IC gg : 1.567 1.567 0.045 0.845 0.845 0.596 0 0.196 1.567 0.045     (uncorrected 2 2 0.478 1.278 1.278 1.029 0.078 0.629 2 0.478)
ASSERT n=5: sequence and counts routes give the same height  FAIL  (seq minus counts matrix = -0.433 in every column)
ASSERT JASPAR TP53 (18 cols): tops == 2 - H  PASS max IC 1.996 at col 13;  consensus AACATGCCCGGGCATGTC
RNA auto: letters ACGU  PASS;  unequal-length input: ERROR: Sequences in alignment must have identical lengths
n=1 input warnings: All positions have zero information content ... Setting all information content to 2.
protein n=200 pos8 4.253 (max log2 20 = 4.322), dominant S at position 8  PASS
```

Column IC equals the independent computation at n = 5, 20, 2000 to 2e-16; at n = 200 only the columns whose IC is below the 0.4% stack pad (0.002 bits) are not drawn. Images opened: `run/out/r_dna_n200.png` (A C - G/T T G - A C G at the right heights), `r_jaspar_TP53_bits.png` (p53 half-site pattern), `r_protein_custom_scheme.png` (S dominant at 8, K/R at 5, V/M/L/I at 9), `r_block1_multi.png`.

### 2. Logomaker (`run/i3_logomaker.py`, `logs/i3_logomaker.out`)

```
ASSERT information df column-sum == independent IC with pseudocount=1 default  PASS lm=[0.911 0.57 0.408 0.516]
ASSERT information df row-sum == plain IC (log2 4 - H) with NO pseudocount   FAIL plain IC=[2. 1.278 1. 1.078]
ASSERT SKILL block draws the logo on the fig it created (ax=ax passed)        FAIL
ASSERT bg=GC-rich IC == independent relative entropy sum p log2(p/q)         PASS [1.644 1.644 ... 2.474]
ASSERT n=5 Logomaker applies Schneider small-sample correction                FAIL max |lm - corrected| = 0.433
Logo(matrix_type='counts') -> TypeError Glyph.__init__() got an unexpected keyword argument 'matrix_type'
ASSERT JASPAR TP53 IC ~= 2-H within pseudocount effect  PASS max diff 0.0021; consensus AACATGCCCGGGCATGTC
```

`Arial Rounded MT Bold` is not installed: 32 `findfont` warnings, silent fallback. Opened `py_block_information.png` (logo rendered when `logo.fig` is saved) and `py_block_information_fig_as_written_BLANK.png` (the figure the SKILL code creates: empty axes).

### 3. WebLogo (`run/i4_weblogo.sh`, `i4b_weblogo_extra.sh`, `i4c_weblogo_check.py`, `i5_weblogo_win.sh`)

SKILL command verbatim in WSL: exit 0, pdf 6,018 B; png 8,260 B; png_print 18,301 B; svg 39,832 B; eps 18,168 B; jpeg 10,502 B. `--weight 0` heights equal the independent uncorrected IC to 1e-4 at every n. Under the default weight WebLogo uses a Dirichlet prior (`weight x composition`), n=5 column 1.136 vs Schneider 1.567; `--composition` explicit dict on the GC-rich set gives 1.617/1.617/2.438 vs ideal 1.644/1.644/2.474 and `'H. sapiens'` works (species `S. coelicolor` is not accepted). Opened `out/wl/logo_n200.png`, `logo_n5.png`, `logo_gc500_equi.png`. Windows pip weblogo 3.9.0: `pdf`, `png`, `svg` exit 1 `Could not find Ghostscript` (only eps and logodata work); the Skill does not list Ghostscript.

Extra: `--sequence-type dna` (as hard-coded in the Skill's command) on RNA input silently drops U: position 4 counted 103 of 200 sequences, IC 1.884 vs 0.964 bits with `--sequence-type rna`.

### 4. Small-sample (edge)

See headline 3. Random n=5 columns average 0.546 raw bits (first-order e_n = 0.433 slightly under-corrects). ggseqlogo clamps corrected IC at 0 and does not draw columns below its stack pad.

### 5. Alphabets and malformed input

RNA identical to DNA in all three tools once declared; ggseqlogo also auto-detects U. The Skill's Common Errors row "RNA U renders as box" did not reproduce. Protein: ggseqlogo pos 8 4.253 bits (e_n at K = 20), Logomaker/WebLogo 4.322. `t(pwm)` without rownames: `Matrix must have letters for row names`. Logomaker transposed df: `ValueError invalid literal for int() with base 10: 'A'`. WebLogo unequal length: exit 2 with a clear message.

### 6. Adversarial: GC-rich background

Figure claims background correction the tool did not apply (input 1 numbers above); the Skill's own bias-direction sentences are reversed (headline 4).

### 7. Shipped example (`run/i2_example.sh`, `i2b_pdf2png.sh`)

```
== (a) as shipped, no inputs ==  Error in file(con, "r") : cannot open file 'aligned_motif.fa'
== (b1) with FASTA inputs but without ctcf_seqs ==  Error: object 'ctcf_seqs' not found
== (b2) all inputs supplied ==  3 x "Ignoring unknown parameters: `bg_freq`"; logo_comparison.pdf 45 KB, multi_logo.pdf 44 KB, protein_logo.pdf 23 KB
```

Opened the rendered pages (`run/out/ex/*.png`): letters correct, order correct, palette applied, but the top panel title reads "Motif logo (bits; N = 200; human bg)" over uniform-background heights.

## Static score (71/100)

| Category | Score | Note |
|---|---|---|
| Functional suitability | 7/12 | ggseqlogo background parameter does not exist; bias direction reversed |
| Reliability | 8/12 | transposed/unequal-length modes accurate; RNA-box mode stale; n=1 fallback missing |
| Performance and context | 6/8 | 278-line SKILL.md + 86-line guide that repeats it |
| Agent usability | 10/16 | placeholders (`seqs_a`, `genome_composition`, `protein_pwm`); silent wrong result |
| Human usability | 6/8 | vague orientation tip |
| Security | 11/12 | nothing risky |
| Maintainability | 8/12 | version stamp cannot be true for `bg_freq`; Streptomyces composition = 64% GC, not about 72% |
| Agent-specific | 15/20 | good trigger; description promises the failing feature; all Related Skills exist |

## Vetoes

Skill veto: all PASS. Research veto: PASS on all four (methodology is principled and works on two routes; the nonexistent argument is recorded as P0, not a fabrication). Shipped-means-present (gate 8): `examples/seqlogo_phd.R` present; the five Related Skills exist at this commit; the example's own input FASTAs are not shipped (P1).

## Recommendations

- **P0** `bg_freq` does not exist in ggseqlogo; remove it, use `method = 'custom'` with relative-entropy heights or Logomaker/WebLogo, and stop labelling figures "human bg" unless applied.
- **P1** Correct the direction of the uniform-background bias and the Streptomyces figures.
- **P1** Document, per tool, what "small-sample correction" the default performs (ggseqlogo sequences: Schneider e_n; ggseqlogo matrix: none; Logomaker: pseudocount 1; WebLogo: prior weight).
- **P1** Fix the Logomaker block (`ax=ax`, state the pseudocount default, font).
- **P1** Make the example runnable (ship a planted FASTA, define the three motif sets, derive N and the background label from the data).
- **P2** Remove `matrix_type='counts'` and the stale RNA-box row; correct the ggseqlogo orientation comment; do not equate Logomaker weights with EDLogo.
- **P2** Warn on n < 5 (fabricated 2 bits), tell RNA users to pass `--sequence-type rna`, list Ghostscript.

## Files

Scripts in `run/`: `gen_data.py`, `common.py`, `i0*_src.R/.py` (source inspection of ggseqlogo and Logomaker), `i1_ggseqlogo.R`, `i2_example.sh`, `i2b_pdf2png.sh`, `i3_logomaker.py`, `i4_weblogo.sh`, `i4b_weblogo_extra.sh`, `i4c_weblogo_check.py`, `i5_weblogo_win.sh`, `finalize_report.py`; logs in `run/logs/`; figures in `run/out/`; data in `run/data/`. `run/scratch_ex/b` is an empty directory that Windows would not let me remove (a handle held by a stopped task).
