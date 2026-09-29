# Independent scientific source checks

These bounded checks test claims material to inherited findings and the final
readiness decision. They are not a new literature review.

- The 3.3 pg haploid-genome convention and 303 GE/ng conversion are supported
  directly in peer-reviewed cfDNA methods and quantification literature. The
  arithmetic in the candidate is exact under its stated convention.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8017778/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC7387491/
- Fang et al. identify HCC1395 as ATCC CRL-2324, HCC1395BL as ATCC CRL-2325,
  raw data as SRA SRP162370, and the somatic reference call set as v1.2. This
  supports the candidate's separation of the paired tumor-normal truth-set
  program from the Sample A/B program.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8532138/
- Jones et al. describe Sample A as pooled genomic DNA from ten cancer cell
  lines historically used for Agilent UHRR and Sample B as Agilent OneSeq Human
  Reference DNA 5190-8848. The candidate's revised sample identities are
  materially correct.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8051128/
  - https://link.springer.com/article/10.1186/s13059-021-02316-z
- The primary ctDNA proficiency methods describe Sample D and E before
  fragmentation, Df and Ef afterward, Pippin size selection from 110 to 190 bp,
  and an average fragment length of about 165 bp. The candidate's exact
  `130–170 bp` statement is directionally descriptive but not the preparation
  range reported by this cited method, so `ADV-006` is retained as P2.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8434938/
- The same ctDNA proficiency study shows why the candidate's interpretation
  boundary is necessary: low-VAF performance depends on input, recovery,
  fragment depth, assay workflow, and false positives, and contrived materials
  do not by themselves establish clinical thresholds.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8434938/

The panel-methodology decision did not require an external inference. The
shipped function uses only input mass, equal per-locus VAF, N, k, a GE
conversion, and an independent Poisson/binomial model. Because it contains no
empirical recovery, consensus-depth, background-error, false-positive, or
calling-rule measurements, its revised sampling-only lower-bound label is the
scientifically valid interpretation.
