import pandas as pd
import os
import json
import glob

file_path = "/home/dnguyen/panel2/nifi/application/config/xlsx_config/"
for file in glob.glob(file_path + "*.xlsx"):
    name = os.path.basename(file)
    market = name.split("_")[0]
    country = name.split("_")[1]


    xlsx = pd.ExcelFile(file)

    sheets=len(xlsx.sheet_names)
    template = {
            "GENERAL": {
                "logger_name": "",
                "input_filename": "stdin",
                "output_filename": "stdout",
                "context": "panel",
                "global_index": "ANNONCE_LINK",
                "delimiter": ","
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
            template['GENERAL']['logger_name']= market.lower() + "_" + country.lower() + "_" + i.lower()
            #new_file_path="/home/dnguyen/panel_dqc/nifi/application/config/json_config/"
            new_file_path=file_path.replace("xlsx_config","json_config")
            out_name = market.upper() + "_" + country.upper() + "_" + i + "_general.json"

            with open (new_file_path + out_name, "w") as f:
                json.dump(template,f)
