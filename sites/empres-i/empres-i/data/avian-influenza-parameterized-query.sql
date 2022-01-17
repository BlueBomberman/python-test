SELECT * 
FROM `fao-empres-re.empres_hih_views.vw_diseases_for_portal`
where (case when observation_date is null then report_date else observation_date end >= @start_date and case when observation_date is null then report_date else observation_date end <= @end_date)
  and ( @diagnosis_status = "all" or ifnull(`fao-maps-review.fao_bq_utils.f_normalize_col_name`(diagnosis_status),'no_value') = @diagnosis_status)
  and ( @animal_type = "all" or ifnull(`fao-maps-review.fao_bq_utils.f_normalize_col_name`(animal_type),'no_value') = @animal_type)
  and ( disease="Influenza - Avian"); 
  