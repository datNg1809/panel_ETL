import os
from glob import glob
import fileinput
os.chdir("/home/dnguyen/panel2/nifi/logs/nifi/")

for file_name in os.listdir("/home/dnguyen/panel2/nifi/logs/nifi/"):
    if "dqc_panel_JOBS_" in file_name:
        for line in fileinput.input(file_name, inplace=1):
            print(line.replace("JOB", "JOBS"))

