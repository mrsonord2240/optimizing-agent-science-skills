#!/bin/bash
# Input 3 - conversion as the Skill writes it (NOT executed: no msconvert build here).
for r in *.raw; do
  msconvert "$r" --mzML --filter "demultiplex optimization=overlap_only"          # Skill's filter, verbatim
done
# What ProteoWizard/Skyline and DIA-NN docs additionally require (auditor note, not in the Skill):
#   msconvert "$r" --mzML --32 --filter "peakPicking vendor msLevel=1-" --filter "demultiplex optimization=overlap_only massError=10.0ppm"
