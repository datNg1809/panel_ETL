from DqcTools import DqcTools
import logging
import os
from time import gmtime, strftime


class Panel(DqcTools.DqcTools):

    def __init__(self, my_df, config):

        super().__init__(my_df, config)

        self.my_df = my_df
        self.config = config
        self.panel_timestamp = self.config['GENERAL']['year'] + "-" + self.config['GENERAL']['month'] + "-01 00:00:00"
        self.logger = logging.getLogger(' - '.join([self.config['GENERAL']['market'],
                                                    self.config['GENERAL']['country'],
                                                    self.config['GENERAL']['website'],
                                                    self.panel_timestamp]))

        #if os.getenv("use_nifi_logger") == 'yes':
        fh = logging.FileHandler('/nifi/logs/dqc_panel_{}_{}_{}_{}_{}_{}.log'.format(
                                                                               self.config['GENERAL']['market'],
                                                                               self.config['GENERAL']['country'],
                                                                               self.config['GENERAL']['website'],
                                                                               self.config['GENERAL']['year'],
                                                                               self.config['GENERAL']['month'],
                                                                               strftime("%Y-%m-%dT%H:%M:%S",
                                                                                        gmtime()))
                                                                               )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        fh.setLevel(logging.INFO)
        self.logger.addHandler(fh)
