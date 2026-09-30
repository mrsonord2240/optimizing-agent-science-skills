import json
def A(t,r,n): return {"text":t,"result":r,"note":n}
def inp(i,typ,label,note,b,s,asr):
    p=sum(1 for a in asr if a['result']=='PASS'); t=b+s
    return {"index":i,"type":typ,"label":label,"status":"COMPLETED","status_flag":"✅" if t>=75 else "⚠️","note":note,"basic":b,"specialized":s,"total":t,"assertions_passed":p,"assertions_total":len(asr),"assertions":asr}
I=[
inp(1,"Canonical","ENCODE-style TSS enrichment: real GM12878 slice plus planted bigWig","Real 11.381 vs deepTools 11.391; planted 21.0 for plus, minus, gene-interval and multi-chrom cases",36,52,[
A("Real-slice score agrees with independent deepTools profile","PASS","11.381 (1,373 TSS used) vs 11.391 from the earlier deepTools matrix"),
A("Planted bigWig returns 21.0 for plus, minus and chr2 TSS","PASS","t_tss.log"),
A("Gene-interval BED6 uses start for plus and end-1 for minus","PASS","21.0 after correcting my own fixture (first attempt gave 11.0 because my plus-strand gene start was 1 kb off the planted TSS; t_tss_gene2.log)"),
A("Absent chromosome, empty BED and BED3 fail loudly with exit 1","PASS","exit 1 each with used/skipped counts or BED6 message"),
A("Mixed valid/absent/edge rows report used and skipped counts","PASS","used 1, chrom_not_in_bigwig 1, window_outside_chrom 1")]),
inp(2,"Canonical","NRF/PBC1/PBC2 on real unfiltered and filtered BAM plus planted PE/SE","Real 0.778/0.798/5.074 equals independent counter; planted truth 250/160/0.64/0.625/2.0 in PE and SE",36,54,[
A("Real unfiltered BAM equals independent fragment counter","PASS","601203/467814; NRF 0.7781, PBC1 0.7985, PBC2 5.074 in both"),
A("Planted PE and SE reproduce hand-computed truth after MAPQ and chrM filters","PASS","total 250, distinct 160; unfiltered total 630"),
A("Deduplicated BAM triggers warning and PBC2 null","PASS","NRF 1.0 with warning"),
A("Output is strict JSON and empty result exits 1","PASS","strict parse ok; exit 1"),
A("MT/M contig names are excluded","PASS","BAM renamed 1/MT gives 250 (excluded 600); with exclusion off 550")]),
inp(3,"Variant A","atac_qc_metrics.R: real filtered slice with IDR .bed.gz peaks, planted BAM, hg19 TxDb argument, seqlevel mismatch","Real rep1 TSSEscore 23.54, NFR+mono, FRiP 0.671; planted 250 nuclear pairs; mismatch stops",34,48,[
A("Real slice metrics reproduce and periodicity class is NFR+mono","PASS","460,309 pairs; NFR 28.4%, mono 14.7%, di 15.6%"),
A("Planted BAM nuclear pairs equal 250 after chrM, MAPQ and dup exclusion","PASS","out/R/pl_metrics.csv"),
A("Non-default TxDb argument is honored","PASS","hg19 TxDb ran (TSSEscore 1.29 vs 5.13 hg38 on same reads); real non-hg38 data not available"),
A("BAM/TxDb seqlevel mismatch stops with message","PASS","no shared seqlevels error, exit 1"),
A("Fragment-size PDF is legible","FAIL","1-page 15.5 KB PDF written; no renderer available, so not visually inspected")]),
inp(4,"Variant B","aggregate_qc.py multi-sample and flat input, MultiQC hand-off","Grades PASS/WARN/FAIL/INCOMPLETE correct for 5 samples; MultiQC parsed table",35,53,[
A("Per-metric and overall grades match threshold table incl inverted mt_fraction","PASS","A PASS, B WARN, C FAIL, D INCOMPLETE"),
A("null and absent metrics grade NA, not PASS","PASS","PBC2 null and missing FRiP"),
A("Non-numeric and boolean values exit 2","PASS","exit 2"),
A("Extra keys noted on stderr","PASS","junk ignored note"),
A("MultiQC 1.35 ingests the *_mqc.tsv as a sample table","PASS","5 sample rows in multiqc_atac_encode_qc.txt")]),
inp(5,"Variant B","samtools/Picard/deepTools/MultiQC recipes on real slice","flagstat, Picard median 191, Spearman 0.9577, fingerprint curves, MultiQC modules detected",35,50,[
A("flagstat/idxstats report expected counts","PASS","1,048,048 mapped; synthetic idxstats chrM 600/1260 = 0.476 (labeled synthetic; slice has no chrM)"),
A("Picard insert size metrics are plausible","PASS","median 191, mean 252.7"),
A("Spearman heatmap and matrix are consistent","PASS","0.9577; heatmap rendered and labeled (2x2, no cell annotation)"),
A("Fingerprint curves render and diverge from diagonal","PASS","fingerprint.png inspected; synthetic AUC about 0.497"),
A("MultiQC detects Picard, samtools, deepTools and preseq outputs","PASS","multiqc_sources.txt")]),
inp(6,"Variant B","preseq c_curve/lc_extrap recipes with -P on coordinate-sorted unfiltered BAM","c_curve -P -s 1e5 gives 10 rows to 0.9M; lc_extrap -P monotone with ordered CI",33,47,[
A("c_curve -P -s 1e5 returns a multi-row curve","PASS","10 data rows, distinct 84,302 to 561,698"),
A("lc_extrap -P is monotone with ordered CI","PASS","0.61M at 1M reads to 2.44M at 19M"),
A("Extrapolated counts are consistent with observed curve","PASS","608,697 expected at 1M vs observed c_curve trend"),
A("Documented lc_extrap -e 200M -s 5M literal command was run","FAIL","run at reduced -e 20M -s 1M for time; literal values not re-executed here"),
A("Step guidance yields non-header-only output","PASS","-s 1e5 gives rows; header-only for -s 1e6 reproduced only by the fixer")]),
inp(7,"Edge","Silent-failure guards across scripts","Planted probes for TSS, complexity, aggregation and R stop or grade correctly",34,50,[
A("TSS script cannot report success with zero scored TSS","PASS","exit 1 in three cases"),
A("Complexity script cannot report success with no reads","PASS","exit 1"),
A("aggregate_qc never grades missing data PASS","PASS","NA/INCOMPLETE"),
A("R script stops on genome-build seqlevel mismatch","PASS","stop message"),
A("aggregate_qc rejects non-numeric input rather than coercing","PASS","exit 2 for string and boolean")])]
ex=round(sum(i['total'] for i in I)/7,1)
cats={"functional_suitability":(10,"Seven metrics covered; scripts now deliver documented filters, periodicity class and per-sample MultiQC table; mt fraction only exercised on synthetic data"),
"reliability":(11,"Empty/absent/invalid inputs fail loudly with counts; residual: out-of-coverage TSS slowness, mate MAPQ not inspected (documented)"),
"performance_context":(7,"13 KB SKILL.md with routed references"),
"agent_usability":(14,"Explicit script args, bigWig recipe and preseq -P; BED6 contract stated"),
"human_usability":(6,"Prompts and tips; still no worked sample-level example"),
"security":(11,"Read-only file access, no credentials or destructive ops"),
"maintainability":(10,"Small documented scripts; thresholds sourced to ENCODE vs convention; no shipped tests"),
"agent_specific":(17,"Precise trigger, version-drift guidance, provenance; claims now match execution")}
mx={"functional_suitability":12,"reliability":12,"performance_context":8,"agent_usability":16,"human_usability":8,"security":12,"maintainability":12,"agent_specific":20}
sub=sum(v[0] for v in cats.values())
sw=round(sub*0.4,1); dw=round(ex*0.6,1); sc=round(sw+dw)
ta=sum(i['assertions_total'] for i in I); pa=sum(i['assertions_passed'] for i in I)
rep={"meta":{"skill_name":"bio-atac-seq-atac-qc","description":"ATAC-seq library quality control: TSS enrichment, FRiP, fragment-size periodicity, library complexity (NRF/PBC1/PBC2), mitochondrial fraction, and ENCODE 4 thresholds.","evaluated_on":"2026-09-30","evaluator_version":"skill-auditor@1.0","category":"Data Analysis","execution_mode":"B","complexity":"Complex","n_inputs":7},
"veto_gates":{"skill_veto":{"gate":"PASS","stability":"PASS","contract":"PASS","determinism":"PASS","security":"PASS"},
"research_veto":{"applicable":True,"gate":"PASS","scientific_integrity":{"result":"PASS","detail":"Thresholds labeled ENCODE vs working convention; no fabricated values"},"practice_boundaries":{"result":"PASS","detail":"Research QC guidance only"},"methodological_ground":{"result":"PASS","detail":"NRF/PBC computed on fragments and matches an independent counter"},"code_usability":{"result":"PASS","detail":"All four scripts ran on numpy 2.5, pandas 3.0, deepTools 4.0"}}},
"static_score":{"subtotal":sub,"max":100,"categories":{k:{"score":v[0],"max":mx[k],"note":v[1]} for k,v in cats.items()}},
"dynamic_score":{"execution_avg":ex,"max":100,"assertion_pass_rate":{"passed":pa,"total":ta},"inputs":I},
"final":{"static_weighted":sw,"dynamic_weighted":dw,"score":sc,"max":100,"grade":"Production Ready" if sc>=85 else "Limited Release","grade_symbol":"⭐" if sc>=85 else "✅","deployable":True,"veto_override":False},
"key_strengths":["All ten prior findings reproduced as fixed against real GM12878 data and planted truth","Fragment-level NRF/PBC matches an independent counter exactly on 601,203 fragments","Silent-success paths in TSS, complexity and aggregation scripts now exit non-zero or grade NA","Thresholds separate ENCODE-sourced values from working convention"],
"recommendations":[
{"priority":"P2","title":"Fragment-size PDF never visually inspected","observed_in":[3],"problem":"atac_qc_metrics.R PDF written but not rendered in any audit","root_cause":"No PDF renderer in the prepared environments","fix":"Render once in a tooling-delta pass or replace with PNG output"},
{"priority":"P2","title":"TSS script slow when many TSS lie outside bigWig coverage","observed_in":[1,7],"problem":"Tooling pass saw more than 9 minutes for out-of-slice TSS","root_cause":"pyBigWig.values on uncovered regions","fix":"Optional note or per-chromosome coverage pre-check"},
{"priority":"P2","title":"No shipped fixtures or tests","observed_in":[2,4,7],"problem":"Planted-truth checks exist only in audit logs","root_cause":"Origin ships no tests","fix":"Ship a tiny synthetic BAM/bigWig and expected values"}]}
json.dump(rep,open('report.json','w',encoding='utf-8'),indent=2,ensure_ascii=False)
print(sub,ex,sw,dw,sc,pa,ta)
assert all(i['basic']+i['specialized']==i['total'] and 3<=len(i['assertions'])<=5 for i in I)
assert [r['priority'] for r in rep['recommendations']]==sorted(r['priority'] for r in rep['recommendations'])
print('avg basic',sum(i['basic'] for i in I)/7,'avg spec',sum(i['specialized'] for i in I)/7)
