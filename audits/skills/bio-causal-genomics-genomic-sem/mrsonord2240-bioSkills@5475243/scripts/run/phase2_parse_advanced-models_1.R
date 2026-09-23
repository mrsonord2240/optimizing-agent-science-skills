model_esem <- '
    F1 =~ NA*trait1 + trait2 + trait3 + trait4
    F2 =~ NA*trait1 + trait2 + trait3 + trait4
    F1 ~~ 1*F1
    F2 ~~ 1*F2
    F1 ~~ F2
'
esem_fit <- usermodel(covstruc = ldsc_results, model = model_esem, estimation = 'DWLS')
# Rotate post-fit via GPArotation::GPForth/GPFoblq or lavaan::rotate()
