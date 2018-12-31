import sys
from DqcTools import Dqc
from dotenv import load_dotenv
import json
import great_expectations as ge
import os


def main(market):
    #
    # read all environnement and config

    load_dotenv()
    with open("./config/" + market + '_config.json', 'r') as f:
        config = json.load(f)
    context = config['GENERAL']['context']

    ge_df = ge.read_csv('./data/' + config['GENERAL']['input_filename'], delimiter=";", index_col=False,
                        dtype={'TELEPHONE': 'str'})
    module_ = __import__('Panel', fromlist=[context.capitalize()])
    module2_ = getattr(module_, context.capitalize())
    class_ = getattr(module2_, context.capitalize())
    my_df = class_(ge_df, config)
    dqc = Dqc.Dqc(config, my_df)
    dqc.dqc()


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    filename = sys.argv[1]
    (file, extention) = filename.split(".")
    (market, country_, website_, year_, month_) = file.split("_")
    main(market)
