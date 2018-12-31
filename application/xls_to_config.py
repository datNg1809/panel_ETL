
# coding: utf-8

import pandas as pd
import os
import sys
from datetime import datetime
import json
import yaml


path = os.path.dirname(os.path.realpath(__file__))
filename = sys.argv[1]
(file, extention) = filename.split(".")
(market, country, website, year, month) = file.split("_")

general_config = pd.read_excel(path + '/config/{}_config_file.xlsx'.format(market), sheet_name=market)
website_config = pd.read_excel(path + '/config/{}_config_file.xlsx'.format(market), sheet_name=(country + "_" + website).lower())

total_config = pd.concat([website_config, general_config])

with open(path + '/config/{}_general.json'.format(market)) as json_file:
    data = json.load(json_file)
for index, row in total_config.iterrows():
    expectation_type = row['name']
    kwargs = {"column": row["columns"]}
    for index_items, item in yaml.load(row["parameters"]).items():
        kwargs[index_items] = item
    logs = {}
    for index_items, item in yaml.load(row["logs"]).items():
            logs[index_items] = item
    data["expectations"].append({"expectation_type": expectation_type, "kwargs": kwargs, "logs": logs})

print(json.dumps(data))
with open(path + '/config/{}_config.json'.format(market), 'w') as outfile:
    json.dump(data, outfile)
