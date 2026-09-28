# Primary-source checks

- Sharp and Li's original CAI paper defines the score relative to a set of highly expressed genes and treats it as an index of codon-use adaptation, supporting the candidate's host-reference-relative interpretation: https://pmc.ncbi.nlm.nih.gov/articles/PMC340524/
- The Biopython 1.85 API and installed source define `CodonAdaptationIndex`, `calculate`, and `optimize`; the audit used the installed 1.85 implementation because the docstring's warning sentence does not match the observed `strict=False` path: https://biopython.org/docs/1.85/api/Bio.SeqUtils.html and https://github.com/biopython/biopython/blob/master/Bio/SeqUtils/__init__.py
- Wright's original Nc paper defines the 20-to-61 standard statistic from codon usage and describes it as independent of amino-acid composition, supporting the conclusion that the candidate's per-family sum is not interchangeable with standard Nc: https://pubmed.ncbi.nlm.nih.gov/2110097/
- dos Reis, Savva, and Wernisch introduced tAI as adaptation to the genomic tRNA pool, supporting the candidate's supply-side distinction while not certifying any particular downstream package: https://pmc.ncbi.nlm.nih.gov/articles/PMC521650/
- Tuller et al. report a low-efficiency region across approximately the first 30–50 codons and propose reduced ribosomal traffic as its function, supporting the candidate's cautious translation-ramp warning: https://pubmed.ncbi.nlm.nih.gov/20403328/

These source checks were used only to adjudicate scientific claims. Current Biopython behavior was established by exact local execution, not inferred from prose documentation.
