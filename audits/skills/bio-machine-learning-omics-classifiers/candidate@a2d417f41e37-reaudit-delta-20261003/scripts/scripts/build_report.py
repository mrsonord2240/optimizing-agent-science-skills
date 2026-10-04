import json
P=r'F:/optimizing-agent-science-skills/audits/skills/bio-machine-learning-omics-classifiers/candidate@906900fae480-reaudit2-lane3-20261003/'
R=r'F:/OpenScience/audits/bio-machine-learning-omics-classifiers/reaudit-delta-20261003/'
NEW='a2d417f41e37007d7a2a3ea4d76b744cf1be42485be95576f42dee806584616f'
r=json.load(open(P+'report.json',encoding='utf-8'))
m=r['meta']
m['description']="Use when building a classifier from expression, methylation, or variant data, choosing an algorithm for high-dimensional small-n data, or diagnosing a suspiciously perfect AUC."
m['audit_kind']="delta re-audit (frontmatter description trimmed to the Use-when clause; certified identity 906900fae480 scores carried forward)"
m['evaluated_on']='2026-10-03'
m['auditor_independent']=True
a=r['dynamic_score']['inputs'][6]['assertions']
a+= [
 {"text":"Delta qualifies: reverting edits.json on a scratch copy reproduces the certified identity 906900fa... and only the description: line of SKILL.md differs","result":"PASS","note":"scratch revert -> manifest 906900fae480655dca3808442d858f84b17aace68513ed281607842a0151276f, files=7, bytes=50806; diff -r of the tree shows one changed line (SKILL.md line 4); bytes 50806 -> 50363"},
 {"text":"New frontmatter parses as valid YAML and keeps name, category, tool_type, primary_tool, license, author unchanged","result":"PASS","note":"yaml.safe_load: 7 keys, description is one 176-character string"},
 {"text":"New description is accurate to the Skill and introduces no false statement; it states when to use the Skill","result":"PASS","note":"Each of the three Use-when cases (classifier from expression/methylation/variant data; algorithm choice for high-dimensional small-n data; suspiciously perfect AUC) is covered by SKILL.md sections and by the certified runs (inputs 1, 3, 6); the dropped method list and see-also pointers remain in the body (decision table lines 61-62, Related Skills lines 272-275)"},
]
inp=r['dynamic_score']['inputs'][6]
inp['assertions_passed']+=3; inp['assertions_total']+=3
r['dynamic_score']['assertion_pass_rate']={"passed":34,"total":36}
r['static_score']['categories']['agent_specific']['note']="Trigger is a plain Use-when clause covering the three entry cases; hand-offs to model-validation, biomarker-discovery, prediction-explanation and survival-analysis now live only in the body (decision table, Related Skills), so the description alone distinguishes this Skill less sharply (OC-013); scope of each rule is stated."
r['key_strengths'].insert(0,"Delta re-audit: the trimmed description is the only change to the certified bytes; reverting it reproduces identity 906900fa and the scores carry forward unchanged.")
r['recommendations'].append({
 "priority":"P2",
 "title":"OC-013 Trimmed description drops the cues that separate this Skill from model-validation and prediction-explanation",
 "observed_in":[7],
 "problem":"The trigger 'diagnosing a suspiciously perfect AUC' now stands alone; model-validation ('detecting leakage', 'estimating performance honestly') and prediction-explanation ('debugging shortcut/batch learning') both advertise overlapping cases, and the pointers that used to disambiguate were removed. Class imbalance, calibration of tree ensembles and batch shortcut learning, this Skill's distinctive content, no longer appear in the description, so an agent asked only about those may route elsewhere. The other siblings (biomarker-discovery, survival-analysis, atlas-mapping) stay well separated by their own triggers. Not a defect of the intentional trim; no behaviour changed.",
 "root_cause":"The description was reduced to the Use-when clause by request; the AUC clause was written to sit beside the hand-off pointers.",
 "fix":"Optional, text-only: add the verb 'build' scoping to the AUC clause, e.g. 'diagnosing a suspiciously perfect AUC from a classifier you are building', and optionally name class imbalance and batch shortcuts in the Use-when list, if Sam wants routing sharper."})
json.dump(r,open(R+'report.json','w',encoding='utf-8'),indent=2,ensure_ascii=False); open(R+'report.json','a').write('\n')
s=json.load(open(P+'source-identity.json',encoding='utf-8'))
s['schema']="scientific-skill-audit-source-identity-v1"
s['phase']="delta re-audit (frontmatter description trimmed)"
s['skill_id']='bio-machine-learning-omics-classifiers'
s['independent_auditor']=True
c=s['candidate']
c['content_sha256']=NEW; c['bytes']=50363; c['file_count']=7
for f in c.get('files',[]) if 'files' in c else []: pass
for f in s['files']:
    if f['path']=='SKILL.md': f['sha256']='44ed2cf314af3b997fe0d097e07237e2137c8ee60951255aa765e92400050b95'; f['bytes']=26216-(len(open(r'F:/OpenScience/audits/bio-machine-learning-omics-classifiers/fix-description-20261003/edits.json',encoding='utf-8').read()) and 0)
s['candidate']['status_after_execution']="unchanged: tools/skill_preflight.py --offline reports the same manifest hash before and after the delta audit; no Skill byte edited"
s['audit']={"kind":"delta re-audit, independent of the normalizer, auditors and fixers","previous_identity":"906900fae480655dca3808442d858f84b17aace68513ed281607842a0151276f","previous_record":"candidate@906900fae480-reaudit2-lane3-20261003","fix_evidence":"F:\OpenScience\audits\bio-machine-learning-omics-classifiers\fix-description-20261003","delta_qualification":"scripts/revert_check.py on scratch copy reproduces 906900fae480...; diff -r shows only SKILL.md line 4","reused_evidence":"all execution evidence of the certifying record (behaviour unchanged: scripts, references and usage-guide hashes equal)"}
s['origin']['checkout_read_only']=s['origin'].get('checkout_read_only')
json.dump(s,open(R+'source-identity.json','w',encoding='utf-8'),indent=2,ensure_ascii=False); open(R+'source-identity.json','a').write('\n')

# post-fix applied: audit.fix_evidence path escaped; SKILL.md bytes 25773 (sum 50363)
