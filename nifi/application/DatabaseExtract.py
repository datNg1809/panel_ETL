import pandas as pd
import os
import sys
import mysql.connector as mariadb
from datetime import datetime, timedelta
import logging

# Setup working env & pre set arguments: market, country, year, month
os.chdir("/usr/local/src/")
market = sys.argv[1]
country = sys.argv[2]
if sys.argv[3] != "":
    year = sys.argv[3]
else:
    year = datetime.today().strftime('%Y')
if sys.argv[4] != "":
    month = sys.argv[4]
else:
    month = datetime.today().strftime('%m')

# create folder export_log to store logs of extraction
if not os.path.exists("/usr/local/src/export_log/"):
    os.makedirs("/usr/local/src/export_log/")

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("./export_log/{}_{}_{}_{}.log".format(market, country, year, month))
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Connect to OP6 database
connector = mariadb.connect(user='PANEL-RO', password='PNL-P@n3l', database='DMT_PANEL', host='172.17.0.1', port=33306)
########################################################################################################################

def adapt_filename(market, country):
    """
    Depended on market and country, file name format on database is not consistent. This function returns
    value which matches with database's filename
    :param market:
    :param country:
    :return:
    """
    return market + "_" + country + "__" + country


def adapt_website_name(market, country, website_name):
    """
    Returns official website name which is displayed on Grafana dashboard
    """
    if (market == "VO") & (country == "BE"):
        official_website_name = {"MOBILEDE":"MOBILE",
                                 "VLANAUTO":"AUTOVLAN",
                                 "AUTOSCOUT":"AUTOSCOUT24"}
    else:
        official_website_name = {"IDEALISTAES":"IDEALISTA",
                                 "IDEALISTAIT":"IDEALISTA",
                                 "AUTOSCOUT":"AUTOSCOUT24",
                                 "GUMTREEUK":"GUMTREE",
                                 "KIJIJIIT":"KIJIJI",
                                 "KIJIJICA":"KIJIJI",
                                 "LESPAC":"LESPACS",
                                 "FACEBOOK_MARKETPLACE":"FACEBOOK"}
    if website_name in official_website_name:
        return official_website_name[website_name]
    else:
        return website_name

filename_without_datetime = adapt_filename(market, country)
if market in ["VO", "NPV", "CAMION"]:
    # First query to identify which websites that will be downloaded
    query_a = """
            select distinct SITE 
            from {name}_{year}_{month};
            """.format(name=filename_without_datetime, year=year, month=month)
    df_a = pd.read_sql_query(query_a, connector)

    # Check log to skip websites which are already downloaded in the month
    f = open("./export_log/{}_{}_{}_{}.log".format(market, country, year, month), "r")
    log_lines = f.readlines()
    website_list = []
    for web in df_a['SITE']:
        official_web = adapt_website_name(web.upper())
        ticker = "n"
        for line in log_lines:
            if "{}_{}_{}_{}_{} has been downloaded".format(market, country, official_web.upper(), year, month) in line:
                # if market is VO or NPV, website will be downloaded again 3 days after the first downloading time
                previous_date = datetime.strptime(line[0:10], "%Y-%m-%d")
                three_days_after = previous_date + timedelta(3)
                if datetime.date(three_days_after) != datetime.date(datetime.now()):
                    ticker = "y"
        if ticker == "n":
            website_list.append(web)

    # Second query to download data per website
    for website in website_list:
        query_b = """
            select ADRESSE, ANNEE, ANNONCE_LINK,
                    CARBURANT, CARROSSERIE, CP,
                    GARAGE_ID, ID_CLIENT, IMMAT,
                    KM, LITRE, MARQUE,
                    MODELE, MOIS, NOM,
                    OPTIONS, PHOTO, PLACE,
                    PORTE, PRIX, PROVINCE,
                    SITE, TELEPHONE, TYPE,
                    VILLE, VN_IND, MARQUE_CORRECTED,
                    MODELE_CORRECTED, CYLINDRE, DEPARTEMENT
            from {name}_{year}_{month}
            where SITE='{website}';
            """.format(name=filename_without_datetime, year=year, month=month, website=website)
        official_website = adapt_website_name(website.upper())
        print("filename=" + market + "_" + country + "_" + official_website.upper() + "_" + year + "_" + month)
        df_b = pd.read_sql_query(query_b, connector)
        df_b.to_csv(sys.stdout)
        logger.info("{}_{}_{}_{}_{} has been downloaded".format(market, country, official_website.upper(), year, month))
elif market in ["IMMO", "JOBS"]:
    # First query to identify which tables that will be downloaded
    query_a = """
                select table_name
                from information_schema.TABLES
                where table_name like "%{}_*_{}_{}%";
                """.format(filename_without_datetime, year, month)
    df_a = pd.read_sql_query(query_a, connector)
    # Check log to skip files which are already downloaded in the month
    f = open("./export_log/{}_{}_{}_{}.log".format(market, country, year, month), "r")
    log_lines = f.readlines()
    table_list = []
    ticker = "n"
    for table_name in df_a['table_name']:
        for line in log_lines:
            if "{} has been downloaded".format(table_name) in line:
                ticker = "y"
        if ticker == "n":
            table_list.append(table_name)
    # Second query to download data per table
    for table in table_list:
        query_b = """
                Select ACHAT_LOC, ADRESSE, AGENCE_ADRESSE,
                        AGENCE_CP, AGENCE_ID, AGENCE_NOM,
                        AGENCE_TEL, AGENCE_VILLE, ANNONCE_DATE,
                        ANNONCE_LINK, ANNONCE_TEXT, CATEGORIE,
                        CP, DEPARTEMENT, ID_CLIENT,
                        M2, M2_TOTALE, MAISON_APT,
                        MINI_SITE_ID, NOM, PAYS_AD,
                        PHOTO, PIECE, PRIX, VILLE
                from {}""".format(table)
        website = table.split('_')[4]
        official_website = adapt_website_name(website.upper())
        print("filename=" + market + "_" + country + "_" + official_website.upper() + "_" + year + "_" + month)
        df_b = pd.read_sql_query(query_b, connector)
        df_b.to_csv(sys.stdout)
        logger.info("{} has been downloaded".format(table))
connector.commit()
connector.close()

