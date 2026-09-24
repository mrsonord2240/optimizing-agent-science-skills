python -c "import cyvcf2;print('cyvcf2',cyvcf2.__version__)"
python norm_check.py
echo "-- true count of records bcftools changes (reference-aware) --"
bcftools norm -m- -f ../../data/ref.fa -c x callerB.vcf.gz -Ou 2>&1 >/dev/null | tail -1
