# Scientific source checks

These checks are bounded corroboration for claims that materially affect the
audit findings. They are not a new literature review.

- Haploid genome mass: a peer-reviewed cfDNA QC paper uses approximately 303
  haploid genome equivalents per ng, consistent with 3.3 pg per haploid genome.
  The candidate intentionally computes with 330 but describes that as a
  "diploid-6.6 pg/rounding convention"; that explanation is dimensionally
  confusing and yields a roughly 9% difference from 303. Source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC7387491/
- CLSI-style limits: the Gaussian shortcut LoB = mean(blank) + 1.645 SD(blank)
  and LoD = LoB + 1.645 SD(low concentration) are supported, with the important
  caveat that EP17 contains finite-sample and nonparametric detail and expects
  replicate verification. Source:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2556583/
- iDES: Newman et al. support approximately 15-fold combined error suppression
  and ctDNA monitoring down to 4 in 100,000 cfDNA molecules; the candidate's
  numerical summary is broadly supported. Source:
  https://pubmed.ncbi.nlm.nih.gov/27018799/
- Duplex sequencing: Schmitt et al. report a theoretical background error rate
  below one artifactual mutation per billion nucleotides. Source:
  https://pubmed.ncbi.nlm.nih.gov/22853953/
- Reference materials: Fang et al. establish HCC1395/HCC1395BL tumor-normal
  reference call sets, while the SEQC2 Sample A/B/D/E and fragmented 130-170 bp
  liquid-biopsy materials are described in distinct SEQC2 work. The candidate
  collapses these into one "SEQC2 Sample A / HCC1395" recommendation under the
  Fang citation. Sources:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8532138/
  https://pmc.ncbi.nlm.nih.gov/articles/PMC9017191/
- The panel-integrated P0 finding does not depend on external interpretation:
  the shipped function's signature contains only input mass, VAF, number of
  loci, and the k-of-N threshold, and its per-locus probability is only a
  Poisson template-presence calculation. It has no recovery, consensus depth,
  locus-specific background, false-positive model, or empirically fitted
  detection process, yet labels the result `panel_integrated_lod95`.
