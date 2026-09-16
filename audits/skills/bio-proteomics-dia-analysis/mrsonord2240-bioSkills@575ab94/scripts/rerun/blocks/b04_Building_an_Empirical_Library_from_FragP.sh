# Real easypqp subcommands: convert, library, insilico-library (NOT a convert --format diann).
# 1) per run: pepXML + spectra (mzXML; MGF for timsTOF) -> <run>.psmpkl and <run>.peakpkl ('psmpkl'/'peakpkl' in the names)
easypqp convert --pepxml interact-run1.pep.xml --spectra run1.mzXML --psms run1.psmpkl --peaks run1.peakpkl
# 2) library from all pickles; --psmtsv requires --peptidetsv
easypqp library \
    --psmtsv psm.tsv --peptidetsv peptide.tsv \
    --rt_reference irt.tsv \
    --out library.tsv \
    *.psmpkl *.peakpkl
# With psm.tsv + peptide.tsv given, easypqp ignores --psm/--peptide/--protein_fdr_threshold (FragPipe already filtered).
# FragPipe's DIA workflow can emit a DIA-NN-format library directly -- prefer that when in FragPipe.
