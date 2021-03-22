library(neatStats)
setwd(path_neat('data'))
filenames = list.files(pattern = "^speed_acc_.*txt$")

for (file_name in enum(filenames)) {
#  file_name = c(1, "speed_acc_cit4_02_20210312122705.txt")
  cat(file_name, fill = TRUE)
  subj_data = read.table(
  file_name[2],
  sep = "\t",
  header = TRUE,
  fill = TRUE,
  quote = "\"",
  stringsAsFactors = FALSE
    )

  # dems_row = subj_data[startsWith(as.character(subj_data$subject_id), 'dems'), ]
  # dems_heads = strsplit(dems_row[[2]], "/")[[1]]
  # dems_dat = strsplit(dems_row[[3]], "/")[[1]]
  # dems = do.call(rbind.data.frame, list(dems_dat))
  # colnames(dems) = dems_heads
  
  subj_itms_base = subj_data[subj_data$phase == 'main', ]
  
  #if (nrow(subj_itms_base) != 2*162) {
    # just double-check
    # print("number of rows:")
    # print(nrow(subj_itms_base))
  #  stop("trial num incorrect: ", nrow(subj_itms_base))
  #}
  
  subj_itms_base$valid_trial = ifelse(
    subj_itms_base$incorrect == 0 &
      subj_itms_base$too_slow == 0,
    1,
    0
  )
  
  rts = aggr_neat(
    subj_itms_base,
    rt_start,
    group_by = c('stim_type'),
    method = mean,
    prefix = 'rt',
    filt = (rt_start > 150 & incorrect == 0)
  )
  
  ers = aggr_neat(
    subj_itms_base,
    valid_trial,
    group_by = c('stim_type'),
    method = mean,
    prefix = 'er'

  )
  
  er_overall = aggr_neat(subj_itms_base,
                         valid_trial,
                         method = mean,
                         group_by = c('stim_type'))$aggr_value
  

  
  rbind_loop(
    subjects_merged,
    subject_id = subj_itms_base$subject_id[1],
    condition = subj_itms_base$condition[1],
    er_overall = er_overall,
    rts,
    ers
  )
}

# subjects_merged$rt_mean_diffs_0 = subjects_merged$rt_mean_probe_0 - subjects_merged$rt_mean_irrelevant_0
# subjects_merged$rt_mean_diffs_1 = subjects_merged$rt_mean_probe_1 - subjects_merged$rt_mean_irrelevant_1
# 
# subjects_merged$acc_rate_diffs_0 = subjects_merged$acc_rate_probe_0 - subjects_merged$acc_rate_irrelevant_0
# subjects_merged$acc_rate_diffs_1 = subjects_merged$acc_rate_probe_1 - subjects_merged$acc_rate_irrelevant_1
# 
# subjects_merged$dur_mean_diffs_0 = subjects_merged$dur_mean_probe_0 - subjects_merged$dur_mean_irrelevant_0
# subjects_merged$dur_mean_diffs_1 = subjects_merged$dur_mean_probe_1 - subjects_merged$dur_mean_irrelevant_1

  
# plus statistcs etc.

#data_final = excl_neat(subjects_merged, THREE INTERQUARTILE RANGE)

#datafinal$pi_rt_mean etc.


#anova_neat() through conditions

#t_neat()

