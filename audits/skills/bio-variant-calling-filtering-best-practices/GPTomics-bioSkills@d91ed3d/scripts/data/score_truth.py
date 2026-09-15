"""Score a filtered SYNTHETIC cohort VCF against data/cohort_truth_classes.tsv (auditor helper).
usage: python score_truth.py <kept_positions.tsv(chrom\tpos)> [label]"""
import sys, csv, collections
truth = {(r['chrom'], int(r['pos'])): r['class'] for r in csv.DictReader(open(sys.argv[0].rsplit('/',1)[0] + '/cohort_truth_classes.tsv' if '/' in sys.argv[0] else 'cohort_truth_classes.tsv'), delimiter='\t')}
kept = set()
for line in open(sys.argv[1]):
    c, p = line.strip().split('\t')[:2]
    kept.add((c, int(p)))
tot = collections.Counter(truth.values()); k = collections.Counter(truth[x] for x in kept if x in truth)
label = sys.argv[2] if len(sys.argv) > 2 else ''
print(label, ' '.join(f'{c}:{k[c]}/{tot[c]}' for c in ['true_snp', 'true_homalt', 'true_indel', 'excess_het', 'artifact_snp', 'artifact_indel']))
