"""Input 5 (Stress/multi-part) -- reproduce SKILL.md's documented 'Megablast for cross-species'
failure mode with the SAME query used in Input 1 (whose blastn/word=11 run found real mouse/rat
orthologs at 79-86% identity). If megablast (word=28) misses those same cross-species hits, that
is a live confirmation of the Skill's own claim, not a hypothetical.

Also demonstrates save-to-XML + re-parse (save_and_parse.py pattern) as part of the same input.
"""
import time
from io import StringIO
from Bio.Blast import NCBIWWW, NCBIXML

QUERY = '''>HBB_partial
ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAACGTGGATGAAGTTGGTGGTGAGGCCCTGGGCAG'''

t0 = time.time()
print('Submitting MEGABLAST (word=28 default) to NCBI against refseq_select_rna...', flush=True)
handle = NCBIWWW.qblast(
    program='blastn',   # SKILL.md's own table lists program='megablast' as if it were a
    megablast=True,     # valid qblast(program=...) value; qblast rejects that string outright
                         # (ValueError: "Program specified is megablast. Expected one of blastn,
                         # blastp, blastx, tblastn, tblastx"). The real API requires
                         # program='blastn' + megablast=True. Corrected here to prove the fix.
    database='refseq_select_rna',
    sequence=QUERY,
    expect=1e-10,
    hitlist_size=500,
    format_type='XML',
)
raw = handle.read()
handle.close()
with open('input5_megablast_raw.xml', 'w', encoding='utf-8') as f:
    f.write(raw)
print(f'Elapsed: {time.time()-t0:.1f}s, raw XML bytes: {len(raw)}')

# save_and_parse.py pattern: write then re-read from disk
with open('input5_megablast_raw.xml') as f:
    record = NCBIXML.read(f)

print(f'Query length: {record.query_length}')
print(f'Total alignments (megablast): {len(record.alignments)}')
species_seen = set()
for aln in record.alignments:
    hsp = aln.hsps[0]
    ident = hsp.identities / hsp.align_length
    print(f'  {aln.accession:<14} id={ident:.2f}  {aln.title[:80]}')
    # crude species tag from title
    for tag in ('Homo sapiens', 'Mus musculus', 'Rattus norvegicus'):
        if tag in aln.title:
            species_seen.add(tag)

print(f'\nSpecies represented in megablast hit list: {sorted(species_seen)}')
print('Input 1 (blastn word=11) found: Homo sapiens, Mus musculus, Rattus norvegicus '
      '(NM_008220 mouse 86% id, NM_033234 rat 84% id, etc.)')
if species_seen == {'Homo sapiens'}:
    print('CONFIRMED: megablast (word=28) misses the cross-species mouse/rat hits that '
          'blastn (word=11) found on the identical query -- matches SKILL.md Failure Modes '
          '"Megablast for cross-species" exactly.')
else:
    print('NOT CONFIRMED as described: megablast still found non-human hits -- see list above.')
