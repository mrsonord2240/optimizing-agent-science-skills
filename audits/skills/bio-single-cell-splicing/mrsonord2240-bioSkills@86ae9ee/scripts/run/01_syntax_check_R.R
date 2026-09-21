for (f in list.files('blocks', pattern='[.]R$', full.names=TRUE)) { e <- parse(f); cat('R OK', f, length(e), 'expressions\n') }
