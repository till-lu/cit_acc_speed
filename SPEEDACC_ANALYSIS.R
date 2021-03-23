# libs ----

library("neatStats")

# COLLECT DATA ----

setwd(path_neat(""))

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

  if (nrow(subj_itms_base) != 2*162) {
    # just double-check
    # print("number of rows:")
    # print(nrow(subj_itms_base))
    stop("trial num incorrect: ", nrow(subj_itms_base))
  }

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

  subj_rt_mean = neatStats::aggr_neat(
    dat = subj_itms_base,
    values = rt_start,
    method = mean,
    group_by = c("stim_type"),
    filt = (valid_trial == 1),
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
    overall_acc
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

for (grp in unique(main_cit_data$filler_type)) {
  cat(grp, fill = TRUE)
  grp_dat = main_cit_data[main_cit_data$filler_type == grp, ]
  main_cit_data = excl_neat(
    main_cit_data,
    (
      overall_acc_main >= lofence(grp_dat$overall_acc_main) &
        overall_acc_target >= lofence(grp_dat$overall_acc_target) &
        overall_acc_filler >= lofence(grp_dat$overall_acc_filler)
    ) | main_cit_data$filler_type != grp
  )
}

full_data = main_cit_data

# demographics

neatStats::dems_neat(full_data, percent = F, group_by = 'condition')

anova_neat(full_data, values = 'rt_mean_diff', between_vars = 'condition')

