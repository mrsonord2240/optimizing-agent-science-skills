python miss.py
echo "-- bcftools: sites where SYN_S6 is ./. --"; bcftools view -H -i 'GT[5]="mis"' ../../data/cohort.vcf | wc -l
