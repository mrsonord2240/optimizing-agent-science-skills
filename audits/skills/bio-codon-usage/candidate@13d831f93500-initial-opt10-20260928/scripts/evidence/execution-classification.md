# Execution classification

| Surface | Classification | Audit evidence |
|---|---|---|
| `scripts/basic_analysis.py` | executed | Two exact standalone runs plus imported-helper boundary matrix. |
| `scripts/rscu_analysis.py` | executed | Two exact standalone runs plus standard/table-aware and malformed-input probes. |
| `scripts/cai_optimization.py` | executed | Two exact standalone runs; standard protein assertion reproduced. |
| Biopython 1.85 CAI API | executed | Stops, pseudocount normalization, ties, empty/excluded-only inputs, partial input, table 2, and protein preservation. |
| Documented simplified Nc helper | executed | Exact fenced helper on heterogeneous and public `thrA` fixtures. |
| codonW comparator | executed | codonW 1.4.4 on the same two exact sequences. |
| tAI | documented-only | No implementation is shipped; primary-source interpretation only. |
| RNA structure, regulatory-element, restriction-site, codon-pair, and synthesis screens | documented-only | Correctly described as required downstream screens; no implementation is shipped and no readiness credit was assigned. |

Restricted-access surfaces: none. Blocked surfaces: none. Documented-only surfaces cannot support final execution readiness.
