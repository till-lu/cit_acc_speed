# libs ----

library("neatStats")
library("clipr")
library("bayestestR")



#exclusion

lofence = function(numvec) {
  quantile_1st = as.numeric(stats::quantile(numvec, .25, na.rm = TRUE))
  quantile_3rd = as.numeric(stats::quantile(numvec, .75, na.rm = TRUE))
  # return(3 * (quantile_3rd - quantile_1st) + quantile_3rd)
  return(quantile_1st - 3 * (quantile_3rd - quantile_1st))
}

# COLLECT DATA ----

setwd(path_neat("realdata"))

file_names = list.files(pattern = "^speed_acc_.*txt$")


for (fname in enum(file_names)) {
  # fname = c(1, "speed_acc_cit1_10_20210319115636.txt")
  cat(fname, ' ')
  subj_data = read.table(
    fname[2],
    sep = "\t",
    header = TRUE,
    fill = TRUE,
    quote = "\"",
    stringsAsFactors = FALSE
  )
  
  dems_row = subj_data[startsWith(as.character(subj_data$subject_id), 'dems'), ]
  dems_heads = strsplit(dems_row[[1]], "/")[[1]][-1]
  dems_dat = strsplit(dems_row[[2]], "/")[[1]]
  dems = do.call(rbind.data.frame, list(dems_dat))
  colnames(dems) = dems_heads
  
  subj_itms_base = subj_data[subj_data$phase == 'main', ]

  subj_itms_base$stim_type[grepl('^irrelevant', subj_itms_base$stim_type)] = "irrelevant"
  

  subj_itms_base$exclusion <- "fillers"
  subj_itms_base$exclusion[subj_itms_base$stim_type == 'probe' | subj_itms_base$stim_type == 'irrelevant'] <- "mainitems"
  subj_itms_base$exclusion[subj_itms_base$stim_type == 'target'] <- 'targets'

  if (nrow(subj_itms_base) != 2*162) {
    # just double-check
    # print("number of rows:")
    # print(nrow(subj_itms_base))
    stop("trial num incorrect: ", nrow(subj_itms_base))
  }
  

#subj_itms_base = excl_neat(subj_itms_base, trial_number > 112 & block_number == 5) 
#subj_itms_base = excl_neat(subj_itms_base, trial_number > 50 & block_number == 4)
  
  
  
  subj_itms_base$valid_trial = ifelse(
    subj_itms_base$incorrect == 0 &
      subj_itms_base$too_slow == 0,
    1,
    0
  )
  
  subj_acc_rates = neatStats::aggr_neat(
    dat = subj_itms_base,
    values = valid_trial,
    method = mean,
    group_by = c("stim_type"),
    prefix = "acc_rate"
  )
  
  subj_acc_rates_exclusion = neatStats::aggr_neat(
    dat = subj_itms_base,
    values = valid_trial,
    method = mean,
    group_by = c("exclusion"),
    prefix = "excl_rate"
  )
  
  subj_rt_mean = neatStats::aggr_neat(
    dat = subj_itms_base,
    values = rt_start,
    method = mean,
    group_by = c("stim_type"),
    filt = (valid_trial == 1 & rt_start >= 150),
    prefix = "rt_mean"
  )
  
  subj_itms_base$press_duration = as.numeric(subj_itms_base$press_duration)
  subj_dur_mean = neatStats::aggr_neat(
    dat = subj_itms_base,
    values = press_duration,
    method = mean,
    group_by = c("stim_type"),
    filt = (valid_trial == 1),
    prefix = "dur_mean"
  )
  
  overall_acc = neatStats::aggr_neat(
    dat = subj_itms_base,
    values = valid_trial,
    method = mean,
    group_by = c("stim_type"),
    prefix = "overall_acc"
  )
  
  rbind_loop(
    main_cit_merg,
    subject_id = subj_data$subject_id[1],
    condition = subj_data$condition[1],
    dems,
    subj_acc_rates,
    subj_rt_mean,
    subj_dur_mean,
    overall_acc,
    subj_acc_rates_exclusion
  )
}

main_cit_prep = main_cit_merg

# add probe-irrelevant differences

for (colname in names(main_cit_prep)) {
  if (class(main_cit_prep[[colname]]) ==  "numeric" &
      grepl("_probe", colname, fixed = TRUE)) {
    dat_probe = main_cit_prep[[colname]]
    dat_irrel = main_cit_prep[[sub("_probe", "_irrelevant", colname)]]
    newcol = sub("_probe", "_diff", colname)
    main_cit_prep[[newcol]] = dat_probe - dat_irrel
  }
}

main_cit_data = main_cit_prep



for (grp in unique(main_cit_data$group)) {
  cat(grp, fill = TRUE)
  grp_dat = main_cit_data[main_cit_data$group == grp, ]
  main_cit_data = excl_neat(
    main_cit_data,
    (
      excl_rate_targets >= lofence(grp_dat$excl_rate_targets) &
        excl_rate_fillers >= lofence(grp_dat$excl_rate_fillers) &
        excl_rate_mainitems >= lofence(grp_dat$excl_rate_mainitems) 
    ) | main_cit_data$group != grp
  )
}

full_data = main_cit_data

full_data$error_rate_irrelevant = (1 - full_data$overall_acc_irrelevant) * 100
full_data$error_rate_target = (1 - full_data$overall_acc_target) * 100
full_data$error_rate_targetref = (1 - full_data$overall_acc_targetref) * 100
full_data$error_rate_nontargref = (1 - full_data$overall_acc_nontargref) * 100
full_data$error_rate_probe = (1 - full_data$overall_acc_probe) * 100
full_data$error_rate_diff = (full_data$error_rate_probe) -  (full_data$error_rate_irrelevant) 

# full_data = excl_neat(full_data, subject_id != "187_20210503100937")
# full_data = excl_neat(full_data, subject_id != "188_20210503101011")
# full_data = excl_neat(full_data, subject_id != "16_20210408094158")

#last
# full_data = excl_neat(full_data, subject_id != "135_20210422124314")
# full_data = excl_neat(full_data, subject_id != "124_20210422084023")


# demographics

neatStats::dems_neat(full_data, percent = F, group_by = 'condition')
neatStats::dems_neat(full_data, percent = F, group_by = 'group')
anova_neat(full_data, values = 'rt_mean_diff', between_vars = 'group') #condition


anova_neat(
       full_data,
       values = 'rt_mean_diff',
       between_vars = 'group',
       plot_means = T, bf_added = T
  )

anova_neat(
  full_data,
  values = 'error_rate_diff',
  between_vars = 'group',
  plot_means = T,  norm_plots = T,
  norm_tests = 'all',
  bf_added = T,
  var_tests = TRUE
)


write_clip(table_neat(
  list(
    aggr_neat(full_data, error_rate_irrelevant, round_to = 3),
    aggr_neat(full_data, error_rate_nontargref, round_to = 3),
    aggr_neat(full_data, error_rate_probe, round_to = 3),
    aggr_neat(full_data, error_rate_target, round_to = 3),
    aggr_neat(full_data, error_rate_targetref, round_to = 3),
    aggr_neat(full_data, error_rate_diff, round_to = 3)

  ),
  group_by = 'group'
))

table_neat(
  list(
    aggr_neat(full_data, rt_mean_irrelevant),
    aggr_neat(full_data, rt_mean_nontargref),
    aggr_neat(full_data, rt_mean_probe),
    aggr_neat(full_data, rt_mean_target),
    aggr_neat(full_data, rt_mean_targetref),
    aggr_neat(full_data, rt_mean_diff)
    
  ),
  group_by = 'group'
)



anova_neat(
  full_data,
  values = c(
    'rt_mean_target',
    'rt_mean_irrelevant',
    'rt_mean_targetref',
    'rt_mean_nontargref',
    'rt_mean_probe'
  ),

  between_vars = 'group',
  plot_means = TRUE,
  line_colors = c("#ecb90e",
    "#521aa6",
    "#60a87a",
    "#d7cfe5",
    "#0b0a2d"),
  norm_tests = 'all',
  var_tests = TRUE,
  bf_added = T
)

anova_neat(
  full_data,
  values = c(
    'error_rate_target',
    'error_rate_targetref',
    'error_rate_irrelevant',
    'error_rate_nontargref',
    'error_rate_probe'
  ),
  
  between_vars = 'group',
  plot_means = TRUE,
  line_colors = c("#fb3155",
"#6c191c",
"#624634",
"#94674f",
"#f1d5b9", "#01579b"),
  norm_tests = 'all',
  var_tests = TRUE
)




write_clip(table_neat(
  list(
    aggr_neat(full_data, rt_mean_irrelevant),
    aggr_neat(full_data, rt_mean_nontargref),
    aggr_neat(full_data, rt_mean_probe),
    aggr_neat(full_data, rt_mean_target),
    aggr_neat(full_data, rt_mean_targetref),
    aggr_neat(full_data, rt_mean_diff)
    
  ),
  group_by = 'group'
))

speed_data = excl_neat(full_data, group == 'speed')
acc_data = excl_neat(full_data, group == 'acc')
control_data = excl_neat(full_data, group == 'control')


t_neat(speed_data$rt_mean_diff,
       control_data$rt_mean_diff,
       bf_added = T,
       nonparametric = F)
t_neat(acc_data$rt_mean_diff,
       control_data$rt_mean_diff,
       bf_added = T)
t_neat(speed_data$rt_mean_diff,
       acc_data$rt_mean_diff,
       nonparametric = F,
       bf_added = T)


t_neat(speed_data$error_rate_diff,
       control_data$error_rate_diff,
       bf_added = T,
       nonparametric = F)
t_neat(acc_data$error_rate_diff,
       control_data$error_rate_diff,
       bf_added = T,
       nonparametric = F)
t_neat(speed_data$error_rate_diff,
       acc_data$error_rate_diff,
       nonparametric = F,
       bf_added = T)




plot_neat(full_data, 
          values = 'rt_mean_diff',
          between_vars = 'group',
          y_title = 'Mean reaction time difference (Probe - Irrelevant) in ms',
          bar_colors = c("#FDE725FF", "#440154FF"),
          line_colors = c("#FDE725FF", "#440154FF"))

plot_neat(full_data, 
          values = 'error_rate_diff',
          between_vars = 'group',
          y_title = 'Mean accuracy difference (Probe - Irrelevant) in %')

sim_auc = function(preds) {
  neatStats::t_neat(
    preds,
    bayestestR::distribution_normal(1000,
                                    mean = 0,
                                    sd = sd(preds) * 0.5 + 7),
    bf_added = F,
    auc_added = T
  )
}

sim_auc(full_data$rt_mean_diff)
sim_auc(speed_data$rt_mean_diff)
sim_auc(acc_data$rt_mean_diff)
sim_auc(control_data$rt_mean_diff)

sim_auc(speed_data$error_rate_diff)
sim_auc(acc_data$error_rate_diff)
sim_auc(control_data$error_rate_diff)


write_clip(neatStats::dems_neat(full_data, percent = F, group_by = 'group')
)


anova_neat(
  full_data,
  values = c(
    'rt_mean_irrelevant'#,
    #'rt_mean_probe'
  ),
  
  between_vars = 'group',
  plot_means = TRUE,
  # line_colors = c("#ecb90e",
  #                 "#521aa6",
  #                 "#60a87a",
  #                 "#d7cfe5",
  #                 "#0b0a2d"),
  norm_plots = T,
  norm_tests = 'all',
  bf_added = F,
  var_tests = TRUE
)

anova_neat(
  full_data,
  values = c(
    'error_rate_irrelevant',
    'error_rate_probe'
  ),
  
  between_vars = 'group',
  plot_means = TRUE,
  # line_colors = c("#ecb90e",
  #                 "#521aa6",
  #                 "#60a87a",
  #                 "#d7cfe5",
  #                 "#0b0a2d"),
  norm_plots = T,
  norm_tests = 'all',
  bf_added = T,
  var_tests = TRUE
)


write_clip(table_neat(
  list(
    aggr_neat(full_data, rt_mean_irrelevant),
    aggr_neat(full_data, rt_mean_nontargref),
    aggr_neat(full_data, rt_mean_probe),
    aggr_neat(full_data, rt_mean_target),
    aggr_neat(full_data, rt_mean_targetref),
    aggr_neat(full_data, rt_mean_diff)
    
  ),
  group_by = 'group'
))






write_clip(table_neat(
  list(
    aggr_neat(full_data, error_rate_irrelevant, round_to = 3),
    aggr_neat(full_data, error_rate_nontargref, round_to = 3),
    aggr_neat(full_data, error_rate_probe, round_to = 3),
    aggr_neat(full_data, error_rate_target, round_to = 3),
    aggr_neat(full_data, error_rate_targetref, round_to = 3),
    aggr_neat(full_data, error_rate_diff, round_to = 3)
    
  ),
  group_by = 'group'
))

# peek_neat(full_data, 'rt_mean_irrelevant', group_by = 'group')
# peek_neat(full_data, 'rt_mean_targetref', group_by = 'group')
# peek_neat(full_data, 'rt_mean_nontargref', group_by = 'group')
# peek_neat(full_data, 'rt_mean_target', group_by = 'group')
# peek_neat(full_data, 'rt_mean_probe', group_by = 'group')