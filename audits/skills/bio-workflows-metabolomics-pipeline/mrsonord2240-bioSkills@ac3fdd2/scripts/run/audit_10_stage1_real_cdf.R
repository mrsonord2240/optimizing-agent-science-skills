# Input 10: execute the current Stage 1 script on six real faahKO CDF files.
files <- c(
  'F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO/KO/ko15.CDF',
  'F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO/KO/ko16.CDF',
  'F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO/KO/ko18.CDF',
  'F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO/WT/wt15.CDF',
  'F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO/WT/wt16.CDF',
  'F:/OpenScience/audit-envs/untargeted-metabolomics-analyst/public-data/faahKO/WT/wt18.CDF'
)
stopifnot(all(file.exists(files)))
mzml_files <- files
pd <- data.frame(sample_group = c('QC', 'QC', 'QC', 'Control', 'Treatment', 'Treatment'), row.names = basename(files))
ionization_mode <- 'positive'
# The direct default backend launched 22 Windows RSOCK workers and made no output before the
# audit window; constrain the *audit runtime* to serial execution without changing the Skill.
BiocParallel::register(BiocParallel::SerialParam())
source('F:/OpenScience/wt/workflows-metabolomics-pipeline/workflows/metabolomics-pipeline/scripts/stage1_xcms_extract.R')
cat('Stage 1 extracted:', nrow(feat), 'features x', ncol(feat), 'samples.\n')
stopifnot(nrow(feat) > 0, ncol(feat) == length(files), nrow(defs) == nrow(feat))
if (!'mode' %in% colnames(defs)) {
  cat('MODE-LOCK FAILURE: defs$mode is absent after the shipped Stage 1 script.\n')
} else if (!all(as.character(defs$mode) == 'positive')) {
  cat('MODE-LOCK FAILURE: defs$mode does not preserve the supplied ionization mode.\n')
} else {
  cat('MODE-LOCK PASS: all feature rows retain positive mode.\n')
}
