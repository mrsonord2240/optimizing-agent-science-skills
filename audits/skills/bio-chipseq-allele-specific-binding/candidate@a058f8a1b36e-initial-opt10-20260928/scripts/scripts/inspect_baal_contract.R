args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L) {
    stop("usage: inspect_baal_contract.R OUTPUT")
}

samples <- data.frame(
    SampleID = c("HCC1395_FOXA1_rep1", "HCC1395_FOXA1_rep2"),
    Tissue = "TNBC",
    Target = "FOXA1",
    BAM = c("rep1.wasp.bam", "rep2.wasp.bam"),
    Peaks = c("rep1.narrowPeak", "rep2.narrowPeak"),
    Group = "HCC1395"
)

dirname_result <- tryCatch(
    dirname(samples),
    error = function(e) paste0("ERROR: ", conditionMessage(e))
)

required_sample_columns <- c(
    "group_name", "target", "replicate_number", "bam_name", "bed_name"
)
candidate_het_columns <- c("CHROM", "POS", "REF", "ALT", "AF")

simulated_report <- list(HCC1395 = data.frame(
    ID = "rs1", CHROM = "chr1", POS = 1L, REF = "A", ALT = "G",
    AR = 0.6, Corrected.AR = 0.58, isASB = TRUE
))
candidate_report_result <- tryCatch({
    asb_table <- simulated_report
    asb_sig <- asb_table[
        asb_table$isASB == TRUE & abs(asb_table$Corrected.AR - 0.5) > 0.1,
    ]
    paste0("rows=", nrow(asb_sig))
}, error = function(e) paste0("ERROR: ", conditionMessage(e)))

candidate_script <- paste0(
    "/mnt/openscience/wt/opt10-chipseq-asb/skills/",
    "bio-chipseq-allele-specific-binding/scripts/baalchip_workflow.R"
)
parse_result <- tryCatch({
    parse(file = candidate_script)
    "PASS"
}, error = function(e) paste0("ERROR: ", conditionMessage(e)))

lines <- c(
    paste("candidate_r_parse", parse_result, sep = "\t"),
    paste("candidate_samplesheet_type", class(samples)[1L], sep = "\t"),
    paste("official_constructor_dirname_result", dirname_result, sep = "\t"),
    paste("required_sample_columns", paste(required_sample_columns, collapse = ","), sep = "\t"),
    paste("candidate_sample_columns", paste(colnames(samples), collapse = ","), sep = "\t"),
    paste("required_columns_present", all(required_sample_columns %in% colnames(samples)), sep = "\t"),
    paste("candidate_het_columns", paste(candidate_het_columns, collapse = ","), sep = "\t"),
    paste("required_ID_present", "ID" %in% candidate_het_columns, sep = "\t"),
    paste("required_RAF_present", "RAF" %in% candidate_het_columns, sep = "\t"),
    paste("detached_cnv_bed_consumed", FALSE, sep = "\t"),
    paste("official_report_type", class(simulated_report)[1L], sep = "\t"),
    paste("candidate_report_index_result", candidate_report_result, sep = "\t")
)

writeLines(lines, args[[1L]], useBytes = TRUE)
