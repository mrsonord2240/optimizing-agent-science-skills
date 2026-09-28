# Scientific and interface source notes

This initial audit used the pinned fgbio 4.1.1 source and live help as the
interface authority, plus primary literature for the decision-rule check.

## fgbio interfaces

- `ExtractUmisFromBam` requires molecular-index tags associated with molecular
  segments; `--single-tag` can additionally concatenate multiple indices. The
  exact candidate recipe supplies two `M` segments and zero molecular-index
  tags. Official documentation:
  <https://fulcrumgenomics.github.io/fgbio/tools/latest/ExtractUmisFromBam.html>
- The fgbio best-practice alignment path converts uBAM to FASTQ, aligns, and
  uses `ZipperBams` to transfer metadata. It does not pass BAM bytes as a BWA
  sequence file:
  <https://github.com/fulcrumgenomics/fgbio/blob/main/docs/best-practice-consensus-pipeline.md>
- `FilterConsensusReads` requires queryname-sorted or query-grouped input and
  documents a streaming name-sort pattern. The candidate instead supplies a
  coordinate-sorted and indexed BAM:
  <https://fulcrumgenomics.github.io/fgbio/tools/latest/FilterConsensusReads.html>

## Biological and analytical claims

- Snyder et al. supports the 167 bp peak and about 10.4 bp periodicity, with
  library-preparation effects on observed ends (PMID 26771485; DOI
  10.1016/j.cell.2015.11.050).
- Underhill et al. supports shorter ctDNA distributions, including reported
  134–144 bp versus 167 bp and BRAF mutant 132–145 bp versus 165 bp examples
  (PMID 27428049; DOI 10.1371/journal.pgen.1006162).
- Mouliere et al. supports enrichment in the 90–150 bp window and the use of
  long-fragment features including 250–320 bp; it also demonstrates that size
  selection changes the population being analyzed (PMID 30404863; DOI
  10.1126/scitranslmed.aat4921).
- Kennedy et al. supports the high specificity attainable with duplex
  sequencing and detection beyond one mutant per 10^7 wild-type nucleotides
  (PMID 25299156; DOI 10.1038/nprot.2014.170).
- Newman et al. reports about threefold gains from molecular barcoding and
  about threefold from in-silico background suppression, about fifteenfold
  combined, and detection down to 4 in 10^5 molecules in that assay (PMID
  27018799; DOI 10.1038/nbt.3520). This is direct counterevidence to treating
  duplex as universally mandatory for every sub-0.1% or MRD use case: the
  appropriate conclusion is conditional on assay design and validation.
- Burnham et al. is bibliographically identifiable (PMID 27297799; DOI
  10.1038/srep27859), but the candidate should attach stable identifiers and
  exact source locations to the precise 10.7-fold and 71.3-fold enrichment
  values rather than leaving those values traceable only by author/year.

These sources support the general fragment-biology overview. They do not turn
illustrative thresholds or one assay's achieved sensitivity into a universal
preprocessing mandate.
