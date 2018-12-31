# coding: utf-8

import json
import datetime
from great_expectations.dataset import PandasDataset, MetaPandasDataset
import numpy as np
import logging
import re
import phonenumbers


class DqcTools(PandasDataset):
    """
    all tools for DQC
    """

    def __init__(self, df, config):
        """

        :param df:
        :param config:
        """
        super().__init__(df)
        self.df = df
        self.config = config
        self.logger = logging.getLogger(config['GENERAL']['logger_name'])

    def __str__(self):
        """

        :return:
        """
        return str(self.__class__) + ": " + str(self.__dict__)

    def string_with_comma_to_float(self, row):
        """
        transform strings with comma to floats
        :param x: 
        :return: 
        """
        return float(row.replace(",", "."))

    def string_date_to_year(self, the_date):
        """
        convert a string representing a date to the year
        :param the_date: 
        :return: 
        """
        return int(the_date.split('-')[0])

    def log_generic_error(self, result, logs_config=None):
        """

        :param result:
        :param logs_config:
        :return:
        """
        if not result['success']:
            msg = "undefined dqc error"
            self.logger.error(msg + json.dumps(result))

    def log_expect_column_values_to_not_be_in_set(self, result, logs_config):
        """

        :param result:
        :param logs_config:
        :return:
        """
        if "keyword" not in logs_config:
            msg = "FATAL_ERROR - Logs config not set for expect_column_values_to_not_be_in_set"
            self.logger.error(msg)
        elif not result['success']:
            for unexpected_index in result['result']['unexpected_index_list']:
                msg = logs_config["keyword"] + " - " + 'Value in ' + result['expectation_config']['kwargs']['column'] +\
                      ' is equal to zero '
                if 'index' in logs_config:
                    msg += ' for VIN ' + self.df.ix[unexpected_index][logs_config['index']]
                else:
                    msg += ' on line  ' + str(unexpected_index)
                self.logger.error(msg)

    def log_expect_column_pair_values_A_to_be_greater_than_B(self, result, logs_config):
        """

        :param result:
        :param logs_config:
        :return:
        """
        if "keyword" not in logs_config:
            msg = "FATAL_ERROR - Logs config not set for expect_column_pair_values_A_to_be_greater_than_B"
            self.logger.error(msg)
        else:
            for unexpected_index in result['result']['unexpected_index_list']:
                msg = logs_config["keyword"] + " - " + 'Value in ' + result['expectation_config']['kwargs']['column_A'] + \
                      ' should be greater than value in column ' + \
                      result['expectation_config']['kwargs']['column_B'] + ' for VIN ' + self.df.ix[unexpected_index]['VIN']
                self.logger.error(msg)

    def log_expect_returning_row_count(self, result, logs_config):
        """
        
        :param result:
        :param logs_config:
        :return:
        """
        if "keyword" not in logs_config:
            msg = "FATAL_ERROR - Logs config not set for expect_returning_row_count"
            self.logger.error(msg)
        else:
            msg = "[NUM] - " + logs_config["keyword"] + " - " + str(result['result']['observed_value'])
            self.logger.error(msg)

    def log_expect_table_row_count_to_be_between_depending_on_day(self, result, logs_config):
        """

        :param result:
        :param logs_config:
        :return:
        """
        if "keyword" not in logs_config:
            msg = "FATAL_ERROR - Logs config not set for expect_table_row_count_to_be_between_depending_on_day"
            self.logger.error(msg)
        elif not result['success']:
            msg = logs_config["keyword"] + " - " + str(result['result']['observed_value'])
            self.logger.error(msg)

    def log_expect_returning_column_count(self, result, logs_config):
        """

        :param result:
        :param logs_config:
        :return:
        """
        if "keyword" not in logs_config:
            msg = "FATAL_ERROR - Logs config not set for expect_returning_column_count"
            self.logger.error(msg)
        elif not result['success']:
            msg = logs_config["keyword"] + " - " + "Wrong number of column " + str(result['result']['observed_value'])
            self.logger.error(msg)

    def log_expect_column_to_exist(self, result, logs_config):
        """

        :param result:
        :param logs_config:
        :return:
        """
        if "keyword" not in logs_config:
            msg = "FATAL_ERROR - Logs config not set for expect_returning_column_count"
            self.logger.error(msg)
        if not result['success']:
            msg = logs_config["keyword"] + " - " + "Missing column " + result['expectation_config']['kwargs']['column']
            self.logger.error(msg)

    def log_expect_column_value_lengths_to_equal(self, result, logs_config):
        """

        :param result:
        :param logs_config:
        :return:
        """
        if "keyword" not in logs_config:
            msg = "FATAL_ERROR - Logs config not set for expect_column_value_lengths_to_equal"
            self.logger.error(msg)
        elif not result['success']:
            for unexpected_index in result['result']['unexpected_index_list']:
                msg = logs_config["keyword"] + " - " + "Wrong character count for column " + \
                      result['expectation_config']['kwargs']['column'] + ' on line  ' + str(unexpected_index)
                self.logger.error(msg)

    def log_expect_column_values_to_be_of_type(self, result, logs_config):
        """

        :param result:
        :param logs_config:
        :return:
        """
        if "keyword" not in logs_config:
            msg = "FATAL_ERROR - Logs config not set for expect_column_values_to_be_of_type"
            self.logger.error(msg)
        elif not result['success']:
            for unexpected_index in result['result']['unexpected_index_list']:
                msg = logs_config["keyword"] + " - " + "Wrong type for column " + result['expectation_config']['kwargs']['column'] + \
                      ' on line  ' + str(unexpected_index)
                self.logger.error(msg)

    def log_expect_column_values_to_be_in_set(self, result, logs_config):
        """

        :param result:
        :param logs_config:
        :return:
        """
        if "keyword" not in logs_config:
            msg = "FATAL_ERROR - Logs config not set for expect_column_values_to_be_in_set"
            self.logger.error(msg)
        elif not result['success']:
            for unexpected_index in result['result']['unexpected_index_list']:
                msg = logs_config["keyword"] + " - " + "Wrong value for column " + result['expectation_config']['kwargs']['column'] + \
                      ' on line  ' + str(unexpected_index) + " should be in list " + \
                      str(result['expectation_config']['kwargs']['values_set'])
                self.logger.error(msg)

    def log_expect_column_values_to_be_between(self, result, logs_config):
        """

        :param result:
        :param logs_config:
        :return:
        """
        if "keyword" not in logs_config:
            msg = "FATAL_ERROR - Logs config not set for expect_column_values_to_be_between"
            self.logger.error(msg)
        elif not result['success']:
            for unexpected_index in result['result']['unexpected_index_list']:
                msg = logs_config["keyword"] + " - " + "Wrong value for column " + result['expectation_config']['kwargs']['column'] + \
                      ' on line  ' + str(unexpected_index) + " value should be in list > " + \
                      str(result['expectation_config']['kwargs']['min_value']) + " and < " + \
                      str(result['expectation_config']['kwargs']['max_value'])
                self.logger.error(msg)

    @MetaPandasDataset.column_aggregate_expectation
    def expect_returning_row_count(self, column):
        """

        :param column:
        :return:
        """
        return {
            "success": True,
            "result": {
                "observed_value": column.count()
            }
        }

    @MetaPandasDataset.column_aggregate_expectation
    def expect_returning_column_count(self, column, min_column, max_column):
        """

        :param column:
        :param min_column:
        :param max_column:
        :return:
        """
        nb_column = len(list(self.df))
        status = True
        if nb_column < min_column:
            status = False
        if nb_column > max_column:
            status = False

        return {
            "success": status,
            "result": {
                "observed_value": nb_column
            }
        }

    @MetaPandasDataset.column_aggregate_expectation
    def expect_vehicles_observable(self, column, ratio):
        """

        :param column:
        :param ratio:
        :return:
        """
        nb_column = column.count()
        nb_ok = column[column == "1"].count()
        status = True
        ratio_observed = 1
        if nb_ok == 0:
            status = False
            ratio_observed = 0
        elif nb_ok / nb_column < ratio:
            status = False
            ratio_observed = nb_ok / nb_column
        return {
            "success": status,
            "result": {
                "observed_value": ratio_observed
            }
        }

    @MetaPandasDataset.column_aggregate_expectation
    def expect_table_row_count_to_be_between_depending_on_day(self, column, min_day_of_week, min_not_day_of_week,
                                                              maximum):
        """

        :param column:
        :param min_day_of_week:
        :param min_not_day_of_week:
        :param maximum:
        :return:
        """
        nb_column = column.count()
        status = True
        msg = ""
        if nb_column > maximum:
            status = False
            msg += "Number of rows is too large (" + str(nb_column) + ' > ' + str(maximum) + ')'
        if datetime.datetime.today().weekday() >= 5 and nb_column < min_not_day_of_week:
            status = False
            msg += "Number of rows is too low (" + str(nb_column) + ' < ' + str(min_not_day_of_week) + ')'
        if datetime.datetime.today().weekday() < 5 and nb_column < min_day_of_week:
            status = False
            msg += "Number of rows is too low (" + str(nb_column) + ' < ' + str(min_day_of_week) + ')'
        return {
            "success": status,
            "result": {
                "observed_value": msg
            }
        }

    @MetaPandasDataset.column_map_expectation
    def expect_column_values_to_be_phone_number(self, column, country=None,
                                                mostly=None,
                                                result_format=None, include_config=False, catch_exceptions=False,
                                                meta=None):
        """
        Phone number test
        :param column:
        :param country:
        :param mostly:
        :param result_format:
        :param include_config:
        :param catch_exceptions:
        :param meta:
        :return:
        """

        return column.map(lambda x: self._is_phone_number(x, country))

    def _is_phone_number(self, phone, country):
        """

        :param phone:
        :param country:
        :return:
        """
        try:
            x = phonenumbers.parse(phone, country)
            success = phonenumbers.is_possible_number(x)
        except phonenumbers.NumberParseException as error:
            success = False
        return success

    def _length_is_between(self, val, min_value, max_value):
        """

        :param min_value:
        :param max_value:
        :return:
        """
        if min_value is not None and max_value is not None:
            return len(str(val)) >= min_value and len(str(val)) <= max_value

        elif min_value is None and max_value is not None:
            return len(str(val)) <= max_value

        elif min_value is not None and max_value is None:
            return len(str(val)) >= min_value
        else:
            return False

    @MetaPandasDataset.column_map_expectation
    def expect_column_value_lengths_to_be_between_2(self, column, min_value=None, max_value=None,
                                                    mostly=None, result_format=None, include_config=False,
                                                    catch_exceptions=None, meta=None):
        """
        Value length test: convert integer to string
        :param column:
        :param min_value:
        :param max_value:
        :param mostly:
        :param result_format:
        :param include_config:
        :param catch_exceptions:
        :param meta:
        :return:
        """

        return column.map(self._length_is_between)


class Panel(DqcTools):

    def __init__(self, my_df, config):
        super().__init__(my_df, config)