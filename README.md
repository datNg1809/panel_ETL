# Generic DQC and quotation

The goal of thist stack is :
1. to grab a file from a folder or ftp server
2. to preform a first Quality Check
3. to quote vehicles in the file
4. to perform a post quotation quality check
5. to store the data in mongoDb
6. to send the quoted file to users through ftp or email

Steps 1, 5 and 6 are performed by Nifi, others by python scripts launched by nifi.

Python scripts are governed by json config files passed to python by nifi, with three main parts :
- general config
- pre-quotation DQC
- post-quotation DQC

# Installation
```
git clone ....
git checkout x.y.z
cd infrastructure
docker-compose up -d
```

# Configuration

## general config section
```
"GENERAL": {
    "logger_name":"daily_psa_import",
    "preprocess": [],
    "preprocess_control_params": {},
    "postprocess": [],
    "postprocess_control_params": {},
    "rename": {}
  }
  ```
  
 - logger_name : name of the logger used for ELK injection
 - preprocess : array of test to be done at preprocessing stage
 - preprocess_control_params : parameters of preprocess test
 - postprocess : array of test to be done at postprocess stage
 - postprocess_control_params  parameters of postprocess test
 - rename : list of fields to be rename between input and output
 
## Metrics available (for reporting purpose)
- get_file_metrics : return the number of lines in the file (header excluded)


## Tests available
-  check_empty_file : check if the file is not empty
- check_column_number : check if the number of columns is between `min_count` and `max_count` parameters
- check_mandatory_columns_presence : check if mandatory columns are present (`['COLUMNS']['check_mandatory_columns_presence']`)
- check_number_of_rows : check if the number of rows is over a minimum (`["ROWS"]["min_day_of_week"]` or  `["ROWS"]["min_not_day_of_week"]`) and lower than `["ROWS"]['max]`
- check_if_mandotory_columns_are_empty : self explained, (`['COLUMNS']['check_mandatory_columns_presence']`)
- check_if_some_cells_empty_in_mandatory_columns : self explained, (`['COLUMNS']['check_mandatory_columns_presence']`)
- check_columns_size : check the number of chars in a column (`['COUNTS'][column_name]`)
- check_columns_type : check the type of a column (`['types'][column_name]` in string, int, ...)
- check_values_in_list : check if values in a column are restrained to a specified list (`['VALUES_LIST'][column_name]`)
- check_values_numeric: check if numeric values are in the right window (`['VALUES_NUMERIC'][column_name]`)
- check_column_a_greater_than_b : check if value in a column is greater than in another for the same row (`['A_greater_B']`)
- check_column_a_equals_b : check if value in a column is equal than in another for the same row (`['A_equals_B']`)
- check_excluded_values : verify if column dos not contain excluded values (`['enrichment_params']['EXCLUDED_VALUES']`)
- check_quotation_mode : check if ratio of MCCLBP+Ref is correct (`['enrichment_params']['TOLERANCES']['nb_bas_mcclbp']`)
- check_rpi_brut : check if rpi_brut is ok (`['enrichment_params']['TOLERANCES']['ambition'], ['enrichment_params']['TOLERANCES']['rpi']`)
- check_b2c_values : check if b2c futures value is in tolerance (`['enrichment_params']['TOLERANCES']['b2c_future']`)
- check_b2b_ambition : check if b2b futur ambition value is in tolerance (`['enrichment_params']['TOLERANCES']['b2b_ambition']`)
- check_observables : check if observable cars are well quoted 
