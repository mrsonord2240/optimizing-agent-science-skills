import json
r = json.load(open('F:/OpenScience/audits/bio-data-visualization-upset-plots/eval_report_bio-data-visualization-upset-plots_result.json', encoding='utf-8'))
sc = r['static_score']; assert sc['subtotal'] == sum(c['score'] for c in sc['categories'].values()), 'static'
ins = r['dynamic_score']['inputs']; assert len(ins) == r['meta']['n_inputs']
for i in ins:
    assert i['basic'] + i['specialized'] == i['total']; a = i['assertions']; assert 3 <= len(a) <= 5
    assert i['assertions_passed'] == sum(x['result'] == 'PASS' for x in a) and i['assertions_total'] == len(a)
avg = round(sum(i['total'] for i in ins) / len(ins), 1); print('avg', avg, r['dynamic_score']['execution_avg'])
print('final', round(sc['subtotal'] * .4 + avg * .6, 1), r['final']['score'])
print('assertions', sum(i['assertions_passed'] for i in ins), sum(i['assertions_total'] for i in ins))
print('L1', sum(i['basic'] for i in ins) / 5, 'L2', sum(i['specialized'] for i in ins) / 5)
