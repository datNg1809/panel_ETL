import pandas as pd
import os



file_path = "/home/dnguyen/panel/data/input/"
name = "VO_ZA_GUMTREE_2019_02.csv"
input = os.path.join(file_path + name)
csv = pd.read_csv(input, sep=';')
#line = round(len(csv)/10)
#out_file = csv[:line]
out_file=csv.sample(frac=1/5)
new_file_path="/home/dnguyen/panel/data/input/"

out_file.to_csv(new_file_path + name, index=False, sep=";")

