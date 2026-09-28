# Scientific source notes

- Brnich et al. 2020 primary open article, Table 3: <https://pmc.ncbi.nlm.nih.gov/articles/PMC6938631/>. It states `<0.053` BS3, `<0.23` moderate, `<0.48` supporting, `0.48-2.1` indeterminate, and `>2.1`, `>4.3`, `>18.7`, `>350` pathogenic Supporting through Very Strong. Candidate code and table match; one explanatory sentence does not.
- Bergquist et al. 2025, *Genetics in Medicine* 27:101402, PMID 40084623, DOI 10.1016/j.gim.2025.101402: <https://pubmed.ncbi.nlm.nih.gov/40084623/> and author-hosted paper <https://ccs.neu.edu/home/radivojac/papers/bergquist_genetmed_2025.pdf>. Candidate AlphaMissense bands and explicit -3/+3 point labels match the table.
- ClinGen SVI current guidance index (updated July 2025): <https://www.clinicalgenome.org/tools/clingen-variant-classification-guidance/>. It points to the PP5/BP6 reputable-source recommendation.
- Biesecker and Harrison 2018, ClinGen SVI, PMID 29543229: <https://pmc.ncbi.nlm.nih.gov/articles/PMC6709533/>. PP5/BP6 rely on assertions not linked to primary evidence and risk double counting; the current ClinGen VCEP SOP states they should not be applied in any context. The candidate still accepts both.
- ClinGen Variant Curation SOP v1: <https://www.clinicalgenome.org/site/assets/files/3677/clingen_variant-curation_sopv1.pdf>. The reputable-source section says PP5/BP6 should not be applied and are disabled in the VCI.
- ClinGen SVI splicing guidance: <https://pmc.ncbi.nlm.nih.gov/articles/PMC9980257/>. Canonical splice PVS1 strength depends on predicted/observed transcript consequence and review of rescue mechanisms. The new stop states pass, but contradictory NMD representations are not reconciled.
- GeneBe official API documentation: <https://docs.genebe.net/docs/api/overview/>. The current single-variant GET uses `chr`, `pos`, `ref`, `alt`, and `genome`; candidate live execution passed.
- ClinGen CSpec current read-only service was verified at <https://cspec.genome.network/cspec/srvc> and the GATM version route on 2026-09-28; candidate live execution returned six version records.

The live inputs were public documentation examples and a public gene symbol. No patient, private, authenticated, proprietary, or protected-health data was used.
