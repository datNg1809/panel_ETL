import pandas as pd
import os
import json

file_path = "/home/dnguyen/panel/application/config/xlsx_config/"
name = "VO_ZA_CONFIG.xlsx"
input = os.path.join(file_path + name)

xlsx = pd.ExcelFile(input)

sheets=len(xlsx.sheet_names)
template = {
        "GENERAL": {
            "logger_name": "",
            "input_filename": "stdin",
            "output_filename": "stdout",
            "context": "panel",
            "global_index": "ANNONCE_LINK",
            "delimiter": ";"
        },
        "dtype": {
            "AGENCE_FAX": "str",
            "AGENCE_TEL": "str",
            "TELEPHONE": "str",
            "FAX": "str"
        },
        "enrichment": [],
        "expectations": []
    }
for i in xlsx.sheet_names[1:]:
    if i != 'Glossary of Expectations':
        template['GENERAL']['logger_name']= "vo_za_" + i.lower()
        new_file_path="/home/dnguyen/panel/application/config/json_config/"
        out_name = "VO_ZA_" + i + "_general.json"

        with open (new_file_path + out_name, "w") as f:
            json.dump(template,f)
