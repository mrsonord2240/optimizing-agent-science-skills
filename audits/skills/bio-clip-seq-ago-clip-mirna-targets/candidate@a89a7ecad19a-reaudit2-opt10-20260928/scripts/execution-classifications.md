# Execution classifications

Audit date: 2026-09-28  
Candidate identity: `a89a7ecad19a3cc207ab6b82bc0910b126b663e32e7c74c3c2b74dc105d780fa`

| Surface | Classification | Evidence and result |
|---|---|---|
| Shipped `tests/test_scripts.py` | `executed` | 6/6 pass; stdout/stderr captured in `evidence/shipped-tests.*`. |
| Independent parser and wrapper controls | `executed` | 9/9 pass, including orientation, expression schema, reason codes, path quoting, overwrite refusal, status propagation, failed replacement preservation, and stage cleanup; `evidence/contract-results.json`. |
| Pinned Hyb end-to-end wrapper | `executed` | Two fresh complete two-replicate workflows using official test reads and hOH7 at commit `028ab6371ce793ca5e86f475fce1f2cc6ad3c677`; four raw outputs each 111 rows x 16 fields. Both runs accepted 111, excluded 0; structured outputs and all non-stdout files matched. |
| Hyb stdout logs | `executed` with retained limitation | Each replicate's stdout differs only in its first wall-clock timestamp line; subsequent lines are byte-identical. Overall stdout files are not byte-identical. |
| Per-read assignment support | `executed` | All 111 rows show the same assignment in 2/2 replicates, support indices `1,2`, and accepted=true. |
| Targeted-miR-eCLIP UMI extractor | `executed` | Synthetic declared 9-nt and 10-nt successes; missing length, zero, non-integer, blank library, blank protocol, and too-short R2 fail closed with no output files (8/8 checks). |
| Expression threshold and provenance | `executed; failed` | A synthetic NaN measurement with threshold 100 exited zero and was accepted as a consensus row. This is open finding AGO-009 and fails the Research Veto methodological-ground gate. |
| TargetScan UTR-to-genome conversion | `executed` | Plus/minus multi-exon fixtures converted to BED12; `bedtools intersect -split -s` retained only matching-strand peaks; release mismatch and out-of-range site failed closed. |
| Yeo total-route UMI extraction and paired trimming | `executed` on synthetic fixture | UMI-tools extracted the 10-nt read-1 prefix; cutadapt removed fixture adapters and retained paired 20-nt inserts. This does not represent the full biological workflow. |
| Soft-clipped BAM diagnostic | `executed` on synthetic fixture | samtools/awk counted one `5M5S` record and excluded a `10M` control. The Skill explicitly says this is not a chimera call. |
| Full Yeo chimeric-eCLIP | `blocked` / resource deferred | No real library or species-matched repeat/genome STAR indices were available. User action: provide those inputs, confirm protocol layout, and run the pinned CWL route. |
| HEAP wet-lab reproduction | `blocked` / biological route unavailable | Requires Halo-Ago2 experimental material. User action: scope and provide the biological experiment. |
| DIANA microT-CDS example endpoint | `blocked` / remote unavailable | Previous bounded documented request returned HTTP 500; not credited as executed. User action: retry after service recovery or choose a versioned prediction file. |
| AGO peak-calling workflow | `static-only` | No peak caller is shipped; workflow and evidence boundaries are documented. |
| miRDB prediction service/download and other authenticated or paid services | `static-only` | Access and interpretation statements were inspected; no private credentials or gated access were used. |

No dependencies were installed. No R, notebook, model, GPU, GUI/native app, or bundled compiled tool is shipped.
