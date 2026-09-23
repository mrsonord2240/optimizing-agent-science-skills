model_pfactor <- '
    # First-order factors
    INT =~ NA*trait_anx + trait_dep + trait_neuro       # internalizing
    EXT =~ NA*trait_adhd + trait_alc + trait_subst       # externalizing
    THT =~ NA*trait_scz + trait_bp                       # thought-disorder
    # Second-order p-factor
    p =~ NA*INT + EXT + THT
    INT ~~ 1*INT
    EXT ~~ 1*EXT
    THT ~~ 1*THT
    p ~~ 1*p
'
