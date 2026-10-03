"""Run the tail of the SKILL.md inline snippet (reliability filter) after repairing line 1 locally, to see if later lines work."""
import pandas as pd
se_jc = pd.read_csv('rmats_real/out/SE.MATS.JC.txt', sep='\t')
per_rep_inc = se_jc['IJC_SAMPLE_1'].str.split(',').apply(lambda x: list(map(int, x)))
per_rep_skip = se_jc['SJC_SAMPLE_1'].str.split(',').apply(lambda x: list(map(int, x)))
min_inc = per_rep_inc.apply(min); min_skip = per_rep_skip.apply(min)
reliable = se_jc[(min_inc + min_skip) >= 20]
# per-replicate total >= 20 in every replicate (the intent stated by "per-replicate minimum")
per_rep_ok = [all(i + s >= 20 for i, s in zip(a, b)) for a, b in zip(per_rep_inc, per_rep_skip)]
print('tail runs; rows passing Skill filter (min IJC + min SJC >= 20):', len(reliable), '; rows where every replicate has IJC+SJC >= 20:', sum(per_rep_ok))
mis = [(a, b) for a, b, ok in zip(per_rep_inc, per_rep_skip, per_rep_ok) if not ok]
both = se_jc[((min_inc + min_skip) >= 20)].index
print('Skill filter passes but a replicate has <20 junction reads:', sum(1 for i in both if not per_rep_ok[i]))
