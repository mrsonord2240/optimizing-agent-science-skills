# BAD (confounded): batch is aliased with condition -> non-identifiable
#   batch 1: treat, treat, treat, treat       batch 2: ctrl, ctrl, ctrl, ctrl
# GOOD (balanced): batch is orthogonal to condition -> batch effect estimable, removable
#   batch 1: 2 treat + 2 ctrl                 batch 2: 2 treat + 2 ctrl
