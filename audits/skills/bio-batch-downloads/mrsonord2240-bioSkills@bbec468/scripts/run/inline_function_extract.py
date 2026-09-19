
def checkpointed_batch_download(db, term, out_path, ckpt_path, rettype='fasta',
                                 retmode='text', batch_size=500, max_retries=3):
    '''Download all matching records with disk checkpoint for resumability.'''
    delay = 0.1 if Entrez.api_key else 0.34
    ckpt = Path(ckpt_path)
    start = json.loads(ckpt.read_text())['start'] if ckpt.exists() else 0

    h = Entrez.esearch(db=db, term=term, usehistory='y', retmax=0)
    s = Entrez.read(h); h.close()
    webenv, query_key, total = s['WebEnv'], s['QueryKey'], int(s['Count'])
    print(f'{total:,} records matched; resuming at {start:,}')

    mode = 'a' if start else 'w'
    with open(out_path, mode) as out:
        while start < total:
            for attempt in range(max_retries):
                try:
                    h = Entrez.efetch(db=db, rettype=rettype, retmode=retmode,
                                      retstart=start, retmax=batch_size,
                                      webenv=webenv, query_key=query_key)
                    body = h.read(); h.close()
                    if isinstance(body, bytes):
                        body = body.decode('utf-8', errors='replace')
                    if '<ERROR>' in body[:500]:
                        raise RuntimeError(f'Server error in body: {body[:200]}')
                    out.write(body)
                    break
                except HTTPError as e:
                    if e.code == 429:
                        wait = 10 * (attempt + 1)
                        print(f'  Rate-limited; sleeping {wait}s')
                        time.sleep(wait)
                    elif attempt == max_retries - 1:
                        raise
                    else:
                        time.sleep(5 * (attempt + 1))
                except RuntimeError as e:
                    # Likely WebEnv expired; re-run ESearch
                    print(f'  {e}; refreshing WebEnv')
                    h = Entrez.esearch(db=db, term=term, usehistory='y', retmax=0)
                    s = Entrez.read(h); h.close()
                    webenv, query_key = s['WebEnv'], s['QueryKey']

            start += batch_size
            ckpt.write_text(json.dumps({'start': start, 'total': total}))
            time.sleep(delay)
            print(f'  {min(start, total):,}/{total:,}')
    ckpt.unlink(missing_ok=True)

