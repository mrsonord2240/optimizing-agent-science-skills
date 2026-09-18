import re, sys
skill_md = open(sys.argv[1], encoding='utf-8').read()
# Find the "Single SRR via ENA mirror" section's bash code fence
m = re.search(r"### Single SRR via ENA mirror.*?```bash\n(.*?)```", skill_md, re.S)
if not m:
    print("NOT FOUND", file=sys.stderr)
    sys.exit(1)
sys.stdout.write(m.group(1))
