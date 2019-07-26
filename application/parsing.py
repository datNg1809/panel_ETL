#import pandas as pd
import sys
import csv
import os
from io import StringIO
from itertools import groupby

"""
sys.argv[1]: folder name ~ market_country, for ex, IMMO_DE
sys.argv[2]: time pattern, for ex, 2019_07
sys.argv[3]: directory to save output, here is /home/d.nguyen/panel/data/input
"""

os.chdir(sys.argv[3])

#csvfile=sys.stdin.read().splitlines()
#dialect = csv.Sniffer().sniff(csvfile.read(1024))
df = csv.reader(sys.stdin)
header = next(df)
site_index=header.index("SITE")

groupfunc = lambda row: row[site_index]

for key, rows in groupby(sorted(df, key=groupfunc), groupfunc):
    with open(sys.argv[1] + "_"+ key.upper() + "_" + sys.argv[2] + ".csv", "w") as output:
        cw = csv.writer(output,delimiter=";")
        cw.writerow([g for g in header])
        cw.writerows(rows)
print("writing completed")