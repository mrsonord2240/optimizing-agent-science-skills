# Diagnostic test inputs

## Input 1 - Canonical

Apply the documented paired-end WASP route to a coordinate-sorted ChIP-seq
BAM, preserve the paired-end remap contract, and verify the final retained
paired alignments and attrition counts.

## Input 2 - Variant A

Run the shipped HCC1395 cancer BaalChIP workflow with the stated sample sheet,
heterozygous variants, blacklist, imprinting intervals, sex handling, and
ASCAT copy-number BED. Verify from the live BaalChIP 1.38.0 contract that every
input is consumed and that the exported report is parsed with the actual
return type.

## Input 3 - Edge

Run the imprinted-locus and chrX filters on a three-row fixture. Confirm exact
retained rows and assess what happens when chromosome naming or interval
assemblies do not agree.

## Input 4 - Variant B

Run the documented RASQUAL route on the public bundled C11orf21 example.
Verify a finite 25-column result, convergence, feature routing, and whether the
candidate defines a cohort-scale reporting and multiple-testing contract.

## Input 5 - Stress

Attempt the documented AlleleSeq personalized-genome route in the prepared
bounded environment. Verify prerequisite completeness, inspect the generated
Make plan for populated read/sample variables, and classify inaccessible
legacy dependencies without substituting an unofficial toolchain.
