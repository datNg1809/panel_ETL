import pandas as pd
import os

file_path = "/home/dnguyen/panel/data/backup/new/"
name = "IMMO_ES_VENTADEPISOS_2018_12.csv"
input = os.path.join(file_path + name)

xlsx = pd.read_csv(input, engine="python")

out_name="IMMO_ES_VENTADEPISOS_2018_12.csv"
xlsx.to_csv(file_path + out_name, sep=";")