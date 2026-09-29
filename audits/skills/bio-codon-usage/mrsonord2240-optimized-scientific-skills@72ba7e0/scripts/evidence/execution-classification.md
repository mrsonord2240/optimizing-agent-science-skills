# Execution classification — bio-codon-usage final re-audit

The rubric's structural pre-check passed all four skill veto dimensions and
classified complexity as Moderate / Mode B. Its keyword-only category helper
returned `Other` because none of its narrow category keywords appear in the
frontmatter; the independent auditor overrode that heuristic to `Data
Analysis` because the promised and executed work is codon-counting,
bioinformatics metric calculation, validation, and sequence optimization.

| Surface | Classification | Independent evidence |
|---|---|---|
| `scripts/basic_analysis.py` | Executed | Two exit-zero runs, empty stderr, byte-identical stdout; counts, frequencies, GC123, and amino-acid usage printed from a validated CDS. |
| `scripts/rscu_analysis.py` | Executed | Two exit-zero runs, empty stderr, byte-identical stdout; RSCU was computed from shared validated state. |
| `scripts/cai_optimization.py` | Executed | Two exit-zero runs, empty stderr, byte-identical stdout; optimized CAI was 1.000 and `MAALDDKG*` was preserved. |
| `scripts/codon_utils.py` | Executed | Strict/permissive validation, counts, frequencies, CAI guards, table mismatch, and standard/table-2 optimization were directly exercised. |
| `tests/test_codon_usage.py` | Executed | Twelve tests passed on each of two independent invocations; normalized case/outcome streams matched. |
| Biopython 1.85 CAI behavior | Executed | Indexed stop contribution, GCC pseudocount normalization to 0.05, silent `strict=False`, rejecting `strict=True`, and guarded excluded-only queries were directly observed. |
| Table-2 genetic-code route | Executed | All four TGA/TGG x AGA/AGG cases validated and optimized to a sequence translating as `MW*` under table 2. |
| Public table-11 `thrA` | Executed | The 2,463-nt / 821-codon CDS validated as ATG...TGA with no discards; counts, frequencies, RSCU, and GC123 ran from that exact state. |
| codonW external Nc control | Executed external comparator | Fresh codonW 1.4.4 invocations reproduced Nc 30.77 and 47.41 for the bounded fixtures. This does not make Nc a candidate capability. |
| Nc inside candidate | Documented external boundary | No candidate implementation or trigger claim exists. The references require a separately validated Wright/codonW-compatible estimator and forbid cross-study use of the removed approximation. |
| tAI, RNA-structure, translation-ramp, cryptic-element, and codon-pair screening | Documented-only | The candidate explicitly names these as downstream or external analyses and does not claim to execute them. |

No runnable candidate surface was blocked, simulated, or scored from documentation alone.
