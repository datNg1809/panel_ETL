import sys
from DqcTools import Dqc
from dotenv import load_dotenv
import json
import great_expectations as ge
import os
from io import StringIO

def main(market):
    #
    # read all environnement and config

    load_dotenv()
    with open("/usr/local/src/config/final_config/" + market + '_' + country_ + '_' + website_ + '_' + year_ + '_' +
              month_ + '_config.json', 'r') as f:
        config = json.load(f)
    context = config['GENERAL']['context']

    delimiter = config['GENERAL'].get('delimiter', "\t")

    if config['GENERAL']['input_filename'] == "stdin":
        if not sys.stdin.isatty():
            file = sys.stdin.readlines() 

        file = ''.join(file)
        file = StringIO(file)
        ge_df = ge.read_csv(file, 
                            delimiter=delimiter, 
                            index_col=False,
                            dtype=config['dtype'])

    else:
        ge_df = ge.read_csv('/usr/local/src/data/' + config['GENERAL']['input_filename'], 
                            delimiter=delimiter, 
                            index_col=False,
                            dtype=config['dtype'])  

    module_ = __import__('Panel', fromlist=[context.capitalize()])
    module2_ = getattr(module_, context.capitalize())
    class_ = getattr(module2_, context.capitalize())
    my_df = class_(ge_df, config)
    dqc = Dqc.Dqc(config, my_df, class_)
    dqc.dqc()


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    filename = sys.argv[1]
    (file, extention) = filename.split(".")
    (market, country_, website_, year_, month_) = file.split("_")
    main(market)
