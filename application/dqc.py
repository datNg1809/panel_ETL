# coding: utf-8
import great_expectations as ge
import sys
from dotenv import load_dotenv
import json
import re
import DqcTools

#
# read all environnement and config
if len(sys.argv) != 2:
    print('Usage : dqc.py place context filename')
    print("config_file : relative path to config_file")
    sys.exit()
config_file = sys.argv[1]
load_dotenv()
with open("./" + config_file , 'r') as f:
    config = json.load(f)
context = config['GENERAL']['context']

#
# read csv file
#
# and prepare some extra parameters
#
module_ = __import__('DqcTools')
class_ = getattr(module_, context.capitalize())

ge_df = ge.read_csv(config['GENERAL']['input_filename'], delimiter=";", index_col=False)
my_df = class_(ge_df, config)

# # find the right class
renaming_scheme = {}
for column in my_df.columns.values:
    renaming_scheme[column] = column.replace(' ', '_').upper()
if 'rename' in config['GENERAL']:
    for key in config["GENERAL"]['rename']:
        renaming_scheme[key] = config["GENERAL"]['rename'][key]
my_df.rename(columns=renaming_scheme, inplace=True)
for column in my_df.columns.values:
    renaming_scheme[column] = column.replace('.', '_').upper()
    if re.match("\d.*", column):
        renaming_scheme[column] = "_" + renaming_scheme[column]
my_df.rename(columns=renaming_scheme, inplace=True)

# do enrichment
if 'enrichment' in config:
    for dqc_method in config['enrichment']:
        dqc_func = getattr(class_, dqc_method['name'])
        if "column" in dqc_method:
            if 'kwargs' in dqc_method:
                dqc_func(my_df, **dqc_method['kwargs'])
            else:
                my_df[dqc_method['target']] = my_df[dqc_method['column']].apply(lambda row: dqc_func(my_df, row))
        else:
            if 'kwargs' in dqc_method:
                dqc_func(my_df, **dqc_method['kwargs'])
            else:
                my_df[dqc_method['target']] = my_df.apply(lambda row: dqc_func(my_df, row), axis=1)

if 'expectations' in config:
    # prepare log config
    log_configs = {}
    for config_expectation in config['expectations']:
        log_configs[config_expectation['expectation_type']] = {}
        if 'logs' in config_expectation:
            log_configs[config_expectation['expectation_type']] = config_expectation['logs']
    # do DQC
    my_expectations_config = {'dataset_name': None}
    my_expectations_config['meta'] = {}
    my_expectations_config['meta']['great_expectations.__version__'] = '0.4.4'
    my_expectations_config['expectations'] = config['expectations']

    results = my_df.validate(expectations_config=my_expectations_config, catch_exceptions=False, result_format={'result_format': 'COMPLETE'})

    # generate error logs
    for result in results['results']:
        expectation_type = result['expectation_config']['expectation_type']
        log_config = None
        if expectation_type in log_configs:
            log_config = log_configs[expectation_type]
        dqc_func = getattr(my_df, "log_" + expectation_type, getattr(my_df, 'log_generic_error'))
        dqc_func(result, log_config)

# produce output flowfile
my_df.index = my_df[config['GENERAL']['global_index']]
my_df.index.name = '_id'
if config['GENERAL']['output_filename'] == "stdout":
    print(my_df.to_csv(None))
elif len(config['GENERAL']['output_filename']) > 0:
    # @TODO write to file
    pass
