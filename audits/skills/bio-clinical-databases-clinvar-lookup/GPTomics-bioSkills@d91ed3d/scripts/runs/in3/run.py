import importlib.util, time, collections
import pandas as pd
spec = importlib.util.spec_from_file_location('ex', 'clinvar_query.upstream_copy.py')
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)

print('== parse_clnsig_conflict on real CLNSIGCONF strings ==')
for line in open('conflicts.tsv'):
    vid, sig, rev, conf = line.rstrip('\n').split('\t')
    print(vid, conf, '->', ex.parse_clnsig_conflict(conf))
print('parse_clnsig_conflict(None) ->', repr(ex.parse_clnsig_conflict(None)), '(return type differs from the dict returned otherwise)')

print('\n== clinvar_summary star_rating for real review-status strings ==')
ids = [l.split('\t')[0] for l in open('conflicts.tsv')][:3] + ['17661', '209232', '438907']
rows = []
for vid in ids:
    s = ex.clinvar_summary(int(vid)); time.sleep(0.4)
    rows.append({'variation_id': vid, **s})
    print(vid, '|', s['germline_class'], '|', s['germline_review_status'], '| star_rating =', s['star_rating'])
print('\nREVIEW_STATUS_STARS keys:', list(ex.REVIEW_STATUS_STARS))
df = pd.DataFrame(rows)
kept = ex.filter_by_star_and_freshness(df, min_star=2, max_age_months=36)
print('\nfilter_by_star_and_freshness(min_star=2, max_age_months=36) keeps:', kept[['variation_id', 'germline_class', 'germline_review_status', 'germline_last_evaluated', 'star_rating']].to_string(index=False) if len(kept) else 'nothing')
print('age_months computed:', df.assign(d=pd.to_datetime(df['germline_last_evaluated'], errors='coerce'))[['variation_id', 'germline_last_evaluated']].to_string(index=False))
