library(proDA)

fit <- proDA(protein_matrix, design = ~condition + batch, col_data = sample_info,
             reference_level = 'Control')
result_names(fit)  # Intercept, conditionTreatment, batch...: test a coefficient name
results <- test_diff(fit, 'conditionTreatment')
# columns: name, pval, adj_pval, diff (log2FC), t_statistic, se
# do not report diff for proteins with no observed value in a group: the location prior sets it (sign can be wrong)
