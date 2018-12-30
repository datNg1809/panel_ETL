# coding: utf-8

import logging
from dotenv import load_dotenv
import json
import time


#
# read all environnement and config
load_dotenv()

with open('/usr/local/bin/src/f2ml.json', 'r') as f:
    config = json.load(f)

# setup the logging system
logging.basicConfig(level=logging.DEBUG,\
      format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')
test_logger = logging.getLogger('daily_psa_import')


test_logger.error("Quotation start")
time.sleep(1)
test_logger.error("Quotation stop")
