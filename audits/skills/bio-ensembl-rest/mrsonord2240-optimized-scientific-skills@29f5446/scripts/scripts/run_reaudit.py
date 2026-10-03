"""Independent re-audit assertions for bio-ensembl-rest (live Ensembl REST). Read-only on the candidate."""
import sys, time
import requests
CAND = 'F:/OpenScience/wt/dbaccess-ensembl-rest/skills/bio-ensembl-rest'
sys.path.insert(0, CAND + '/scripts')
sys.dont_write_bytecode = True
import ensembl_client as c

def check(label, fn, expect=None):
    t0 = time.time()
    try:
        r = fn()
        ok = True if expect is None else bool(expect(r))
        print(f'[{"PASS" if ok else "FAIL"}] {label}: {str(r)[:200]}  ({time.time()-t0:.1f}s)')
    except Exception as e:
        print(f'[EXC ] {label}: {type(e).__name__}: {str(e)[:260]}  ({time.time()-t0:.1f}s)')
    time.sleep(0.4)

check('A1 symbol BRCA1', lambda: c.symbol_to_id('human', 'BRCA1'),
      lambda r: r['id'] == 'ENSG00000012048' and r['seq_region_name'] == '17' and r['strand'] == -1)
check('ENS-001 protein by ENSP', lambda: c.sequence_for_id('ENSP00000269305', 'protein'),
      lambda r: len(r['seq']) == 393 and r['seq'].startswith('MEEPQSDPSV'))
check('ENS-001 gene+multiple_sequences', lambda: c.sequence_for_id('ENSG00000139618', 'protein', multiple_sequences=True),
      lambda r: isinstance(r, list) and len(r) > 1 and all('seq' in x for x in r))
check('ENS-001 gene plain protein -> HTTPError with server message', lambda: c.sequence_for_id('ENSG00000139618', 'protein'),
      lambda r: False)
check('ENS-002 HGVS c.803C>T', lambda: c.vep_hgvs('human', 'ENST00000366667:c.803C>T')[0],
      lambda r: r['most_severe_consequence'] == 'missense_variant')
check('ENS-003 GRCh37 coord on grch37 host', lambda: c.vep_region('human', '17:41276135-41276135:1', 'G', base=c.GRCH37)[0]['most_severe_consequence'],
      lambda r: r == 'splice_region_variant')
check('ENS-003 usage-guide GRCh38 17:43044295 T>A', lambda: c.vep_region('human', '17:43044295-43044295:1', 'A')[0],
      lambda r: r['allele_string'] == 'T/A')
check('ENS-004 regulatory overlap', lambda: c.genes_in_region('human', '17:43000000-43200000', feature='regulatory'),
      lambda r: len(r) > 10)
check('ENS-004 homology/id/human/ENSG..', lambda: c.get_with_retry(c.BASE + '/homology/id/human/ENSG00000141510', params={'type': 'orthologues', 'target_species': 'mouse'}).json()['data'][0]['homologies'],
      lambda r: any(h['target']['id'] == 'ENSMUSG00000059552' for h in r))
check('ENS-005 renamed symbol -> 400 message', lambda: c.symbol_to_id('human', 'MARCH1'), lambda r: False)
check('ENS-005 Homo_sapiens accepted', lambda: c.symbol_to_id('Homo_sapiens', 'BRCA1')['id'], lambda r: r == 'ENSG00000012048')
check('ENS-006 batch w/ bad symbols', lambda: {k: (v.get('id') or v.get('error'))[:70] for k, v in c.batch_symbols('human', ['BRCA1', 'MARCH1', 'NOTAGENE']).items()},
      lambda r: r['BRCA1'] == 'ENSG00000012048' and 'No valid lookup' in r['NOTAGENE'])
check('ENS-006 e90 HTML -> EnsemblError', lambda: c.symbol_to_id('human', 'BRCA1', base='https://e90.rest.ensembl.org'), lambda r: False)
check('ENS-006 timeout -> EnsemblError', lambda: c.get_with_retry(c.BASE + '/lookup/symbol/human/BRCA1', timeout=0.001, max_retries=2), lambda r: False)
check('A4 e110 pinned', lambda: c.symbol_to_id('human', 'BRCA1', base=c.ARCHIVE_E110), lambda r: r['id'] == 'ENSG00000012048' and r['start'] == 43044295)
check('A4 e111 info', lambda: c.get_with_retry('https://e111.rest.ensembl.org/info/data').json(), lambda r: r['releases'] == [111])
check('A4 GRCh37 coords', lambda: c.symbol_to_id('human', 'BRCA1', base=c.GRCH37), lambda r: r['assembly_name'] == 'GRCh37' and r['start'] == 41196312)
check('A4 e116 archive (service 503 expected)', lambda: c.symbol_to_id('human', 'BRCA1', base='https://e116.rest.ensembl.org')['id'], lambda r: r == 'ENSG00000012048')
check('LD pairwise CEU', lambda: c.ld_pairwise('human', 'rs6792369', 'rs1042779'), lambda r: r and 0 <= float(r[0]['r2']) <= 1)
check('gene_info expand', lambda: c.gene_info('ENSG00000012048'), lambda r: len(r['Transcript']) > 10 and r['canonical_transcript'].startswith('ENST'))
check('genes_in_region', lambda: [g.get('external_name') for g in c.genes_in_region('human', '17:43000000-43200000')], lambda r: 'BRCA1' in r)
check('vep_id rs699', lambda: c.vep_id('human', 'rs699')[0], lambda r: r['most_severe_consequence'] == 'missense_variant')
check('TP53->mouse', lambda: c.orthologs_by_symbol('human', 'TP53', target='mouse'), lambda r: len(r) == 1 and r[0]['target']['id'] == 'ENSMUSG00000059552' and r[0]['type'] == 'ortholog_one2one')
check('BRCA1 paralogs', lambda: c.paralogs_by_symbol('human', 'BRCA1'), lambda r: isinstance(r, list))
