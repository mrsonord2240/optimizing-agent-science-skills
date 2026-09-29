# Scientific source notes — bio-codon-usage final re-audit

- Live behavior was adjudicated against the pinned Biopython 1.85 installation, not against prose alone. The public API contract for `CodonAdaptationIndex(sequences, table=...)`, `calculate`, and `optimize` is documented at <https://biopython.org/docs/1.82/api/Bio.SeqUtils.html>; exact 1.85 edge behavior is retained in `reaudit-results.json`.
- NCBI genetic-code table 2 lists TGA/TGG as tryptophan and AGA/AGG as stops in the vertebrate-mitochondrial code: <https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi?chapter=tgencodes>. The four executable cases matched those codon meanings and preserved `MW*`.
- Wright's original Nc paper identifies the effective number of codons as a reference-free codon-usage measure with the conventional 20-to-61 interpretation: PMID 2110097, DOI 10.1016/0378-1119(90)90491-9, <https://pubmed.ncbi.nlm.nih.gov/2110097/>.
- The CodonW project documents Nc among its standard codon-usage indices: <https://codonw.sourceforge.net/>. Fresh local codonW 1.4.4 controls were used only to test the candidate's non-implementation boundary.
- Public `thrA` sequence provenance, feature response, retrieval date, and checksum remain in `F:\OpenScience\audit-envs\bio-codon-usage\fixtures\PROVENANCE.md`. It was used as a mechanics control, not as a highly expressed CAI reference set.

No network-dependent result is required to reproduce the candidate's executable verdict; the cited pages anchor terminology and biological code assignments.
