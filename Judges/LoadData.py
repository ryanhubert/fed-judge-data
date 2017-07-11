#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ryan Hübert
# Department of Political Science
# University of California, Davis

"""
This Python 3 script takes the Federal Judicial Center's Biographical 
Directory of Article III Federal Judges and generates a json file formatted 
for easy import/use in other federal courts-related research applications.
"""

# Import Modules
import os, csv, json, re, datetime
from urllib.request import urlopen

def UpdateData(directory):
    # Download most recent judicial biography
    with urlopen("https://www.fjc.gov/sites/default/files/history/judge-export.csv") as webpage:
        reader2 = csv.DictReader(webpage.read().decode('utf-8').splitlines())
        fjcdict = {}
        for row in reader2:
            fjcdict[row['nid']] = row
    
    # Save as JSON
    if os.path.exists(directory + "judges.json"):
        modtime = re.sub('[^\d]','',str(datetime.datetime.fromtimestamp(os.stat(directory+"judges.json").st_mtime))[:-2])
        os.rename(directory + "judges.json",directory + "judges" + modtime + ".json")
    with open(directory + 'judges.json', 'w') as fp:
        json.dump(fjcdict, fp, sort_keys=True, indent=4)
        
    return(fjcdict)

def LoadData(directory):
    if os.path.exists(directory + "judges.json"):
        with open(directory + 'judges.json', 'r') as fp:
            fjcdict = json.load(fp)
        return(fjcdict)
    elif input("Local data does not exist. Download new version? [y/n] ") == "y":
        fjcdict = UpdateData(directory)
        return(fjcdict)
    else:
        raise Exception("No data loaded!")