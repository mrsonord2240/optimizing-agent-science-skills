# Scientific and public-data source notes

- Candidate origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/allele-specific-accessibility`; canonical provider blobs were resolved from the clean pinned checkout.
- Mapping-bias correction implementation: WASP commit `d3b8447fd7719fffa00b856fd1f27c845554693e`.
- Joint-model implementation: RASQUAL commit `5aa553cf1b6501cf7ecd61a5efb34f7f20d354c6`.
- Public ATAC source: ENCODE `ENCFF415FEC`, experiment `ENCSR095QNB`, GM12878, bounded locally to chr1. ENCODE data use is unrestricted with citation requested.
- Public genotype source: IGSR/1000 Genomes phase 3 GRCh38-liftover NA12878 phased calls, bounded locally to chr1:1-30 Mb. The source has phased GT but no PS field.
- Reference source: UCSC hg38 chr1 sequence and a Bowtie2 index derived from it.
- The re-audit's successful end-to-end path used a clearly labeled bounded test derivative assigning constant `PS=1` over chr1:1-5 Mb because the source GT is chromosome-wide phased. The unmodified PS-free source was separately executed and required to fail closed. This test device is not a general phase-set inference method.
- The public path is an execution and contract test, not evidence for a biological discovery. Its one aggregate row was non-significant and is not presented as a validated regulatory association.
