import pandas as pd
import sys
import csv
import os
from io import StringIO




with open(sys.stdin, 'r') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))

if not sys.stdin.isatty():
    file = sys.stdin.readlines()
file = ''.join(file)
file = StringIO(file)


df= pd.read_csv(file, sep=dialect, enconding="utf-8")

webs= df.SITE.value_counts().index.tolist()
for web in webs:
    outfile = df[df['SITE'] == web]
    out_name= sys.argv[1] + "_" + str(web).upper() + "_" + sys.argv[2] + ".csv"
    output=os.path.join(sys.argv[3] + out_name)
    outfile.to_csv(output, sep=';', index=False, encoding = 'utf-8')
    sys.stdout = open(outfile, 'w')