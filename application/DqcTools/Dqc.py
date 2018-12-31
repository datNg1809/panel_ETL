# coding: utf-8
import great_expectations as ge
import sys
import json
import re


class Dqc:
    def __init__(self, config, my_df):
        self.config = config
        self.my_df = my_df

    def dqc(self):
        renaming_scheme = {}
        for column in self.my_df.columns.values:
            renaming_scheme[column] = column.replace(' ', '_').upper()
        if 'rename' in self.config['GENERAL']:
            for key in self.config["GENERAL"]['rename']:
                renaming_scheme[key] = self.config["GENERAL"]['rename'][key]
                self.my_df.rename(columns=renaming_scheme, inplace=True)
        for column in self.my_df.columns.values:
            renaming_scheme[column] = column.replace('.', '_').upper()
            if re.match("\d.*", column):
                renaming_scheme[column] = "_" + renaming_scheme[column]
                self.my_df.rename(columns=renaming_scheme, inplace=True)

        # do enrichment
        if 'enrichment' in self.config:
            for dqc_method in self.config['enrichment']:
                dqc_func = getattr(self.class_, dqc_method['name'])
                if "column" in dqc_method:
                    if 'kwargs' in dqc_method:
                        dqc_func(self.my_df, **dqc_method['kwargs'])
                    else:
                        self.my_df[dqc_method['target']] = self.my_df[dqc_method['column']].apply(lambda row: dqc_func(self.my_df, row))
                else:
                    if 'kwargs' in dqc_method:
                        dqc_func(self.my_df, **dqc_method['kwargs'])
                    else:
                        self.my_df[dqc_method['target']] = self.my_df.apply(lambda row: dqc_func(self.my_df, row), axis=1)

        if 'expectations' in self.config:
            # prepare log config
            log_configs = {}
            for config_expectation in self.config['expectations']:
                log_configs[config_expectation['expectation_type']] = {}
                if 'logs' in config_expectation:
                    log_configs[config_expectation['expectation_type']] = config_expectation['logs']
            # do DQC
            my_expectations_config = {'dataset_name': None}
            my_expectations_config['meta'] = {}
            my_expectations_config['meta']['great_expectations.__version__'] = '0.4.5'
            my_expectations_config['expectations'] = self.config['expectations']

            results = self.my_df.validate(expectations_config=my_expectations_config, catch_exceptions=False,
                                          result_format={'result_format': 'COMPLETE'})

            # generate error logs
            for result in results['results']:
                expectation_type = result['expectation_config']['expectation_type']
                log_config = None
                if expectation_type in log_configs:
                    log_config = log_configs[expectation_type]
                dqc_func = getattr(self.my_df, "log_" + expectation_type, getattr(self.my_df, 'log_generic_error'))
                dqc_func(result, log_config)
        # produce output flowfile
        self.my_df.index = self.my_df[self.config['GENERAL']['global_index']]
        self.my_df.index.name = '_id'
        if self.config['GENERAL']['output_filename'] == "stdout":
            print(self.my_df.to_csv(None))
        elif len(self.config['GENERAL']['output_filename']) > 0:
            # @TODO write to file
            pass
