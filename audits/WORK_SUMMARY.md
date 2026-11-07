# Scientific Skill audit work — retired

- Sam ended the effort on 2026-11-07 after reporting no further Open Science engagement and no repository activity. He requested prose-only bullet accounts and deletion of detailed logs and outputs.
- The accounts below condense the recorded audit and fix work. They are historical descriptions, not newly executed tests or current certifications.
- The original scientific Skills were authored by GPTomics under MIT; the audit method was derived from AIPOCH’s MIT-licensed skill-auditor. Sam commissioned the refinement work.
- Detailed reports, viewers, assertions, run scripts, raw inputs and outputs, and duplicate evidence archives were retired. Ordinary Git history is not rewritten by this cleanup.

## bio-admet-prediction

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included Triage 300 real compounds with the Skill's own druglike_score and alerts snippets; The ADMETlab 3.0 route -- the Skill's declared primary tool; The in-house chemprop D-MPNN route for a custom endpoint; The hERG endpoint checked against 300 measured ChEMBL IC50 values.
- Fix work addressed these recorded problems: No executable ADMET prediction route; ADMETlab was declared primary but shipped no request; Runnable OOD mitigation unavailable; offline point predictions included salts/metals without a signal; Chemprop reproducibility advice used invalid --seed.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-alignment-amplicon-clipping

- Recorded 3 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included Real ARTIC v5.3.2 nanopore BAM: Skill workflow verbatim, mode table and iVar block re-measured; Synthetic 800-read paired-end panel with planted SNPs under primers: three example modes + planted truth; Strand/both-ends outcome table, BED formats and --tolerance semantics (synthetic single reads); Hard-clip archive copy, iVar block, consensus, removed-claim and pointer checks.
- Fix work addressed these recorded problems: Example exits 0 on contig mismatch and wrong reference; "--both-ends overrides --strand" false; "forgot --strand" diagnosis inverted; ARTIC/long-read --strand leaves 3' primer in 97.5% of reads.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-alignment-filtering

- Recorded 3 audit versions between 2026-09-20 and 2026-09-23.
- Recorded exercises included High-quality primary BAM filtering and duplicate prerequisite; Exhaustive FLAG filtering; BED and region parsing; Seeded subsampling and target matching.
- Fix work addressed these recorded problems: -n (--exclude-no-read-group) is 1.23, not 1.24; Somatic-row rationale contradicted by a real Mutect2 run; pysam BED recipe not equal to -L on zero-width/space rows.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-alignment-indexing

- Recorded 3 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included Archived regression: BAI/CSI indexing, regions, idxstats and shipped Python snippets; Archived regression: CRAM reference, REF_PATH, idxstats and faidx; Archived regression: unsorted BAMs, missing indices, contig names and parser boundaries; Archived regression: large-contig BAI/CSI boundaries and BAM position limits.
- Fix work addressed these recorded problems: Staleness snippet and batch loop break for CSI-indexed BAMs; CRAM: no reference guidance, pysam idxstats silently 0, helpers ignore .crai; Large-genome section wrong in four places.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-alignment-io

- Recorded 4 audit versions between 2026-09-19 and 2026-09-24.
- Recorded exercises included Shipped examples from a clean copy, round-2 inference/override/cwd targets (regression); Stockholm: real Pfam + real Rfam RF00005 (954x118) + synthetic RNA, annotations, NEXUS, Infernal/HMMER…; PHYLIP pitfalls, every plain SKILL code block verbatim (incl. Batch, MrBayes recipe, pyhmmer streaming),…; MAF minus-strand helper on real UCSC MAF with UCSC-API ground truth; real hmmalign A2M and HH-suite A3M….
- Fix work addressed these recorded problems: MAF helper wrong for minus strand (66 vs 60); convert_formats.py ValueError at NEXUS write, 0-byte file; slice_alignment.py / convert_formats.py need unshipped alignment.aln; slice writes 0-column FASTA.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-alignment-msa-parsing

- Recorded 3 audit versions between 2026-09-19 and 2026-09-22.
- Recorded exercises included Pfam globin seed: IDs, conserved columns, gaps, consensus (real data); Clean: gappy columns, gappy/duplicate sequences, ID filter, save; Messy files: all-gap column, single sequence, ragged, A2M '.' gaps, A3M; Map proximal His of myoglobin (PDB 1MBN) to an alignment column.
- Fix work addressed these recorded problems: Gap symbol hard-coded to -; . and lowercase break helpers silently; mi_apc.py ignores APC guard; noise on the seed; thresholds disagree (0.5 vs 1); Protein consensus default N is asparagine.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-alignment-msa-statistics

- Recorded 3 audit versions between 2026-09-20 and 2026-09-22.
- Recorded exercises included Pfam PF00042 seed (real, 73x141): identity matrix, conservation, entropy/IC, gaps, SP, PSSM, JSD; Real tool output: MAFFT/Clustal Omega (upper), hmmalign AFA (lowercase inserts + dots), Pfam seed with "."…; Hand-computed 3x8 protein alignment with terminal gaps, an internal gap, ambiguity and a gap-only column…; Six real mammalian HBB CDS aligned with MAFFT --auto (nucleotide output is lowercase): Ti/Tv, DNA IC, PSSM,….
- Fix work addressed these recorded problems: No case / gap-glyph / ambiguity normalisation; PID1 code contradicts its definition; alignment_score charges gap/gap pairs.
- The published source version recorded 97/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-alignment-multiple

- Recorded 2 audit versions between 2026-09-11 and 2026-09-24.
- Recorded exercises included 15 proteins, most accurate MSA for phylogeny + reliability check; 10 CDS -> codon alignment for codeml; 13 contigs: 3 reverse-strand, 1 non-homologous; Is the column holding P01 residue 142 stable?.
- Fix work addressed these recorded problems: Fix MUSCLE5 ensemble commands (-super5 has no .efa); Correct the mafft --auto strategy table; Add homology/strand pre-flight and note _R_ renaming.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-alignment-pairwise

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Real human HBA vs HBB global BLOSUM62 alignment, cross-checked against 4 tools; Local DNA alignment of a real 150-nt HBB segment planted in synthetic 1.15 kb sequence; Semiglobal fragment-in-reference, length mismatch, off-spec residues; Empirical significance of real protein pairs with the shipped empirical_pvalue.py.
- Fix work addressed these recorded problems: aligner.max_alignments raises AttributeError; "Default gaps are 0" false; "BLASTP defaults -11/-1" off by one.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-alignment-sorting

- Recorded 3 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included Coordinate-sort, index, and CRAM conversion of shuffled real BAMs; Natural versus ASCII queryname order and duplicate marking; Tag, template-coordinate, malformed, and mislabeled alignments; Merge lanes, read groups, and name-sorted inputs.
- Fix work addressed these recorded problems: sort -n documented as lexicographic; -N never mentioned; Picard crashes on -n; Example needs undocumented bwa index; exits 0 on mid-stream aligner failure; "Trust the @HD header / authoritative"; ensure_coordinate_sorted returns a mislabelled BAM; awk check misses contig-order violations.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-alignment-structural

- Recorded 3 audit versions between 2026-09-20 and 2026-09-23.
- Recorded exercises included Pairwise globin superposition; Foldseek local structural search; Known correspondence and offset refusal; Seeded Foldmason structural MSA.
- Fix work addressed these recorded problems: Foldmason example not reproducible (no --refine-seed); Foldseek-Multimer commands wrong or lossy; -mm 4 -byresi 0 remedy wrong.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-alignment-trimming

- Recorded 3 audit versions between 2026-09-15 and 2026-09-24.
- Recorded exercises included Single 15-taxon protein gene: smart-gap, --log, sensitivity trees; 20-locus DNA supermatrix: kpic-smart-gap, BMGE, PHYLIP output; Unbalanced 30 ingroup + 3 outgroups: kpic failure mode; HMM prep: trimAl -gappyout, -colnumbering, reproducibility.
- Fix work addressed these recorded problems: Default kpic-smart-gap breaks own 40%/0.7 rule; distorts outgroup branch lengths; kpi inflates lengths; Inconsistent 20%/20-30%/40%/0.7 thresholds; --output-format.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-alignment-validation

- Recorded 3 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included Primary paired-end BAM validation; Archived defect-fixture regression set; Fresh tiny, no-SQ, and unreadable-CRAM inputs; Same-RG fingerprint collision.
- Fix work addressed these recorded problems: CrosscheckFingerprints misses a mismatch when BAMs share RG ID/PU; Picard chart options require R; Shell validator reports an unreadable CRAM as a QC fail.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-analytical-validation

- Recorded 3 audit versions between 2026-09-28 and 2026-09-28.
- Recorded exercises included Single-locus Poisson sampling calculation; Blank plus public aggregate LoD95 fit; Invalid physical and statistical inputs; Panel-integrated LoD resolution and monotonicity.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-atac-seq-allele-specific-accessibility

- Recorded 4 audit versions between 2026-09-28 and 2026-09-28.
- Recorded exercises included Real single-sample WASP-to-GATK core stages; Peak aggregation and empty-result boundaries; Multi-sample genotype and sample-identity boundary; Public RASQUAL feature analysis.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-atac-seq-atac-peak-calling

- Recorded 5 audit versions between 2026-09-30 and 2026-09-30.
- Recorded exercises included ENCODE-style script on GM12878 rep1/rep2 chr1:1-30Mb (passing library, MACS3, bigWig); Genuinely failing library (rep2 = 6% subsample), ratio-logic unit cases, MACS=macs2 mode; Documented Genrich joint and macs3 hmmratac commands on GM12878; Input guards, chrM guard on a synthetic BAM, idxstats chrM-removal recipe and its -f 2 orphan follow-up.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 88/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-atac-seq-atac-qc

- Recorded 5 audit versions between 2026-09-30 and 2026-09-30.
- Recorded exercises included ENCODE-style TSS enrichment on real GM12878 chr1 slice; NRF/PBC on real unfiltered and ENCODE-filtered BAMs; ATACseqQC R script on filtered slice with ENCODE IDR peaks; aggregate_qc.py grading and MultiQC hand-off.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 86/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-atac-seq-co-accessibility

- Recorded 5 audit versions between 2026-09-30 and 2026-09-30.
- Recorded exercises included Shipped CLI on real 3-chromosome PBMC Multiome ATAC slice (766 peaks x 2,701 cells, pattern-format .mtx) with…; run_cicero_pipeline API: window=1e6 (multi-chromosome), tss_bed=NULL branch, seed reproducibility; ArchR addCoAccessibility/getCoAccessibility as documented on public PBMC 5k chr1 slice; Synthetic planted-truth dataset (60 peaks, 4 latent states, 4 co-varying peak groups) plus a threshold that….
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 85/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-atac-seq-consensus-peakset

- Recorded 6 audit versions between 2026-09-28 and 2026-09-30.
- Recorded exercises included Public 3,000-row hg19 narrowPeak workflow; Two-file per-replicate glob; Missing narrowPeak summit column; Malformed rows and R/Python summit guards.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 91/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-atac-seq-deep-learning-atac

- Recorded 5 audit versions between 2026-09-30 and 2026-09-30.
- Recorded exercises included Shipped chromBPNet pipeline, fresh OUTDIR, then RESUME tail and guards; Variant-effect log2FC correctness (P0) with three independent methods; pred_bw regions contract and Enformer reference guard; Attributions, TF-MoDISco and report (lite and tomtom) on the real ENCODE GM12878 model.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 89/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-atac-seq-differential-accessibility

- Recorded 5 audit versions between 2026-09-30 and 2026-09-30.
- Recorded exercises included CLI DESeq2 run on ENCODE GM12878 vs K562 (2 vs 2 reps, hg38 chr1:1-30Mb); run_diff(normalize_mode=DBA_NORM_LIB) via sourced function, same data; run_diff(use_sva=TRUE) on 4 samples (SVA hidden-batch branch); Documented CLI usage: Rscript diff_accessibility.R sheet.csv mypfx DBA_NORM_LIB 0.01 3.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 88/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-atac-seq-enhancer-gene-linking

- Recorded 5 audit versions between 2026-09-30 and 2026-09-30.
- Recorded exercises included Usage-guide example verbatim: run_abc.sh, K562 chr22, real ENCODE Hi-C ENCFF621AIY read remotely…; run_abc.sh no-Hi-C powerlaw contact (HIC_TYPE=none), K562 chr22, with H3K27ac; run_abc.sh accessibility-only (ACCESS_TYPE=ATAC on the DNase BAM, no H3K27ac, powerlaw); mechanics only; run_abc.sh with PEAKS= from MACS3 3.0.4 (documented macs2-shim alternative), powerlaw.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 88/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-atac-seq-footprinting

- Recorded 5 audit versions between 2026-09-30 and 2026-09-30.
- Recorded exercises included run_tobias.sh unmodified, GM12878 vs K562 chr1:1-30 Mb; NFR filter, +4/-5 shift and TOBIAS on NFR BAMs; Motif set without CTCF; output dir containing a space; HINT-ATAC and Wellington via the documented install.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 88/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-atac-seq-motif-deviation

- Recorded 5 audit versions between 2026-09-30 and 2026-09-30.
- Recorded exercises included Shipped bulk script, unmodified, with depth.tsv on ENCODE GM12878 x3 vs K562 x3 (chr1:1-30 Mb, 6,357 peaks);…; Failure guard and stochasticity control on the bulk script; Signac direct-chromVAR route extracted verbatim from single-cell.md, run on Signac 1.17.1 and 1.16.0 (10x…; ArchR NA guard and getMarkerFeatures on the saved 216-cell ArchR project (upstream chain lines identical to….
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 87/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-atac-seq-nucleosome-positioning

- Recorded 5 audit versions between 2026-09-30 and 2026-09-30.
- Recorded exercises included V-plot at 300 chr1 protein-coding TSS, GM12878 rep1 (vplot.py, strand column); NRL estimate from fragment sizes (estimate_nrl.py) on three real BAMs; ATACseqQC pipeline (nucleosome_analysis.R) on GM12878 rep1 with protein-coding TSS BED; NucleoATAC from a clean py2.7 install following usage-guide.md, then the documented patch.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 85/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-atac-seq-single-cell-atac

- Recorded 6 audit versions between 2026-09-30 and 2026-09-30.
- Recorded exercises included Shipped signac_workflow.R on 10x ATAC 1.0.1 PBMC 5k (chr1 fragments), documented args and relaxed 1 1000; Shipped script auto-detecting Cell Ranger ARC 2.0.0 per_barcode_metrics.csv, PBMC 3k Multiome, whole-genome…; Shipped script on 10x ATAC 2.1.0 10k PBMC v2 (chr1 fragments slice), documented args and relaxed; AMULET BAM route on ARC per the new flag table (ARC chr1 1-30 Mb CB-tagged BAM slice).
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 89/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-bam-statistics

- Recorded 4 audit versions between 2026-09-20 and 2026-09-23.
- Recorded exercises included Real human PE BAM and real 1000G BAM: flagstat/idxstats/stats/coverage, batch row, every mean-depth and >=Nx…; NEW synthetic planted-depth BAM: zero-coverage regions, contig with no reads, contig-end stack, deletions,…; Planted flag categories (secondary, supplementary, QC-fail, duplicate, unmapped, singleton, mate on other…; Depth-cap trap: synthetic 9500x stack plus real ARTIC nanopore BAM, every tool in the cap table (regression….
- Fix work addressed these recorded problems: 1 Mean-depth and >=Nx recipes divide by covered positions (568x vs 16.8x; 79.3% vs 2.34%); 1b pysam mean_depth() 579.7 (columns only) and coverage_stats() (lost orphan positions, capped); 2 pysam counting snippets and qc_report.py count secondary/supplementary/QC-fail.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-batch-downloads

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included EPost 600 real distinct nucleotide IDs in 200-chunks, fetch by WebEnv/QueryKey; History-server download with disk checkpoint, resumed after a simulated mid-job crash; Exact 200/201-ID EPost boundary using examples/batch_by_ids.py's own functions, unmodified; "Download every PubMed abstract for 'CRISPR AND 2024[PDAT]' in MEDLINE format" (usage-guide.md Quick Start,….
- Fix work addressed these recorded problems: examples/robust_download.py's checkpointed_download() crashes with TypeError: a bytes-like object is required, not 'str' on the documented…; examples/batch_fasta.py's unguarded SeqIO.parse('insulin_mrna.fasta', ...) crashes FileNotFoundError because its own query (insulin[Gene…; SKILL.md's decision matrix has a hard cap (≤4 workers) but only a soft "consider" for record counts far beyond its documented brackets — no….
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-batch-processing

- Recorded 3 audit versions between 2026-09-28 and 2026-09-28.
- Recorded exercises included Count, split, and index a bounded FASTA set; Compressed FASTX reader selection and quality encoding; Empty discovery and invalid chunk size; High-cardinality and hostile prefix splitting.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 97/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-biomart-queries

- Recorded 3 audit versions between 2026-09-17 and 2026-09-24.
- Recorded exercises included Bulk ID mapping: 5 Ensembl Gene IDs -> HGNC/RefSeq/UniProt; Coordinate table: protein-coding genes on chr21; Discover real attributes/filters before trusting field names; Ortholog wide-table: human/mouse/zebrafish chr17, 1:1 only.
- Fix work addressed these recorded problems: Flagship "Bulk ID mapping" pattern + examples/bulk_id_mapping.py raise BiomartException on filters={'ensembl_gene_id': ...} before any…; SKILL.md pins "pybiomart 0.9+"; no such release exists (only 0.1, 0.2.0 on PyPI); Coordinate-table pattern lists attribute biotype; real attribute is gene_biotype.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-blast-searches

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Identify an unknown partial DNA sequence via BLASTN (reproducible db); Find mammalian homologs of human hemoglobin alpha in Swiss-Prot; BLAST a 12-aa proteomics peptide (short-query parameters); Whether E-values from an nr search and a swissprot search can be compared directly.
- Fix work addressed these recorded problems: SKILL.md's "Short peptide search" pattern (PAM30, no gapcosts) crashes: NCBI defaults gap costs to BLOSUM62's (11,1), which PAM30 rejects; megablast/dc-megablast documented as program= values; NCBIWWW.qblast() only accepts blastn/blastp/blastx/tblastn/tblastx -- the real form…; Missing FASTA defline documented as producing record.query=None; audit found the real placeholder is the string 'No definition line' plus a….
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-causal-genomics-colocalization-analysis

- Recorded 4 audit versions between 2026-09-17 and 2026-09-22.
- Recorded exercises included Canonical GWAS-eQTL coloc.abf with p12 sensitivity (synthetic single shared causal variant); coloc.susie multi-causal via the Skill's own toy LD pattern (synthetic 2-causal-SNP GWAS); coloc.abf PP.H3-dominance diagnosis for a distinct-causal-in-LD locus (synthetic); SMR + HEIDI CLI recipe verification against the real SMR 1.3.1 binary (no real BESD data).
- Fix work addressed these recorded problems: Both shipped coloc.susie examples crash unconditionally (estimate_s_rss lambda 0.21-0.39, susie_suff_stat "estimated prior variance is…; PP.H3-inflation trigger (r2 0.3-0.6) overstated; MHC exclusion enforced only by prose, no code gate.
- The published source version recorded 98/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-causal-genomics-effector-gene-prioritization

- Recorded 3 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included Open Targets L2G + PoPS + coloc concordance for a PCSK9-region lead SNP; Custom trait from scratch: MAGMA -> PoPS -> concordance (usage-guide's own example prompt); HLA-region lead SNP (chr6:32.15Mb, hg38); Tissue-unknown prioritisation for a schizophrenia GWAS.
- Fix work addressed these recorded problems: No explicit research-only / clinical-boundary language; MAGMA gene-set enrichment (--set-annot) has an undocumented minimum-gene-count requirement; Undocumented Windows filename mismatch between MAGMA output (<prefix>.genes.out.txt) and PoPS input (<prefix>.genes.out).
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-causal-genomics-fine-mapping

- Recorded 4 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included susie_rss on a matched-LD summary-statistics locus, 2 planted causals; susie(X, y, L=10) on individual-level genotypes; LD reference mismatch diagnostic (estimate_s_rss / kriging_rss); coloc.susie two-trait colocalization, shared planted causal.
- Fix work addressed these recorded problems: coloc.susie example crashes with a cryptic data.table error unless z/LD carry SNP names; No platform caveat that FINEMAP / SuSiEx / PAINTOR / DAP-G are POSIX-only CLI tools; All technical depth sits inline in SKILL.md rather than in references/.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-causal-genomics-genetic-correlation

- Recorded 2 audit versions between 2026-09-17 and 2026-09-24.
- Recorded exercises included Global rg via cross-trait LDSC (GenomicSEM ldsc() route), no sample overlap; Sample-overlap intercept stress test (two overlapping UKB-style GWAS); Underpowered pilot GWAS (N~3000, mean chi-square below 1.02 floor); Trans-ancestry rg via Popcorn (EUR vs EAS T2D).
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 97/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-causal-genomics-genomic-sem

- Recorded 3 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included Common-factor CFA on 4 psychiatric GWAS (synthetic, planted loadings 0.75/0.65/0.70/0.55); commonfactorGWAS with Q_SNP classification on 20 synthetic SNPs (5 factor, 5 heterogeneous, 10 null); Heywood-case diagnosis on near-collinear BMI/WHRadjBMI pair (rg=0.97, synthetic); Two-factor confirmatory usermodel: lipid factor + glycemic factor, F1~~F2 free (synthetic, planted rF=0.40).
- Fix work addressed these recorded problems: 3 of 4 core functions crash under the Skill's own supported lavaan range; commonfactor()'s own error message misdiagnoses the crash as non-convergence; No scope-boundary / escape-hatch section.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-causal-genomics-heritability-partitioning

- Recorded 3 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included Total h2 from EUR T2D-style GWAS sumstats via LDSC --h2; Partitioned h2 across functional categories (baseline-LD v2.2 stand-in) for a schizophrenia GWAS; Cross-trait genetic correlation between two non-overlapping GWAS (BMI vs MDD framing); Case-control liability-scale h2 (population prevalence 0.5%, sample 8% cases).
- Fix work addressed these recorded problems: Primary tool's --h2/--rg CLI broken in the exact recommended fork/version; Finucane 2018 --h2-cts unconditionally broken; No scope/escape-hatch guidance for patient-facing PRS misuse.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-causal-genomics-mediation-analysis

- Recorded 4 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included eQTL single-mediator observational mediation with Imai sensitivity; 4-way VanderWeele decomposition via CMAverse with exposure-mediator interaction; Small-pilot single-mediator mediation (n=60, below the Skill's own stated floor); MVMR-mediation (total-minus-direct) for LDL->CHD through HDL.
- Fix work addressed these recorded problems: HIMA covariate fix in SKILL.md (factor()) is backwards on HIMA >= 2.3; HIMA return type documented as data.frame; actually a list; CMAverse component names in SKILL.md prose (intref/intmed) stale vs verified output (ERintref/ERintmed).
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-causal-genomics-mendelian-randomization

- Recorded 4 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included Standard two-sample MR battery on real GIANT-BMI15 x PGC-MDD18 GWAS (95 harmonised SNPs); cis-MR drug-target analysis with colocalization triangulation (synthetic cis-pQTL window, planted…; 3-SNP sparse cis-instrument set, below Egger's 10-SNP and MR-PRESSO's 4-SNP documented floors; MVMR of LDL and HDL jointly on CHD with conditional F, IVW-MVMR, and Q_A heterogeneity.
- Fix work addressed these recorded problems: examples/two_sample_mr.R's MR-PRESSO reporting line crashes on real pleiotropic data; Decision Tree / Operational rule name MR-RAPS as the fix for one-sample-equivalent designs generally; SIMEX correction was prose-only in SKILL.md; the natural in-formula weighting pattern crashes.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-causal-genomics-pleiotropy-detection

- Recorded 3 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included Standard battery on real BMI(GIANT15) x MDD(PGC18) GWAS data; CHP-suspected scenario, synthetic planted correlated pleiotropy, ground truth = 0; 3-SNP cis-MR instrument set; Weak-instrument regime (mean F=2.65), MR-RAPS vs IVW.
- Fix work addressed these recorded problems: SIMEX example crashes as shipped; LCV usage snippet references a field name that doesn't exist; MR-Mix / contamination mixture don't fail the way Common Errors says.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-causal-genomics-proteome-mr-drug-target

- Recorded 2 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included PCSK9 cis-MR vs CAD, coloc.abf + PAV-excluded sensitivity + correlated cis-IVW; IL6R cis-MR vs rheumatoid arthritis, Olink vs SomaScan cross-platform replication; Minimal cis-pQTL window (ANGPTL4 vs triglycerides), small-N coloc; PCSK9 phenome-wide cis-MR, Bonferroni-corrected on-target adverse-effect scan.
- Fix work addressed these recorded problems: TwoSampleMR::mr_ivw shadows MendelianRandomization::mr_ivw depending on load order; SKILL.md's documented mr_ivw(mr_obj, model='default',…; Shipped examples/phewas_drug_target_mr.R line 65 runs lapply(outcomes_filt$id[1:200], scan_one_outcome) — the exact [1:200] shortcut…; SKILL.md carries the full methodological corpus inline, no references/ split.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-causal-genomics-transcriptome-wide-association

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included S-PrediXcan LDL-cholesterol TWAS, GTEx v8 MASHR liver; FUSION TWAS on CAD GWAS + conditional/joint analysis; FOCUS fine-mapping at a 7-gene co-significant locus; S-PrediXcan multi-tissue + S-MultiXcan joint test, schizophrenia GWAS.
- Fix work addressed these recorded problems: pip install pyfocus (bare, as usage-guide.md instructed) crashes every focus call: pandas>=2.2 removed delim_whitespace, called throughout…; FUSION.post_process.R crashes on single-SNP ("top1") genes: Error in wgt.matrix[qc$flip, ] : incorrect number of dimensions; pyfocus pin+patch insufficient: focus finemap crashes at "Calculating PIPs" with DataFrame.pivot() takes 1 positional argument….
- The published source version recorded 90/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-cfdna-preprocessing

- Recorded 3 audit versions between 2026-09-28 and 2026-09-28.
- Recorded exercises included Public cfDNA insert-size QC; Simplex UMI consensus wrapper; Reciprocal duplex UMI consensus wrapper; QC flags, bounds, and empty BAM.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-chipseq-allele-specific-binding

- Recorded 4 audit versions between 2026-09-28 and 2026-09-28.
- Recorded exercises included Paired-end WASP mapping-bias route; Cancer BaalChIP workflow with RAF or gDNA correction; Imprinting, blacklist, chrX, and contract boundaries; Public two-feature RASQUAL cohort.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-clinical-biostatistics-adaptive-designs

- Recorded 3 audit versions between 2026-09-28 and 2026-09-28.
- Recorded exercises included O'Brien-Fleming and survival group-sequential design; Blinded variance sample-size re-estimation; Promising-zone documented-only boundary; BOIN boundaries and seeded operating characteristics.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-clinical-databases-acmg-classification

- Recorded 4 audit versions between 2026-09-28 and 2026-09-28.
- Recorded exercises included Shipped regression and guarded demonstration; PVS1 gates, review stops, and contradictory state; Brnich OddsPath boundaries and prose consistency; Current evidence-family and predictor integrity.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-clinical-databases-clinvar-lookup

- Recorded 3 audit versions between 2026-09-15 and 2026-09-24.
- Recorded exercises included VCV summary and CA ID for VariationID 17661; Annotate a VCF from the weekly ClinVar VCF; Conflicting classifications and star filter; All P/LP VariationIDs in a gene.
- Fix work addressed these recorded problems: car_id() PUT rejected (403); Gene search truncates at 500; Stale review-status string; ALLELEID labelled vcv_id.
- The published source version recorded 88/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-clinical-databases-dbsnp-queries

- Recorded 2 audit versions between 2026-09-15 and 2026-09-15.
- Recorded exercises included Resolve rs429358; Trace a merged rsID; Multi-allelic and nonexistent rsIDs; VCF to canonical SPDI and rsID.
- Fix work addressed these recorded problems: resolve_merge_chain KeyError on live merge schema; vcf_to_canonical_spdi reads non-existent data.spdi; SKILL map chr1/chr17 only; ALFA frequencies not in RefSNP JSON.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-clinical-databases-gnomad-frequencies

- Recorded 2 audit versions between 2026-09-15 and 2026-09-15.
- Recorded exercises included rs334 frequency in gnomAD v4; Whiffin max credible AF and frequency tags; GRCh37 coordinates and chrX constraint; Batch FAF95 and bottleneck exclusion.
- Fix work addressed these recorded problems: Constraint guidance was stale after gnomAD v4.1.1.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-clinical-databases-myvariant-queries

- Recorded 2 audit versions between 2026-09-15 and 2026-09-15.
- Recorded exercises included Multi-source annotation with versions; ClinVar P/LP variants in a gene; High-CADD region and multi-allelic rsID; AlphaMissense search with versions.
- Fix work addressed these recorded problems: Field paths return nothing (clinvar.clinical_significance, gnomad_exome.faf95, dbnsfp.cadd.phred); Source table misstates gnomAD version and ClinVar freshness; Version tracking via _meta does not work.
- The published source version recorded 90/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-clip-seq-ago-clip-mirna-targets

- Recorded 5 audit versions between 2026-09-28 and 2026-09-28.
- Recorded exercises included Current Hyb official-data route and workflow-level repeatability; Strict failure, path, overwrite, and atomic-publication boundaries; 16-column orientation, expression provenance, schema, and ambiguity controls; TargetScan spliced-coordinate projection and strand-safe overlap.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-codon-usage

- Recorded 3 audit versions between 2026-09-28 and 2026-09-28.
- Recorded exercises included Run the three supplied standard-code examples; Alternate genetic code 2; Empty partial shifted and ambiguous inputs; CAI tie stop and pseudocount semantics.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 97/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-comparative-genomics-ancestral-reconstruction

- Recorded 4 audit versions between 2026-09-28 and 2026-09-28.
- Recorded exercises included PAML protein and codon ASR; IQ-TREE marginal protein ASR; Discrete trait stochastic mapping and hidden rates; Continuous-trait BM and OU reconstruction.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-conformer-generation

- Recorded 3 audit versions between 2026-09-19 and 2026-09-24.
- Recorded exercises included 20 ETKDGv3 conformers for aspirin, MMFF94-optimized; Single low-energy ibuprofen conformer for docking, written to SDF; Phenylboronic acid: MMFF94-parameter-missing -> UFF fallback; Macrocycle-aware embedding on a 14-membered ring.
- Fix work addressed these recorded problems: CREST + GFN2-xTB escalation path has no Windows caveat despite CREST publishing no Windows build anywhere upstream; SKILL.md's gen_conformers() omits the mol is None guard present in macrocycle_conformers() and crest_workflow() in the same file; Function names diverge between SKILL.md (gen_conformers/prune_conformers_rmsd/filter_by_energy) and examples/gen_conformers.py….
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-covalent-design

- Recorded 3 audit versions between 2026-09-19 and 2026-09-22.
- Recorded exercises included Classify acrylamide/chloroacetamide candidates + flag for GSH testing (verbatim usage-guide prompt); Alpha-C substitution vs measured GSH/kinact-Ki on an 8-compound acrylamide series (verbatim usage-guide…; Invalid SMILES, empty string, no-warhead, overlapping-match, and charged-species robustness; Lysine/tyrosine-directed warheads: sulfonyl fluoride, fluorosulfate (SuFEx), reversible aldehyde.
- Fix work addressed these recorded problems: Shipped WARHEAD_SMARTS catalog omits 2 of 14 SKILL.md-documented classes (alpha-haloketone, alpha,beta-unsaturated ketone); acrylamide/alpha_substituted_acrylamide/methacrylamide SMARTS co-match the same compound, undocumented; No explicit escape hatch for individual-patient/clinical-decision misuse.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-bagel-essentiality

- Recorded 3 audit versions between 2026-09-16 and 2026-09-22.
- Recorded exercises included fc->bf->pr pipeline on real HAP1 TKOv3 data; Tumor-suppressor calling via interpret_bagel() on the same screen; Reference-set failure-mode diagnosis (species mismatch + -e/-n swap); BAGEL2 vs MAGeCK hit-set Jaccard comparison.
- Fix work addressed these recorded problems: BAGEL2 non-deterministic and undisclosed (Skill Veto T3 FAIL); interpret_bagel() flags 86.5% of genes as tumor suppressor on a dropout screen; Reference-set failure modes documented inaccurately ("median BF near zero" claimed for every bad-reference case).
- The published source version recorded 91/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-base-editing-analysis

- Recorded 3 audit versions between 2026-09-16 and 2026-09-22.
- Recorded exercises included CBE saturation library design tiling a target region (find_be_spacers, BE4max); Editing-efficiency filtering on real CRISPResso2 pilot output (filter_by_editing_efficiency); ABE7.10 zero-bystander spacer search for a single-variant install (find_be_spacers, target_base='A'); Bystander deconvolution from a real CRISPResso2 allele-frequency table (deconvolute_bystander).
- Fix work addressed these recorded problems: find_be_spacers() silently misattributes target/bystander for reverse-strand spacers: genomic_pos computed in reverse-complement coordinate…; filter_by_editing_efficiency() crashes (KeyError: 'Position') — real Quantification_window_nucleotide_percentage_table.txt has no Position…; deconvolute_bystander() crashes (KeyError: 'Reference_pct') — real Alleles_frequency_table.zip has no such column.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-batch-correction

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included Real HAP1 TKOv3, planted 2-batch shift, ComBat with condition covariate; Unknown/unannotated batch -> RUVg on synthetic NTC-anchored counts; Batch fully confounded with condition -> ComBat vs MLE-covariate; Batch as explicit covariate in MAGeCK MLE design matrix (real HAP1 subset).
- Fix work addressed these recorded problems: combat_correct() crashes on its own "Critical" covariate usage: mod passed as a one-hot array and data as a raw ndarray; Forcing ComBat on a batch-free design silently returns 100% NaN; RUV example's cIdx is integer positions; RUVg's SeqExpressionSet method requires character rownames.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-combinatorial-screens

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Cas12a multiplex paralog screen: per-pair GI scoring at representative scale; Architecture choice: Big Papi (paired-Cas9) vs Inzolia (Cas12a multiplex) for the same pair set; GI scoring on a small (8-pair) library -- z-score cutoff behavior at low N; MAGeCK MLE with explicit interaction terms on a 4-condition combinatorial screen.
- Fix work addressed these recorded problems: gi_score() docstring/body used paired_lfc/single_lfc; examples/gi_scoring.py and usage-guide use lfc, causing KeyError on the documented…; No explicit clinical/practice-boundary escape hatch (Input 6 declined a patient-therapy request on general judgment only); No minimum-N guidance for the z<-2 GI cutoff (demonstrated at N=8 and N=9).
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-copy-number-correction

- Recorded 3 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included Diagnose + correct a planted 17q12/HER2 amplicon in real HAP1 TKOv3 counts; Apply CRISPRcleanR to a single-cell-line screen without a CN profile; Single cell line with matched CN profile -- per the decision tree, 'CRISPRcleanR or Chronos; Either works'; DepMap-scale multi-cell-line panel with CN profiles -- apply Chronos end-to-end.
- Fix work addressed these recorded problems: Chronos example unrunnable: readcounts orientation is the transpose of what check_inputs requires; Decision tree claimed Chronos works for a single cell line with matched CN; Spearman CN-bias diagnostic misses a single focal amplicon.
- The published source version recorded 98/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-crispresso-editing

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included Single Cas9 amplicon indel quantification (FANCF locus); CBE base-editor quantification-window code path; Low-alignment / wrong-amplicon diagnostic; 2-amplicon arrayed validation pool (CRISPRessoPooled).
- Fix work addressed these recorded problems: parse_crispresso() crashes on real output (ValueError: too many values to unpack) and reads READS_ALIGNED_PERCENTAGE, a column absent from…; CRISPRessoPooled silently returns all-NA on a realistic pilot-scale pool (242-250 reads/amplicon); --min_reads_to_use_region defaults to…; Single-Amplicon worked example's --min_average_read_quality 30 changes the reported % (26.38%->24.89%) with no disclosure.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-drugz-chemogenomic

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included Standard PARPi-style vehicle vs drug run on synthetic HAP1 TKOv3-derived counts; Excluding CEGv2 essentials from the null distribution via -r (SKILL.md's own worked example); Multi-dose consistency check (mid-dose vs high-dose, both vs vehicle); Diagnosing a 'no sensitizers found' report caused by comparing Day-0 instead of vehicle.
- Fix work addressed these recorded problems: examples/run_drugz.py Step 2 joins raw CEGv2.txt lines, so -r matches nothing and the "CEG-excluded" run is identical to the unfiltered one; No documented relationship between total guide count and --half_window_size; Dose-response section's only code is commented-out pseudocode.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-hit-calling

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included 2-method MAGeCK+BAGEL2 consensus on real HAP1 TKOv3 data, validated against CEGv2/NEGv1; Method selection for a 5-cell-line cancer panel (Chronos vs MAGeCK MLE vs JACKS); Second-best-sgRNA rule applied to real MAGeCK sgrna_summary.txt for Tier-1 genes; Spearman rho audit between MAGeCK neg|score and BAGEL2 BF (usage-guide.md's own prompt).
- Fix work addressed these recorded problems: BAGEL2 non-determinism named in scope, unaddressed; 3 conflicting MAGeCK-FDR/BAGEL-BF threshold pairs (SKILL.md inline fn 0.05/5, examples/consensus_hits.py 0.1/5, Quantitative Thresholds…; Empty-consensus guidance has only one cause (screen quality); real failure mode is merging non-comparable comparisons.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-in-vivo-screens

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Focused immune-evasion library design, B16 syngeneic, 2M cells; CRISPR-StAR setup for a genome-scale (72,000 sgRNA) screen at 2M cells; Genome-wide (80,000 sgRNA) library at 1M cells, no CRISPR-StAR; Per-animal MAGeCK + Stouffer meta-analysis on 6-animal synthetic in vivo screen (executed).
- Fix work addressed these recorded problems: Compound hit-calling threshold (meta-FDR<0.05 AND >=50% animals at per-animal FDR<0.05) called 0/5 planted hits on the audit's synthetic…; SKILL.md/usage-guide.md never mention IACUC / ethical review anywhere, despite describing live-animal tumor implantation throughout; mageck mle's permutation-derived FDR values drift run-to-run, no seed control, undocumented.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-jacks-analysis

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included Multi-screen joint analysis on JACKS' own bundled Project Score data (13 cell lines, matched per-sample…; Single-screen essentiality on real HAP1 TKOv3 data, benchmarked against CEGv2/NEGv1; Reference efficacy prior from the wrong library (SKILL.md's own documented failure mode); Run the Skill's own shipped downstream-analysis code (examples/run_jacks.py + SKILL.md's efficacy_summary())….
- Fix work addressed these recorded problems: efficacy_summary() does groupby('Gene') on the grna file, whose only columns are sgrna, X1, X2; examples/run_jacks.py analyze_results() uses undefined output_prefix; Canonical Python example sets apply_w_hp=True against the Skill's own advice.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-library-design

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included Cas9 KO library, 8 synthetic DDR genes (synthetic CDS); CRISPRi Dolcetto-window library, 5 synthetic lncRNAs; CRISPRa Calabrese-window library, 4 synthetic TFs; Edge: short/PAM-less synthetic CDS, guide-independence gap.
- Fix work addressed these recorded problems: No minimum-spacing/independence filter on candidate guides — find_sgrna_candidates filters composition only; a short/GC-tied region can…; SKILL.md vs usage-guide.md contradiction on Azimuth 2.0 usability; Shipped examples/design_library.py implements a different, simpler algorithm (random sequences + GC heuristic) than the documented CDS/TSS….
- The published source version recorded 91/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-mageck-analysis

- Recorded 3 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included RRA test on real HAP1 TKOv3 data + visualization; Time-course MLE design matrix + monotonic-trend function; Heavy-selection screen (>40% guides changing) normalization diagnosis; Drug screen with sgRNA-efficiency injection.
- Fix work addressed these recorded problems: MLE permutation-FDR undocumented-sensitive to --permutation-round/covariates; MAGeCKFlute FluteRRA example fails as documented; No platform caveat/fallback for mageck-vispr.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-perturb-seq-analysis

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Mixscape escaper filtering + PyDESeq2 pseudobulk DE on a synthetic CROP-seq dataset; Architecture selection for a 1,500-perturbation primary-T-cell screen needing surface-protein readout; sgRNA per-cell assignment at MOI producing a 5% multiplet rate; Low-MOI calibrated DE via SCEPTRE on the package's own bundled example data.
- Fix work addressed these recorded problems: PyDESeq2.test_contrasts()/result columns stale for pertpy >=1.0 (contrast=(col,group,baseline) tuple + log2FoldChange/padj); Multiomic RNA+ATAC section is a 4-line non-functional stub despite frontmatter promising multiome coverage; Genome-scale cost/channel figures ($50-100K/10-30 channels) don't scale-check against a literal ~19,000-gene request.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-prime-editing-screens

- Recorded 4 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included pegRNA library design via PRIDICT2 batch CLI, following SKILL.md's documented command; Bundled design_pegrna_pridict2.py example on a realistic, PE-designable synthetic variant; CRISPResso2 prime-editing quantification: correct vs SKILL.md-documented pegRNA element order; PRIDICT2 single-mode determinism and spacer-convention check on the audit's own synthetic sequence.
- Fix work addressed these recorded problems: pegRNA Architecture diagram lists PBS before RTT; building --prime_editing_pegRNA_extension_seq in that order makes real CRISPResso2…; design_pegrna_pridict2.py's find_pegrna_candidates() crashes with KeyError: 'pridict2_efficiency' on a realistic PE-designable variant…; SKILL.md's PRIDICT2 batch CLI example is broken: --summarize as a bare flag crashes argparse; correcting only that but keeping the….
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-crispr-screens-screen-qc

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included Full QC audit on real HAP1 TKOv3 counts; Plasmid Gini/skew diagnostic reasoning (usage-guide example prompt); Copy-number bias diagnostic on a synthetic focal amplicon; Planted fault: 8% guide dropout in one endpoint replicate.
- Fix work addressed these recorded problems: CN-bias Spearman threshold misses a real focal amplicon; Shipped examples/screen_qc.py uses stage-blind thresholds and correlates non-replicate pairs; No escape hatch for research-vs-clinical scope creep.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-data-visualization-color-palettes

- Recorded 3 audit versions between 2026-09-20 and 2026-09-27.
- Recorded exercises included CVD-safe categorical palette for 7 cell types on a UMAP, grey reserved for unassigned (Okabe-Ito); Diverging log-fold-change heatmap, Crameri vik, symmetric bounds, zero must map to pure white; Audit candidate palettes for grayscale monotonicity and CVD safety using the Skill's own check blocks; Migrate a matplotlib spatial-expression figure from jet, plus signed and cyclic (phase) data, in Python.
- Fix work addressed these recorded problems: Turbo offered as perceptually uniform; Mandatory CVD pre-flight used cvd_emulator incorrectly; Pure-white midpoint contradicted built-in diverging palettes.
- The published source version recorded 97/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-data-visualization-dimensionality-reduction-plots

- Recorded 3 audit versions between 2026-09-20 and 2026-09-27.
- Recorded exercises included Bulk PCA (sklearn) on synthetic 3-condition x 2-batch counts, variance-labelled axes; PCAtools biplot/scree/loadings on REAL airway vst data (R route); scanpy PCA -> neighbors -> UMAP -> Leiden -> save on synthetic 4-cluster counts + real pbmc68k_reduced; t-SNE (openTSNE Kobak-Berens block, Rtsne, uwot), seeds and small-n perplexity on a 6-cluster hierarchy.
- Fix work addressed these recorded problems: Rtsne silently ignores seed=42; Scikit-learn PCA was called deterministic although auto selected a randomized solver; Shipped example and prerequisites were incomplete.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-data-visualization-distribution-plots

- Recorded 2 audit versions between 2026-09-20 and 2026-09-23.
- Recorded exercises included Current R box, guarded violin, quasirandom, and ggdist raincloud; Current Python RainCloud and seaborn boxenplot; Tied/all-zero fallback and missing or low-N split cells; Prior real ALL microarray split-violin input.
- Fix work addressed these recorded problems: Archived gghalves raincloud fails on ggplot2 4.x; SJ blanks a panel when a stratum is tied or constant; Split violin changes side with a missing cell or tiny group.
- This trail was outside the 195-Skill published shelf at retirement. Recorded scores ranged from 69.5 to 93.1.

## bio-data-visualization-forest-funnel-plots

- Recorded 2 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included REML BCG forest with log-ratio axis and prediction interval; Funnel, contour funnel, Egger, and trim-and-fill safeguards; Three-study small-k meta-analysis; Cox covariate forest and treatment-by-subgroup forest.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-data-visualization-ggplot2-fundamentals

- Recorded 7 audit versions between 2026-09-20 and 2026-10-03.
- Recorded exercises included create_volcano default on airway DESeq2 results (19,772 genes, 1,534 NA padj) plus the create_pca_plot…; Label-overlap envelope: drawn ggrepel label boxes for every row the Skill claims, standalone and…; create_volcano default top_n = NULL heuristic and input guards: 8/9-character boundary, NA or empty labels,…; save_publication_figure, PDF fonts and page size, PNG pixels, theme/Okabe-Ito consistency, boxplot and PCA….
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 90/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-data-visualization-heatmaps-clustering

- Recorded 2 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included Annotated ComplexHeatmap with pathway row split + OLO: both shipped examples, SKILL.md OLO/annotation blocks,…; seaborn.clustermap block (row z-score, ward, col_colors) on a log-expression matrix; Failure-mode and reconciliation claims: ward.D vs ward.D2, outliers, sparse rows, ordered time course,…; Sample-correlation QC heatmap and expression + log2FC concatenated heatmaps with shared row order….
- Fix work addressed these recorded problems: Explicit OLO dendrogram plus categorical row_split crashes; Seaborn limits came from raw values while z_score=0 plotted another scale; Circular row selection and three advertised workflows lacked executable guidance.
- This trail was outside the 195-Skill published shelf at retirement. Recorded scores ranged from 78 to 90.

## bio-data-visualization-lollipop-protein-maps

- Recorded 2 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included Exact shipped TP53 maftools demonstration; Exact shipped paired lollipopPlot2; HGVSp edge cases and short-isoform guidance; Exact trackViewer TP53 map and references.
- Fix work addressed these recorded problems: Shipped example was incomplete and painted factor-indexed colours incorrectly; maftools behavior and protein identifier guidance were misstated; TP53 domains and transcript were wrong.
- This trail was outside the 195-Skill published shelf at retirement. Recorded scores ranged from 65 to 93.

## bio-data-visualization-matplotlib-fundamentals

- Recorded 7 audit versions between 2026-09-20 and 2026-10-03.
- Recorded exercises included Run scripts/matplotlib_phd.py unchanged: rcParams, 89 mm scatter, 2x3 grid, Crameri heatmap, seaborn scatter,…; SKILL.md seaborn volcano recipe on real airway DESeq2 results (18,238 genes); SKILL.md Standard Setup rcParams and Saving block: PDF, PNG, TIFF, SVG, EPS at 89 mm; references/chart-recipes.md blocks as a 6-panel figure (scatter, line, bar, boxplot, hist, imshow, axis….
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 90/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-data-visualization-multipanel-figures

- Recorded 2 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included Exact shipped R patchwork figure; cowplot and gridExtra alternative R arrangements; Exact shipped matplotlib grid, mosaic, and subfigures; Compatibility, bounding-box, and misleading-legend guards.
- Fix work addressed these recorded problems: plot_annotation(theme=...) did not style patchwork tags; Axis collection did nothing for the nested 2x2 recipe; Python changed the requested dimensions and emitted Type 3 fonts.
- This trail was outside the 195-Skill published shelf at retirement. Recorded scores ranged from 71 to 94.1.

## bio-data-visualization-network-visualization

- Recorded 4 audit versions between 2026-09-20 and 2026-09-27.
- Recorded exercises included SKILL 'NetworkX + matplotlib' block verbatim on a synthetic 100-node graph with 4 planted communities and 3…; SKILL 'Layout Algorithms' block, every layout line, plus directed gene-regulatory network with Graphviz dot…; Shipped examples/network_plots.py from a copy: four figures, content of each captured from the matplotlib…; R route: ggraph/igraph layouts, community colouring, edge bundling (SKILL blocks 2 and 4 verbatim, then….
- Fix work addressed these recorded problems: examples/cytoscape_automation.py fails silently; Community legend mislabels communities; PyVis mutates edge weights and loses direction.
- The published source version recorded 97/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-data-visualization-oncoprint-mutation-matrices

- Recorded 3 audit versions between 2026-09-20 and 2026-09-27.
- Recorded exercises included ComplexHeatmap oncoPrint of the top 20 genes of real TCGA-LAML (193 samples), FAB + vital-status tracks; maftools::oncoplot(top=20) with clinical features and sortByAnnotation on TCGA-LAML; Synthetic 30-sample cohort: multi-class cell, two hits of the same class, CNV+SNV cell, empty gene,…; comut.py co-mutation plot from TCGA-LAML long-format data (Skill Python block).
- Fix work addressed these recorded problems: comut block cannot run as written; Denominator claims contradict tool behaviour; Matrix and annotation construction left as comments.
- The published source version recorded 97/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-data-visualization-sequence-logos

- Recorded 2 audit versions between 2026-09-20 and 2026-09-23.
- Recorded exercises included Uniform-background ggseqlogo bits route and matrix orientation; Custom relative-entropy ggseqlogo route; Logomaker information and signed-weight snippets; WebLogo DNA and RNA commands.
- Fix work addressed these recorded problems: ggseqlogo(..., bg_freq=...) is not an API and silently left figures uncorrected; Uniform-background bias direction was reversed and the illustrative GC composition was inconsistent; Small-sample behaviour was treated as one method across three tools.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-data-visualization-statistical-annotation

- Recorded 3 audit versions between 2026-09-20 and 2026-09-27.
- Recorded exercises included Three skewed groups, unequal n (12/15/9), Wilcoxon + Holm brackets: SKILL ggpubr, rstatix and statannotations…; Paired pre/post (n=14 subjects, planted +2.5 shift, large between-subject variance): paired Wilcoxon and t,…; Borderline family: raw p 0.042 / 0.00032 / 0.045 (planted so two pairs lose significance under Holm); ggpubr,…; Four groups, unequal n (14/11/16/9), six comparisons, planted null (A-B) and two effects: Holm/Bonferroni/BH,….
- Fix work addressed these recorded problems: stat_compare_means(comparisons, p.adjust.method='holm') draws raw p; statannotations Holm/BH display raw p/stars; False claim that ggpubr defaults to t-test.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-data-visualization-upset-plots

- Recorded 2 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included ComplexUpset block 1 verbatim on the Skill's 4 sets, then the same call on SYNTHETIC planted 8 sets (D subset…; ComplexUpset queries (block 3), attribute panels (block 4), degree vs cardinality sort,…; Python upsetplot: SKILL.md block verbatim, shipped upset_python.py verbatim, then planted 8-set and its…; UpSetR route (block verbatim, shipped upset_gene_sets.R verbatim), UpSetR vs ComplexUpset reconciliation,….
- Fix work addressed these recorded problems: Python route crashed on show_counts, pandas 3, and .to_frame() misuse; ComplexUpset queries targeted empty intersections or over-highlighted ranges; Empty sets, blank/NA IDs, and UpSetR nsets=4 silently lost data.
- This trail was outside the 195-Skill published shelf at retirement. Recorded scores ranged from 70.4 to 93.

## bio-data-visualization-volcano-and-ma-plots

- Recorded 6 audit versions between 2026-09-20 and 2026-10-03.
- Recorded exercises included scripts/volcano_phd.R unchanged on the fitted airway dds (29,391 genes, 17,994 with padj): volcano, MA,…; scripts/volcano_plot.R volcano_plot(): uncapped, y_cap = 30, other fdr/lfc cutoffs, absent label gene; Every SKILL.md R block verbatim: DESeq + lfcShrink apeglm/ashr/svalue, EnhancedVolcano with colCustom,…; scripts/ma_plot.py on the real shrunken airway table, matplotlib size claim, sanbomics.plots.volcano….
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 89/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-differential-expression-deseq2-basics

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included Pseudobulk DE on CD14+ monocytes from 8 donors; Design formulas: batch and sex as nuisance, plus a paired design; Three genes with padj = NA for three different reasons; Interaction design, the resultsNames trap and the apeglm footgun.
- Fix work addressed these recorded problems: Shared Windows R runtime exits 139 after every DESeq2 route, including library(DESeq2).
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-differential-splicing

- Recorded 3 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included rMATS-turbo 3v3 on planted exon-skipping set + Skill filter snippet + shipped example; leafcutter 3v3 on planted set, SKILL.md steps and shipped R example; Real chrX 2v2 (GBR vs YRI) across rMATS, leafcutter, Shiba, SUPPA2 + permuted control; SUPPA2 diffSplice loop on synthetic 3v3 TPM (planted truth).
- Fix work addressed these recorded problems: SUPPA2 -m classical for n<=3 has zero power; table said min reps n>=2; leafcutter default flags stop at 3v3 and 2v2; n>=2/3 claim unbacked; group-file names, -k True undocumented; Confounder route (residuals + rank-sum) powerless at n=3, biased; fully confounded batch not warned.
- The published source version recorded 89/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-duplicate-handling

- Recorded 3 audit versions between 2026-09-20 and 2026-09-22.
- Recorded exercises included Standard paired-end duplicate workflow; Shipped pipeline and failure cleanup; Common errors and rerun behavior; Bulk UMI and duplex consensus.
- Fix work addressed these recorded problems: Duplex consensus crashes after adjacency grouping; umi_tools example omits sort/index and --paired; Optimized pipeline fails from clean dir and hides it.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-ensembl-rest

- Recorded 3 audit versions between 2026-10-02 and 2026-10-03.
- Recorded exercises included Symbol to ID, e110 pinning, gene structure, protein, region overlap (lookup_and_overlap.py); VEP by region, dbSNP ID, HGVS with consequence summary (vep_annotation.py); Compara orthologs and paralogs (compara_homology.py); Release pinning: e110, e111, e116, GRCh37, and a retired archive.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 87/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-entrez-fetch

- Recorded 3 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included Version-pinned sequence routes; Bulk summaries; PubMed formats; ClinVar ElementTree.
- Fix work addressed these recorded problems: bulk_summaries() (SKILL.md + examples/fetch_summaries.py) KeyError: 'Organism' on every nucleotide ESummary docsum; PMC-ID extraction (SKILL.md's pubmed_full() extended, and examples/fetch_pubmed.py) TypeError: string indices must be integers; SKILL.md's own inline sra_runinfo() TypeError: a bytes-like object is required, not 'str'.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-entrez-link

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Curated (RefSeq) vs all-protein link ratio for BRCA1 + BioProject->SRA cross-reference; Curated gene->PubMed RIF subset check for TP53; Asymmetric round-trip warning example (PMID 35412348) on live, zero-hit current data; Discover all available linknames via cmd='acheck' (gene/nucleotide/pubmed).
- Fix work addressed these recorded problems: cmd='acheck' discovery crashes: KeyError: 'Name' (current Biopython 1.88/NCBI keys LinkInfo entries as LinkName); LinkInfo entries can omit MenuTag/HtmlTag entirely, unguarded (confirmed: nuccore_nuccore_mrnaonly, pubmed_pmc_local); Canonical asymmetric-round-trip example (PMID 35412348) shows 0/0 on live data, no longer demonstrates the asymmetry.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-entrez-search

- Recorded 4 audit versions between 2026-09-17 and 2026-09-24.
- Recorded exercises included Regression: reproducible PubMed TMB/NSCLC 2024 query with QueryTranslation; EInfo DbInfo[0] fix, generalized to databases outside the fixer's own verification set; Regression: history-server queue, human RefSeq protein set; Regression: MARCH1 ambiguous gene symbol vs current usage-guide.md wording.
- Fix work addressed these recorded problems: Entrez.egquery() documented as core utility, doesn't exist on Biopython 1.88; breaks SKILL.md's decision table, examples/global_query.py,…; EInfo DbInfo indexed as a dict in SKILL.md's list_fields() and examples/database_info.py's db_info(); Biopython 1.88 returns a list-of-one; No progressive disclosure despite ~300-line SKILL.md; examples/ never linked from SKILL.md/usage-guide.md.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-experimental-design-batch-design

- Recorded 3 audit versions between 2026-09-15 and 2026-09-23.
- Recorded exercises included 24 plasma samples into 3 LC-MS batches, condition and sex balanced; 60 plasma samples into 4 TMTpro 16plex plexes with a pooled bridge channel; All cases on day 1, all controls on day 2: can ComBat rescue it?; Hidden batches in a MaxQuant log2 LFQ matrix with missing values.
- Fix work addressed these recorded problems: SVA block fails on matrices with missing values; No verification step after optimization; Bridge/reference-channel layout not shown.
- The published source version recorded 97/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-experimental-design-multiple-testing

- Recorded 4 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included BH plus Storey q-value on 18,000 synthetic DE p-values with planted truth; BH versus BY under positive block and negative pairwise dependence, 400 replicates; Forty synthetic enrichment terms, none truly enriched, plus a pi0 stability sweep; IHW with mean expression as covariate against plain BH, 18,000 genes.
- Fix work addressed these recorded problems: IHW has no failure-mode coverage; canonical ihw(pvalue ~ mean_expression, data = de_table, alpha = 0.05) segfaults; q-value one-liner unreliable on small families; qvalue(pvalues) throws or gives bad pi0-hat below ~1000 tests; BH-to-BY rule prescribes a large power loss on an undiagnosable symptom.
- The published source version recorded 92.4/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-experimental-design-power-analysis

- Recorded 4 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included Bulk RNA-seq replicate sizing (CV=0.3, 1.5-fold, 80% power) confirmed by simulation; Fixed-budget allocation: 20M reads x 4 samples vs 10M reads x 8 samples; n=2/group boundary case, plus a near-impossible 1.05-fold at 95% power target; scRNA-seq disease-vs-control: 3 patients x 10k cells vs 10 patients x 3k cells.
- Fix work addressed these recorded problems: scRNA-seq route (powsimR) ships no runnable code; ATAC/ChIP/methylation route ships no runnable code; Proteomics route ships no runnable code, separate from its multiplicity gap below.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-experimental-design-randomization-blocking

- Recorded 4 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included Experimental unit / pseudoreplication: 300 cells x 4+4 mice, true n?; Restricted (block) randomization of 30 embryos across 3 days + run-order randomization; Blocking on a near-noise factor (cage) with only 2 blocks available; Split-plot: 3 sequencing lanes (whole plot), 2 WT/2 KO per lane (sub-plot).
- Fix work addressed these recorded problems: Split-plot section's anti-conservative claim had no worked whole-plot-fixed-effect example (only sub-plot fixed effect shown); No caution that RCBD block-variance estimates are unreliable with very few blocks; Related Skills list duplicated near-verbatim across SKILL.md and usage-guide.md.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-experimental-design-sample-size

- Recorded 4 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included Bulk RNA-seq sizing from a literature dispersion (20k genes, 5% DE, FC 1.5, disp 0.2); Size the full study from a 4-sample (2v2) pilot using DESeq2 dispersions; Budget fixed at n=6 - what power and true FDR? And an unreachable 1.2-fold target; scRNA-seq donors versus cells at a fixed 30k-cell budget.
- Fix work addressed these recorded problems: ssizeRNA_vary called with scalars errors on every call; Worked example returns NA and NaN as its headline answers; PROPER and powsimR routes ship with no executable pattern.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-geo-data

- Recorded 4 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Breast cancer RNA-seq search + live SuperSeries/SubSeries check; GSE147507 -> SRR via pysradb (preferred path); GSE470 series matrix parse + Sample_data_processing audit; PubMed->GEO citation link, shipped vs corrected PMID.
- Fix work addressed these recorded problems: examples/geo_from_pubmed.py hardcodes PMID 32228226, labeled Blanco-Melo et al. 2020 *Cell*, but that PMID is a different paper (*Emerg…; examples/search_geo.py's detect_super_series() raises ValueError: Invalid mode: 'rt' on every call (gzip.GzipFile(..., mode='rt') has no…; examples/geo_to_sra.py's gse_to_srr_entrez() fallback raises TypeError: a bytes-like object is required, not 'str' on current Biopython….
- The published source version recorded 90.9/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-interaction-databases

- Recorded 5 audit versions between 2026-10-03 and 2026-10-03.
- Recorded exercises included STRING ID resolution, confidence tiers, channels, physical network, hubs (examples/string_network.py); STRING + OmniPath + SIGNOR directed graph with provenance (examples/interaction_query.py); BioGRID LT physical interactions with the registered key; key-leak retest with real and fake keys; SIGNOR signed, directed records for TP53 and AKT1 (signor_for_gene).
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 87/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-isoform-switching

- Recorded 4 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included SKILL workflow block verbatim on synthetic 3v3 (DEXSeq) and 6v6 (satuRn), shuffled SRR IDs, plus null…; Manual DRIMSeq-DEXSeq-stageR block verbatim on synthetic 6v6 (and 3v3), shuffled IDs; Real chrX 2 GBR v 2 YRI: SKILL block, shipped example (demo + real mode), count-route table and cause tests; Consequence block verbatim (ORFs, sequences, CPC2, hmmscan + converter, Pfam) on synthetic and real chrX.
- Fix work addressed these recorded problems: Manual DTU stops at samples(d) (Biobase masks DRIMSeq); Default importIsoformExpression count route finds 0 switches on real chrX (vs 26 with raw counts); example stops "No genes were considered…; Shipped example is a banner plus functions that do not run.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-local-blast

- Recorded 3 audit versions between 2026-09-17 and 2026-09-24.
- Recorded exercises included Build+search custom protein DB (ref_proteins.fasta vs query_proteins.fasta), v5 + parse_seqids + hash_index,…; Cross-species dc-megablast: synthetic mouse cDNA (12%/28% diverged) vs synthetic human refseq RNA; Taxonomy-filtered blastp: v5 DB with -taxid_map, filter to human taxid (9606) via -taxids / -taxidlist; Short primer search (<25nt) against synthetic human reference, -task blastn-short.
- Fix work addressed these recorded problems: v4 was incorrectly described as unable to store per-sequence taxids; v4 filtering behavior was conflated with the v5-without-taxonomy-data no-op; -taxids/-taxidlist silently no-op without taxdb.tar.gz.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-long-read-splicing

- Recorded 4 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included FLAIR workflow (correct-collapse-quantify-diffSplice --test) on planted 3v3 HiFi and real LRGASP cDNA; IsoQuant discovery/quantification and Bambu with NDR 0.1; SQANTI3 classification and filtering, with CAGE and polyA support; Shipped example from a clean copy: hifi, ont, drna, +SR_JUNCTIONS, real ONT cDNA, real direct RNA.
- Fix work addressed these recorded problems: Shipped example aborts (isoquant.py, flair correct --genome, SQANTI3 --output <dir>, filter on IsoQuant GTF); flair correct --genome --shortread rejected by FLAIR 3.0.1; isoquant.py absent (M4); -uf prescribed for unstranded ONT cDNA (decision tree, usage-guide, example).
- The published source version recorded 91/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-machine-learning-atlas-mapping

- Recorded 6 audit versions between 2026-10-03 and 2026-10-03.
- Recorded exercises included scripts/scarches_annotation.py unmodified on the staged PBMC pair, run twice (seeded), then…; SKILL.md python blocks 1-3 executed as written (200/100/20/100 epochs) against a saved reference_model/; Held-out Monocytes: reference without Monocytes, map PBMC3k, curated markers, own distance gate; Held-out B cells: reference without B cells, map PBMC3k, curated markers, own distance gate.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 87/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-machine-learning-biomarker-discovery

- Recorded 3 audit versions between 2026-10-03 and 2026-10-03.
- Recorded exercises included Leakage-safe Pipeline, nested GridSearchCV and in-fold MRMRSelect (SKILL.md blocks 0-2) on Golub, with…; BorutaPy snippet and boruta_feature_selection.py; Elastic-net LogisticRegressionCV with scoring pinned to accuracy: stated size table and partition dependence; scripts/stability_selection.py on Golub: determinism, unit invariance, permuted-label null and every stated….
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 88/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-machine-learning-model-validation

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included Nested CV against flat CV on a real hERG ECFP4 classifier; Feature-selection and preprocessing leakage on data with zero true signal; Group-aware CV with chemical scaffold as the unit of independence; The scikit-learn calibration API drift the Skill predicts.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-machine-learning-omics-classifiers

- Recorded 5 audit versions between 2026-10-03 and 2026-10-03.
- Recorded exercises included Core Workflow snippet (StandardScaler + LogisticRegressionCV elastic net) on real Golub ALL/AML, 70/30…; class_weight=balanced vs probability calibration on a risk model (known linear generative model, 8%…; SMOTE placement and "no AUC gain" claim (imblearn Pipeline vs resample-before-CV; known linear model, 8 draws); Probability Calibration snippet (FrozenEstimator + isotonic) on Golub (tiny calibration fold) and on a….
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 88/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-machine-learning-prediction-explanation

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included TreeSHAP on a hERG ECFP4 random forest, with module aggregation before ranking; The central claim: does conditional SHAP credit a feature the model never uses?; Permutation importance under correlated predictors; Background choice and the silent feature_perturbation='auto' flip.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-machine-learning-survival-analysis

- Recorded 5 audit versions between 2026-10-03 and 2026-10-03.
- Recorded exercises included SKILL.md fit and evaluation blocks run verbatim on GBSG2 (686 patients), stratified held-out split; scripts/cox_regression.py (synthetic, Coxnet vs RSF, Uno C, AUC(t), IBS vs KM baseline); Competing risks: scripts/competing_risks_cif.py plus tiny hand-computed table, 1-KM vs Aalen-Johansen; Metric-direction traps and deep models: lifelines/sksurv C signs, Harrell vs Uno under censoring, pycox….
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 87/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-metabolomics-isotope-tracing

- Recorded 3 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included IsoCor natural-abundance correction of synthetic U-13C5-glutamine areas; AccuCor correction of real accucor extdata vs shipped ground truth; Steady-state boundary check + IsoCor length-mismatch error; Tracer-selection guidance for PPP vs glycolysis (decision-tree reasoning).
- Fix work addressed these recorded problems: Steady-state check compares only the last timepoint pair, letting a still-decelerating series pass as plateau; Common Errors table's "half-defined resolution" text is more specific than the real error; AccuCor snippet doesn't document its default file-write side effect; auditor's first run wrote into the installed package's own extdata/.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-metabolomics-lipidomics

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included lipidr end-to-end: ISTD normalize -> de_analysis on synthetic ground-truth data; Goslin honest resolution-level canonicalization of 7 lipid names; SPLASH/EquiSPLASH internal-standard design for PC/PE/TG/Cer classes; Shotgun (direct-infusion) elevated LPC 16:0 -- artifact or biology?.
- Fix work addressed these recorded problems: Goslin honest-downgrade (get_lipid_string(LipidLevel.MOLECULAR_SPECIES)) raises unhandled RuntimeException for names parsed at or below…; lipidr's importer can't parse the ;O2/;O1/;O3 sphingoid suffix this Skill's own hierarchy table documents; a name like Cer 18:1;O2/16:0…; No explicit practice-boundary statement; the correct refusal of a patient-diagnosis question (audit Input 7) relied on general model….
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-metabolomics-metabolite-annotation

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included matchms library match with score+peak floor on synthetic MS/MS; SIRIUS formula/fingerprint/structure/CANOPUS chain on a library-absent feature; MetFrag structure ranking for a feature with no library spectrum; MS1-only accurate mass + isotope pattern, no MS/MS.
- Fix work addressed these recorded problems: Common Errors table + Version Compatibility note + code comment claim missing precursor_mz makes ModifiedCosine "score all zero"; matchms…; MetFrag named as one of three annotation routes with zero executable guidance (no params.txt skeleton, unlike SIRIUS's full bash block); matchms library-matching code takes max(pairs, ...), so a tied library match (the isomer wall the prose warns about) can never be surfaced….
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-metabolomics-msdial-preprocessing

- Recorded 3 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included Build DDA console command, import AlignResult into R, filter honestly; DIA/SWATH console command and ABF input requirement; GC-EI data on MS-DIAL 5 -- is GC-MS supported?; Parse an existing AlignResult.txt into pandas and map annotation tags to MSI levels.
- Fix work addressed these recorded problems: MsdialConsoleApp lcmsdda/lcmsdia do not exist; "MS-DIAL 5-alpha excludes GC-MS" / GC-EI needs MS-DIAL 4; Silent MSI-level bug porting the R filter idiom to Python (pandas auto-bool-cast).
- The published source version recorded 95.5/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-metabolomics-normalization-qc

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included QC-RSD/D-ratio filter + QC-RSC drift correction on real MTBLS79 (2488x172, 38 QC, 8 batches), validated on…; PQN urine normalization + dilution-vs-phenotype guardrail check (synthetic, clean and confounded dilution…; Mechanism-aware imputation: diagnose MNAR vs MAR, impute with QRILC vs missForest, compare to wrong-method; Drift correction attempted with only 3 QC injections in a batch (below the Skill's 5-6 sparse-QC threshold).
- Fix work addressed these recorded problems: QCRSC(minQC=5) on a batch with fewer QCs neither errors nor warns; silently returns every feature as all-NA; pqn_normalisation()'s documented return exposes no per-sample factor, so the Skill's own phenotype-correlation guardrail has no API to call; "ComBat under imbalance" failure-mode entry doesn't distinguish partial imbalance (didn't reproduce the effect at 85/15 in the audit) from….
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-metabolomics-pathway-mapping

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included ORA on 12 TCA-cycle-adjacent compounds; SKILL.md's flagship background-correction fix; Mummichog/PSEA on a full 1500-feature synthetic negative-mode table (R_all background); Mummichog fed significant-features-only background (the Skill's own named pitfall); FELLA network diffusion on 6 KEGG compound IDs (live KEGG graph build).
- Fix work addressed these recorded problems: Documented background-correction ORA path is unrunnable: SetMetabolomeFilter(mSet, TRUE) alone never restricts the background (needs the…; MetaboAnalystR silently sends compound lists to a remote API, undisclosed; Mummichog/PSEA prerequisites are incomplete (RJSONIO/fitdistrplus missing).
- The published source version recorded 92.3/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-metabolomics-statistical-analysis

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included Welch t-test + explicit BH FDR on synthetic case/control data with a detection-rate-confound block; PCA with explicit Pareto scaling and QC-clustering check on real MTBLS79 data; Permutation-validated OPLS-DA reliability probe (10 seeded runs) + Pareto-vs-UV scaling comparison; Per-metabolite linear mixed model for a 4-timepoint longitudinal design, adjusting for BMI.
- Fix work addressed these recorded problems: No escape-hatch guidance for individual-patient-adjacent requests (audit Input 6: "my patient's homocysteine is elevated, should they take…; Hotelling T2 / PCA outlier check named in the Decision Tree row but never demonstrated with code; pca@suppLs$outlierDF is NULL for a plain…; PCA code block gives no warning that opls() cannot tolerate NAs; the auditor had to add an ad hoc per-feature median imputation just to run….
- The published source version recorded 98/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-metabolomics-targeted-analysis

- Recorded 3 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included Weighted calibration + IS-normalized quantification of unknown plasma samples; IS-strategy advisory: 40-analyte panel, one global internal standard; LOD/LLOQ from blank scatter + single-transition (no qualifier) defensibility; Ion-ratio confirmation + IS-normalized matrix factor across 6 lots (planted interference).
- Fix work addressed these recorded problems: SKILL.md requires both intra-day and inter-day precision acceptance but gives no formula for inter-day; a naive pooled SD across days can…; No output-format template for the final deliverable; Trigger description is jargon-dense (MRM/SRM/%RE vocabulary).
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-metabolomics-xcms-preprocessing

- Recorded 3 audit versions between 2026-09-16 and 2026-09-22.
- Recorded exercises included 12-file KO/WT faahKO cohort -> full feature table (detect/align/group/fill); UHPLC/Q-Exactive tight-peakwidth CentWave + QC-anchored PeakGroupsParam alignment; 2-file (1 case/1 control) profile-mode (uncentroided) input; CAMERA redundancy collapse on the Input-1 feature table.
- Fix work addressed these recorded problems: PeakGroupsParam(minFraction=0.85, ...) — SKILL.md's own commented alternative-alignment example — fails with a cryptic low-level error…; featureValues() can retain NA cells after fillChromPeaks (240/6888 in the audit's run) with no SKILL.md guidance on the case; Redundancy Collapse code block shows only library(CAMERA); running it against a saved xdata in a fresh session fails with could not find….
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-microbiome-amplicon-processing

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Multi-run 16S V4 paired DADA2 pipeline (real fixture, 2 runs, 10 samples); Low-biomass decontam using real blank-control metadata; V3-V4 near-zero merge rate diagnosis (truncation budget); Fungal ITS2 processing with ITSxpress + truncLen=0.
- Fix work addressed these recorded problems: SKILL.md's inline DADA2 example (truncLen=c(240,160)) and examples/dada2_workflow.R (truncLen=c(240,200)) both truncate longer than the…; P2: no ITS fixture exists to verify the ITS analysis path end-to-end; P2: no reproducibility/seed guidance in the DADA2 examples.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-microbiome-differential-abundance

- Recorded 3 audit versions between 2026-09-19 and 2026-09-24.
- Recorded exercises included ALDEx2 + ANCOM-BC2 consensus, control vs treated (real fixture, 200 taxa x 40 samples, 17 planted DA taxa); ANCOM-BC2 with Age+Sex covariates, BH vs default Holm, passed_ss required; LinDA repeated-measures mixed model vs naive pseudo-replicated model (longitudinal fixture, 12 subjects x 3…; ZicoSeq with Batch covariate; zero-variance-feature crash trap.
- Fix work addressed these recorded problems: LinDA section's own code crashes on a real phyloseq object (invalid class "sample_data" object); GUniFrac::ZicoSeq() crashes outright on zero-variance features; no SKILL.md code or warning; 4 of 8 frontmatter-named tools (ZicoSeq, MaAsLin3, LEfSe, DESeq2) had no runnable code anywhere in the Skill.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-microbiome-diversity-analysis

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Full alpha+beta diversity, PERMANOVA+betadisper on a real phyloseq fixture (control vs treated); Sampling-depth choice: quantify min(sample_sums) vs plateau-based depth; No phylogenetic tree available -- non-phylogenetic fallback; Real QIIME2 core-metrics-phylogenetic pipeline on the moving-pictures 16S dataset (4 body sites) +….
- Fix work addressed these recorded problems: examples/diversity_analysis.R crashes with "object 'Group' not found" at the adonis2 call — meta <- data.frame(sample_data(ps_rare)) never…; SKILL.md's Beta Diversity/PERMANOVA section had no repeated-measures/pseudo-replication guidance, unlike the parallel Alpha Diversity…; P2: NMDS never mentioned; RPCA named in Tool Taxonomy/Decision Tree but only a one-line CLI reference, no worked example.
- The published source version recorded 97/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-microbiome-functional-prediction

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Full PICRUSt2 pipeline on real moving-pictures 16S ASVs (770 ASVs, 34 gut/palm/tongue samples, DADA2-denoised); QIIME2 .qza path via q2-picrust2 plugin (feature table + rep-seqs already in QIIME2); PICRUSt2 on out-of-reference synthetic ASVs (poor alignment, expected quality-gate refusal); Mandatory NSTI distribution + dropped-read-fraction QC report on real PICRUSt2 output.
- Fix work addressed these recorded problems: Mandatory NSTI snippet hardcodes marker_predicted_and_nsti.tsv.gz, which does not exist in real PICRUSt2 2.6.3 output; Standard biom convert --to-tsv export crashes picrust2_pipeline.py after ~9 min of real compute, no warning in docs; "Report ≥2 CoDA tools, intersection" guidance silently returns an empty/wrong consensus because MaAsLin2 sanitizes MetaCyc IDs….
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-microbiome-qiime2-workflow

- Recorded 2 audit versions between 2026-09-19 and 2026-09-19.
- Recorded exercises included Casava per-sample paired-end import; Alternate import on-ramps (V2 manifest + BIOM); Import/type/visualization error handling; Metadata typing, provenance replay, export/extract.
- Fix work addressed these recorded problems: Phred-offset error described as "silently mis-decoded quality scores" in 3 places (Common Errors, Manifest-Phred failure-mode section,…; No explicit guard in SKILL.md against hand-editing a classifier .qza's embedded metadata.yaml to bypass the scikit-learn version-pin check….
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-microbiome-taxonomy-assignment

- Recorded 4 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included QIIME2 classify-sklearn, region-matched (extract-reads -> fit-classifier-naive-bayes) on real 16S V4 ASVs; DADA2 assignTaxonomy + addSpecies, region-matched, on the same 770 real V4 ASVs; Full-length vs. region-matched classifier: quantifying SKILL.md's central 'Trap 1' claim on real data; DECIPHER IdTaxa, trained (LearnTaxa) on the real region-matched SILVA subset, on the same 770 ASVs.
- Fix work addressed these recorded problems: assignTaxonomy() non-deterministic without set.seed() — fires Skill Veto T3; DECIPHER IdTaxa flattening code (x$taxon[match(ranks, x$rank)]) silently returns 100%-NA against a LearnTaxa()-trained set; No memory-budget warning for training against the full SILVA/GTDB reference (OOM-crashed the audit VM twice).
- The published source version recorded 89/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-molecular-descriptors

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included Physicochemical panel and six drug-likeness rule sets over 1,000 real compounds; Construct every fingerprint in the taxonomy table and check the tabulated properties; ECFP radius/diameter convention and the bit-collision claim, measured; 3D shape descriptors over a conformer ensemble for flexible drug-like molecules.
- Fix work addressed these recorded problems: MMFF status 1 discarded every flexible 3D ensemble; MAP4 was claimed as a tested PyPI dependency though no distribution was obtainable; Shipped 3D helper was unseeded.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-molecular-io

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included 3,224 SMILES to a property-carrying SDF and back; The SDF V2000 999-atom limit and the SetForceV3000 fix; The Open Babel route for MOL2, PDBQT and InChI; Aromaticity models -- the Skill's 'most common silent error'.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 99/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-molecular-standardization

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included Prepare 3,966 ChEMBL hERG IC50 rows as a deduplicated QSAR training set; ChEMBL get_parent_mol vs LargestFragmentChooser on 12 registry salt/solvate/co-crystal forms; Eight tautomer pairs: does the ChEMBL route register them twice, and does InChIKey rescue it?; Join a 300-compound ChEMBL slice against a synthetic in-house registry with known ground truth.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-ncbi-datasets-cli

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Download phiX174 reference genome (GCF_000819615.1) + assembly stats; BRCA1 gene metadata across Mammalia (dataformat tsv gene); Dehydrated discovery + rehydrate for a single accession; NCBI ortholog set for human BRCA1 (dataformat tsv gene).
- Fix work addressed these recorded problems: "Gene metadata across species" pattern (SKILL.md's flagship example, gene_metadata.sh's own default): --taxon Mammalia on summary gene…; dataformat --fields names stale across every shipped code block (genome and gene); bulk_dehydrated.sh's aria2c awk transform silently corrupts every downloaded filename.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-ortholog-inference

- Recorded 4 audit versions between 2026-10-03 and 2026-10-03.
- Recorded exercises included Ensembl Compara single gene, MARCH1 rename, five-gene zebrafish batch with per-symbol status…; Cross-resource TP53: Compara, OMA 1:1, OrthoDB verified group (cross_resource.py, unchanged file); KEGG Orthology gene to KO to members (kegg_orthology.py, unchanged); Client retry/timeout guards on the changed module (local HTTP stub), OrthoDB null parser, batch status schema.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 87/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-outlier-splicing-detection

- Recorded 2 audit versions between 2026-09-20 and 2026-09-20.
- Recorded exercises included FRASER2: one patient vs 29 controls, planted outliers (synthetic); OUTRIDER expression outliers, n=30 synthetic counts + OUTRIDER's own simulator; FRASER with a cohort below the stated minimum (n=12 and n=8); LeafcutterMD annotation-free outliers on the same synthetic cohort.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-pathway-enrichment-visualization

- Recorded 4 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included Collapse GO-DAG redundancy with simplify() before dotplot, report term counts; GSEA plots preserving direction (NES dotplot, ridgeplot, gseaplot2); Small significant-term-count gene-concept network and similarity-map judgment call; compareCluster faceted dotplot plus enrichment map and treeplot.
- Fix work addressed these recorded problems: upsetplot()'s ggupset Suggests-only dependency undocumented; treeplot() on a compareClusterResult crashes under the installed enrichplot/ggplot2; No guidance for zero surviving terms/sets.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-pathway-go-enrichment

- Recorded 4 audit versions between 2026-09-15 and 2026-09-23.
- Recorded exercises included GO BP ORA on a proteomics hit list with the quantified proteome as universe; Effect of omitting universe= on a null hit list; UniProt accessions and a 15-protein hit list; GO-DAG redundancy: simplify per ontology, ont='ALL', groupGO.
- Fix work addressed these recorded problems: enrichResult column list stale (missing RichFactor/FoldEnrichment/zScore); simplify() on ont='ALL' — Skill predicted "redundancy not removed, or an error"; examples/go_all_ontologies.R reads an unshipped de_results.csv, cannot run standalone.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-pathway-gsea

- Recorded 4 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included Full DESeq2 table, Wald-stat ranking, GO BP preranked GSEA; MSigDB Hallmark GSEA plus gseKEGG against the live API; edgeR QL table: no Wald stat, symbol IDs, 300 duplicate rows, exact-zero p-values, unsorted; Per-sample pathway activity matrix with GSVA and ssGSEA.
- Fix work addressed these recorded problems: nPerm claimed "an argument error"; actually accepted with a warning, silently downgrades fgseaMultilevel to fgseaSimple; pmax(pvalue, 1e-300) clamp makes exact-zero p-values ~75x the strongest measured gene's weight, >16% of total ranking weight, erasing…; Bare limma::camera(...) inherits limma's preset inter.gene.cor = 0.01, giving no protection.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-pathway-kegg-pathways

- Recorded 3 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included Human KEGG ORA (enrichKEGG) with explicit measured universe; Human KEGG GSEA (gseKEGG) on full ranked log2FC vector, no cutoff; Prokaryotic KEGG ORA on E. coli locus tags, keyType='kegg', no OrgDb/bitr; Signed-topology perturbation (SPIA) on human named log2FC + universe, direction/topology, and why not….
- Fix work addressed these recorded problems: graphite + runSPIA code pattern never runs as documented; SPIA's own worked example omits set.seed(); No explicit agent instruction to refuse/warn on missing background gene set.
- The published source version recorded 90/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-pathway-reactome

- Recorded 4 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included Reactome ORA on 97 significant genes vs. 3000-gene measured background; Reactome GSEA on a 3000-gene ranked vector with fixed seed; Verifying the documented SYMBOL-not-ENTREZ failure mode; Hierarchy dedup: are 4 top-ranked pathways one finding or four?.
- Fix work addressed these recorded problems: examples/reactome_gsea.R ranked every gene by rnorm(), null by construction — 0 enriched terms every run, plotting branch dead code; examples/reactome_ora.R's universe was every SYMBOL in org.Hs.eg.db (~20,000+ genes) — almost the same size as the implicit ~11,200-gene…; SKILL.md's Per-Method Failure Modes and Common Errors described the SYMBOL/ENSEMBL-without-bitr failure as "zero rows"/"0 rows"; the….
- The published source version recorded 89/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-pathway-wikipathways

- Recorded 4 audit versions between 2026-09-17 and 2026-09-23.
- Recorded exercises included ORA on ~63 significant human genes (SYMBOL) against a ~3080-gene tested universe, top 15 by p.adjust with…; GSEA (gseWP) on the full ranked gene list, no cutoff; universe=NULL vs a matched tested-gene universe, on both a null gene list and the planted-signal list; Reproducible analysis: pin a dated GMT, split the term field, run enricher on the pinned sets, report the date.
- Fix work addressed these recorded problems: SKILL.md's/usage-guide.md's worked reproducibility example and the shipped examples/wikipathways_explore.R hardcode…; enrichWP()/gseWP() return NULL silently on a wrong organism string (e.g. 'zebrafish' vs 'Danio rerio'), reproduced live by the audit, but…; No documented recovery when the computed archive_date itself 404s.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-pharmacophore-modeling

- Recorded 3 audit versions between 2026-09-19 and 2026-09-22.
- Recorded exercises included Receptor-based pharmacophore from a real co-crystal (PDB 1HSG, HIV-1 protease + indinavir precursor MK1) via…; Shipped examples/pharmacophore.py feature-family prefilter, real HIV protease inhibitors vs real unrelated…; SKILL.md's own ligand-based EmbedPharmacophore code block, run verbatim on real molecules (single-active edge…; PLIP water-bridge detection, direct contrast test of the Skill's own documented failure mode on 1HSG….
- Fix work addressed these recorded problems: shared_feature_types_prefilter/has_feature_types conformer embedding has no fixed random seed (non-reproducible geometry across runs); feature_family_prefilter silently rejects a true positive (ritonavir) with no diagnostic; No troubleshooting row for PLIP's ValueError: inchikey is not a recognised Open Babel format on Windows (openbabel-wheel ships no InChI….
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-phylo-bayesian-inference

- Recorded 2 audit versions between 2026-09-15 and 2026-09-15.
- Recorded exercises included 12-taxon GTR+I+G MrBayes run with convergence proof vs known tree; User's finished 20k-generation 60-taxon run: write up clade PPs; Near-zero internode (0.0005): is PP support trustworthy?; Stepping-stone GTR+G vs JC with 2lnBF.
- Fix work addressed these recorded problems: stoprule=yes stopval=0.01 halts before scalars are sampled; Advice without runnable commands (assertion rate); RWTY burnin=25 is trees.
- The published source version recorded 91/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-phylo-distance-calculations

- Recorded 3 audit versions between 2026-09-15 and 2026-09-24.
- Recorded exercises included 20-specimen COI barcode: K2P NJ tree with bootstrap; Deep 12-taxon gene: TN93+gamma FastME with 500 bootstraps; Saturation pre-flight on a 4x-deep 12-taxon alignment; GC-heterogeneous 8 taxa: LogDet vs stationary corrections.
- Fix work addressed these recorded problems: Bio.Phylo bootstrap_consensus with NJ gives deflated support; Bootstrap drops the point tree's gamma; Saturation gate is a test the agent cannot run.
- The published source version recorded 97/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-phylo-divergence-dating

- Recorded 2 audit versions between 2026-09-15 and 2026-09-15.
- Recorded exercises included MCMCTree fossil-calibrated dating, prior-only then approximate likelihood; Temporal signal + LSD2 tip-dating on heterochronous virus data; Virus samples spanning 0.4 yr: no temporal signal; BEAST2 prior-only vs with-data runs and the Skill's MCC comparison snippet.
- Fix work addressed these recorded problems: Bio.Phylo MCC snippet reads .confidence (None) and zips mismatched nodes; BDparas without flag; bare usedata = 2; >/< "silently ignored" row false on 4.10.
- The published source version recorded 90/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-phylo-modern-tree-inference

- Recorded 2 audit versions between 2026-09-11 and 2026-09-15.
- Recorded exercises included 12-taxon 1.2 kb gene: ModelFinder + UFBoot2 + SH-aLRT; 10-locus supermatrix: MFP+MERGE partitioning, -p linkage; 6 short (250 bp) isolates, two identical; AU test: Primates+Rodents constraint vs ML tree.
- Fix work addressed these recorded problems: --gcf with --scfl in one call exits with "Do not specify --scf or --gcf with --scfl"; iqtree2 not on PATH after bioconda install (IQ-TREE 3 ships iqtree3/iqtree); False --alrt/-bb/-nt flag-form warnings (item 10).
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-phylo-species-trees

- Recorded 2 audit versions between 2026-09-15 and 2026-09-15.
- Recorded exercises included 10-species radiation, 150 loci: gene trees -> wASTRAL/ASTRAL + CFs; Anomaly zone: concatenation vs coalescent, 400 loci (+2000-locus stress test); 120-bp loci with missing taxa: gene-tree error vs ASTRAL; ILS vs introgression from q1/q2/q3 on 200 loci.
- Fix work addressed these recorded problems: --gcf + --scfl in one call exits 2; ASTRAL units statement wrong for ASTER; ASTRAL-Pro command omits gene->species map.
- The published source version recorded 90/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-phylo-tree-io

- Recorded 2 audit versions between 2026-09-15 and 2026-09-15.
- Recorded exercises included BEAST MCC -> side table of posteriors/HPDs, then plain Newick; Split IQ-TREE 2.4.0 SH-aLRT/UFBoot labels; Tip names with spaces, quotes, commas, non-ASCII; join to metadata; MrBayes posterior .t sets and .con.tre.
- Fix work addressed these recorded problems: Phylo.convert to Newick "annotations dropped" is false; Bio.Phylo fails on MrBayes .con.tre and names foreign NeXML tips by otu id; No encoding or quoted-label guidance.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-phylo-tree-manipulation

- Recorded 3 audit versions between 2026-09-15 and 2026-09-24.
- Recorded exercises included Root IQ-TREE ML tree on OutA+OutB, check ingroup monophyly; Induced subtree of 8 non-clade taxa, distances preserved (Bio.Phylo + ete3); Collapse UFBoot<95 and zero-length branches on dual-label IQ-TREE tree; No outgroup, deep tree with rate shift: midpoint vs MAD vs MinVar.
- Fix work addressed these recorded problems: Outgroup guard refuses valid outgroups on IQ-TREE trees; root_with_outgroup gives a trifurcating root; collapse_all silently no-ops on SH-aLRT/UFBoot labels; Zero-length tolerance 1e-8 misses IQ-TREE 1e-6.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-phylo-tree-visualization

- Recorded 4 audit versions between 2026-09-15 and 2026-09-23.
- Recorded exercises included IQ-TREE SH-aLRT/UFBoot treefile to support-labelled vector phylogram (Bio.Phylo); Colour great apes red and Old World monkeys blue, ladderize, PDF+SVG; 320-tip coronavirus tree unreadable as rectangular; colour by host; BEAST2 MCC chronogram with 95% HPD bars and posterior labels.
- Fix work addressed these recorded problems: support_label ignores IQ-TREE dual labels; hard-coded "Bootstrap" title; Bio.Phylo rerooting shifts node-held support; geom_range default re-centres asymmetric HPDs.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-pileup-generation

- Recorded 4 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included Archived real human text pileup, defaults, output format, and pysam table; Archived planted SNVs, read access, helper functions, and shipped CLI; Archived defaults, flags, BAQ, depth-cap, and hostile-input checks; Archived bcftools germline, BCF, joint, and parallel-by-contig flows.
- Fix work addressed these recorded problems: pysam examples print pileup_column.n as depth (differs at 1087/1157 real positions); Ref-skips counted as DEL in every pysam helper; pileup_text is not a pileup (no ^ $ +N -N, no qualities, disagrees with own depth).
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-population-genetics-rare-variant-association

- Recorded 3 audit versions between 2026-09-15 and 2026-09-24.
- Recorded exercises included regenie masks with SKAT-O and ACAT-O; SKAT, burden and SKAT-O in R; Mixed directions and LoF-only architecture; SAIGE-GENE+ for an imbalanced trait.
- Fix work addressed these recorded problems: SAIGE-GENE+ --annotation_in_groupTest separators reversed; regenie step-1 block omits --bt; rare_variant_test.sh runs step 1 on rare-variant genotypes.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-pose-validation

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included PoseBusters dock config on a real Vina-redocked benzamidine pose vs 3PTB receptor; MMFF94 relative strain energy on the same docked pose, using the Skill's ligand_strain_mmff verbatim; Deliberately implausible poses (clash, stretched bond, puckered ring) plus a control good pose; redock config with the real 3PTB co-crystal benzamidine as mol_true: RMSD + PB-valid reconciliation.
- Fix work addressed these recorded problems: SKILL.md's dock config table claimed "all checks except RMSD reference"; Standalone aromatic_planarity() snippet claimed a 0.25 Å cutoff; examples/validate_poses.py shipped no test fixtures; __main__ was a no-op print.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-protac-degraders

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included CRBN PROTAC series for a kinase target (linker enumeration + properties); Ternary complex prediction request (PRosettaC unavailable); Malformed attachment points (double bond, two dummies, invalid SMILES); CRBN to VHL E3 switch, same target and linker set.
- Fix work addressed these recorded problems: primary_tool (PRosettaC) and every named ternary predictor (DeepTernary, AlphaFold3, Boltz-1/2, HADDOCK) are unexecutable locally -- web…; No shipped example for cooperativity-alpha / DC50/Dmax/hook-effect workflows; DC50/Dmax fit underestimates Dmax with no warning when the hook onset is close to DC50 (audit input 9: planted 65 -> fitted 51, noise-free….
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-proteomics-data-import

- Recorded 4 audit versions between 2026-09-11 and 2026-09-25.
- Recorded exercises included MaxQuant proteinGroups.txt -> clean log2 LFQ matrix; DIA-NN 1.9 report.parquet -> protein x run matrix at 1% FDR; Mixed DDA/DIA/AIF mzML: precursor m/z, charge, isolation-window width; Intensity vs LFQ vs iBAQ on a run with a loading failure, plus QFeatures.
- Fix work addressed these recorded problems: DIA-NN import omits Global.PG.Q.Value; DIA missingness labelled MCAR against the Skill's own diagnostic; DIA block keeps PG.MaxLFQ zeros (-inf after log2).
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-proteomics-dia-analysis

- Recorded 3 audit versions between 2026-09-11 and 2026-09-24.
- Recorded exercises included DIA-NN library-free on 8 Exploris runs -> 1% FDR protein matrix; Filter existing report.parquet for a cohort matrix; explain matrix count; Staggered 2x8 Th overlapping-window data: conversion and search; FragPipe DDA library via EasyPQP -> DIA-NN library-based search.
- Fix work addressed these recorded problems: easypqp library snippet fails as written; Staggered-window guidance overstated and incomplete; Mass-accuracy advice contradicts DIA-NN docs.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-proteomics-differential-abundance

- Recorded 3 audit versions between 2026-09-11 and 2026-09-23.
- Recorded exercises included MaxQuant LFQ proteinGroups, 4 v 4, two acquisition days; Two TMT10plex batches, PSM counts, DEqMS; Heavy MNAR missingness and on/off proteins, no imputation; 12 v 12 plasma, Python-only Welch + BH.
- Fix work addressed these recorded problems: proDA block calls a coefficient that does not exist; limma and DEqMS blocks break on real MaxQuant matrices; treat() silently drops trend and robust.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-proteomics-peptide-identification

- Recorded 3 audit versions between 2026-09-11 and 2026-09-22.
- Recorded exercises included pyOpenMS search of a synthetic mzML + DECOY_ FASTA, 1% FDR idXML; q-values from a Comet .txt (concatenated, 5 rows per scan); 33-PSM single-bait pulldown, all q = 0; rank-1 decoy variant; PEP vs q-value: PI wants the 'safer' PEP <= 0.01 list.
- Fix work addressed these recorded problems: Elias-Gygi 2d/(t+d) given as the separate-search estimator; peptide_ids = [] fails on pyOpenMS 3.5; Table snippet not rank-1, no +1.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-proteomics-protein-inference

- Recorded 3 audit versions between 2026-09-11 and 2026-09-22.
- Recorded exercises included pyOpenMS grouping + picked-group FDR on a 1%-PSM-FDR idXML (SYNTHETIC, 6,150 PSMs); Interpret MaxQuant proteinGroups.txt: leading protein, razor vs unique, two-peptide filter; IP-MS map with indistinguishable TPM1 isoforms, a subset fragment and few decoys; 'is isoform 2 present?'; EPIFANY Bayesian inference + group FDR on a PEP-scored idXML.
- Fix work addressed these recorded problems: BasicProteinInferenceAlgorithm called parsimony; 8.6% true FDP at 1%; EpifanyAlgorithm absent; [] fails; bytes accessions; Example drops indistinguishable proteins as subsumable; lead order-dependent.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-proteomics-proteomics-qc

- Recorded 3 audit versions between 2026-09-11 and 2026-09-23.
- Recorded exercises included QC a MaxQuant LFQ run (8 samples, 2 batches) before limma; DIA-NN 1.9 report.parquet: per-run IDs at 1% global FDR and matrix QC; Failed-loading T4 hidden by MaxLFQ (user says LFQ boxplots look fine); TMT 2x10-plex channel-loading balance with pooled reference 131.
- Fix work addressed these recorded problems: raw_sample_qc counts MaxQuant zeros as quantified; Un-normalised column never named; no ID threshold; pca_batch_check crashes / centres failed sample.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-proteomics-ptm-analysis

- Recorded 4 audit versions between 2026-09-11 and 2026-09-23.
- Recorded exercises included Regulated phosphosites adjusted for protein abundance (MSstatsPTM); Multiplicity expansion of a Phospho (STY)Sites table; Phospho-only run, no global proteome; Motif enrichment + kinase activity from adjusted sites.
- Fix work addressed these recorded problems: MSstatsPTM block fails: append assertion, data.type = 'LF'; Protein dataset never built (evidence_prot missing); Melt adds a bogus Intensity run.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-proteomics-quantification

- Recorded 3 audit versions between 2026-09-11 and 2026-09-23.
- Recorded exercises included MSstats TMP summarization of MaxQuant evidence.txt (8 runs); iq::maxLFQ vs MSstats TMP sensitivity on the same peptides; SILAC H/L with heavy-only proteins, 93% labeling, limma downstream; TMT10 reporter extraction + impurity correction from mzML.
- Fix work addressed these recorded problems: MaxQuant read.table silently drops rows at apostrophes; makeImpuritiesMatrix(x = 10) blocks non-interactive runs; MBimpute = FALSE contradicts "censored-value handling" / MSstats-AFT.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-proteomics-spectral-libraries

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Prosit-via-Koina prediction + iRT calibration; Local MS2PIP + DeepLC prediction (no Koina dependency); NCE scan + malformed peptide inputs; OpenSWATH format conversion + decoy generation.
- Fix work addressed these recorded problems: OpenSwathDecoyGenerator's real data requirements undocumented; Shuffle decoy generation non-deterministic, no documented seed control; Reference DeepLC snippet stale against deeplc 4.5.0 (DeepLC class removed).
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-qsar-modeling

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included RF + ECFP4 hERG regression on a scaffold split with an applicability-domain gate on the report; chemprop 2.x training and prediction, following the CLI blocks as a pair; Conformal prediction for calibrated intervals, and whether the version bound is real; Leverage and Mahalanobis, the two remaining tabulated AD methods, on the recommended representation.
- Fix work addressed these recorded problems: Prediction omitted the training featurizer and failed at 517 vs 300 inputs; Leverage and Mahalanobis were presented as raw-fingerprint AD methods; Scaffold/time split caveat was disconnected from conformal exchangeability.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-reference-operations

- Recorded 3 audit versions between 2026-09-20 and 2026-09-23.
- Recorded exercises included Prepare a reference for GATK/Picard: index, dict, chrom.sizes for 12 filename shapes; Extract regions / revcomp / subset / pysam multi-region, error table; chr22 vs 22, GRCh38 flavour/contig tables against real files, reheader recipe (BAM, CRAM, VCF); Consensus from real BAMs: SKILL commands, viral command, real-data agreement, version notes.
- Fix work addressed these recorded problems: Reheader recipe fails on full hg38 headers (map emits na), leaves 0-byte output; -T described as filling low coverage; Description omits renaming / extraction / CRAM.
- The published source version recorded 90/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-remote-homology

- Recorded 3 audit versions between 2026-09-19 and 2026-09-22.
- Recorded exercises included Pfam domain annotation of PRKACA (P17612) via hmmscan --cut_ga; MMseqs2 twilight-zone search: default vs -s 7.5 sensitivity; Sequence-only structural homology via Foldseek + ProstT5 (no structure available); PSI-BLAST 3-iteration PSSM build and reuse per SKILL.md's saved-PSSM pattern.
- Fix work addressed these recorded problems: examples/pfam_annotation.sh awk line labels hmmscan's query-accession/qlen ($5,$6) as full_evalue/full_score; Documented foldseek --version setup-verification command fails on every Foldseek subcommand (Invalid Command, exit 1); No escape hatch for a user demanding unqualified certainty, dropping statistics.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-sam-bam-basics

- Recorded 3 audit versions between 2026-09-20 and 2026-09-23.
- Recorded exercises included Regression: inspect the real human PE BAM (header, FLAG decode, coordinates, counts, regions, view_bam.py,…; Regression: BAM<->SAM<->CRAM conversions with samtools, pysam and convert_formats.sh; Regression: synthetic edge SAM (unmapped-with-position, secondary/supplementary, hard/soft clips, N, MAPQ…; Regression: CRAM offline (resolution order, REF_CACHE recipe, proving a CRAM readable, archive lossless).
- Fix work addressed these recorded problems: samtools view -c claimed to prove a CRAM's reference is reachable; view_bam.py crashes unindexed/empty/SAM; Mapped 0 / Unmapped 0 on CRAM; unlabelled 0-based; unmapped shown as None:-1 + None; Overlapping multi-region queries duplicate records silently.
- The published source version recorded 91/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-sashimi-plots

- Recorded 3 audit versions between 2026-09-20 and 2026-09-23.
- Recorded exercises included ggsashimi grouped 3v3 planted BAM overlay; ggsashimi missing-BAM and unknown-contig guards; Batch plot of significant planted rMATS SE event; rmats2sashimiplot helper on matching planted SE data.
- Fix work addressed these recorded problems: rmats2sashimiplot block: -t SE rejected; exit 0 and empty Sashimi_plot/ on colour/group mistakes; group_def.txt never defined; library(leafviz) / run_leafviz() do not exist; annotation code unexplained; Jutils venn comma list; rmats.tsv name.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-scaffold-analysis

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included Bemis-Murcko chemotype census of 3,224 hERG compounds; The shipped scaffold_split at three train fractions, checked for leakage and representativeness; R-group decomposition, on the worked example and on a real 53-member series; The documented scaffold failure modes, one by one.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-shape-similarity

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included USRCAT pre-filter + Open3DAlign rescore, 10-compound synthetic library, run twice for determinism; Scaffold-hop candidate search with thresholds calibrated on a labeled reference set (not the illustrative…; Failure-mode handling: malformed SMILES, empty string, disconnected-fragment (salt) input; Conformer-ensemble shape search (n_conf=20) over a 3-compound library using SKILL.md's….
- Fix work addressed these recorded problems: SKILL.md's shape_search_ensemble discarded an entire library molecule if even 1 of n_conf MMFF-optimized conformers failed to converge,…; Disconnected-fragment (salt) SMILES like [Fe+2].[Cl-].[Cl-] pass MMFFHasAllMoleculeParams trivially and generate meaningless conformers…; ShaEP example (shaep -q query.mol2 target.mol2 ...) assumes .mol2 files already exist; RDKit has no Mol2 writer and the SMILES->mol2 step….
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-similarity-searching

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included Analog search around astemizole across 3,224 hERG compounds; Butina clustering and what a 0.4 cutoff actually guarantees; Tversky alpha=1, beta=0 as a substructure-like ranking; Activity-cliff diagnosis at Tanimoto >= 0.85 and >= 2 log units.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-batch-integration

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included Harmony on two 10x lanes, with the Skill's own before/after evaluation; scVI then scANVI with 60% of labels hidden; BBKNN when only clustering and UMAP are needed; Seurat v5 IntegrateLayers - the R snippet the Skill actually prints.
- Fix work addressed these recorded problems: Seurat RPCA exceeds its default future globals limit; FastMNNIntegration and scVIIntegration are not bare Seurat symbols; Harmony theta wording did not give a useful scale.
- The published source version recorded 97/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-cell-annotation

- Recorded 3 audit versions between 2026-09-16 and 2026-09-25.
- Recorded exercises included CellTypist Immune_All_Low on 6,049 clustered PBMCs; SingleR against celldex HumanPrimaryCellAtlas, 3,023 cells; Query whose var_names are Ensembl IDs, not symbols; Azimuth pbmcref on the real public 10x PBMC 1k v3 run.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 91/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-cell-communication

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included LIANA rank_aggregate consensus on real annotated PBMC 1k v3 data; CellPhoneDB v5 statistical (permutation) specificity test on the same real PBMC data; CCC requested with only one cell-type group present; NicheNet: which Monocyte ligand best explains activated-vs-naive CD8 T cell DE genes.
- Fix work addressed these recorded problems: SKILL.md's CellPhoneDB code block crashes with a multiprocessing RuntimeError on Windows under score_interactions=True; CellPhoneDB permutation p-values non-deterministic (debug_seed defaults to -1, never set in the documented call); Frontmatter promises "comparing communication across conditions" but no method has runnable code for it.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-clustering

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included Cluster 6,049 QC'd PBMCs; choose n_pcs and resolution defensibly; Seurat route with a resolution vector and clustree; Sorted CD4 capture - one population or several?; Subcluster a 1,107-cell CD4 T cluster - two routes compared.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-cnv-inference

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included inferCNV reference-based malignant/CNV calling; copyKAT reference-free aneuploid/diploid call; Flat CNV profile / CNV-quiet tumor interpretation; Numbat allele-aware subclone/LOH resolution.
- Fix work addressed these recorded problems: inferCNV malignant-calling code reads infercnv.observations.txt, which 1.22's default HMM=TRUE no longer writes; Numbat df_allele documented with 7 columns; check_allele_df() also requires cM, REF, ALT; SCEVAN recommended in the method table with zero example code.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-data-io

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Load raw 10x PBMC h5 (Python), keep non-GEX features; Load filtered 10x PBMC h5 into Seurat (R); Convert rich AnnData (layers/raw/obsm/categorical) to SCE via schard and zellkonverter, verify nothing…; Move a Seurat object to h5ad for Python, verify no layers were dropped (usage-guide.md's own example prompt).
- Fix work addressed these recorded problems: zellkonverter::readH5AD(reader='R', raw=TRUE) silently fails to recover .raw from an h5ad the .raw group genuinely exists in; usage-guide.md's "Move this Seurat object to h5ad" example prompt has no backing code anywhere in SKILL.md; scale.data workaround shows extraction but not persistence.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-differential-abundance

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included propeller on 8 donors: did any population change?; Milo, the Skill's primary_tool, on the same 8-donor design; scCODA, and does the reference cell type really change the verdict?; One donor per condition - can anything be concluded?.
- Fix work addressed these recorded problems: Milo (primary tool) false negative on the canonical case; No seed anywhere; propeller transform default named wrongly.
- The published source version recorded 90/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-doublet-detection

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included scDblFinder per sample on 8 PBMC lanes, ground-truth scored; Scrublet in scanpy, per sample, rate from recovered cells; FACS-sorted CD4 T cells - one population, is the doublet call meaningful?; Legacy DoubletFinder route on an existing Seurat pipeline.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-hashing-demultiplexing

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included HTODemux, 4-sample equal pooling, clean staining; hashsolo, 2-hashtag scanpy AnnData (Skill's own advertised use case); demuxmix rescue of an oversized Negative pile (weak staining); Choosing genetic vs. hashtag demultiplexing (no hashing performed).
- Fix work addressed these recorded problems: sce.pp.hashsolo silently classifies 100% of cells "Negative" at exactly 2 hashtags (number_of_noise_barcodes defaults to len(cols)-2 = 0),…; demuxmix() can throw an uncaught glm.nb error ("missing value where TRUE/FALSE needed") on underdispersed HTO background instead of…; No runnable example for demuxEM/pegasus or GMM-Demux.
- The published source version recorded 92/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-lineage-tracing

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Build CRISPR-scar tree, collapse mutationless edges, report missingness; Solver panel under homoplasy/dropout, Robinson-Foulds + triplets-correct; Build character matrix from raw aligned barcode reads; CoSpar clone+state integration, Day2 vs Day4 fate bias.
- Fix work addressed these recorded problems: pip install cassiopeia-lineage cospar scanpy installs a broken, wrong-API package; Cassiopeia/CoSpar hard numpy conflict (numpy<2 vs numpy>=2); NeighborJoiningSolver raises DistanceSolverError as documented.
- The published source version recorded 90/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-markers-annotation

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included Scanpy markers on 12 clusters, then manual PBMC labelling; Seurat FindAllMarkers and the v5 default changes; A sorted CD4 population - marker ranking with only one group; Aggregate to pseudobulk before handing off to DESeq2.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-metabolite-communication

- Recorded 2 audit versions between 2026-09-19 and 2026-09-24.
- Recorded exercises included Run MEBOCOST and filter on permutation FDR; Which cells express PGE2 enzymes vs. sensors; Mouse-cased gene symbols against species='human'; Compare metabolite communication tumor vs normal.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 97/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-multimodal-integration

- Recorded 4 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included CITE-seq: DSB denoise from empty droplets, then WNN, report modality weights (R); totalVI: train on CITE-seq MuData, get denoised protein + foreground probabilities (Python); DSB denoising when only the filtered/cell matrix is available (no true empty droplets); 10x Multiome: PCA on RNA, TF-IDF/LSI on ATAC, drop depth-correlated LSI, joint WNN (R).
- Fix work addressed these recorded problems: totalVI code block non-deterministic as shipped (audit: max abs latent diff 0.9723 unseeded vs 0.0000 seeded, 2 runs each); Same reproducibility gap in GLUE's VAE training, not covered by the audit run (scglue not run: no Windows wheel); DSB's own documented failure mode (filtered-only matrix as empty_drop_matrix) produces no error/warning, silently wrong output (audit:….
- The published source version recorded 91/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-perturb-seq

- Recorded 4 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Assign guides with a mixture model, run Mixscape to remove escapers (real papalexi_2021 CROP-seq data); Calibrated SCEPTRE test with a negative-control calibration check first (R); All cells for target gene X are Mixscape 'NP' -- is the gene non-functional?; Rank perturbations by E-distance and run the permutation E-test in a pinned PCA embedding.
- Fix work addressed these recorded problems: assign_mixture_model needs undocumented JAX extra; Shipped pertpy_analysis.py KeyError (perturbation columns on mdata.obs, not adata.obs); Milo example structurally incompatible with pooled Perturb-seq design.
- The published source version recorded 88/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-preprocessing

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included 8-donor PBMC drug study, QC through PCA with per-sample MAD; SoupX ambient removal on Cell Ranger raw+filtered, 8 samples + real PBMC 1k; 120-nucleus low-complexity capture where MAD collapses to zero; Normalization choice for a set containing a composition-divergent population.
- Fix work addressed these recorded problems: SoupX called autoEstCont() without clusters; Universal 8% mitochondrial cap could erase valid populations; Packaged Scanpy and Seurat examples retained flat cutoffs.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-scatac-analysis

- Recorded 5 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included 10X scATAC fragments through QC, TF-IDF/LSI, clustering (Signac); Framework choice for a 1.2M-nuclei atlas; DepthCor flags component 3, not component 1; Consensus peak calling + depth-aware differential accessibility.
- Fix work addressed these recorded problems: SKILL.md's documented RunChromVAR(obj, genome=...) throws could not find function "RunChromVAR" on Signac 1.17.1 — removed upstream in…; biovizBase is a required but undocumented dependency — GetGRangesFromEnsDb() throws Please install biovizBase unless already present; NucleosomeSignal() / TSSEnrichment() (and StringToGRanges()) deprecated in Signac 1.17.x.
- The published source version recorded 96/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-splicing

- Recorded 3 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included BRIE2 per-cell PSI on real Smart-seq2 (130 mouse E6.5 cells); BRIE2 two-group differential splicing on planted Smart-seq-like data with dropout; Sparse real plate data: 130 cells, most cell-event pairs with 0 reads, random-label null; MARVEL plate workflow: SKILL block on the package demo, then corrected chain on planted PSI truth.
- Fix work addressed these recorded problems: MARVEL block: AssignModality(EventType=), CompareValues(n.cells=, psi.delta=) do not exist; level missing; MARVEL Exp = read.table(row.names=1) loses gene_id -> CheckAlignment(gene) fails; MARVEL event tables / IntronCounts never sourced; GTF read with rtracklayer::import.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-single-cell-trajectory-inference

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included PAGA continuum test + DPT rooted on a known marker (Paul15 real hematopoietic progenitor data); Palantir fate probabilities + entropy at a real branch point (Paul15); PAGA continuum-vs-discrete test on real PBMC 1k (mature, discrete cell types); scVelo RNA velocity, dynamical mode, on real pancreatic endocrinogenesis data.
- Fix work addressed these recorded problems: mode='dynamical'/mode='stochastic' crash inside scvelo 0.3.4's own internals against numpy 2.5.3/pandas 3.0.5; CellRank fate-mapping block needs allow_overlap=True and a Windows multiprocessing guard; PAGA's threshold=0.03 isolated-cluster heuristic doesn't flag real discrete PBMC types.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-splice-variant-prediction

- Recorded 3 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included SpliceAI D50 on the 10-variant GRCh37 chrX panel, parsed and labelled with the fixed splice_parsers…; Pangolin exactly as the fixed Skill directs on GRCh38 GENCODE v45 (create_db.py, -m False/True, canonical vs…; MMSplice per the Skill block on the GRCh37 panel and on GRCh38 (GENCODE v45 basic GTF); Malformed and edge records: REF mismatch, 150-bp deletion (> 2*D), intergenic, multi-allelic, insertion,….
- Fix work addressed these recorded problems: Pangolin recipe unrunnable (deps, create_db, mask); -m True erases the GLA pseudoexon gain; mask trade-off with numbers; Concordance snippet fails on real outputs.
- The published source version recorded 90/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-splicing-qc

- Recorded 3 audit versions between 2026-09-20 and 2026-09-24.
- Recorded exercises included Known vs novel junction classification of a library with planted class fractions (RSeQC junction_annotation +…; Junction saturation on planted deep / mid / shallow libraries, real chrX, and contig-name mismatch; Strandedness verification (infer_experiment) on planted dUTP / forward / unstranded / leaky PE libraries,…; Per-junction read counts, overhang and ">=10 reads" helpers vs planted CIGARs, multi-mappers, real chrX,….
- Fix work addressed these recorded problems: Known/novel snippet prints 0.0% / 0.0% (RSeQC writes " annotated" with a leading space); junction_annotation / junction_saturation exit 1 without Rscript; Rscript unlisted; generate_qc_report crashes on a BAM without spliced reads (EmptyDataError).
- The published source version recorded 90/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-splicing-quantification

- Recorded 5 audit versions between 2026-10-03 and 2026-10-03.
- Recorded exercises included Fresh rMATS-turbo 4.4.0 on real chrX 2v2 BAMs, then parse per the Skill (inline snippet, 5 types x JC/JCEC); Planted hand-checkable SE data: effective-length PSI and IncFormLen statements; SUPPA2 PSI via run_suppa2_quantification, write_suppa_tpm and filter_reliable_events on planted and real chrX…; parse_rmats_output on engineered NA/low-read tables for all 5 types x JC/JCEC, and on zero-event files.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 85/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-sra-data

- Recorded 5 audit versions between 2026-09-17 and 2026-09-24.
- Recorded exercises included Regression: ENA-mirror single-accession happy path via SKILL.md's own inline snippet, real accession; Regression: shipped download_batch.sh, all-good 3-accession batch, real accessions; NEW: independent synthetic missing-fastq_ftp fixture, inline snippet; THE CRUX: mixed 3-accession batch -- real good, synthetic bad (middle), real good.
- Fix work addressed these recorded problems: ENA-mirror off-by-one column bug: SKILL.md's "preferred default" snippet and examples/download_batch.sh both assumed…; No dbGaP / controlled-access guidance anywhere (grep-confirmed absent); an agent would attempt a controlled-access human accession the same…; pigz called with no Windows fallback in download_single.sh, download_batch.sh(N/A, no pigz call)/prefetch_large.sh and 3 SKILL.md code….
- The published source version recorded 91/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-substructure-search

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included PAINS_A triage of 800 screening hits, flag-not-delete; HTS library prep with the prescribed PAINS_A + BRENK + ZINC combination; The five documented SMARTS failure modes, each reproduced and each fix tested; Custom reactive-warhead filter over covalent drugs, plus the covalent-design exemption.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 94/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-uniprot-access

- Recorded 4 audit versions between 2026-10-03 and 2026-10-03.
- Recorded exercises included Entry parse, bulk search with total, stream, ID mapping (examples/uniprot_query.py); Isoforms and cross-references (examples/isoforms_and_xrefs.py, list_isoforms, xref_summary); ID mapping job handling: full stream, unmapped inputs, stuck and failed jobs, obsolete accessions; Search syntax, field names and corpus-size claims in SKILL.md.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 88/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-variant-annotation

- Recorded 4 audit versions between 2026-09-11 and 2026-09-27.
- Recorded exercises included rsID + grpmax FAF + ClinVar + bcftools csq triage; Parse VEP CSQ on the MANE block; Usage-guide rare-variant recipe on a VCF with its own INFO/AF; One calibrated predictor instead of four.
- Fix work addressed these recorded problems: Piped annotate -a <vcf> recipes fail; bcftools csq lacks --phase; Rare recipe clobbers cohort INFO/AF.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-variant-calling-filtering-best-practices

- Recorded 3 audit versions between 2026-09-15 and 2026-09-24.
- Recorded exercises included GATK hard filters on an 8-sample joint callset; bcftools replica of the GATK filter plus cyvcf2 version; VQSR requested for an 8-sample panel; Genotype-level no-calls before cohort metrics.
- Fix work addressed these recorded problems: filter_variants.sh fails at bcftools concat on multi-contig input; Somatic post-filter FMT/AF[0] rejected; obvious AF[0:0] tests the normal; Usage-guide allele-balance expression does not parse.
- The published source version recorded 91/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-variant-normalization

- Recorded 4 audit versions between 2026-09-11 and 2026-09-27.
- Recorded exercises included GATK-like vs FreeBayes-like caller comparison; ClinVar 'absent' homopolymer deletion; Multiallelic split with Number=A/R/G/. fields and rejoin; vt- vs bcftools-normalized cohorts disagree.
- Fix work addressed these recorded problems: Recommended atomize -> split order emits spurious * records; csq advice omits --phase; Example hides bcftools errors behind 2>/dev/null.
- The published source version recorded 98/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-vcf-basics

- Recorded 2 audit versions between 2026-09-11 and 2026-09-24.
- Recorded exercises included Inspect header, samples, table and type counts; Allele balance from AD and QUAL vs GQ; Missing vs hom-ref and PL/GQ relationship; Is this gVCF analysis-ready?.
- Fix work addressed these recorded problems: Wrong bcftools query -H tip in usage guide; Update the bgzip error string; Add a gVCF variant-site extraction recipe.
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-vcf-manipulation

- Recorded 3 audit versions between 2026-09-11 and 2026-09-24.
- Recorded exercises included Cohort from single-sample VCFs: merge default vs -0; Stitch per-chromosome files; --naive; overlapping windows; Three-caller set operations; Subset cases; stale INFO; -R vs -T.
- Fix work addressed these recorded problems: reheader cannot fix chr1-vs-1 record naming; concat sample-order fix wrong; -R overlapping-region duplication claim.
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-vcf-statistics

- Recorded 5 audit versions between 2026-09-15 and 2026-09-27.
- Recorded exercises included Callset QC summary; Swap / duplicate / relatedness screen; Should every HWE failure be dropped?; Contamination check from the VCF.
- Fix work addressed these recorded problems: Het allele-balance one-liner mixes all samples (0.729); plot-vcfstats needs pdflatex/tectonic; Quick PASS count treats FILTER '.' as not passing (item 14).
- The published source version recorded 91/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-virtual-screening

- Recorded 3 audit versions between 2026-09-19 and 2026-09-23.
- Recorded exercises included Dock benzamidine into trypsin's S1 pocket (PDB 3PTB), full receptor+ligand prep; Screen a 5-compound library against the same active site, rank by affinity; Pocket is unknown on this structure -- find candidate binding sites before docking; Rescore my Vina poses with GNINA CNN scoring for better ranking.
- Fix work addressed these recorded problems: mk_prepare_receptor.py is not the installed command name; --read_pqr route crashes on insertion-code residues (e.g. trypsin/chymotrypsin numbering); No seed/determinism guidance for Vina (pose ranks 2+ vary run-to-run).
- The published source version recorded 95/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-workflows-crispr-screen-pipeline

- Recorded 7 audit versions between 2026-09-16 and 2026-10-04.
- Recorded exercises included HAP1 and A375: qc.py (real, grouped, default pattern, QC-passing resampled) then rra.py on the QC-passing…; HAP1: BAGEL2 fc/bf/pr with --seed 42 (route commands), then consensus.py on three methods; count route: FASTQ to guide counts with library.csv columns as the route text states; Cancer line: cn_correction.R (WSL crispr-ccr, CRISPRcleanR 3.0.1) then rra.py on raw and corrected tables.
- Fix work addressed these recorded problems: BAGEL2 bf unseeded, destabilizes Step 7 Tier consensus (Skill Veto T3 FAIL, Research Veto M3 FAIL); Shipped "Replicate Pearson" QC formula conflates replicate and non-replicate pairs (Research Veto M3 FAIL); Step 2's and Step 6a's own worked examples don't compose (hard MAGeCK error).
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-workflows-metabolomics-pipeline

- Recorded 3 audit versions between 2026-09-16 and 2026-09-23.
- Recorded exercises included Stage1->Stage2 xcms-to-pmp orientation hand-off, real faahKO feature table; Real Stage2->Stage4 chain on MTBLS79 (cow/sheep serum, 8 batches, 38 QCs); Bundled reference example, examples/metabolomics_workflow.R, run as shipped; Stage3->Stage5 MSI-confidence gate ("only Level 1-2 enter identified-ORA").
- Fix work addressed these recorded problems: Stage2->Stage4 hand-off crashes on real multi-batch data: imputation is a comment, not code; Stage1->Stage2 orientation comment contradicts its own code; Two of three governing commitments (mode-lock, MSI-confidence gate) have no enforcing code anywhere.
- The published source version recorded 91/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-workflows-proteomics-pipeline

- Recorded 2 audit versions between 2026-09-15 and 2026-09-23.
- Recorded exercises included Regression: MaxQuant LFQ proteinGroups.txt, 4 control vs 4 treated, two batches, to a differential protein…; Regression: DIA-NN report.parquet for the same 8 samples, through the DIA-NN block to limma; Three-condition dose design (Control / LowDose / HighDose, n=4 each, two batches) through the Complete R…; "Our sample_annotation.csv is not in the same order as the intensity columns -- does that matter?".
- Fix work addressed these recorded problems: MSstats block silently truncates MaxQuant tables (Input 5); DIA-NN block feeds -Inf into limma (Input 2); SILAC block crashes and reports unadjusted p-values (Input 7).
- The published source version recorded 93/100 and Production Ready; this historical label does not certify later normalized drafts.

## bio-workflows-scrnaseq-pipeline

- Recorded 2 audit versions between 2026-09-16 and 2026-09-24.
- Recorded exercises included 8 Cell Ranger samples to annotated cell types, end to end; The Complete R Workflow block, run verbatim; The Scanpy alternative path, run verbatim; 'My collaborator only sent the filtered matrix'.
- A separate fix pass and verification account was recorded; its detailed trace has been retired.
- The published source version recorded 97/100 and Production Ready; this historical label does not certify later normalized drafts.
