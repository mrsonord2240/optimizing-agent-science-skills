import json,sys
d=json.load(open(r'F:\OpenScience\audits\bio-outlier-splicing-detection\eval_report_bio-outlier-splicing-detection_result.json',encoding='utf-8'))
assert list(d.keys())==['meta','veto_gates','static_score','dynamic_score','final','key_strengths','recommendations']
c=d['static_score']['categories']; assert len(c)==8 and d['static_score']['subtotal']==sum(v['score'] for v in c.values())
for k,v in c.items(): assert 0<=v['score']<=v['max'] and v['note']
ins=d['dynamic_score']['inputs']; assert len(ins)==d['meta']['n_inputs']==7
for i in ins:
    assert i['basic']+i['specialized']==i['total']; assert 3<=len(i['assertions'])<=5
    assert i['assertions_passed']==sum(a['result']=='PASS' for a in i['assertions']); assert i['assertions_total']==len(i['assertions']); assert isinstance(i['executed'],bool)
assert d['dynamic_score']['execution_avg']==round(sum(i['total'] for i in ins)/7,1)
f=d['final']; assert f['static_weighted']==round(d['static_score']['subtotal']*0.4,1); assert f['dynamic_weighted']==round(d['dynamic_score']['execution_avg']*0.6,1); assert f['score']==round(f['static_weighted']+f['dynamic_weighted'])
assert 2<=len(d['key_strengths'])<=5
pr=[r['priority'] for r in d['recommendations']]; assert pr==sorted(pr)
assert d['dynamic_score']['assertion_pass_rate']['total']==sum(i['assertions_total'] for i in ins)
print('OK',f, d['dynamic_score']['assertion_pass_rate'], pr)
