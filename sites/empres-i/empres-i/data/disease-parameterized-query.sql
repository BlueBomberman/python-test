SELECT * 
FROM `fao-empres-re.empres_hih_views.vw_diseases`
where (case when observation_date is null then report_date else observation_date end >= @start_date and case when observation_date is null then report_date else observation_date end <= @end_date)
  and ( @diagnosis_status = "all" or ifnull(`fao-maps-review.fao_bq_utils.f_normalize_col_name`(diagnosis_status),'no_value') = @diagnosis_status)
  and ( @animal_type = "all" or ifnull(`fao-maps-review.fao_bq_utils.f_normalize_col_name`(animal_type),'no_value') = @animal_type)
  and ( (@disease = "all" and disease in ("African horse sickness","African swine fever","Anthrax","Bluetongue","Bovine spongiform encephalopathy","Bovine tuberculosis",
"Brucellosis","Brucellosis (Brucella abortus)","Brucellosis (Brucella melitensis)","Brucellosis (Brucella suis)",
"Classical swine fever","Contagious bovine pleuropneumonia","Equine infectious anaemia","Foot and mouth disease","Glanders",
"Hendra Virus Disease","Influenza - Avian","Influenza - Equine","Influenza - Swine","Japanese Encephalitis","Leptospirosis",
"Lumpy skin disease","MERS-CoV","Newcastle disease","Peste des petits ruminants","Porcine reproductive and respiratory syndrome",
"Rabies","Rift Valley fever","Schmallenberg","Sheep pox and goat pox","West Nile Fever")) 
  or ifnull(`fao-maps-review.fao_bq_utils.f_normalize_col_name`(disease),'no_value') = @disease)