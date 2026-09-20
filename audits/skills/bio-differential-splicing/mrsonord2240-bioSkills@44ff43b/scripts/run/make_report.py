#!/usr/bin/env python3
"""Builds eval_report_bio-differential-splicing_result.json and eval_viewer_bio-differential-splicing.md from the scored data below.
Every number in the notes comes from the run outputs under run/out (see the viewer)."""
import json, os, sys
OUT = sys.argv[1]
SRC = 'mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/differential-splicing'
SKILL = 'bio-differential-splicing'
DESC = ("Detects differential alternative splicing between conditions using rMATS-turbo (binomial LRT on junction counts), leafcutter "
        "(Dirichlet-multinomial GLM on intron clusters), MAJIQ V3 deltapsi/HET, SUPPA2 (empirical-null on TPM-derived PSI), or Shiba. "
        "Reports FDR-corrected significance and delta PSI effect sizes; tools differ in statistical model, annotation dependence, "
        "calibration regime and replicate requirements.")

static = {
    'functional_suitability': (8, 12, 'Core rMATS/leafcutter/SUPPA2 commands and output columns verified against installed tools (rMATS 4.4.0, leafcutter 0.2.9, SUPPA2 2.4, Shiba 0.8.2) and recover planted truth. Deductions: SUPPA2 -m classical advised for n<=3 has zero power; leafcutter n>=2/3 claim conflicts with default -i 5; --paired-stats prerequisite (PAIRADISE) missing; MAJIQ V3 block not executable here; no single-end (-t single) guidance.'),
    'reliability': (7, 12, 'Common Errors table exists, but the important failures are silent or unlisted: rMATS with wrong -t / readLength exits 0 with a header-only file; --paired-stats exits 0 with a header-only file; leafcutter_ds.R default flags stop at 3v3 with a message the Skill never mentions; group-file name mismatch gives "undefined columns selected".'),
    'performance_context': (6, 8, 'SKILL.md is 421 lines with no references/ directory; usage-guide.md repeats the tool summary. Workflow is otherwise linear.'),
    'agent_usability': (12, 16, 'Decision tree by design, thresholds table, output-column table and reconciliation table are clear and usable. Deductions: effect-size sign conventions are documented only for rMATS (SUPPA2 and leafcutter report group2-group1, Shiba alt-ref); Shiba invocation is left to an external website; leafcutter group-file name rule undocumented.'),
    'human_usability': (5, 8, 'Natural triggers (compare splicing between treatment groups, tissues, disease states). Little forgiveness: wrong -t/readLength/libType/-i values give empty or halted runs without guidance.'),
    'security': (11, 12, 'No credentials; system() call uses a fixed string; no eval of user strings. Minor: no input validation advice for file lists.'),
    'maintainability': (8, 12, 'Single monolithic SKILL.md plus a usage-guide and two examples; no test data or expected outputs; neither shipped example runs cleanly from a copy without edits.'),
    'agent_specific': (16, 20, 'Precise long description, good related-skill routing (outlier-splicing-detection for n=1 vs cohort), some out-of-scope routing; no stop condition for n=1 vs n=1 or for single-end data.'),
}

def A(t, ok, n):
    return {'text': t, 'result': 'PASS' if ok else 'FAIL', 'note': n}

inputs = [
 dict(index=1, type='Canonical', label='rMATS-turbo 3v3 on planted exon-skipping set + Skill filter snippet + shipped example',
  status='COMPLETED', status_flag='\u2705', basic=34, specialized=50, executed=True,
  execution_note='Ran on WSL as-core, rMATS-turbo 4.4.0. Planted single-end 3v3: adapted command (-t single --readLength 50 --novelSS --cstat 0.05) gave IncLevel1 0.8,0.8,0.769 / IncLevel2 0.2,0.2,0.208, IncLevelDifference +0.587 (truth 0.586966), FDR 1.2e-26; swapping --b1/--b2 gave -0.587 (sign claim verified). SKILL.md command verbatim (-t paired --readLength 150 --libType fr-firststrand) on the single-end data: rc 0, 0 events, header-only file. SKILL.md pandas filter ran; assertion (1 event, dPSI 0.587, min_inc 20, min_skip 10) printed ASSERT OK. Shipped examples/diff_splicing_rmats.sh from a copy on real chrX 75 nt reads: as shipped (READ_LENGTH=150) rc 0, prints "analysis complete", SE.MATS.JC.txt has 0 rows; with READ_LENGTH=75 it gives 197 SE events and its awk filter (no coverage filter) lists 4 hits whose counts are 0-3 reads.',
  assertions=[A('rMATS recovers the planted dPSI (0.587 +/- 0.002) with the documented b1-b2 sign', True, 'IncLevelDifference 0.587; -0.587 when b1/b2 swapped'),
              A('SKILL.md filter (FDR<0.05, |dPSI|>0.10, per-rep coverage>=10) keeps the planted event and runs unmodified', True, 'ASSERT OK printed; 1 of 1 events kept'),
              A('SKILL.md rMATS command runs on the design given without silent failure', False, '-t paired on single-end data: rc 0, header-only output; Skill never mentions -t single'),
              A('Shipped rMATS example produces results from a clean copy on real paired-end data', False, 'READ_LENGTH=150 on 75 nt reads: 0 SE rows, rc 0, "analysis complete" printed')]),
 dict(index=2, type='Variant A', label='leafcutter 3v3 on planted set, SKILL.md steps and shipped R example',
  status='COMPLETED', status_flag='\u26a0\ufe0f', basic=31, specialized=44, executed=True,
  execution_note='WSL as-core (regtools 1.0.0, clustering) + as-rleaf (leafcutter 0.2.9). regtools flags from SKILL.md (-a 8 -m 50 -s XS) accepted; junc scores 40,10,40. Clustering as documented gave 0 introns on contig chrP (script drops non-chr1-22/X/Y; -k True needed), then counts 40 44 38 10 12 9 etc. leafcutter_ds.R with the Skill\'s options (no -i) and 3v3: rc 1 "smallest group is less than min_samples_per_intron" (default -i 5); the Common-Errors flags --min_samples_per_intron 5 --min_samples_per_group 3 fail the same way. With -i 3: cluster p 4.0e-9, skipping-intron usage 0.118 vs 0.663, deltapsi +0.5446 (hand value 0.55). Group file with the Skill placeholder names s1..s6 -> "undefined columns selected". exon_file with columns chr,start,end,strand,gene_name labelled the cluster G1. leafcutter_ds.R is not on PATH after installing the R package. Shipped diff_splicing_leafcutter.R runs; its load_leafcutter_results()/annotate_clusters() work on real output (assert: 3 introns, max deltapsi 0.545) but the script writes a groups.txt (sample1..6) that cannot match the counts-table names, so its own pipeline stops with "undefined columns selected".',
  assertions=[A('leafcutter recovers the planted skipping-intron shift (|deltapsi| ~0.55) at FDR<0.05', True, 'deltapsi 0.5446, p.adjust 4e-9 with -i 3'),
              A('Documented command sequence runs at n=3 vs 3 with the flags given', False, 'default -i 5 stops; the -i/-g/-c flags are not mentioned; Common-Errors flags also stop'),
              A('Documented group-file recipe works with the counts table produced by the documented clustering step', False, 'sample names must equal junc basenames; s1..s6 / sample1..6 fail with "undefined columns selected"'),
              A('Shipped R helper functions run on real leafcutter output and merge cluster with effect tables', True, 'ASSERT OK: 3 introns, max deltapsi 0.545')]),
 dict(index=3, type='Edge', label='Real chrX 2v2 (GBR vs YRI) across rMATS, leafcutter, Shiba, SUPPA2 + permuted control',
  status='COMPLETED', status_flag='\u26a0\ufe0f', basic=32, specialized=46, executed=True,
  execution_note='Real 2x75 nt data, 4 samples, GRCh37 (public-data\\rnasplice; XS-tagged copies for leafcutter/Shiba). rMATS (-t paired --readLength 75 --variable-read-length --novelSS --cstat 0.05, unstranded): SE 226, A3SS 106, A5SS 90, MXE 20, RI 54 events; 9 events (7 genes) reach FDR<0.05 & |dPSI|>0.10 but 0 pass the Skill per-replicate coverage filter (min_inc+min_skip>=10), i.e. the coverage filter removes all low-count hits. With the Skill libType fr-firststrand on unstranded data SE events 226 -> 121 and summed junction counts 13,314 -> 5,570 (the "wrong libType halves junctions" pitfall verified). leafcutter with the Skill -m 50: 0 clusters on this ~100k-read subset; -m 10 -i 2 -g 2 -c 5: 13 clusters tested, 0 significant (real), 1 (permuted); default flags stop at 2v2. Shiba (shiba.py --mame, strand XS): 0 differential events real and permuted. SUPPA2 from Salmon TPM: empirical (-gc) 36 events / 32 genes at FDR<0.05 & |dPSI|>0.10 in the real comparison and 24 events / 23 genes in the permuted one; classical 0 in both (min p 0.22). Read-count tools agree there is nothing reliable at this depth; SUPPA2 empirical calls are the unstable ones, consistent with the Skill warning against n<=3.',
  assertions=[A('All four documented tools run to completion on the 2v2 real data', True, 'rMATS, Shiba, SUPPA2 ok; leafcutter needs -i 2 -g 2 -c 5 and -m 10 on this depth'),
              A('Skill coverage filter suppresses low-count rMATS hits', True, '9 FDR/dPSI hit events, 0 after min_inc+min_skip>=10'),
              A('Skill wrong-libType pitfall is real', True, 'fr-firststrand on unstranded data: SE events 226 -> 121, counts -58%'),
              A('Skill n=2 guidance (leafcutter n>=2) works with the documented command', False, 'default flags stop at 2v2; need -i 2 -g 2 -c 5'),
              A('Shiba route in SKILL.md (snakemake -s snakeshiba.smk ... --use-singularity) runs as written', False, 'snakeshiba.smk lives in share/shiba-0.8.2-0, config needs a container key (KeyError line 58); shiba.py config.yaml is what ran')]),
 dict(index=4, type='Variant B', label='SUPPA2 diffSplice loop on synthetic 3v3 TPM (planted truth)',
  status='COMPLETED', status_flag='\u26a0\ufe0f', basic=28, specialized=38, executed=True,
  execution_note='WSL as-suppa (SUPPA2 2.4). SYNTHETIC 120-gene sim (24 strong + 6 weak planted dPSI, 90 no-change), TPM from the same molecules as the BAMs, 3v3. SKILL.md loop (generateEvents -f ioe -e SE SS MX RI; psiPerEvent; diffSplice -gc) ran. Empirical: 23/24 strong detected, 0/6 weak, direction 23/23 (SUPPA2 dPSI = cond2 - cond1, verified in diff_tools.py and on G000), 3 false positives among 26 calls (11.5% vs 5% nominal) all in low-coverage genes; null A vs C: 2 false positives. Classical (the Skill\'s advice for n<=3): 0/30 planted events detected, minimum p 0.064 before/at BH, null minimum 0.1. Cause verified in lib/diff_tools.py: classical = unpaired Mann-Whitney U, whose smallest two-sided p is 0.1 at 3v3 and 0.33 at 2v2; BH cannot lower it. TPM files must have a header of sample names only (undocumented); generateEvents on an SE-only annotation writes empty A5/A3/MX/RI files.',
  assertions=[A('SUPPA2 empirical recovers planted strong events with correct direction', True, '23/24, 23/23 direction'),
              A('SUPPA2 empirical is roughly calibrated at n=3 on the null comparison', False, '2 FPs on A vs C; 3/26 calls false on A vs B (Skill itself warns 15-30% FDR)'),
              A('Skill advice "-m classical for n<=3" yields usable detections', False, '0/30 detected; Mann-Whitney min p is 0.1 at 3v3'),
              A('Skill table entry SUPPA2 classical "min reps n>=2" is a usable minimum', False, 'no p<0.33 is reachable at n=2 and none <0.1 at n=3')]),
 dict(index=5, type='Stress', label='Synthetic 120-gene simulation, 3v3 and 2v2, rMATS/leafcutter/Shiba, null and planted',
  status='COMPLETED', status_flag='\u2705', basic=35, specialized=52, executed=True,
  execution_note='SYNTHETIC data (run/make_sim.py): 24 strong (|d| 0.3-0.5) + 6 weak (0.15) planted DS genes, 70 no-change genes, 20 low-coverage no-change genes; A vs B truth, A vs C null. 3v3: rMATS (Skill flags; FDR<0.05,|dPSI|>0.10, per-rep coverage >=10) 24/24 strong, 0/6 weak, direction 24/24, 0 false positives (without the coverage filter 2 low-coverage false positives); null 0 calls. leafcutter (-i 3) 22/24 strong, 1/6 weak, 0 FP, direction 23/23; null 0. Shiba 22/24, 1/6, 1 FP, null 0. rMATS x leafcutter concordance: 22 shared calls, 22 true, 0 null; null: 0/0 (concordance rule verified). 2v2: rMATS 22/24 strong 3 FP with Skill filter, leafcutter 20/24 with 2-3 FP, Shiba 20/24 with 3 FP and 2 calls on the null comparison; the Skill claim that Shiba beats rMATS at n=2 is not supported in a sim without planted junction imbalance (and cannot be tested here). Shiba 0.8.2 crashes (KeyError) unless the GTF contains every event type with reads; decoy genes were added to make it run.',
  assertions=[A('rMATS with the Skill filters recovers planted strong events with correct sign and no null false positives', True, '24/24, 24/24 sign, 0 FP; null 0'),
              A('leafcutter stays quiet on the null comparison and gets direction right', True, '0 calls on A vs C; 23/23 direction'),
              A('Two-family concordance rule (rMATS + leafcutter) yields only true calls', True, '22 concordant, all planted; 0 in null'),
              A('Skill claim that Shiba outperforms rMATS at n=2v2 holds on planted truth', False, 'Shiba 2 null calls and 3 FP; rMATS 0 null calls (no imbalance planted; claim untestable)'),
              A('Weak (|dPSI| 0.15) planted events are detected at standard thresholds', False, 'rMATS 0/6, leafcutter 1/6 at n=3 (power table in Skill says marginal below 0.2)')]),
 dict(index=6, type='Scope Boundary', label='MAJIQ HET cohort, paired tumor-normal --paired-stats, single patient vs cohort hand-off',
  status='PARTIAL', status_flag='\u274c', basic=27, specialized=36, executed=False,
  execution_note='PARTIAL. MAJIQ V3 / VOILA are licence-gated academic downloads and are NOT installed: none of the MAJIQ commands (build, deltapsi, heterogen, voila view) were executed; the public MAJIQ page confirms V3 exists but does not show command syntax, so flags such as --minreads/--minpos/--mem-profile and splicegraph.zarr could not be checked. rMATS --paired-stats (Skill advice for tumor-normal) was executed on the synthetic sim: rc 0, log "Error in library(PAIRADISE): there is no package called PAIRADISE", output SE.MATS.JC.txt is header-only with no FDR column. No PAIRADISE install was attempted (shared env). leafcutterMD.R -h runs and lists -o -s -c -t -p (the hand-off tool for n=1 vs cohort exists); the FRASER2 hand-off was not exercised here.',
  assertions=[A('Skill states which tools need a licence and routes n=1 vs cohort to outlier tools', True, 'usage-guide names academic licence for MAJIQ; SKILL.md routes single patient to FRASER2/leafcutterMD'),
              A('Advertised paired tumor-normal route (--paired-stats) works on a stock rMATS install', False, 'PAIRADISE missing: rc 0 with header-only output, no warning in Skill'),
              A('MAJIQ commands were verified against the installed version', False, 'MAJIQ not installed; not executed; flags unverified'),
              A('Hand-off tool named for the out-of-scope regime exists and is invocable', True, 'leafcutterMD.R -h ran')]),
 dict(index=7, type='Adversarial', label='Batch-confounded design, perfectly confounded batch, and n=1 vs n=1 pilot',
  status='COMPLETED', status_flag='\u274c', basic=26, specialized=36, executed=True,
  execution_note='Synthetic sim, 3v3 A vs B with an arbitrary imbalanced batch and random RIN. SKILL.md logit-PSI residual snippet (verbatim block) ran; testing residuals by group with a rank-sum test (as the Skill says) gave minimum p 0.1000 (assert printed: cannot reach 0.05 at 3v3): 0/20 strong planted events at p<0.05. OLS logit_psi ~ group + batch + RIN (group coefficient tested) found 13/20 strong with 1 false positive in 55 null events. leafcutter_ds.R with batch as a third groups-file column (Skill claim, verified in the script source) ran and returned results; with batch identical to group it also exits 0 and returns 4 significant clusters with no rank-deficiency warning. rMATS n=1 vs n=1: runs, rc 0; on the null comparison 4 of 118 events pass FDR<0.05 & |dPSI|>0.10 (all false), on the planted comparison 22 calls of which 4 are false; the Skill gives no stop condition for n=1 vs n=1.',
  assertions=[A('Skill leafcutter confounder claim (extra groups-file columns) is accurate', True, 'verified in leafcutter_ds.R source and by a run'),
              A('Skill PSI-residual confounder route can reach significance at n=3 vs 3', False, 'rank-sum on residuals: min p 0.1, 0/20 strong events'),
              A('Skill warns that fully confounded batch/condition cannot be adjusted', False, 'only says check PCA; leafcutter silently returns results when batch = group'),
              A('Skill stops or warns for n=1 vs n=1', False, 'no guidance; rMATS returns 4 false positives on the null comparison')]),
]

for i in inputs:
    i['total'] = i['basic'] + i['specialized']
    i['assertions_passed'] = sum(a['result'] == 'PASS' for a in i['assertions'])
    i['assertions_total'] = len(i['assertions'])
    assert 3 <= i['assertions_total'] <= 5
exec_avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
subtotal = sum(v[0] for v in static.values())
sw, dw = round(subtotal * 0.4, 1), round(exec_avg * 0.6, 1)
score = int(round(sw + dw))
grade, sym = ('Production Ready', '\u2b50') if score >= 85 else ('Limited Release', '\u2705') if score >= 75 else ('Beta Only', '\u26a0\ufe0f') if score >= 60 else ('Reject', '\u274c')
tot_pass = sum(i['assertions_passed'] for i in inputs); tot_all = sum(i['assertions_total'] for i in inputs)
n_exec = sum(1 for i in inputs if i['executed'])

recs = [
 dict(priority='P1', title='SUPPA2 "-m classical for n<=3" has zero power', observed_in=[3, 4],
  problem='Classical mode is an unpaired Mann-Whitney U test; smallest two-sided p is 0.1 at 3v3 and 0.33 at 2v2 and BH cannot lower it. On the planted 3v3 set it detected 0/30 events; on real 2v2 it returned no p below 0.22. The table lists it with min reps n>=2.',
  root_cause='The fallback was chosen for robustness without checking attainable p-values.',
  fix='Delete the advice to switch to classical for n<=3; state that SUPPA2 needs n>=4 per group (rank-sum min p 0.029) for any significance, and route n<=3 to rMATS/leafcutter/Shiba. Change the "Min reps" cell for SUPPA2 classical to n>=4.'),
 dict(priority='P1', title='leafcutter n>=2/3 claim vs leafcutter_ds.R defaults', observed_in=[2, 3],
  problem='With the options the Skill shows, leafcutter_ds.R stops at 3v3 and 2v2 ("smallest group is less than min_samples_per_intron"); the Common-Errors flags (--min_samples_per_intron 5 --min_samples_per_group 3) stop identically. Upstream says calibration is only checked down to 4 per group.',
  root_cause='Defaults (-i 5 -g 3 -c 20) were not reconciled with the stated minimum replicates.',
  fix='Give the runnable command for 3v3 (e.g. -i 3 -g 3 -c 10) and 2v2 (-i 2 -g 2 -c 5), note the n>=4 calibration limit, and remove the -i 5 pre-filter suggestion for small designs. Also state that groups-file sample names must equal the .junc basenames and that non-chr contigs need -k True.'),
 dict(priority='P1', title='Confounder route (residual + rank-sum) is powerless at n=3 and biased if confounded', observed_in=[7],
  problem='Regressing out batch and RIN and testing residuals by group with a rank-sum test cannot give p<0.05 at 3v3 (0/20 strong events, min p 0.1); OLS with group and batch terms found 13/20 with 1/55 false positives. Regressing out only batch removes group signal when batch is imbalanced.',
  root_cause='Residualisation was chosen for simplicity; the group term is left out of the model.',
  fix='Replace with logit-PSI ~ group + batch (+ covariates) and test the group coefficient (or limma/DEXSeq), and warn that residual+rank-sum needs n>=4 per group. State that a batch identical to condition cannot be adjusted (leafcutter silently returns results).'),
 dict(priority='P1', title='Shipped examples fail or mislead from a clean copy', observed_in=[1, 2],
  problem='diff_splicing_rmats.sh hard-codes READ_LENGTH=150: on 75 nt reads it exits 0, prints "analysis complete" and writes 0 SE rows; its awk filter has no coverage filter (4 hits at 0-3 reads). diff_splicing_leafcutter.R writes groups.txt with sample1..6 that cannot match the counts-table column names, so the following leafcutter_ds.R call dies with "undefined columns selected".',
  root_cause='Examples were never run end to end against real data.',
  fix='Take READ_LENGTH from the data (or add --variable-read-length and an assertion that SE.MATS.JC.txt has rows), add the per-replicate coverage filter to the awk, and make the R example derive sample names from the .junc basenames and check them against the counts header before calling leafcutter_ds.R.'),
 dict(priority='P1', title='--paired-stats advertised without its dependency; silent header-only output', observed_in=[6],
  problem='SKILL.md recommends rMATS --paired-stats for tumor-normal. On a stock install rMATS logged "no package called PAIRADISE", returned rc 0 and wrote header-only tables without an FDR column.',
  root_cause='R/PAIRADISE prerequisite not listed; no post-run check.',
  fix='List PAIRADISE (R) as a prerequisite, add a check that the FDR column exists and the file has rows, and say -t single is needed for single-end data.'),
 dict(priority='P2', title='ΔPSI sign conventions differ by tool; reconciliation table blames event class', observed_in=[4, 5],
  problem='rMATS IncLevelDifference = group1 - group2; SUPPA2 dPSI and leafcutter deltapsi = group2 - group1; Shiba dPSI = alt - ref. The table row "Both sig, opposite direction" attributes it to event mismatch only.',
  root_cause='Only the rMATS sign is documented.', fix='Add a one-line sign convention per tool and list it first in the opposite-direction row.'),
 dict(priority='P2', title='Shiba and MAJIQ sections are not runnable or checkable as written', observed_in=[3, 5, 6],
  problem='snakeshiba.smk sits in the package share directory and needs a container key in config.yaml (KeyError otherwise); shiba.py config.yaml runs directly but needs XS tags, a GTF with every event type and reads for each type. Shiba 0.8.2 crashes (KeyError) otherwise. MAJIQ V3 flags were not verifiable (licence-gated) and --minreads/--minpos/--mem-profile are V2-era flags. Shiba superiority at n=2 is a citation, not tested (no advantage on a sim with no imbalance).',
  root_cause='Sections written from tool websites, not run.', fix='Give a minimal config.yaml, the direct shiba.py call, the XS requirement, and mark the MAJIQ block as unverified against V3 with the docs link.'),
 dict(priority='P2', title='Missing practical prerequisites and guards', observed_in=[1, 2, 7],
  problem='No mention of -t single for single-end data (verbatim command exits 0 with 0 events), no stop condition for n=1 vs n=1 (rMATS returns 4/118 null false positives), leafcutter_ds.R is not on PATH after installing the R package, the gencode_exons.txt.gz source is unspecified, and SUPPA2 TPM files need a sample-names-only header.',
  root_cause='Assumes a specific standard design.', fix='Add a short "design gate" (single-end, n=1, batch = condition) and the four prerequisites above.'),
]

meta = dict(skill_name='bio-differential-splicing', description=DESC, evaluated_on='2026-09-20', evaluator_version='skill-auditor@1.0',
            category='Data Analysis', execution_mode='D', complexity='Complex', n_inputs=len(inputs), source=SRC,
            data_note='Planted exon-skipping set (audit-env public-data) and a 120-gene simulation (run/make_sim.py) are SYNTHETIC; chrX 2v2 is real (nf-core rnasplice, GRCh37).')
report = {
 'source': SRC,
 'meta': meta,
 'veto_gates': {
  'skill_veto': dict(gate='PASS', stability='PASS', contract='PASS', determinism='PASS', security='PASS'),
  'research_veto': dict(applicable=True, gate='PASS',
    scientific_integrity=dict(result='PASS', detail='No fabricated citations or results; all numbers in outputs come from runs. Version-dated benchmark citations are hedged ("verify benchmarks").'),
    practice_boundaries=dict(result='PASS', detail='Research-only splicing analysis; the SMA/ASO mention is contextual, no individual diagnosis or prescription.'),
    methodological_ground=dict(result='PASS', detail='No fallacy that inverts conclusions. Weak points (SUPPA2 classical at n<=3, residual+rank-sum confounder route) produce false negatives, recorded as P1 rather than veto.'),
    code_usability=dict(result='PASS', detail='SKILL.md python/R snippets and the R example functions ran; rMATS/regtools/leafcutter/SUPPA2/Shiba flags accepted by installed versions. MAJIQ block not executed (not installed) and not counted as evidence.'))},
 'static_score': dict(subtotal=subtotal, max=100, categories={k: dict(score=v[0], max=v[1], note=v[2]) for k, v in static.items()}),
 'dynamic_score': dict(execution_avg=exec_avg, max=100, assertion_pass_rate=dict(passed=tot_pass, total=tot_all),
   inputs=[{k: i[k] for k in ('index', 'type', 'label', 'status', 'status_flag', 'note', 'basic', 'specialized', 'total', 'assertions_passed', 'assertions_total', 'assertions', 'executed', 'execution_note') if k in i or k == 'note'} if False else
           dict(index=i['index'], type=i['type'], label=i['label'], status=i['status'], status_flag=i['status_flag'], note=i['execution_note'][:240] + ('...' if len(i['execution_note']) > 240 else ''),
                basic=i['basic'], specialized=i['specialized'], total=i['total'], assertions_passed=i['assertions_passed'], assertions_total=i['assertions_total'],
                assertions=i['assertions'], executed=i['executed'], execution_note=i['execution_note']) for i in inputs]),
 'final': dict(static_weighted=sw, dynamic_weighted=dw, score=score, max=100, grade=grade, grade_symbol=sym, deployable=(grade in ('Production Ready', 'Limited Release')), veto_override=False),
 'key_strengths': [
   'Core rMATS-turbo and leafcutter usage is correct and recovered planted truth exactly (dPSI 0.587; deltapsi 0.545; 24/24 and 22/24 strong events with correct direction, no null false positives).',
   'Per-replicate coverage filter and the two-family concordance rule are sound: the filter removed all low-coverage false positives and rMATS x leafcutter concordance gave 22 calls, all true.',
   'Decision tree, thresholds table, output-column table and the wrong-libType / confounder / cryptic-splicing pitfalls are accurate and useful (libType pitfall verified: -58% junction counts).',
   'Good routing to sibling skills for out-of-regime designs, and leafcutter confounder-as-extra-column claim verified against the script source.'],
 'recommendations': recs,
}
assert [r['priority'] for r in recs] == sorted(r['priority'] for r in recs)
os.makedirs(OUT, exist_ok=True)
with open(f'{OUT}/eval_report_{SKILL}_result.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

# ---------------- viewer ----------------
L = []
L.append(f'# Eval Viewer - {SKILL}\n\nGenerated: 2026-09-20  |  Source: `{SRC}`  |  Category: Data Analysis  |  Mode: D (hybrid)  |  Complexity: Complex, N=7\n')
L.append('Env: `F:\\OpenScience\\audit-envs\\alternative-splicing` (rMATS-turbo 4.4.0, leafcutter 0.2.9, SUPPA2 2.4, Shiba 0.8.2, regtools 1.0.0; MAJIQ/VOILA licence-gated, not installed). '
         'Data: planted exon-skipping set and a 120-gene simulation are **synthetic**; chrX 2v2 is **real** (GRCh37). All scripts are in `run\\`.\n')
L.append('## Skill Veto\nT1 PASS, T2 PASS, T3 PASS, T4 PASS. Research Veto: M1-M4 PASS (MAJIQ code not executed, not counted).\n')
L.append('## Static score (25 criteria)\n\n| Category | Score | Note |\n|---|---|---|')
for k, v in static.items():
    L.append(f'| {k} | {v[0]}/{v[1]} | {v[2]} |')
L.append(f'\n**Static subtotal: {subtotal}/100**\n')
L.append('## Summary table\n\n| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |\n|---|---|---|---|---|---|---|---|')
for i in inputs:
    L.append(f"| {i['index']} | {i['type']} | {'yes' if i['executed'] else 'no (partial)'} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} | {i['status_flag']} {i['status']} |")
L.append(f'\n**Execution average: {exec_avg}/100**  |  **Assertion pass rate: {tot_pass}/{tot_all}**  |  Layer 1 avg {sum(i["basic"] for i in inputs)/7:.1f}/40, Layer 2 avg {sum(i["specialized"] for i in inputs)/7:.1f}/60\n')
L.append(f'**Final = {subtotal} x 0.4 + {exec_avg} x 0.6 = {sw} + {dw} = {sw+dw:.1f} -> {score} : {sym} {grade}**; deployable = {report["final"]["deployable"]}; veto override = False. Executed inputs: {n_exec}/7 fully executed (Input 6 partial: MAJIQ not executed; --paired-stats attempted and failed).\n')
L.append('Floors: Static 73 (<80 PR, >=70 LR), Execution avg 73.6 (<75), so Beta Only regardless of the numeric rounding.\n')
L.append('## Test inputs and outputs\n')
prompts = {
 1: 'I have n=3 vs n=3 RNA-seq BAMs; run rMATS-turbo with FDR<0.05 and |dPSI|>0.10, then filter for >=10 junction reads per replicate. (planted exon-skipping set; also run the shipped rMATS example from a copy)',
 2: 'Use leafcutter Dirichlet-multinomial GLM on intron clusters from regtools junctions for annotation-free differential splicing. (planted 3v3; also the shipped R example)',
 3: 'n=2 vs n=2 design (GBR vs YRI, real chrX): compare rMATS, leafcutter, Shiba and SUPPA2 and tell me which hits are trustworthy; include a permuted control.',
 4: 'I only have Salmon TPM for n=3 vs n=3; run the SUPPA2 differential splicing loop and report significant events. (synthetic sim with planted truth)',
 5: 'Run rMATS and leafcutter (and Shiba) on my 3v3 and 2v2 data, require concordance, and tell me the false-positive behaviour. (synthetic 120-gene sim, planted + null)',
 6: 'I have 30 tumor and 30 normal patients (MAJIQ HET), paired tumor-normal with --paired-stats, and one rare-disease patient vs controls.',
 7: 'My samples were prepared in two batches and batch is confounded with condition; adjust for it. Also I only have one sample per group, just run it.',
}
for i in inputs:
    L.append(f"### Input {i['index']} - {i['type']}: {i['label']}\n\n**Prompt:** {prompts[i['index']]}\n\n**executed:** {str(i['executed']).lower()}  \n**What ran and what it printed:** {i['execution_note']}\n")
    L.append(f"**Scores:** Basic {i['basic']}/40 | Specialized {i['specialized']}/60 | Total {i['total']}/100\n\n**Assertions:**")
    for a in i['assertions']:
        L.append(f"- [{a['result']}] {a['text']} - {a['note']}")
    L.append('')
L.append('## Verified claims (from the runs)\n')
L.append('| Claim in SKILL.md / usage-guide | Verdict |\n|---|---|\n'
 '| rMATS IncLevelDifference sign = b1 - b2 | True (+0.587 / -0.587 on swap) |\n'
 '| --cstat sets the |dPSI| null cutoff, default 0.0001 | True (--help) |\n'
 '| rMATS per-replicate coverage filter matters | True (removes 2 low-coverage false positives in sim; all 7 real-data hits) |\n'
 '| wrong --libType halves usable junctions | True (SE junction counts 13,314 -> 5,570 on unstranded data) |\n'
 '| leafcutter confounders = extra groups-file columns; R arg confounders= | True (script source; run) |\n'
 '| leafcutter n>=2 (n>=3 preferred) | Not with the shown flags (default -i 5 stops) |\n'
 '| SUPPA2 empirical inflated FDR at n<=3 | True (2v2 real: 36 events; permuted 24; sim 3/26 and 2 null FPs) |\n'
 '| SUPPA2 classical (Wilcoxon) fixes n<=3 | False (0/30 detected; min p 0.1 at 3v3) |\n'
 '| rMATS n>=3 required | Runs and works at 2v2 in the sim (22/24 strong) |\n'
 '| Shiba better than rMATS at n=2 | Not supported on a sim with no planted imbalance; untestable here |\n'
 '| --paired-stats for tumor-normal | Fails silently on stock install (PAIRADISE absent) |\n'
 '| MAJIQ V3 commands | Not executed; unverified |\n'
 '| rMATS/leafcutter/SUPPA2/Shiba output-column names used in snippets | True (p.adjust, deltapsi, IncLevelDifference, FDR, IJC_SAMPLE_1 etc.) |\n')
L.append('## Shipped-means-present\nSKILL.md and usage-guide.md point at no files that are missing; `examples/` holds both files they imply. No `references/` directory is referenced. Neither example runs cleanly from a clean copy (see P1).\n')
L.append('## Recommendations\n')
for r in recs:
    L.append(f"**[{r['priority']}] {r['title']}**  \nObserved in: {r['observed_in']}  \nProblem: {r['problem']}  \nRoot cause: {r['root_cause']}  \nFix: {r['fix']}\n")
L.append('## Key strengths\n' + '\n'.join(f'- {s}' for s in report['key_strengths']) + '\n')
L.append('## Notes on the audit itself\n- Two auditor errors were caught and fixed before scoring: (1) pandas read the truth class label `null` as NaN so no-change genes were dropped from the false-positive tally (label renamed `nochange`, all sim runs redone); (2) my first SUPPA2 TPM header carried a `Name` label (SUPPA2 wants sample names only). Both leave scripts in `run\\`.\n- Working tmp dirs and copied GTFs were deleted; no `__pycache__` in the source clone.\n')
with open(f'{OUT}/eval_viewer_{SKILL}.md', 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(L))
print('score', score, grade, 'static', subtotal, 'exec', exec_avg, 'assertions', tot_pass, tot_all, 'deployable', report['final']['deployable'])
