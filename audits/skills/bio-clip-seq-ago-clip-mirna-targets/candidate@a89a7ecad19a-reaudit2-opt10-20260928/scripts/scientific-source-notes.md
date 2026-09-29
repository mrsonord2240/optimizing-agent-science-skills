# Scientific source review

The normalized Skill’s key methodological distinctions were checked against primary or authoritative sources:

- The official [TargetScan Release 8 FAQ](https://www.targetscan.org/faqs.Release_8.html) states that site start/end coordinates are calculated from spliced 3′ UTRs, excluding introns. That supports the candidate’s requirement to project UTR-relative sites through a version-matched transcript map before genomic intersection.
- The official [TargetScan seed definition](https://www.targetscan.org/docs/seed.html) defines the seed as mature-miRNA positions 2–7 and family identity by positions 2–8. The skill’s separation of canonical seed classes and weaker 6mer evidence is consistent with this basis.
- The primary [CLEAR-CLIP study](https://www.nature.com/articles/ncomms9864) describes an AGO HITS-CLIP modification that generates miRNA-target chimeras and enables explicit biochemical identification of miRNA sites. This supports distinguishing direct chimera evidence from computational assignment of standard AGO-bound peaks.

The execution evidence does not establish biological validation of the official test-read interactions, functional repression, binding affinity, or generalization to a real library. The skill correctly labels read counts as recovery support, retains non-canonical direct chimera evidence, and defers full biological and remote workflows where inputs or service availability are missing.

The new finding concerns software handling of expression values, not the source literature: IEEE non-finite `NaN` is accepted as if it met a numeric abundance threshold, bypassing the intended matched-expression filter.
