import pandas as pd
import os
import sys
import mysql.connector as mariadb
from datetime import datetime, timedelta
import logging
import time


def adapt_filename(market, country):
    """
    Depended on market and country, file name format on database is not consistent. This function returns
    value which matches with database's filename
    :param market:
    :param country:
    :return:
    """
    if "." in country:
        country.replace(".", "_")
    return market + "_" + country


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


query_vo = """select ADRESSE, ANNEE, ANNONCE_LINK,
                        CARBURANT, CARROSSERIE, CP,
                        GARAGE_ID, ID_CLIENT, IMMAT,
                        KM, LITRE, MARQUE,
                        MODELE, MOIS, NOM,
                        OPTIONS, PHOTO, PLACE,
                        PORTE, PRIX, PROVINCE,
                        SITE, TELEPHONE, TYPE,
                        VILLE, VN_IND, MARQUE_CORRECTED,
                        MODELE_CORRECTED, CYLINDRE, DEPARTEMENT
                From {name}_{year}_{month}
                Where SITE='{website}' 
                ;"""
query_immo = """Select ACHAT_LOC, ADRESSE, AGENCE_ADRESSE,
                        AGENCE_CP, AGENCE_ID, AGENCE_NOM,
                        AGENCE_TEL, AGENCE_VILLE, ANNONCE_DATE,
                        ANNONCE_LINK, ANNONCE_TEXT, CATEGORIE,
                        CP, DEPARTEMENT, ID_CLIENT,
                        M2, M2_TOTALE, MAISON_APT,
                        MINI_SITE_ID, NOM, PAYS_AD,
                        PHOTO, PIECE, PRIX, VILLE
                From {};"""
query_jobs = """Select ANNONCE_LINK, ANNONCE_TEXT, ANNONCEUR,
                        ANNONCEUR_ID, ANNONCEUR_ID_3, CABINET,
                        CONTRAT, DEPARTEMENT, ENTREPRISE,
                        ID_CLIENT, LIEU, METIER,
                        ON_SITE, OTHER_SITE, REGION,
                        TYPE_EMPLOI
                From {};"""


def main(market, country, year, month, logger, overwrite):
    connector = mariadb.connect(user='PANEL-RO', password='PNL-P@n3l', database='DMT_PANEL_{}'.format(market),
                                host='dwh',
                                port=3306)
    if market in ["VO", "NPV", "CAMION"]:
        # First query to identify which websites that will be downloaded
        query_a = """
                select distinct SITE 
                from {name}_{year}_{month};
                """.format(name=adapt_filename(market, country), year=year, month=month)
        df_a = pd.read_sql_query(query_a, connector)

        # Check log to skip websites which are already downloaded in the month
        f = open("./export_log/{}_{}_{}_{}.log".format(market, country, year, month), "r")
        log_lines = f.readlines()
        website_list = []
        if overwrite == "NO":
            for web in df_a['SITE']:
                official_web = adapt_website_name(market, country,web.upper())
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
        elif overwrite == "YES":
            for web in df_a['SITE']:
                website_list.append(web)

        # Second query to download data per website
        for website in website_list:
            query_b = query_vo.format(name= country, year=year, month=month, website=website)
            official_website = adapt_website_name(market, country,website.upper())
            print("filename=" + market + "_" + country + "_" + official_website.upper() + "_" + year + "_" + month)
            df_b = pd.read_sql_query(query_b, connector)
            if len(df_b) < 5:
                continue
            df_b.to_csv(sys.stdout)
        for website in website_list:
            official_website = adapt_website_name(market, country, website.upper())
            logger.info("{}_{}_{}_{}_{} has been downloaded".format(market, country, official_website.upper(), year, month))
    elif market in ["IMMO", "JOBS"]:
        # First query to identify which tables that will be downloaded
        query_a = """
                    select table_name
                    from information_schema.TABLES
                    where table_name like "%{}\_%\_{}\_{}%"
                    and TABLE_TYPE='BASE TABLE'
                    and table_schema='dmt_panel_{}';
                    """.format(adapt_filename(market, country), year, month, market)
        df_a = pd.read_sql_query(query_a, connector)

        # Check log to skip files which are already downloaded in the month
        f = open("./export_log/{}_{}_{}_{}.log".format(market, country, year, month), "r")
        log_lines = f.readlines()
        table_list = []
        if overwrite == "NO":
            ticker = "n"
            for table_name in df_a['table_name']:
                for line in log_lines:
                    if "{} has been downloaded".format(table_name) in line:
                        ticker = "y"
                if ticker == "n":
                    table_list.append(table_name)
        elif overwrite == "YES":
            for table_name in df_a['table_name']:
                table_list.append(table_name)

        # Second query to download data per table
        for table in table_list:
            if market == "IMMO":
                query_b = query_immo.format(table)
            elif market == "JOBS":
                query_b = query_jobs.format(table)
            website = table.split('_')[2]
            official_website = adapt_website_name(market, country,website.upper())
            print("filename=" + market + "_" + country + "_" + official_website.upper() + "_" + year + "_" + month)
            df_b = pd.read_sql_query(query_b, connector)
            if len(df_b) < 5:
                continue
            df_b.to_csv(sys.stdout)
            logger.info("{} has been downloaded".format(table))
    connector.commit()
    connector.close()


if __name__ == "__main__":
    # create folder export_log to store logs of extraction
    os.chdir("/usr/local/src/")
    if not os.path.exists("/usr/local/src/export_log/"):
        os.makedirs("/usr/local/src/export_log/")
    try:
        # Setup working env & pre set arguments: market, country, year, month
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
        if sys.argv[5] != "":
            overwrite = sys.argv[5]
        else:
            overwrite = "NO"

        # Setup logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler("./export_log/{}_{}_{}_{}.log".format(market, country, year, month))
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        main(market, country, year, month, logger,overwrite)
    except Exception as e:
        logger.error("{}_{}_{}_{} was affected : ".format(market, country, year, month) + str(e))
        print("{}_{}_{}_{} was affected : ".format(market, country, year, month) + str(e))


