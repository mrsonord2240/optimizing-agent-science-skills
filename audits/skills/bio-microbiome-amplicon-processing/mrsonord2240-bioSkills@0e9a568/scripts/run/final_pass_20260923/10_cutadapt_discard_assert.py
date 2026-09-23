from pathlib import Path
import re
log = Path(r'F:\OpenScience\audits\bio-microbiome-amplicon-processing\run\final_pass_20260923\01_remove_primers.log').read_text(encoding='utf-8')
discarded = [int(x) for x in re.findall(r'Pairs discarded as untrimmed:\s+(\d+)', log)]
written = [int(x.replace(',', '')) for x in re.findall(r'Pairs written \(passing filters\):\s+([\d,]+)', log)]
assert len(discarded) == 10 and len(written) == 10, (len(discarded), len(written))
assert sum(discarded) == 1 and sum(written) == 19785, (sum(discarded), sum(written))
print(f'CUTADAPT_DISCARD_PASS samples=10 discarded={sum(discarded)} retained={sum(written)}')
