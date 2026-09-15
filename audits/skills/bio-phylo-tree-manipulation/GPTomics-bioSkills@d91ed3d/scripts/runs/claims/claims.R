# Test the Skill's R claims (ape / phangorn / phytools)
suppressPackageStartupMessages({library(ape); library(phangorn); library(phytools)})
cat('ape', as.character(packageVersion('ape')), 'phangorn', as.character(packageVersion('phangorn')),
    'phytools', as.character(packageVersion('phytools')), '\n')

cat('== R1 ape::midpoint exists?\n')
print(exists('midpoint', envir = asNamespace('ape'), inherits = FALSE))
print(tryCatch({ape::midpoint; 'found'}, error = function(e) conditionMessage(e)))
print('midpoint' %in% getNamespaceExports('phangorn'))
print('midpoint.root' %in% getNamespaceExports('phytools'))

tr <- read.tree(text = '((Human:0.1,Chimp:0.2):0.3,(Mouse:0.4,Rat:0.5):0.6,Zebrafish:1.0);')
cat('== R2 drop.tip sums suppressed branch lengths\n')
D0 <- cophenetic(tr)
p <- drop.tip(tr, c('Chimp', 'Zebrafish'))
D1 <- cophenetic(p)
print(write.tree(p))
cat('Human-Mouse before', D0['Human', 'Mouse'], 'after', D1['Human', 'Mouse'], '\n')
cat('max abs diff on shared taxa:', max(abs(D0[rownames(D1), colnames(D1)] - D1)), '\n')

cat('== R3 di2multi tol filters branch LENGTH not support\n')
t2 <- read.tree(text = '((A:0.1,B:0.1)40:0.2,(C:0.1,D:0.1)99:0.00000001,E:0.3);')
print(t2$node.label)
m <- di2multi(t2)  # default tol = 1e-8
cat('default tol=1e-8:', write.tree(m), ' Nnode', t2$Nnode, '->', m$Nnode, '\n')
m2 <- di2multi(t2, tol = 1e-7)
cat('tol=1e-7:', write.tree(m2), '\n')
# Skill recipe: zero out low-support branch lengths, then di2multi
t3 <- t2
sup <- suppressWarnings(as.numeric(t3$node.label))
low <- which(!is.na(sup) & sup < 70) + Ntip(t3)
t3$edge.length[t3$edge[, 2] %in% low] <- 0
m3 <- di2multi(t3)
cat('recipe (zero low-support then di2multi):', write.tree(m3), '\n')
cat('note: the collapsed branch length is lost -> patristic distances change:\n')
cat('A-C before', cophenetic(t2)['A', 'C'], 'after', cophenetic(m3)['A', 'C'], '\n')

cat('== R4 phangorn::midpoint and phytools::midpoint.root\n')
t4 <- read.tree(text = '((A:1,B:1):1,(C:1,D:5):1);')
print(write.tree(phangorn::midpoint(unroot(t4))))
print(write.tree(phytools::midpoint.root(unroot(t4))))
cat('== R5 root() with outgroup + resolve.root\n')
t5 <- read.tree(text = '(OutA:0.1,OutB:0.1,((I1:0.1,I2:0.1):0.1,(I3:0.1,I4:0.1):0.1):0.2);')
r5 <- root(t5, outgroup = c('OutA', 'OutB'), resolve.root = TRUE)
print(write.tree(r5)); print(is.monophyletic(r5, c('I1','I2','I3','I4')))
cat('== R6 multi2di random resolution\n')
set.seed(1); print(write.tree(multi2di(read.tree(text='(A:1,B:1,C:1,D:1);'))))
