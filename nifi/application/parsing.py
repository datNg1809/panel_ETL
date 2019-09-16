##import pandas as pd
import sys
import csv
import os
import codecs
import io
from itertools import groupby

"""
sys.argv[1]: folder name ~ market_country, for ex, IMMO_DE
sys.argv[2]: time pattern, for ex, 2019_07
sys.argv[3]: directory to save output, here is /home/d.nguyen/panel/data/input
sys.argv[4]: Y/N whether to separate big file
sys.argv[5]: output file name
sys.argv[6]: crawler team
"""

os.chdir(sys.argv[3])

#csvfile=sys.stdin.read().splitlines()
#dialect = csv.Sniffer().sniff(csvfile.read(1024))

def myfunc(f):
    #dialect = csv.Sniffer().sniff(f.read(1024))
    if sys.argv[6] == "TUNIS":
        sep = ';'
    else:
        sep = ','
    df = csv.reader(f,delimiter = sep)
    if sys.argv[4] == "Y":
        header = next(df)
        site_index=header.index("SITE")
        groupfunc = lambda row: row[site_index]
        for key, rows in groupby(sorted(df, key=groupfunc), groupfunc):
            with open(sys.argv[1] + "_"+ key.upper() + "_" + sys.argv[2] + ".csv", "w",encoding="utf-8") as output:
                cw = csv.writer(output,delimiter=";")
                cw.writerow([g for g in header])
                cw.writerows(rows)
            output.close()
    elif sys.argv[4] == "N":
        os.rename(sys.argv[5], "TEM_" + sys.argv[5])
        #try:
        with codecs.open(sys.argv[5],'w+') as outfile:
            dw = csv.writer(outfile,delimiter=";")
            #cw.writerow([g for g in header])
            #for line in df:
            dw.writerows(list(df))
        #except UnicodeDecodeError:
        #    with codecs.open(sys.argv[5],'w+',encoding='latin-1') as outfile:
        #        dw = csv.writer(outfile,delimiter=";")
                #for line in df:
                #    dw.writerow([str(r).encode() for r in line])
        #        dw.writerows(list(df))
    print("writing completed")


with io.open(0,mode='rt',encoding='utf-8',errors='replace') as f:
    myfunc(f)
#except UnicodeDecodeError:
#    with open(sys.stdin,mode='rt',encoding='latin-1') as fa:
#        myfunc(fa)

#file = sys.stdin.readlines()
#file = ''.join(file)
#file=io.StringIO(file)
#myfunc(file)



