pe <- msqrobAggregate(pe, i = 'peptideLog', fcol = 'protein', name = 'proteinLmer',
                      formula = ~condition + (1 | sample) + (1 | feature), ridge = FALSE)
pe <- hypothesisTest(pe, i = 'proteinLmer', contrast = L)
