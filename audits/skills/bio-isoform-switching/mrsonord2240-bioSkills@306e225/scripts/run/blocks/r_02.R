# ORFs: annotated CDS come with importRdata; predict only when the GTF had none
if (!any(aSwitchList$orfAnalysis$orf_origin == 'Annotation', na.rm = TRUE)) {
    aSwitchList <- analyzeORF(aSwitchList, orfMethod = 'longest', genomeObject = NULL)
}
aSwitchList <- analyzeAlternativeSplicing(aSwitchList, onlySwitchingGenes = TRUE)
dir.create('sequences', showWarnings = FALSE)
aSwitchList <- extractSequence(aSwitchList, onlySwitchingGenes = TRUE, pathToOutput = 'sequences/', writeToFile = TRUE)

# after running the external tools on sequences/:
aSwitchList <- analyzeCPC2(aSwitchList, pathToCPC2resultFile = 'cpc2_result.txt', removeNoncodinORFs = FALSE)
aSwitchList <- analyzePFAM(aSwitchList, pathToPFAMresultFile = 'pfam_scanfmt.txt')
# licence-gated, not run here: analyzeSignalP(pathToSignalPresultFile=), analyzeIUPred2A(pathToIUPred2AresultFile=)

aSwitchList <- analyzeSwitchConsequences(
    aSwitchList,
    consequencesToAnalyze = c('intron_retention', 'ORF_seq_similarity', 'NMD_status',
                              'coding_potential', 'domains_identified'),   # + one type per extra annotator imported
    dIFcutoff = 0.1
)
