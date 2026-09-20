#!/bin/bash
# NEW input 10, step 1: what do the callers named in the assay table actually filter by default?
# Only GATK (4.6.2.0) is installed; its own --help lists the default read filters. Manta/Strelka2/DeepVariant/clair3/Sniffles/cuteSV/
# GRIDSS/Delly/SvABA are not installed, so their rows stay UNVERIFIED (judged by reading, never by a run).
set -u
for t in HaplotypeCaller Mutect2; do
  echo "===== gatk $t --help (filters and MAPQ options)"
  gatk $t --help > /mnt/openscience/audits/bio-alignment-filtering/run/data/gatk_$t.txt 2>&1
  grep -n -i -E "mapping-quality|MappingQualityReadFilter|NotSecondary|NotSupplementary|NotDuplicate|PassesVendor|MappingQualityAvailable|WellformedReadFilter|MappedReadFilter|GoodCigar|ReadFilter" /mnt/openscience/audits/bio-alignment-filtering/run/data/gatk_$t.txt | head -40
done
echo "===== gatk Mutect2 -min-... arguments containing 'mapping'"
grep -n -i -B1 -A3 "minimum-mapping-quality" /mnt/openscience/audits/bio-alignment-filtering/run/data/gatk_Mutect2.txt | head -20
echo "===== gatk HaplotypeCaller: same"
grep -n -i -B1 -A3 "minimum-mapping-quality" /mnt/openscience/audits/bio-alignment-filtering/run/data/gatk_HaplotypeCaller.txt | head -20
